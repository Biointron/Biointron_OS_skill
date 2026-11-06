"""Terminal-only input collection driven by the same local schemas as MCP."""

from __future__ import annotations

from copy import deepcopy
import base64
import getpass
import json
from pathlib import Path
import sys
import warnings

from .forms import collect_order_input, inspect_order_input
from .client import MAX_FILE_BYTES, RushDataError
from .localization import localize_text, normalize_language


class TerminalInputError(ValueError):
    pass


def require_terminal(*, language: str = "zh") -> None:
    if not sys.stdin.isatty():
        raise TerminalInputError(localize_text("当前不是安全交互终端，已停止且未发起业务写入；请在终端运行，自动化请显式调用 run(args, business_token)。", language))


def answer(prompt: str, *, secret: bool = False, language: str = "zh") -> str:
    require_terminal(language=language)
    try:
        if secret:
            with warnings.catch_warnings():
                warnings.simplefilter("error", getpass.GetPassWarning)
                return getpass.getpass(prompt)
        return input(prompt)
    except (EOFError, KeyboardInterrupt, getpass.GetPassWarning):
        raise TerminalInputError(localize_text("输入已结束或终端无法安全读取凭据，已停止；未继续发起业务写入。", language)) from None


def _node(schema, path):
    for part in path.strip("/").split("/") if path else []:
        schema = schema.get("items", {}) if part.isdigit() else schema.get("properties", {}).get(part, {})
    return schema


def _set(value, path, selected):
    parts = path.strip("/").split("/") if path else []
    if not parts:
        return selected
    if not isinstance(value, dict):
        value = {}
    current = value
    for position, part in enumerate(parts):
        key = int(part) if isinstance(current, list) else part
        if isinstance(current, list):
            while len(current) <= key:
                current.append(None)
        if position == len(parts) - 1:
            current[key] = selected
            break
        expected = list if parts[position + 1].isdigit() else dict
        existing = current[key] if isinstance(current, list) else current.get(key)
        if not isinstance(existing, expected):
            current[key] = expected()
        current = current[key]
    return value


def _field(path, node, question=None, *, language: str = "zh"):
    question = question or {}
    label = node.get("label", localize_text("资料", language))
    print(question.get("title", f"Please enter {label}" if normalize_language(language) == "en" else f"请填写{label}"))
    if description := question.get("description", node.get("description")):
        print(description)
    if examples := question.get("examples", node.get("examples")):
        print(localize_text("仅供格式参考，不能默认使用：", language) + json.dumps(examples, ensure_ascii=False))
    options = question.get("options", [])
    if options:
        for index, option in enumerate(options, 1):
            print(f"  {index}. {option['label']}")
    types = node.get("type", [])
    types = [types] if isinstance(types, str) else types
    while True:
        multiple = question.get("input_type") == "multi_select"
        raw = answer(localize_text("请选择编号（多选用逗号分隔，不检测填 0）：", language) if multiple else
                     localize_text("请选择编号：", language) if options else localize_text("请输入实际值（复杂对象/数组请用 JSON）：", language), language=language)
        if options:
            if multiple:
                parts = raw.replace("，", ",").replace("、", ",").replace(" ", ",").split(",")
                parts = [part for part in parts if part]
                if parts == ["0"]:
                    return []
                if parts and all(part.isdigit() and 1 <= int(part) <= len(options) for part in parts):
                    return [deepcopy(options[int(part) - 1]["value"]) for part in parts]
                print("Please enter the displayed option numbers." if normalize_language(language) == "en" else "请填写展示的项目编号。")
                continue
            if raw.isdigit() and 1 <= int(raw) <= len(options):
                return deepcopy(options[int(raw) - 1]["value"])
            matches = [item for item in options if raw == item["label"] or raw == str(item["value"])]
            if len(matches) == 1:
                return deepcopy(matches[0]["value"])
        elif "string" in types:
            return raw
        else:
            try:
                return json.loads(raw)
            except (ValueError, TypeError):
                return raw
        print(localize_text("输入格式或选项无效，请重新填写；不会使用示例代填。", language))


