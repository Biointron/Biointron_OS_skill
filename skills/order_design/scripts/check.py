"""Run an explicit live RushData check; no retries and no implicit writes."""

from __future__ import annotations

import argparse
import asyncio
import base64
import json
import logging
import re
import tempfile
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

from config.order_design import OrderDesignSettings
from skill.order_design.scripts.auth import exchange_appkey
from skill.order_design.scripts.client import DESIGN_WAIT_MESSAGE, RushDataClient, RushDataError, _order_numbers
from skill.order_design.scripts.interactive import TerminalInputError, _field, answer, collect, require_terminal, select_catalog_product
from skill.order_design.scripts.localization import localize_text, normalize_language


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="RushData integration check: preflight is read-only; other modes write to the business system.")
    result.add_argument("--mode", choices=("preflight", "design", "submit", "full"), default="preflight")
    result.add_argument("--language", choices=("zh", "en"), default="zh", help="Language for customer-facing prompts and messages (default: zh)")
    result.add_argument("--request", type=Path, help="Design request JSON containing customer-provided data")
    result.add_argument("--file", type=Path, help="Customer-provided .xlsx design workbook")
    result.add_argument("--orders", nargs="+", help="Order numbers explicitly selected for submit mode")
    result.add_argument("--report", type=Path, help="Optional local JSON result file; excludes tokens and design contents")
    result.add_argument("--design-result", choices=("view", "skip"),
                        help="Required for non-interactive design/full: view the saved HTML or skip it; interactive mode always asks")
    result.add_argument("--design-result-dir", type=Path, default=Path("."),
                        help="Local directory for requested design HTML (default: current directory)")
    result.add_argument("--auth", choices=("appkey", "jwt"), default="appkey", help="Account + App Key text input (default), or hidden existing JWT")
    result.add_argument("--non-interactive", dest="interactive", action="store_false",
                        help="Never prompt; CLI without injected credentials stops. Automation can call run(args, business_token).")
    return result


def outcome(result: dict) -> dict:
    """Keep reports to identity/status; upstream cart and submission bodies can vary."""
    return {key: result[key] for key in (
        "status", "orderNo", "rushDataServiceId", "orderNos", "experimentSubmissionVerified",
        "design_result_path",
    ) if key in result}


def _prepare_design(args: argparse.Namespace, *, catalog_select=None) -> tuple:
    """Collect design information and retain supplied/catalog cart fields for later."""
    interactive = getattr(args, "interactive", False)
    language = normalize_language(getattr(args, "language", "zh"))
    if interactive:
        require_terminal(language=language)
    request_path, file_path = args.request, args.file
    if not interactive and (request_path is None or file_path is None):
        raise ValueError("design/full modes require --request and --file.")
    while True:
        try:
            data = json.loads(request_path.read_text(encoding="utf-8-sig")) if request_path else {}
            if not isinstance(data, dict):
                raise ValueError("The request file must contain a JSON object.")
            break
        except (OSError, ValueError):
            if not interactive:
                raise
            print(localize_text("请求文件无法读取、解析或不是 JSON 对象，请重新选择路径或留空填写。", language))
            raw = answer(localize_text("请求 JSON 路径（可留空，改用问答填写；原文件不会修改）：", language), language=language).strip().strip('"')
            request_path = Path(raw) if raw else None
    content, filename = b"", ""
    if file_path is not None:
        try:
            if file_path.suffix.lower() != ".xlsx" or not 0 < file_path.stat().st_size <= 10 * 1024 * 1024:
                raise ValueError("The design file must be a nonempty .xlsx workbook no larger than 10 MiB.")
            content = file_path.read_bytes()
            filename = file_path.name
        except (OSError, ValueError):
            if not interactive:
                raise
            print(localize_text("原始文件无法读取，或不是非空且不超过 10 MiB 的 .xlsx，请重新输入本地文件路径。", language))
    # Retain existing cart answers; ask for missing ones only after the saved-design choice.
    cart_data = data.pop("cart_data", None)
    catalog_options = data.pop("catalog_options", [])
    catalog_search = data.pop("catalog_search", None)
    if interactive:
        completed = collect("design", {"data": data, "filename": filename,
                                       "file_base64": base64.b64encode(content).decode("ascii"),
                                       "catalog_options": catalog_options,
                                       **({"catalog_search": catalog_search} if catalog_search is not None else {})},
                            catalog_select=catalog_select, language=language)
        data = completed["data"]
        content = base64.b64decode(completed["file_base64"], validate=True)
        filename = completed["filename"]
        cart_data = cart_data if isinstance(cart_data, dict) else {}
        selected_catalog_cart = completed.get("selected_catalog_cart", {})
        if selected_catalog_cart:
            if cart_data.get("antigens") is None:
                cart_data["antigens"] = []
            antigens = cart_data["antigens"]
            if isinstance(antigens, list):
                for index, antigen in selected_catalog_cart.items():
                    while len(antigens) <= index:
                        antigens.append(None)
                    existing = antigens[index]
                    if existing is None or isinstance(existing, dict) and not any(item is not None and item != "" for item in existing.values()):
                        antigens[index] = antigen
    elif not isinstance(cart_data, dict):
        raise ValueError("Design/full mode requires a top-level cart_data object in the request JSON.")
    return data, content, filename, cart_data


