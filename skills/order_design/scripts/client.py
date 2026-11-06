"""RushData's documented order workflow; no automatic write retries."""

from __future__ import annotations

import asyncio
import json
import math
import re
from collections.abc import Awaitable, Callable
from typing import Any
from urllib.parse import urlsplit

import httpx

from .workbook import count_antibody_records
from .localization import localize_text, normalize_language


MAX_RESPONSE_BYTES = 8 * 1024 * 1024
MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_CATALOG_PAGES = 5
DESIGN_WAIT_MESSAGE = (
    "正在进行订单设计，预计需要较长时间，请耐心等待。\n\n"
    "Biointron provides high-throughput antibody expression and profiling.\n\n"
    "- **10,000 / day** — Antibodies expressed\n"
    "- As fast as **3 days** — CHO cell expression\n"
    "- **30+** — Developability assay readouts\n\n"
    "设计完成后，我会继续反馈结果。"
)
CATEGORIES = ("SAMPLE_TYPE", "PROTEIN_PROPERTY", "BINDING", "DEVELOPABILITY")
BASIC_DESCRIPTION = "上清表达、抗体表达量（上清抗体浓度）检测和 BLI 两点结合检测。"
PACKAGE_DISPLAY_TEXT = {
    "BRD101": "Basic：" + BASIC_DESCRIPTION,
    "BRD201": "Standard：使用纯化抗体，检测纯度和 SPR 结合特性。",
    "BRD301": "Premium：在 Standard 基础上增加热稳定性、多反应性和自身相互作用检测。",
    "BRD401": "Customized：先选择样本形式，再由你逐项选择蛋白性质、结合和开发性检测。",
}
FIXED_ITEMS = {
    "BRD101": (("supernatant",), ("Titer",), ("BLI_Octet_2_points",), ()),
    "BRD201": (("purified antibody",), ("cGE",), ("SPR_Carterra",), ()),
    "BRD301": (("purified antibody",), ("cGE",), ("SPR_Carterra",),
               ("DSF", "PSR ELISA_BVP", "AC_SINS")),
}
BINDING = {
    "SPR_Carterra", "SPR_Biacore", "BLI_Octet_2_points", "BLI_Octet_4_points",
    "FACS_iQue_1_point", "FACS_iQue_8_points", "ELISA_1_point", "ELISA_8_points",
}
DEVELOPABILITY = {
    "PSR ELISA_BVP", "PSR ELISA_Insulin", "PSR ELISA_dsDNA", "AC_SINS", "DSF",
    "DLS_Rh", "DLS_Tagg", "PAIA_HIC", "PAIA_Heparin", "PAIA_OVA", "PAIA_BVP",
}
CUSTOM_ITEMS = {
    "supernatant": {"PROTEIN_PROPERTY": ("Titer",),
                    "BINDING": ("FACS_iQue_1_point", "ELISA_1_point"), "DEVELOPABILITY": ()},
    "purified antibody": {"PROTEIN_PROPERTY": ("cGE", "SEC_HPLC", "SEC_UPLC"),
                          "BINDING": tuple(sorted(BINDING)), "DEVELOPABILITY": tuple(sorted(DEVELOPABILITY))},
}
ITEM_LABELS = {
    "supernatant": "表达上清", "purified antibody": "纯化后的抗体",
    "Titer": "抗体表达量（上清抗体浓度）", "cGE": "cGE 纯度检测",
    "SEC_HPLC": "SEC-HPLC", "SEC_UPLC": "SEC-UPLC", "SPR_Carterra": "SPR-Carterra",
    "SPR_Biacore": "SPR-Biacore", "BLI_Octet_2_points": "BLI-Octet 2 点",
    "BLI_Octet_4_points": "BLI-Octet 4 点", "FACS_iQue_1_point": "FACS-iQue 单点",
    "FACS_iQue_8_points": "FACS-iQue 8 点", "ELISA_1_point": "ELISA 单点", "ELISA_8_points": "ELISA 8 点",
    **{key: key.replace("_", "-") for key in DEVELOPABILITY},
}
IDENTITY_ALIASES = {
    "orderNo": ("orderNo", "order_no"),
    "rushDataServiceId": ("rushDataServiceId", "rush_data_service_id", "id"),
    "orderId": ("orderId", "order_id"),
}


class RushDataError(Exception):
    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.details = details or {}


def _positive_id(value: Any) -> str | None:
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        return None
    text = str(value)
    if not text.isascii() or not text.isdigit() or len(text) > 20:
        return None
    return str(int(text)) if 0 < int(text) <= 9223372036854775807 else None