def select_catalog_product(question: dict, search, *, language: str = "zh") -> dict:
    """Retain verified choices across batches; navigation is never a design field."""
    options = []
    for offered in question.get("options", []):
        product = offered.get("value")
        if isinstance(product, dict) and product.get("sourceType") == "SUPPLIER_CATALOG":
            option = {key: deepcopy(value) for key, value in product.items() if key != "sourceType"}
            option["label"] = offered["label"]
            if isinstance(offered.get("cart_data"), dict):
                option["cart_data"] = deepcopy(offered["cart_data"])
            options.append(option)
    metadata = deepcopy(question.get("catalog_search") or {})
    keyword = metadata.get("keyword", "")
    page_size = metadata.get("page_size", 50)
    page = 1
    fetch = not (options or metadata)
    while True:
        if fetch:
            if search is None:
                print(localize_text("当前调用方未提供产品库查询能力；仍可选择已有候选，查询更多需使用已接入查询的 CLI 入口。", language))
            else:
                while not keyword:
                    entered = answer(localize_text("请输入要查询的抗原名称或关键词（例如 CD2）：", language), language=language).strip()
                    if 1 <= len(entered) <= 255 and not any(ord(char) < 32 for char in entered):
                        keyword = entered
                    else:
                        print(localize_text("请输入 1–255 个字符的抗原关键词。", language))
                try:
                    result = search(keyword, page, page_size)
                except RushDataError as error:
                    if not options:
                        raise
                    print(f"Loading more results failed; previously loaded choices are retained: {error}" if normalize_language(language) == "en" else f"继续加载失败，已保留此前候选：{error}")
                else:
                    incoming = result.get("catalog_options") if isinstance(result, dict) else None
                    if not isinstance(incoming, list) or any(not isinstance(item, dict) for item in incoming):
                        raise TerminalInputError(localize_text("产品库返回的候选格式不完整，请联系服务维护方；未继续下单。", language))
                    next_page = result.get("next_page")
                    if result.get("has_more") is True and (type(next_page) is not int or next_page <= page):
                        raise TerminalInputError(localize_text("产品库没有返回可继续的页码，已停止加载；不能猜测下一页。", language))
                    merged = {(item["supplier"], item["catalogNumber"], item["specification"]): item for item in options}
                    for item in incoming:
                        merged.setdefault((item["supplier"], item["catalogNumber"], item["specification"]), deepcopy(item))
                    options = list(merged.values())
                    metadata = {key: result[key] for key in ("keyword", "page_size", "total", "has_more", "next_page", "catalog_summary")}
                    page_size = metadata["page_size"]
                    print(metadata["catalog_summary"])
                    if result.get("catalog_issues"):
                        print(localize_text("部分查询或产品资料存在问题，已保留成功加载的候选；不能将当前可选数量当作全部匹配结果。", language))
                    if result.get("read_error"):
                        print(localize_text("未完成原因：", language) + result["read_error"]["message"])
        fetch = False
        product_count = len({(item["supplier"], item["catalogNumber"]) for item in options})
        if normalize_language(language) == "en":
            total = f"This source contains {metadata['total']} matching products; " if metadata else "Total and pagination information is unavailable; "
            print(total + f"{product_count} selectable products and {len(options)} specifications have been loaded in total.")
        else:
            total = f"当前来源共匹配 {metadata['total']} 款产品；" if metadata else "查询总数和分页信息未提供；"
            print(total + f"累计载入可选产品 {product_count} 款、规格 {len(options)} 个。")
        more = metadata.get("has_more") is True
        if more:
            print(localize_text("仍有结果未加载，可继续加载更多产品。", language))
        elif metadata:
            print(localize_text("当前查询已到末页；资料不完整的产品或规格不计入可选数量。", language))
        if not options:
            print(localize_text("当前没有可选产品，可更换关键词。", language))
        for index, option in enumerate(options, 1):
            print(f"  {index}. {option['label']}")
        while True:
            raw = answer(localize_text("选择产品编号，0 更换关键词", language) + (localize_text("，N 继续加载更多产品", language) if more else "") + localize_text("，Q 结束输入：", language), language=language).strip()
            if raw.isdigit() and 1 <= int(raw) <= len(options):
                return deepcopy(options[int(raw) - 1])
            if raw == "0":
                if search is None:
                    print(localize_text("当前调用方未提供关键词查询能力；可选择已有产品或结束输入。", language))
                    continue
                options, metadata, keyword, page, page_size, fetch = [], {}, "", 1, 50, True
                break
            if raw.lower() == "n" and more:
                page, fetch = metadata["next_page"], True
                break
            if raw.lower() == "q":
                raise TerminalInputError(localize_text("用户结束了产品选择；未继续发起业务写入。", language))
            print(localize_text("请选择已加载产品编号或所列操作。", language))