def _design_result_choice(*, retry: bool = False, language: str = "zh") -> str:
    english = language == "en"
    title = ("The design has been saved. Would you like to view the design result?" if english else
             "设计已保存，是否查看本次设计结果？")
    labels = (("Yes, view the HTML design result", "No, continue ordering") if english else
              ("需要，查看HTML设计结果", "不需要，继续下单"))
    if retry:
        title = "The design is saved. Please choose the next action." if english else "设计已保存，请选择下一步操作。"
        labels = (("Retry reading the design result", "Continue ordering") if english else
                  ("重试读取设计结果", "继续下单"))
    return _field("", {}, {"title": title, "options": [
        {"label": label, "value": value} for label, value in zip(labels, ("view", "skip"))
    ]}, language=language)


async def _deliver_design_result(client: RushDataClient, saved: dict, directory: Path, *,
                                 interactive: bool, choice: str | None, language: str) -> str | None:
    if interactive:
        choice = await asyncio.to_thread(_design_result_choice, language=language)
    if choice == "skip":
        return
    report = None
    path = None
    while True:
        phase = "readDesignResult"
        try:
            if report is None:
                candidate = await client.get_design_result(saved)
                if (not isinstance(candidate, dict) or candidate.get("status") != "design_result_ready"
                        or not isinstance(candidate.get("html"), str) or not candidate["html"].strip()
                        or not isinstance(candidate.get("filename"), str) or not candidate["filename"]):
                    raise RushDataError("The saved design result is missing its HTML or filename."
                                        if language == "en" else "已保存设计的读取结果缺少 HTML 或文件名。")
                report = candidate
            phase = "saveDesignResult"
            if path is None:
                directory = directory.expanduser().resolve()
                directory.mkdir(parents=True, exist_ok=True)
                stem = re.sub(r"[^A-Za-z0-9_-]", "_", Path(report["filename"]).stem)[:120] or "RushData_Design"
                # The BOM overrides old charset declarations without changing the source HTML.
                with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8-sig", newline="", prefix=f"{stem}_",
                                                 suffix=".html", dir=directory, delete=False) as output:
                    output.write(report["html"])
                path = Path(output.name)
            phase = "deliverDesignResult"
            print(("HTML design result: " if language == "en" else "HTML 设计结果：") + str(path), flush=True)
            return str(path)
        except (RushDataError, OSError, ValueError) as error:
            action = {"readDesignResult": ("read", "读取"), "saveDesignResult": ("saved", "保存"),
                      "deliverDesignResult": ("delivered", "交付")}[phase]
            message = (f"The design is saved, but the HTML result could not be {action[0]}: {error}"
                       if language == "en" else f"设计已保存，但 HTML 结果{action[1]}失败：{error}")
            if not interactive:
                details = error.details if isinstance(error, RushDataError) else {}
                raise RushDataError(message, {**details, "phase": phase}) from None
            print(message, flush=True)
            choice = await asyncio.to_thread(_design_result_choice, retry=True, language=language)
            if choice == "skip":
                return