def _order_number(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and value == value.strip() and not any(
        char == "," or ord(char) < 32 for char in value
    )


def custom_selection_errors(supplied: Any, *, language: str = "zh") -> dict[str, str]:
    """Shared customer-facing selection constraints; multiple Binding variants are allowed."""
    if not isinstance(supplied, dict):
        return {"SAMPLE_TYPE": localize_text("自定义套餐需要先确定样本形式，请选择表达上清或纯化后的抗体。", language)}
    sample = supplied.get("SAMPLE_TYPE")
    if not isinstance(sample, list) or len(sample) != 1 or not isinstance(sample[0], str) or sample[0] not in CUSTOM_ITEMS:
        return {"SAMPLE_TYPE": localize_text("表达上清与纯化后的抗体互斥，请只选择一种样本形式。", language)}
    allowed = CUSTOM_ITEMS[sample[0]]
    errors = {}
    for category, choices in allowed.items():
        values = supplied.get(category)
        if values is None:
            errors[category] = localize_text("请由客户选择并确认这一类检测项目；不检测时也须明确选择，不得跳过或代填。", language)
            continue
        if not isinstance(values, list) or any(not isinstance(item, str) for item in values):
            errors[category] = localize_text("请从可选检测项目中选择，不要填写其他类型的数据。", language)
            continue
        if len(set(values)) != len(values):
            errors[category] = localize_text("同一个检测项目不能重复选择，请去掉重复项。", language)
        invalid = set(values) - set(choices)
        if invalid:
            labels = (", " if normalize_language(language) == "en" else "、").join(
                localize_text(ITEM_LABELS.get(item, "未支持的检测项目"), language) for item in sorted(invalid))
            sample_label = localize_text(ITEM_LABELS[sample[0]], language)
            errors[category] = (f"{sample_label} does not support these selected assays: {labels}. Please revise this selection."
                                if normalize_language(language) == "en" else
                                f"{sample_label}不支持以下已选项目：{labels}。请修改本组选择。")
        elif not values and (category == "PROTEIN_PROPERTY" or (category == "BINDING" and sample[0] == "supernatant")):
            errors[category] = localize_text("本组至少需要选择一个检测项目。", language)
    if supplied.get("BINDING") == [] and supplied.get("DEVELOPABILITY") == []:
        errors["DEVELOPABILITY"] = localize_text("结合检测与开发性检测不能同时不选，请在其中至少选择一项。", language)
    return errors


def _selection(data: dict[str, Any], *, language: str = "zh") -> dict[str, list[str]]:
    catalog = data.get("catalogNumber")
    if not isinstance(catalog, str) or catalog not in (*FIXED_ITEMS, "BRD401"):
        raise RushDataError("catalogNumber must be BRD101, BRD201, BRD301, or BRD401.")
    supplied = data.get("testItems")
    if supplied is None and catalog in FIXED_ITEMS:
        return {category: list(items) for category, items in zip(CATEGORIES, FIXED_ITEMS[catalog])}
    if not isinstance(supplied, dict) or set(supplied) - set(CATEGORIES):
        raise RushDataError("testItems must map test categories to arrays of names; do not supply testItemIds directly.")
    selected = {category: supplied.get(category, []) for category in CATEGORIES}
    if any(not isinstance(items, list) or any(not isinstance(item, str) for item in items)
           or len(set(items)) != len(items) for items in selected.values()):
        raise RushDataError("Each testItems category must contain an array of unique names.")
    if catalog in FIXED_ITEMS:
        if any(set(selected[category]) != set(items)
               for category, items in zip(CATEGORIES, FIXED_ITEMS[catalog])):
            raise RushDataError("Packages 1, 2, and 3 require their exact fixed test combinations.")
        return selected
    errors = custom_selection_errors(supplied, language=language)
    if errors:
        raise RushDataError(("; " if normalize_language(language) == "en" else "；").join(errors.values()), details={"selection_conflicts": errors})
    return selected


def _order_numbers(order_nos: list[str]) -> list[str]:
    if not isinstance(order_nos, list) or not order_nos or any(
        not _order_number(value) for value in order_nos
    ) or len(set(order_nos)) != len(order_nos):
        raise RushDataError("order_nos must be a nonempty array of unique order numbers without commas or control characters.")
    return list(order_nos)


class RushDataClient:
    def __init__(self, settings: Any, transport: httpx.AsyncBaseTransport | None = None, *, language: str = "zh"):
        self.language = normalize_language(language)
        try:
            settings.require_connection()
        except ValueError as error:
            raise RushDataError(localize_text(str(error), self.language)) from None
        self.settings = settings
        self.transport = transport

    def _http(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=self.settings.base_url.rstrip("/") + "/",
            headers={"X-Access-Token": self.settings.access_token, "Accept": "application/json"},
            timeout=self.settings.timeout, follow_redirects=False, trust_env=False,
            transport=self.transport,
        )

    async def _request(self, client: httpx.AsyncClient, method: str, path: str, **kwargs: Any) -> Any:
        # Relative paths preserve a configured API prefix such as /api or /jeecg-boot.
        try:
            async with client.stream(method, path.lstrip("/"), **kwargs) as response:
                if not 200 <= response.status_code < 300:
                    raise RushDataError(f"RushData returned HTTP {response.status_code}.",
                                        {"http_status": response.status_code})
                body = bytearray()
                async for chunk in response.aiter_bytes():
                    body.extend(chunk)
                    if len(body) > MAX_RESPONSE_BYTES:
                        raise RushDataError("The RushData response exceeds 8 MiB.")
                try:
                    payload = json.loads(body)
                except (ValueError, UnicodeError):
                    raise RushDataError("RushData did not return valid JSON.") from None
                if (
                    not isinstance(payload, dict)
                    or type(payload.get("code")) not in (int, float)
                    or payload["code"] != 200
                    or ("success" in payload and payload["success"] is not True)
                ):
                    details = {"http_status": response.status_code}
                    code = payload.get("code") if isinstance(payload, dict) else None
                    if type(code) is int or type(code) is float and math.isfinite(code):
                        details["business_code"] = code
                    raise RushDataError("RushData reported a business error; subsequent steps cannot proceed.", details)
                if "result" not in payload:
                    raise RushDataError("The RushData response is missing result; verify the API contract.")
                return payload["result"]
        except httpx.HTTPError:
            if method.upper() in ("GET", "HEAD"):
                raise RushDataError("The RushData read request timed out or the connection failed; no write was performed.") from None
            raise RushDataError("The RushData request timed out or the connection failed. A write may have taken effect; check its status and do not retry automatically.") from None

    async def _preflight(self, client: httpx.AsyncClient) -> dict[str, Any]:
        company = await self._request(client, "GET", "/customer/companyStatus")
        if not isinstance(company, dict) or company.get("hasCompany") is not True or not _positive_id(company.get("companyId")):
            raise RushDataError("The customer is not linked to a valid company; design cannot start.")
        items = await self._request(client, "GET", "/order/rushData/testItems")
        if not isinstance(items, list) or not items or any(not isinstance(item, dict) for item in items):
            raise RushDataError("The test-item catalog is empty or result is not an array; verify the response structure.")
        return {"company": company, "testItems": items}

    async def preflight(self) -> dict[str, Any]:
        """Read company eligibility and the real test-item catalog; creates no order."""
        async with self._http() as client:
            return await self._preflight(client)

    async def search_antigens(self, keyword: str, page_no: int = 1, page_size: int = 50) -> dict[str, Any]:
        """Merge up to five catalog pages; callers resume with next_page, not page_no + 1."""
        async with self._http() as client:
            first = await self._search_antigen_page(keyword, page_no, page_size, request_client=client)
            # Await every bounded read before closing this customer's request-local connection pool.
            remaining = await asyncio.gather(*(
                self._search_antigen_page(first["keyword"], requested_page, first["page_size"],
                                          request_client=client)
                for requested_page in range(page_no + 1, min(first["pages"], page_no + MAX_CATALOG_PAGES - 1) + 1)
            ), return_exceptions=True)
        options, issues, seen_options = [], [], set()
        records_loaded = pages_loaded = output_bytes = 0
        last_page, next_page = page_no - 1, page_no
        read_error = None
        for offset, page in enumerate([first, *remaining]):
            requested_page = page_no + offset
            if offset:
                try:
                    if isinstance(page, BaseException):
                        raise page
                    if any(page[key] != first[key] for key in ("total", "pages", "page_size")):
                        raise RushDataError(localize_text("产品库分页统计在查询期间发生变化，已停止合并；不能将已有结果视为完整目录。", self.language))
                except RushDataError as error:
                    read_error = {"page_no": requested_page, "message": str(error), "details": error.details}
                    issues.append({"page_no": requested_page, "path": f"pages/{requested_page}",
                                   "code": "page_load_failed", "message": str(error)})
                    break
            new_options, page_keys = [], set()
            for option in page["catalog_options"]:
                key = (option["supplier"], option["catalogNumber"], option["specification"])
                if key not in seen_options and key not in page_keys:
                    new_options.append(option)
                    page_keys.add(key)
            if offset and page["catalog_options"] and not new_options:
                message = localize_text("后续页面只返回了已加载的产品规格，已停止合并；请核对分页，不能确认目录已完整加载。", self.language)
                read_error = {"page_no": requested_page, "message": message}
                issues.append({"page_no": requested_page, "path": f"pages/{requested_page}",
                               "code": "repeated_page", "message": message})
                break
            page_issues = [{**issue, "page_no": requested_page,
                            "path": f"pages/{requested_page}/" + issue["path"]} for issue in page["catalog_issues"]]
            page_bytes = len(json.dumps([new_options, page_issues], ensure_ascii=False).encode("utf-8"))
            # Leave space for the MCP envelope and continuation metadata; keep each page atomic.
            if output_bytes + page_bytes > MAX_RESPONSE_BYTES // 2:
                message = localize_text("本次产品资料较大，已停止合并；请缩小关键词或使用更小的每页数量重新查询。", self.language)
                if not pages_loaded:
                    raise RushDataError(message, {"operation": "search_antigens", "read_only": True,
                                                  "write_performed": False})
                read_error = {"page_no": requested_page, "message": message}
                issues.append({"page_no": requested_page, "path": f"pages/{requested_page}",
                               "code": "result_size_limit", "message": message})
                break
            options.extend(new_options)
            seen_options.update(page_keys)
            issues.extend(page_issues)
            output_bytes += page_bytes
            records_loaded += page["records_loaded"]
            pages_loaded += 1
            last_page = requested_page
            next_page = requested_page + 1 if page["has_more"] else None
            if next_page is None:
                break
        products_loaded = len({(item["supplier"], item["catalogNumber"]) for item in options})
        has_more = next_page is not None
        complete = page_no == 1 and not has_more
        if first["total"] == 0:
            summary = localize_text("百英产品库未找到匹配产品。", self.language)
        elif self.language == "en":
            summary = (f"The Biointron catalog contains {first['total']} matching products. This batch read "
                       f"{records_loaded} product records from pages {page_no}–{last_page}, with "
                       f"{products_loaded} selectable products and {len(options)} specification options.")
            summary += (f" More results remain; continue from page {next_page}." if has_more else
                        " All pages have been read." if complete else
                        " The last page has been reached; earlier pages are not included in this batch.")
            if issues:
                summary += " Some pages or product details have issues; see the details. The number of selectable specifications is not the total number of matching products."
        else:
            summary = (f"百英产品库共 {first['total']} 个匹配产品；本次读取第 {page_no}–{last_page} 页的 "
                       f"{records_loaded} 条产品记录，整理出 {products_loaded} 款可选产品、{len(options)} 个规格选项。")
            summary += (f" 尚未加载完，可从第 {next_page} 页继续。" if has_more else
                        " 已读取全部页面。" if complete else " 已读至末页；本批不包含此前页面。")
            if issues:
                summary += " 部分页面或产品资料存在问题，请查看具体说明；可选规格数不等于匹配产品总数。"
        return {"status": "ready" if options else "catalog_data_error" if records_loaded else "no_results",
                "write_performed": False, "keyword": first["keyword"], "page_no": page_no,
                "page_size": first["page_size"], "total": first["total"], "pages": first["pages"],
                "first_page": page_no, "last_page": last_page, "pages_loaded": pages_loaded,
                "records_loaded": records_loaded, "products_loaded": products_loaded, "options_count": len(options),
                "has_more": has_more, "next_page": next_page, "complete": complete,
                "catalog_summary": summary, "catalog_options": options, "catalog_issues": issues,
                "read_error": read_error}

    async def _search_antigen_page(self, keyword: str, page_no: int, page_size: int, *,
                                   request_client: httpx.AsyncClient | None = None) -> dict[str, Any]:
        """Read and validate one page using the current customer's credentials."""
        if (not isinstance(keyword, str) or not 1 <= len(keyword.strip()) <= 255
                or any(ord(char) < 32 for char in keyword)):
            raise RushDataError(localize_text("请输入 1–255 个字符的抗原关键词，例如 CD2。", self.language))
        if type(page_no) is not int or not 1 <= page_no <= 2147483647:
            raise RushDataError(localize_text("产品库页码必须为正整数。", self.language))
        if type(page_size) is not int or not 1 <= page_size <= 50:
            raise RushDataError(localize_text("产品库每页数量必须为 1–50。", self.language))
        keyword = keyword.strip()
        params = {"keyWord": keyword, "pageNo": page_no, "pageSize": page_size}
        try:
            if request_client is None:
                async with self._http() as client:
                    result = await self._request(client, "GET", "/order/rushData/getBaiYingAntigenList", params=params)
            else:
                result = await self._request(request_client, "GET", "/order/rushData/getBaiYingAntigenList", params=params)
        except RushDataError as error:
            raise RushDataError(str(error), {**error.details, "operation": "search_antigens",
                                             "read_only": True, "write_performed": False}) from None
        if (not isinstance(result, dict) or not isinstance(result.get("records"), list)
                or any(type(result.get(name)) is not int for name in ("current", "size", "total", "pages"))
                or result["current"] != page_no or not 1 <= result["size"] <= 50
                or result["total"] < 0 or result["pages"] < 0
                or result["pages"] != (result["total"] + result["size"] - 1) // result["size"]
                or (result["pages"] > 0 and result["current"] > result["pages"])
                or len(result["records"]) > result["total"]
                or (result["current"] <= result["pages"] and not result["records"])
                or len(result["records"]) > result["size"]):
            raise RushDataError(localize_text("产品库返回的分页结构不完整，请由服务维护方核对；不能把接口错误当作没有产品。", self.language))

        def text_value(record, key, limit, *, required=False):
            value = record.get(key)
            if value is None or value == "":
                if required:
                    raise ValueError(f"Missing {key}" if self.language == "en" else f"缺少 {key}")
                return None
            if (not isinstance(value, str) or len(value.strip()) > limit
                    or any(ord(char) < 32 and char not in "\t\r\n" for char in value)):
                raise ValueError(f"Invalid format for {key}" if self.language == "en" else f"{key} 格式无效")
            value = value.strip()
            if not value and required:
                raise ValueError(f"Missing {key}" if self.language == "en" else f"缺少 {key}")
            return value or None

        def number_value(record, key):
            value = record.get(key)
            if value is not None and (type(value) not in (int, float)
                                      or isinstance(value, float) and not math.isfinite(value)):
                raise ValueError(f"{key} must be a finite number or null" if self.language == "en" else f"{key} 必须为有限数值或空值")
            return value

        options, issues = [], []
        text_limits = {"antigenName": 255, "catalogNo": 128, "supplierName": 255,
                       "sampleLabel": 255, "sampleMolecularWeight": 200, "sampleStorageBuffer": 1000}
        for index, record in enumerate(result["records"]):
            prefix = f"records/{index}"
            try:
                if not isinstance(record, dict):
                    raise ValueError(localize_text("产品记录不是对象", self.language))
                cart = {key: text_value(record, key, limit, required=key in ("antigenName", "catalogNo", "supplierName"))
                        for key, limit in text_limits.items()}
                cart["sampleConcentration"] = number_value(record, "sampleConcentration")
                specs = record.get("specsList")
                if not isinstance(specs, list) or not specs:
                    raise ValueError(localize_text("缺少可选择的产品规格", self.language))
            except ValueError as error:
                issues.append({"path": prefix, "message": str(error)})
                continue
            reference = None
            if record.get("productUrl") not in (None, ""):
                try:
                    reference = text_value(record, "productUrl", 2048)
                    parsed = urlsplit(reference or "")
                    if (parsed.scheme != "https" or not parsed.hostname or parsed.username is not None
                            or parsed.password is not None or any(char.isspace() for char in reference or "")):
                        raise ValueError(localize_text("产品链接格式无效，已省略；仍可按货号选择产品", self.language))
                except ValueError:
                    reference = None
                    issues.append({"path": prefix + "/productUrl", "message": localize_text("产品链接不可用，已省略；仍可按货号选择产品。", self.language)})
            for spec_index, spec in enumerate(specs):
                try:
                    if not isinstance(spec, dict):
                        raise ValueError(localize_text("产品规格不是对象", self.language))
                    specification = text_value(spec, "specs", 255, required=True)
                    cart_data = {**cart, "specification": specification,
                                 "price": number_value(spec, "rmb"), "usdPrice": number_value(spec, "usd")}
                except ValueError as error:
                    issues.append({"path": f"{prefix}/specsList/{spec_index}", "message": str(error)})
                    continue
                parts = [cart["antigenName"], localize_text("货号 ", self.language) + cart["catalogNo"], cart["supplierName"], specification]
                if cart["sampleLabel"]:
                    parts.append(localize_text("标签 ", self.language) + cart["sampleLabel"])
                option = {"label": " · ".join(" ".join(part.split()) for part in parts), "supplier": cart["supplierName"],
                          "catalogNumber": cart["catalogNo"], "specification": specification,
                          "sampleName": cart["antigenName"], "cart_data": cart_data}
                if reference:
                    option["referenceUrl"] = reference
                for source, target in (("sampleLabel", "proteinTag"), ("sampleMolecularWeight", "proteinMolecularWeight"),
                                       ("sampleStorageBuffer", "proteinBuffer")):
                    if cart[source] is not None:
                        option[target] = cart[source]
                if cart["sampleConcentration"] is not None:
                    option["proteinConcentration"] = str(cart["sampleConcentration"])
                options.append(option)
        return {"status": "ready" if options else "catalog_data_error" if result["records"] else "no_results",
                "write_performed": False, "keyword": keyword, "page_no": result["current"],
                "page_size": result["size"], "total": result["total"], "pages": result["pages"],
                "records_loaded": len(result["records"]),
                "has_more": result["current"] < result["pages"], "catalog_options": options, "catalog_issues": issues}

    def _validate_design(self, data: dict[str, Any], content: bytes, filename: str) -> dict[str, list[str]]:
        if not isinstance(data, dict) or set(data) - {
            "id", "projectName", "catalogNumber", "antibodyProjectCount", "antigenCount",
            "sp", "usingdna", "testItems", "antigens", "positiveControls",
        }:
            raise RushDataError("The design request contains unknown fields; use supported fields and testItems name selections.")
        if not isinstance(filename, str) or not filename.lower().endswith(".xlsx") or any(
            char in filename for char in ("/", "\\", "\r", "\n", "\x00")
        ):
            raise RushDataError("Provide an .xlsx filename without a path.")
        if not isinstance(content, bytes) or not 0 < len(content) <= MAX_FILE_BYTES:
            raise RushDataError("The design workbook must be nonempty and no larger than 10 MiB.")
        project = data.get("projectName")
        if not isinstance(project, str) or not 1 <= len(project.strip()) <= 100:
            raise RushDataError("projectName must contain 1-100 characters after trimming whitespace.")
        if type(data.get("antigenCount")) is not int or not 1 <= data["antigenCount"] <= 3:
            raise RushDataError("antigenCount must be an integer from 1 to 3.")
        if data.get("catalogNumber") == "BRD101" and data["antigenCount"] != 1:
            raise RushDataError("The Basic package requires exactly one antigen.")
        if type(data.get("usingdna")) is not bool:
            raise RushDataError("usingdna must be a boolean.")
        if data.get("sp", "") not in ("", "MGWSCIILFLVATATGVHS", "MHSSALLCCLVLLTGVRA"):
            raise RushDataError("sp is not an allowed value.")
        if "id" in data and not _positive_id(data["id"]):
            raise RushDataError("For redesign, id must be the valid original service ID; omit id for a new design.")
        selected = _selection(data, language=self.language)
        if not self.settings.draft_contract_confirmed:
            raise RushDataError("Submitting antigens and positive controls with startDesign requires backend contract confirmation. Writes are blocked until RUSHDATA_DRAFT_CONTRACT_CONFIRMED is verified.")
        antigens = data.get("antigens")
        if not isinstance(antigens, list) or len(antigens) != data["antigenCount"] or any(
            not isinstance(item, dict) for item in antigens
        ):
            raise RushDataError("antigens must be an array of objects with a length equal to antigenCount.")
        for antigen in antigens:
            source = antigen.get("sourceType")
            required = {
                "CUSTOMER_URL": ("referenceUrl",),
                "SUPPLIER_CATALOG": ("supplier", "catalogNumber", "specification"),
                "MANUAL": ("sampleName", "proteinTag", "proteinConcentration", "proteinMolecularWeight", "proteinBuffer"),
            }.get(source) if isinstance(source, str) else None
            if required is None or any(antigen.get(key) is None or not str(antigen[key]).strip() for key in required):
                raise RushDataError("The antigen source type or its required fields do not match the confirmed contract.")
            if "referenceUrl" in antigen:
                reference = antigen["referenceUrl"]
                if not isinstance(reference, str) or len(reference) > 2048:
                    raise RushDataError("Antigen referenceUrl must be an HTTPS URL.")
                try:
                    url = urlsplit(reference)
                except ValueError:
                    raise RushDataError("Antigen referenceUrl is not a valid URL.") from None
                if url.scheme != "https" or not url.hostname or url.username is not None or url.password is not None:
                    raise RushDataError("Antigen referenceUrl must be an HTTPS URL without credentials.")
        if "positiveControls" in data and (not isinstance(data["positiveControls"], list) or any(
            not isinstance(item, dict) for item in data["positiveControls"]
        )):
            raise RushDataError("positiveControls must be an array of objects with backend-confirmed fields; the client does not generate defaults.")
        try:
            json.dumps(antigens, allow_nan=False)
            json.dumps(data.get("positiveControls"), allow_nan=False)
        except (ValueError, TypeError):
            raise RushDataError("Antigens or positive controls contain values that cannot be encoded as JSON.") from None
        return selected

    @staticmethod
    def _resolve_ids(selected: dict[str, list[str]], catalog: list[dict[str, Any]]) -> list[str]:
        # Package sample names stay fixed while the live catalog uses stable keys and display labels.
        sample_keys = {
            "supernatant": "SAMPLE_SUPERNATANT",
            "purified antibody": "SAMPLE_PURIFIED_ANTIBODY",
        }
        ids = []
        for category, names in selected.items():
            for name in names:
                item_key = sample_keys.get(name, name) if category == "SAMPLE_TYPE" else name
                matches = [item for item in catalog if item.get("itemCategory") == category and (
                    item.get("itemKey") in (name, item_key) or item.get("itemName") == name
                )]
                if len(matches) != 1 or not _positive_id(matches[0].get("id")):
                    raise RushDataError(f"The test-item catalog has no unique valid ID for {category}/{name}.")
                ids.append(_positive_id(matches[0]["id"]))
        if len(ids) != len(set(ids)):
            raise RushDataError("Different test items share an ID; verify the backend catalog.")
        return ids

    @staticmethod
    def _capture_identity(payload: dict[str, Any], identity: dict[str, Any]) -> None:
        for key, aliases in IDENTITY_ALIASES.items():
            for alias in aliases:
                if alias not in payload:
                    continue
                value = payload[alias]
                if key == "orderNo":
                    if not _order_number(value):
                        raise RushDataError("The SSE event contains an invalid order number.")
                    known_order = identity.get("orderNo")
                    # The design engine omits RD- in order_no; retain the known canonical number.
                    if (
                        alias == "order_no" and isinstance(known_order, str)
                        and known_order.startswith("RD-") and value == known_order[3:]
                    ):
                        value = known_order
                else:
                    value = _positive_id(value)
                    if value is None:
                        raise RushDataError("The SSE event contains an invalid order ID.")
                if key in identity and identity[key] != value:
                    raise RushDataError("Order identities conflict in the SSE events; subsequent actions have stopped.")
                identity[key] = value

    @staticmethod
    async def _event_lines(response: httpx.Response):
        buffer, size, first = bytearray(), 0, True
        async for chunk in response.aiter_bytes():
            size += len(chunk)
            if size > MAX_RESPONSE_BYTES:
                raise RushDataError("The design SSE stream exceeds 8 MiB; query the order to confirm its outcome.")
            buffer.extend(chunk)
            while buffer:
                endings = [position for position in (buffer.find(b"\r"), buffer.find(b"\n")) if position >= 0]
                if not endings:
                    break
                position = min(endings)
                if buffer[position] == 13 and position == len(buffer) - 1:
                    break  # CRLF may cross a network chunk boundary.
                width = 2 if buffer[position:position + 2] == b"\r\n" else 1
                line = bytes(buffer[:position]).decode("utf-8")
                del buffer[:position + width]
                if first:
                    line, first = line.removeprefix("\ufeff"), False
                yield line
        if buffer.endswith(b"\r"):
            line = bytes(buffer[:-1]).decode("utf-8")
            yield line.removeprefix("\ufeff") if first else line

    async def _design(self, client: httpx.AsyncClient, parts: list, identity: dict[str, Any]) -> None:
        completed = False
        event, data_lines = "message", []
        try:
            async with asyncio.timeout(self.settings.design_timeout):
                async with client.stream(
                    "POST", "order/rushData/startDesign", files=parts,
                    headers={"Accept": "text/event-stream"}, timeout=self.settings.design_timeout,
                ) as response:
                    if not 200 <= response.status_code < 300:
                        raise RushDataError(f"startDesign returned HTTP {response.status_code}.")
                    if response.headers.get("content-type", "").split(";", 1)[0].strip().lower() != "text/event-stream":
                        raise RushDataError("startDesign did not return SSE; design success cannot be confirmed.")
                    async for line in self._event_lines(response):
                        if line.startswith(":"):
                            continue
                        if line:
                            field, _, value = line.partition(":")
                            value = value.removeprefix(" ")
                            if field == "event":
                                event = value
                            elif field == "data":
                                data_lines.append(value)
                            continue
                        if event in {"order_created", "completed", "result_saved", "design_error", "result_save_failed", "proxy_error"}:
                            try:
                                payload = json.loads("\n".join(data_lines))
                            except ValueError:
                                raise RushDataError("A required SSE event does not contain valid JSON.") from None
                            if not isinstance(payload, dict):
                                raise RushDataError("A required SSE event must contain a top-level JSON object; verify the backend structure.")
                            self._capture_identity(payload, identity)
                            if event in {"design_error", "result_save_failed", "proxy_error"}:
                                raise RushDataError(f"The design stream reported the failure event {event}.")
                            if event == "completed":
                                if payload.get("status") != "ok":
                                    raise RushDataError("The design completed status is not ok.")
                                completed = True
                            if event == "result_saved":
                                if not completed or "rushDataServiceId" not in identity:
                                    raise RushDataError("result_saved requires an earlier completed.status=ok and a valid service ID.")
                                return
                        event, data_lines = "message", []
        except (TimeoutError, httpx.HTTPError):
            raise RushDataError("The design connection was interrupted or timed out. The order may exist; query its known identity and do not create another design.") from None
        except UnicodeError:
            raise RushDataError("The design SSE stream is not valid UTF-8.") from None
        raise RushDataError("The design SSE stream ended before both completed.status=ok and result_saved were confirmed.")

    async def _orders(self, client: httpx.AsyncClient, page_no: int) -> dict[str, Any]:
        if type(page_no) is not int or page_no < 1:
            raise RushDataError("page_no must be a positive integer.")
        result = await self._request(client, "GET", "/order/rushData/orders", params={
            "pageNo": page_no, "pageSize": 10, "orderStatus": "00",
        })
        if not isinstance(result, dict) or not isinstance(result.get("records"), list) or any(
            not isinstance(record, dict) for record in result["records"]
        ) or type(result.get("pages")) is not int or not 0 <= result["pages"] <= 1000:
            raise RushDataError("Cart pagination is invalid or exceeds the 1000-page client limit; the order cannot be located reliably.")
        if result.get("current") != page_no or (result["pages"] == 0 and result["records"]):
            raise RushDataError("The cart response has inconsistent page numbers or records.")
        return result

    async def orders(self, page_no: int = 1) -> dict[str, Any]:
        async with self._http() as client:
            return await self._orders(client, page_no)

    async def _cart_records(self, client: httpx.AsyncClient):
        page = 1
        while True:
            result = await self._orders(client, page)
            for record in result["records"]:
                yield record
            if page >= result["pages"]:
                return
            page += 1

    async def start_design(
        self, data: dict[str, Any], file_content: bytes, filename: str, *,
        on_design_start: Callable[[], None] | None = None,
    ) -> dict[str, Any]:
        """Create/re-design and confirm durable results; do not change the cart."""
        if not isinstance(data, dict):
            raise RushDataError("The design request must be an object.")
        if not isinstance(file_content, bytes) or not 0 < len(file_content) <= MAX_FILE_BYTES:
            raise RushDataError("The design workbook must be nonempty and no larger than 10 MiB.")
        data = dict(data)
        data.pop("antibodyProjectCount", None)
        try:
            data["antibodyProjectCount"] = count_antibody_records(file_content)
        except ValueError:
            # Preserve the original file; an unknown count is omitted for API-side validation.
            pass
        selected = self._validate_design(data, file_content, filename)
        identity: dict[str, Any] = {"projectName": data["projectName"].strip()}
        phase = "preflight"
        try:
            async with self._http() as client:
                preflight = await self._preflight(client)
                ids = self._resolve_ids(selected, preflight["testItems"])
                fields = {key: str(data[key]) for key in (
                    "catalogNumber", "antigenCount",
                )}
                if "antibodyProjectCount" in data:
                    fields["antibodyProjectCount"] = str(data["antibodyProjectCount"])
                fields.update(projectName=identity["projectName"], sp=data.get("sp", ""),
                              usingdna=str(data["usingdna"]).lower())
                if "id" in data:
                    fields["id"] = _positive_id(data["id"])
                    identity["rushDataServiceId"] = fields["id"]
                for key in ("antigens", "positiveControls"):
                    if key in data:
                        fields[key] = json.dumps(data[key], ensure_ascii=False, allow_nan=False)
                parts = [(key, (None, value)) for key, value in fields.items()]
                parts.extend(("testItemIds", (None, item_id)) for item_id in ids)
                parts.append(("file", (filename, file_content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")))
                if on_design_start is not None:
                    on_design_start()
                phase = "startDesign"
                await self._design(client, parts, identity)
                return {"status": "result_saved", **identity, "result_saved_verified": True}
        except RushDataError as error:
            error.details = {**error.details, "phase": phase, **identity,
                             "write_may_have_occurred": phase != "preflight", "retry_write": False}
            raise

    async def get_design_result(self, identity: dict[str, Any]) -> dict[str, Any]:
        """Read the existing design HTML for a caller-verified saved identity."""
        english = self.language == "en"
        service_id = _positive_id(identity.get("rushDataServiceId")) if isinstance(identity, dict) else None
        if service_id is None or int(service_id) > 2147483647:
            raise RushDataError("A verified positive int32 service ID is required to read the design result."
                                if english else "查看设计结果需要已核验的正整数 int32 服务 ID。")
        order_no, project_name = identity.get("orderNo"), identity.get("projectName")
        if (not _order_number(order_no) or len(order_no) > 100
                or not isinstance(project_name, str) or not 1 <= len(project_name.strip()) <= 100):
            raise RushDataError("The saved order number and project name are required to read the design result."
                                if english else "查看设计结果需要已保存的订单号和项目名。")
        try:
            async with self._http() as client, client.stream(
                "GET", "order/rushData/report", params={"rushDataServiceId": service_id},
                headers={"Accept": "text/html"},
            ) as response:
                if not 200 <= response.status_code < 300:
                    raise RushDataError(f"The design result request returned HTTP {response.status_code}."
                                        if english else f"设计结果请求返回 HTTP {response.status_code}。",
                                        {"http_status": response.status_code})
                media_type = response.headers.get("content-type", "").split(";", 1)[0].strip().lower()
                if media_type == "application/json" or media_type.endswith("+json"):
                    raise RushDataError("The design result endpoint returned JSON instead of HTML."
                                        if english else "设计结果接口返回了 JSON，未返回 HTML 设计报告。")
                if media_type not in {"", "text/html", "application/xhtml+xml", "text/plain", "application/octet-stream"}:
                    raise RushDataError("The design result endpoint did not return an HTML content type."
                                        if english else "设计结果接口未返回 HTML 内容类型。")
                body = bytearray()
                async for chunk in response.aiter_bytes():
                    body.extend(chunk)
                    if len(body) > MAX_RESPONSE_BYTES:
                        raise RushDataError("The design HTML exceeds the 8 MiB limit."
                                            if english else "设计 HTML 超过 8 MiB 限制。")
                if not body:
                    raise RushDataError("The design result endpoint returned an empty response."
                                        if english else "设计结果接口返回空内容。")
                encoding = response.charset_encoding
                try:
                    html = body.decode(encoding if encoding is not None else "utf-8-sig", errors="strict")
                except (LookupError, UnicodeError):
                    raise RushDataError("The design HTML could not be decoded using its declared character set or UTF-8."
                                        if english else "设计 HTML 无法按声明的字符集或 UTF-8 正确解码。") from None
                prefix = re.match(r"(?:[\ufeff\s]+|<!--.*?-->|<\?xml\s.*?\?>)*", html, re.DOTALL | re.IGNORECASE)
                document = html[prefix.end():]
                if not document:
                    raise RushDataError("The design result endpoint returned an empty HTML document."
                                        if english else "设计结果接口返回空 HTML 文档。")
                if document.startswith(("{", "[")):
                    raise RushDataError("The design result endpoint returned JSON instead of HTML."
                                        if english else "设计结果接口返回了 JSON，未返回 HTML 设计报告。")
                if not re.match(r"(?:<!doctype\s+html(?:\s|>)|<html(?:\s|>))", document, re.IGNORECASE):
                    raise RushDataError("The design result response is not an HTML document."
                                        if english else "设计结果响应不是完整的 HTML 文档。")
        except httpx.HTTPError:
            raise RushDataError("The design result read failed or timed out; no retry or order write was performed."
                                if english else "设计结果读取失败或超时；未重试，也未执行订单写入。",
                                {"phase": "getDesignResult", "read_only": True, "write_performed": False,
                                 "retry_write": False, "orderNo": order_no, "rushDataServiceId": service_id}) from None
        except RushDataError as error:
            error.details = {**error.details, "phase": "getDesignResult", "read_only": True,
                             "write_performed": False, "retry_write": False, "orderNo": order_no,
                             "rushDataServiceId": service_id}
            raise
        safe_order = re.sub(r"[^A-Za-z0-9_-]+", "_", order_no).strip("_") or service_id
        return {"status": "design_result_ready", "orderNo": order_no, "projectName": project_name,
                "filename": f"RushData_Design_{safe_order}.html", "mime_type": "text/html", "html": html,
                "write_performed": False, "report_type": "design"}

    @staticmethod
    def _validate_cart_data(cart_data: dict[str, Any]) -> dict[str, Any]:
        """Validate the current cart body without accepting client-supplied order identity."""
        required = {"projectNo", "shippingRequired", "antigens"}
        if (not isinstance(cart_data, dict) or required - set(cart_data)
                or set(cart_data) - (required | {"positiveControl"})):
            raise RushDataError("cart_data requires projectNo, shippingRequired and antigens; only positiveControl is optional. Order identity cannot be overridden.")
        project_no = cart_data["projectNo"]
        if (not isinstance(project_no, str) or not 1 <= len(project_no.strip()) <= 100
                or project_no.strip() == "—" or any(ord(char) < 32 for char in project_no)):
            raise RushDataError("cart_data.projectNo must be the existing project number, with 1-100 characters and not a placeholder.")
        if type(cart_data["shippingRequired"]) is not bool:
            raise RushDataError("cart_data.shippingRequired must explicitly be true or false; no default is applied.")
        if "positiveControl" in cart_data and not isinstance(cart_data["positiveControl"], str):
            raise RushDataError("cart_data.positiveControl must be a string of selected protein names, or an empty string.")
        antigens = cart_data["antigens"]
        if not isinstance(antigens, list) or not 1 <= len(antigens) <= 3:
            raise RushDataError("cart_data.antigens must contain one to three antigen objects.")
        text_limits = {"antigenName": 255, "catalogNo": 128, "specification": 255, "productUrl": 1000,
                       "sampleLabel": 255, "sampleMolecularWeight": 200,
                       "sampleStorageBuffer": 1000, "supplierName": 255}
        numeric_fields = {"price", "usdPrice", "sampleConcentration"}
        checked = []
        for antigen in antigens:
            if not isinstance(antigen, dict) or set(antigen) - (set(text_limits) | numeric_fields):
                raise RushDataError("Each cart antigen must use the confirmed antigen DTO fields; sourceType and other legacy fields are not accepted.")
            item = dict(antigen)
            for field, limit in text_limits.items():
                value = item.get(field)
                if value is not None:
                    if not isinstance(value, str) or len(value.strip()) > limit:
                        raise RushDataError(f"Cart antigen {field} must be a string of at most {limit} characters, or null.")
                    item[field] = value.strip() or None
            for field in numeric_fields:
                value = item.get(field)
                if value is not None and (type(value) not in (int, float)
                        or isinstance(value, float) and not math.isfinite(value)):
                    raise RushDataError(f"Cart antigen {field} must be a finite JSON number, or null.")
            product_url = item.get("productUrl")
            if product_url:
                try:
                    url = urlsplit(product_url)
                except ValueError:
                    raise RushDataError("Cart antigen productUrl must be a valid HTTPS URL.") from None
                if (url.scheme != "https" or not url.hostname or url.username is not None
                        or url.password is not None or any(char.isspace() for char in product_url)):
                    raise RushDataError("Cart antigen productUrl must be an HTTPS URL without credentials or whitespace.")
                if any(value is not None for field, value in item.items() if field != "productUrl"):
                    raise RushDataError("A URL antigen cannot also contain product fields; provide only productUrl and null fields.")
            elif any(not item.get(field) for field in ("antigenName", "catalogNo", "supplierName")):
                raise RushDataError("A product antigen requires antigenName, catalogNo and supplierName.")
            checked.append(item)
        return {**cart_data, "projectNo": project_no.strip(), "antigens": checked}

    async def verify_cart_identity(self, identity: dict[str, Any], cart_data: dict[str, Any]) -> None:
        """Read the exact saved master order before a cart write; never guess an ID or pick the first order."""
        master_id = _positive_id(identity.get("orderId"))
        if master_id is None or int(master_id) > 2147483647:
            raise RushDataError("Saved design is missing a valid master orderId; verify the original order without recreating the design.")
        body = self._validate_cart_data(cart_data)
        async with self._http() as client:
            detail = await self._request(client, "GET", "/order/rushData/detail", params={"orderId": master_id})
        # 当前前端将 -3 用于草稿、00 用于购物车。旧签名仍有效也不能将已提交/未知状态的订单再加购。
        if not isinstance(detail, dict) or detail.get("orderStatus") not in ("-3", "00"):
            raise RushDataError("The current order is not a confirmed draft or cart item; verify its status without writing again.")
        # detail.id 是 RushData 服务 ID，而 detail.orderId 是主订单 ID，不能混用。
        if (not isinstance(detail, dict)
                or _positive_id(detail.get("id")) != _positive_id(identity.get("rushDataServiceId"))
                or _positive_id(detail.get("orderId")) != master_id
                or detail.get("orderNo") != identity.get("orderNo")
                or detail.get("projectName") != identity.get("projectName")
                or detail.get("projectNo") != body["projectNo"]):
            raise RushDataError("Order detail does not match the saved order identity and cart_data.projectNo; no cart write was sent.")

    async def saved_order_in_cart(self, identity: dict[str, Any]) -> dict[str, Any] | None:
        """Check the exact saved order before writing; this read is not an atomic idempotency guarantee."""
        service_id = _positive_id(identity.get("rushDataServiceId"))
        order_no = identity.get("orderNo")
        if service_id is None or not _order_number(order_no):
            raise RushDataError("A verified service ID and order number are required to check the cart.")
        matches = []
        async with self._http() as client:
            async for record in self._cart_records(client):
                if _positive_id(record.get("id")) == service_id or record.get("orderNo") == order_no:
                    if (_positive_id(record.get("id")) != service_id or record.get("orderNo") != order_no
                            or record.get("orderStatus") != "00"):
                        raise RushDataError("The cart record conflicts with the saved order identity or state; no write was sent.")
                    matches.append(record)
        if len(matches) > 1:
            raise RushDataError("More than one cart record matches this order; verify existing records without writing again.")
        if not matches:
            return None
        return {"status": "cart_confirmed", **identity, "cart": matches[0]}

    async def add_to_cart(
        self, rush_data_service_id: str | int, project_name: str, order_no: str | None = None,
        *, cart_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Internal step: callers must verify server-issued saved-result proof first."""
        service_id = _positive_id(rush_data_service_id)
        if service_id is None or int(service_id) > 2147483647:
            raise RushDataError("rush_data_service_id must be a positive int32 service ID.")
        if not isinstance(project_name, str) or not 1 <= len(project_name.strip()) <= 100:
            raise RushDataError("project_name must contain 1-100 characters after trimming whitespace.")
        if not _order_number(order_no) or len(order_no) > 100:
            raise RushDataError("order_no must be the saved order number and contain at most 100 characters.")
        body = self._validate_cart_data(cart_data)
        identity: dict[str, Any] = {"rushDataServiceId": service_id, "projectName": project_name.strip(),
                                    "orderNo": order_no}
        # Identity comes only from the verified saved result, never from cart_data.
        body.update(identity, rushDataServiceId=int(service_id))
        phase = "addToCart"
        try:
            async with self._http() as client:
                added = await self._request(client, "POST", "/order/rushData/addToCart", json=body)
                if isinstance(added, dict):
                    self._capture_identity(added, identity)
                phase = "confirmCart"
                matches = []
                async for record in self._cart_records(client):
                    if _positive_id(record.get("id")) == identity["rushDataServiceId"]:
                        if not _order_number(record.get("orderNo")) or (
                            "orderNo" in identity and record["orderNo"] != identity["orderNo"]
                        ) or record.get("orderStatus") != "00":
                            raise RushDataError("The cart record has a conflicting order number or state.")
                        matches.append(record)
                if len(matches) != 1:
                    raise RushDataError("The cart write succeeded, but a unique matching record was not found. Confirm with read-only queries; do not create another design.")
                identity["orderNo"] = matches[0]["orderNo"]
                return {"status": "cart_confirmed", **identity, "cart": matches[0]}
        except RushDataError as error:
            error.details = {**error.details, "phase": phase, **identity,
                             "write_may_have_occurred": True, "retry_write": False}
            raise

    async def design_to_cart(
        self, data: dict[str, Any], file_content: bytes, filename: str, *,
        on_design_start: Callable[[], None] | None = None,
        on_design_saved: Callable[[dict[str, Any]], Awaitable[dict[str, Any]]] | None = None,
    ) -> dict[str, Any]:
        """Save the design, await the client's preview choice and cart inputs, then add it."""
        if not callable(on_design_saved):
            raise RushDataError("A saved-design callback is required to ask about the HTML result before cart entry."
                                if self.language == "en" else "进入购物车前必须通过设计保存回调询问是否查看 HTML 结果。",
                                {"phase": "beforeDesign", "write_may_have_occurred": False,
                                 "cart_write_attempted": False, "retry_write": False})
        saved = await self.start_design(data, file_content, filename, on_design_start=on_design_start)
        phase = "designResultChoice"
        try:
            cart_data = await on_design_saved(dict(saved))
            phase = "validateCartData"
            cart_data = self._validate_cart_data(cart_data)
            # A valid project-number format is not proof that it belongs to this saved design.
            phase = "verifyCartIdentity"
            await self.verify_cart_identity(saved, cart_data)
            phase = "addToCart"
            added = await self.add_to_cart(saved["rushDataServiceId"], saved["projectName"], saved.get("orderNo"),
                                           cart_data=cart_data)
            return {**saved, **added}
        except (Exception, KeyboardInterrupt, asyncio.CancelledError) as error:
            # Design already completed; retain its identity even when no cart write was sent.
            if not isinstance(error, RushDataError):
                cancelled = isinstance(error, (EOFError, KeyboardInterrupt, asyncio.CancelledError))
                error = RushDataError(
                    ("The design is saved, but continuation was cancelled." if cancelled else
                     "The design is saved, but continuation could not be completed.") if self.language == "en" else
                    ("设计已保存，后续操作已取消。" if cancelled else "设计已保存，但后续操作未完成。"))
            error.details = {**error.details, **{
                key: saved[key] for key in ("projectName", "rushDataServiceId", "orderNo", "orderId") if key in saved
            }, "phase": error.details.get("phase", phase), "result_saved_verified": True,
                "write_may_have_occurred": True, "cart_write_attempted": phase == "addToCart",
                "retry_write": False,
                "next_action": "Verify the saved order; do not restart design or retry writes automatically."
                if self.language == "en" else "请核查已保存的订单；不要重新设计或自动重试写入。"}
            raise error from None

    async def _quote(self, client: httpx.AsyncClient, order_nos: list[str]) -> dict[str, Any]:
        result = await self._request(client, "POST", "/order/rushData/price/calculate", json={"orderNos": ",".join(order_nos)})
        if not isinstance(result, dict) or not isinstance(result.get("orders"), list) or any(
            not isinstance(order, dict) or not _order_number(order.get("orderNo")) for order in result["orders"]
        ):
            raise RushDataError("The quote structure is invalid; the order cannot be submitted.")
        quoted = [order["orderNo"] for order in result["orders"]]
        if len(quoted) != len(order_nos) or set(quoted) != set(order_nos):
            raise RushDataError("The quoted orders do not exactly match the selection; submission is blocked.")
        return result

    async def quote(self, order_nos: list[str]) -> dict[str, Any]:
        order_nos = _order_numbers(order_nos)
        async with self._http() as client:
            return await self._quote(client, order_nos)

    async def submit(self, order_nos: list[str]) -> dict[str, Any]:
        """Requote the exact selection, submit once, then only read cart state."""
        order_nos = _order_numbers(order_nos)
        phase = "price/calculate"
        try:
            async with self._http() as client:
                quote = await self._quote(client, order_nos)
                if quote.get("canSubmit") is not True:
                    message = quote.get("submitMessage")
                    message = message.replace(self.settings.access_token, "[redacted]")[:500] if isinstance(message, str) else ""
                    raise RushDataError("The quote does not allow submission. " + message)
                phase = "submit/batch"
                result = await self._request(client, "POST", "/order/rushData/submit/batch",
                    json={"orderNos": ",".join(order_nos)}, headers={"Time-Zone": self.settings.time_zone})
                phase = "refreshCart"
                remaining = []
                async for record in self._cart_records(client):
                    if record.get("orderNo") in order_nos:
                        remaining.append(record["orderNo"])
                if remaining:
                    raise RushDataError("Submission succeeded, but the orders remain in the cart. Verify with read-only queries; do not resubmit.", {"remainingOrderNos": remaining})
                return {"status": "submitted_cart_cleared", "orderNos": order_nos, "quote": quote,
                        "result": result, "experimentSubmissionVerified": True}
        except RushDataError as error:
            error.details = {**error.details, "phase": phase, "orderNos": order_nos,
                             "write_may_have_occurred": phase != "price/calculate", "retry_write": False}
            raise