def collect(stage: str, supplied: dict, *, catalog_select=None, language: str = "zh") -> dict:
    """Collect each available batch, then validate and repair complete batches."""
    require_terminal(language=language)
    value = deepcopy(supplied)
    selected_catalog_cart = {}
    validating = False
    while True:
        report = (inspect_order_input(stage, value, language=language, count_workbook=False, batch_questions=True)
                  if validating else collect_order_input(stage, value, language=language))
        if report["status"] == "collected":
            validating = True
            continue
        if report["status"] == "ready":
            if stage == "design":
                value["data"].update(report.get("derived_fields", {}))
                if selected_catalog_cart:
                    value["selected_catalog_cart"] = selected_catalog_cart
            return value
        questions = report.get("interaction", {}).get("questions", [])
        if not questions:
            raise TerminalInputError(localize_text("当前资料无法形成可回答的问题，已停止且未发起业务写入。", language))
        if validating:
            print("Please correct the following information:" if normalize_language(language) == "en" else "请集中修正以下资料：")
            for issue in report.get("issues", []):
                print(f"- {issue.get('label', localize_text('资料', language))}: {issue.get('description', '')}")
        for question in questions:
            path = question["field_paths"][0]
            if question.get("client_action") in ("search_order_antigens", "select_catalog_product"):
                if catalog_select is None and question["client_action"] == "search_order_antigens":
                    raise TerminalInputError(localize_text("当前调用方未提供产品库查询能力；请通过已接入查询的 CLI 入口继续，不能手填或编造货号。", language))
                selected = catalog_select(question) if catalog_select else select_catalog_product(question, None, language=language)
                product = {key: deepcopy(item) for key, item in selected.items() if key not in ("label", "cart_data")}
                product["sourceType"] = "SUPPLIER_CATALOG"
                value = _set(value, path, product)
                value.pop("catalog_options", None)
                value.pop("catalog_search", None)
                if isinstance(selected.get("cart_data"), dict):
                    selected_catalog_cart[int(path.rsplit("/", 1)[-1])] = deepcopy(selected["cart_data"])
            elif question.get("client_action") == "read_local_design_workbook" or question.get("input_type") == "file":
                while True:
                    workbook = Path(answer(localize_text("请输入本次抗体设计表（.xlsx）的本地文件路径：", language), language=language).strip().strip('"'))
                    try:
                        if workbook.suffix.lower() != ".xlsx" or not 0 < workbook.stat().st_size <= MAX_FILE_BYTES:
                            print(localize_text("请提供非空且不超过 10 MiB 的原始 XLSX 文件。", language))
                            continue
                        content = workbook.read_bytes()
                    except OSError:
                        print(localize_text("文件无法读取，请重新输入本次设计表的本地文件路径。", language))
                        continue
                    if not 0 < len(content) <= MAX_FILE_BYTES:
                        print(localize_text("请提供非空且不超过 10 MiB 的原始 XLSX 文件。", language))
                        continue
                    value.update(filename=workbook.name, file_base64=base64.b64encode(content).decode("ascii"))
                    break
            elif question.get("ui_only"):
                # This selection is only UI state; never add sourceType or mode to the cart DTO.
                selected = _field(path, _node(report["schema"], path), question, language=language)
                for field_path in question["fields_by_option"][selected]:
                    entered = _field(field_path, _node(report["schema"], field_path), language=language)
                    value = _set(value, field_path, entered)
            else:
                selected = _field(path, _node(report["schema"], path), question, language=language)
                value = _set(value, path, selected)
                parts = path.strip("/").split("/")
                if stage == "design" and len(parts) == 3 and parts[:2] == ["data", "antigens"] and parts[2].isdigit():
                    for option in question.get("options", []):
                        if option.get("value") == selected and isinstance(option.get("cart_data"), dict):
                            selected_catalog_cart[int(parts[2])] = deepcopy(option["cart_data"])
                    value.pop("catalog_options", None)
                    value.pop("catalog_search", None)