async def run(args: argparse.Namespace, business_token: str, *, prepared_design: tuple | None = None) -> dict:
    language = normalize_language(getattr(args, "language", "zh"))
    interactive = getattr(args, "interactive", False)
    design_result_choice = getattr(args, "design_result", None)
    if args.mode in ("design", "full") and not interactive and design_result_choice not in ("view", "skip"):
        raise ValueError("Non-interactive design/full mode requires --design-result view or --design-result skip before design starts."
                         if language == "en" else "非交互 design/full 模式必须在开始设计前明确提供 --design-result view 或 --design-result skip。")
    # 业务令牌仅用于本次执行，不读取历史环境令牌，也不写回环境或配置文件。
    settings = replace(OrderDesignSettings.from_env(), access_token=business_token)
    settings.require_connection()
    client = RushDataClient(settings, language=language)
    if interactive:
        require_terminal(language=language)
    if args.mode == "preflight":
        await client.preflight()
        # Only persist the readiness summary, not the customer's company data/catalog.
        return {"stage": "preflight", "status": "passed", "full_chain_verified": False}
    if args.mode == "submit":
        orders = args.orders
        while interactive:
            try:
                _order_numbers(orders)
                break
            except RushDataError:
                orders = answer(localize_text("请输入本次明确选中的订单号，多个以空格或逗号分隔：", language), language=language).replace(",", " ").split()
        if not orders:
            raise ValueError("submit mode requires --orders to identify the selected orders.")
        return {"stage": "submit", "result": outcome(await client.submit(orders)), "full_chain_verified": False}
    if prepared_design is None:
        def select_catalog(question):
            return select_catalog_product(question, lambda keyword, page, page_size: asyncio.run(client.search_antigens(keyword, page_no=page, page_size=page_size)), language=language)
        prepared_design = await asyncio.to_thread(_prepare_design, args, catalog_select=select_catalog)
    data, content, filename, cart_data = prepared_design
    design_result_path = None

    async def on_design_saved(saved):
        nonlocal design_result_path
        design_result_path = await _deliver_design_result(
            client, saved, Path(getattr(args, "design_result_dir", None) or "."),
            interactive=interactive, choice=design_result_choice, language=language,
        )
        if interactive:
            completed = await asyncio.to_thread(collect, "cart", {"cart_data": cart_data}, language=language)
            return completed["cart_data"]
        return cart_data

    designed = await client.design_to_cart(
        data, content, filename, on_design_saved=on_design_saved,
        on_design_start=(lambda: print(localize_text(DESIGN_WAIT_MESSAGE, language), flush=True)) if interactive else None,
    )
    if design_result_path:
        designed["design_result_path"] = design_result_path
    if args.mode == "design":
        return {"stage": "design", "result": outcome(designed), "full_chain_verified": False}
    order_no = designed.get("orderNo")
    if not order_no:
        raise RushDataError("The design result is missing orderNo; submission has stopped.", details=designed)
    try:
        submitted = await client.submit([order_no])
    except RushDataError as error:
        error.details = {**error.details, "orderNo": order_no,
                         "rushDataServiceId": designed.get("rushDataServiceId")}
        raise
    return {"stage": "full", "design": outcome(designed), "submission": outcome(submitted), "full_chain_verified": True}


def main() -> int:
    args = parser().parse_args()
    language = normalize_language(args.language)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    report = {"mode": args.mode, "tested_at_utc": datetime.now(timezone.utc).isoformat(), "live": True}
    business_token = ""
    username = ""
    appkey = ""

    def ensure_credentials():
        nonlocal business_token, username, appkey
        if business_token:
            return
        print(localize_text("Biointron Account 与 App Key 可在 https://os.biointron.com/ 核实；仅用于本次执行，不写入请求文件或报告。", language))
        if args.auth == "jwt":
            while not business_token:
                business_token = answer(localize_text("本次已有 JWT（必填，不回显、不保存）：", language), secret=True, language=language)
        else:
            while not username:
                username = answer(localize_text("Biointron Account（必填）：", language), language=language).strip()
            while not appkey:
                appkey = answer(localize_text("App Key（必填）：", language), language=language)
            business_token = asyncio.run(exchange_appkey(OrderDesignSettings.from_env(), username, appkey, language=language))

    def select_catalog(question):
        ensure_credentials()
        settings = replace(OrderDesignSettings.from_env(), access_token=business_token)
        client = RushDataClient(settings, language=language)
        return select_catalog_product(question, lambda keyword, page, page_size: asyncio.run(client.search_antigens(keyword, page_no=page, page_size=page_size)), language=language)

    try:
        if not args.interactive:
            raise TerminalInputError(localize_text("非交互 CLI 未注入本次凭据，已停止且未读取输入；自动化请调用 run(args, business_token)，不使用固定环境令牌。", language))
        require_terminal(language=language)
        prepared_design = _prepare_design(args, catalog_select=select_catalog) if args.mode in ("design", "full") else None
        ensure_credentials()
        report.update(asyncio.run(run(args, business_token, prepared_design=prepared_design)))
        exit_code = 0
    except (EOFError, KeyboardInterrupt):
        report.update(status="blocked", full_chain_verified=False,
                      message=localize_text("用户结束了输入或执行；业务若已开始则结果可能未确认，请先查询，不要自动重试。", language))
        exit_code = 1
    except RushDataError as error:
        report.update(status="blocked_or_failed", full_chain_verified=False,
                      message=str(error), details=error.details)
        exit_code = 1
    except (ValueError, OSError) as error:
        # Do not print source contents or secrets from malformed input files.
        message = localize_text(str(error), language) if not isinstance(error, (json.JSONDecodeError, OSError)) else "The input file could not be read or parsed."
        report.update(status="blocked", full_chain_verified=False, message=message)
        exit_code = 1
    def redact(value):
        # 上游返回字段也可能含令牌，输出和落盘前只处理字符串，不破坏 JSON 结构。
        if isinstance(value, str):
            for secret in (business_token, appkey, username):
                if secret:
                    value = value.replace(secret, "[redacted]")
            return value
        if isinstance(value, dict):
            return {redact(key): redact(item) for key, item in value.items()}
        if isinstance(value, list):
            return [redact(item) for item in value]
        return value

    text = json.dumps(redact(report), ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text + "\n", encoding="utf-8")
    print(text)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
