"""RushData's documented order workflow; no automatic write retries."""

from __future__ import annotations

import asyncio
import json
from typing import Any
from urllib.parse import urlsplit

import httpx


MAX_RESPONSE_BYTES = 8 * 1024 * 1024
MAX_FILE_BYTES = 10 * 1024 * 1024
CATEGORIES = ("SAMPLE_TYPE", "PROTEIN_PROPERTY", "BINDING", "DEVELOPABILITY")
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


def _selection(data: dict[str, Any]) -> dict[str, list[str]]:
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
    sample, protein, binding, develop = (set(selected[category]) for category in CATEGORIES)
    if sample == {"supernatant"}:
        valid = protein == {"Titer"} and bool(binding) and binding <= {
            "FACS_iQue_1_point", "ELISA_1_point",
        } and not develop
    elif sample == {"purified antibody"}:
        valid = bool(protein) and protein <= {"cGE", "SEC_HPLC", "SEC_UPLC"} and bool(
            binding or develop
        ) and binding <= BINDING and develop <= DEVELOPABILITY
    else:
        valid = False
    if not valid:
        raise RushDataError("Package 4 has an invalid sample type, test selection, or combination.")
    return selected


def _order_numbers(order_nos: list[str]) -> list[str]:
    if not isinstance(order_nos, list) or not order_nos or any(
        not _order_number(value) for value in order_nos
    ) or len(set(order_nos)) != len(order_nos):
        raise RushDataError("order_nos must be a nonempty array of unique order numbers without commas or control characters.")
    return list(order_nos)


class RushDataClient:
    def __init__(self, settings: Any, transport: httpx.AsyncBaseTransport | None = None):
        try:
            settings.require_connection()
        except ValueError as error:
            raise RushDataError(str(error)) from None
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
                    raise RushDataError(f"RushData returned HTTP {response.status_code}.")
                body = bytearray()
                async for chunk in response.aiter_bytes():
                    body.extend(chunk)
                    if len(body) > MAX_RESPONSE_BYTES:
                        raise RushDataError("The RushData response exceeds 8 MiB.")
                try:
                    payload = json.loads(body)
                except (ValueError, UnicodeError):
                    raise RushDataError("RushData did not return valid JSON.") from None
                if not isinstance(payload, dict) or str(payload.get("code")) != "200" or (
                    "success" in payload and payload["success"] is not True
                ):
                    raise RushDataError("RushData reported a business error; subsequent steps cannot proceed.")
                if "result" not in payload:
                    raise RushDataError("The RushData response is missing result; verify the API contract.")
                return payload["result"]
        except httpx.HTTPError:
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
        if type(data.get("antibodyProjectCount")) is not int or not 48 <= data["antibodyProjectCount"] <= 999:
            raise RushDataError("antibodyProjectCount must be an integer from 48 to 999.")
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
        selected = _selection(data)
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
                "SUPPLIER_CATALOG": ("supplier", "catalogNumber", "specification", "referenceUrl"),
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
        ids = []
        for category, names in selected.items():
            for name in names:
                matches = [item for item in catalog if item.get("itemCategory") == category and (
                    item.get("itemKey") == name or item.get("itemName") == name
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

    async def start_design(self, data: dict[str, Any], file_content: bytes, filename: str) -> dict[str, Any]:
        """Create/re-design and confirm durable results; do not change the cart."""
        selected = self._validate_design(data, file_content, filename)
        identity: dict[str, Any] = {"projectName": data["projectName"].strip()}
        phase = "preflight"
        try:
            async with self._http() as client:
                preflight = await self._preflight(client)
                ids = self._resolve_ids(selected, preflight["testItems"])
                fields = {key: str(data[key]) for key in (
                    "catalogNumber", "antibodyProjectCount", "antigenCount",
                )}
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
                phase = "startDesign"
                await self._design(client, parts, identity)
                return {"status": "result_saved", **identity, "result_saved_verified": True}
        except RushDataError as error:
            error.details = {**error.details, "phase": phase, **identity,
                             "write_may_have_occurred": phase != "preflight", "retry_write": False}
            raise

    async def add_to_cart(
        self, rush_data_service_id: str | int, project_name: str, order_no: str | None = None,
    ) -> dict[str, Any]:
        """Internal step: callers must verify server-issued saved-result proof first."""
        service_id = _positive_id(rush_data_service_id)
        if service_id is None:
            raise RushDataError("rush_data_service_id must be a valid service ID.")
        if not isinstance(project_name, str) or not 1 <= len(project_name.strip()) <= 100:
            raise RushDataError("project_name must contain 1-100 characters after trimming whitespace.")
        if order_no is not None and not _order_number(order_no):
            raise RushDataError("order_no must be a valid order number.")
        identity: dict[str, Any] = {"rushDataServiceId": service_id, "projectName": project_name.strip()}
        if order_no is not None:
            identity["orderNo"] = order_no
        phase = "addToCart"
        try:
            async with self._http() as client:
                added = await self._request(client, "POST", "/order/rushData/addToCart", params={
                    "rushDataServiceId": identity["rushDataServiceId"], "projectName": identity["projectName"],
                })
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

    async def design_to_cart(self, data: dict[str, Any], file_content: bytes, filename: str) -> dict[str, Any]:
        """Create/re-design, await durable results, then add and identify the cart item."""
        saved = await self.start_design(data, file_content, filename)
        try:
            added = await self.add_to_cart(saved["rushDataServiceId"], saved["projectName"], saved.get("orderNo"))
            return {**saved, **added}
        except RushDataError as error:
            # Preserve the server-observed identity so an MCP adapter can sign recovery proof.
            error.details = {**error.details, **{
                key: saved[key] for key in ("projectName", "rushDataServiceId", "orderNo", "orderId") if key in saved
            }, "result_saved_verified": True}
            raise

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
                    message = message[:500].replace(self.settings.access_token, "[redacted]") if isinstance(message, str) else ""
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
