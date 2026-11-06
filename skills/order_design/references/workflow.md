# Order Workflow Rules

This is a detailed execution reference, not a prerequisite for the opening package question or product-library search. Before the first design, cart, quote or submission operation, load `order_design(phase="execute", language=language)` once and reuse its default `detail="compact"` execution rules and connection metadata across later stages. An existing order follows the same rule. Only a concrete question unresolved by that guidance warrants explicit `detail="full"` or reading the relevant reference section. Library search uses current tool descriptions and `catalog_auth` from the local input response. Read [business-context.md](business-context.md) for a specific business explanation when needed; do not routinely load both references. That reference distinguishes the 2026-11-04 business requirements from current API support; it does not override the request contracts below.

## Local Input Requirements

The client selects `language="zh"` or `language="en"` from the customer's natural-language instructions, retains it through keywords, SKUs, paths, credentials, numbers and short selections, and follows a clear later language change. Pass it explicitly to every `order_design` prompt and order MCP call, including subsequent validation, search pages, authentication guidance, preflight and write results. CLI uses `--language zh` or `--language en`; omitted language defaults to `zh` only for backward compatibility. Do not infer language from the wording of this reference or keep mutable global language on the server. Store it only in the outer client conversation/handoff, never in `supplied`, `data`, business requests or signed `workflow_context`.

All customer-facing text follows that language: package introductions, question titles/help, options, missing-input and validation errors, credential/configuration guidance, catalog summaries/navigation and wait/result messages. Preserve the chosen-language fixed copy verbatim. API field names, enum values, assay keys, brands, original customer/product data and credentials remain unchanged. Keep raw backend errors as evidence; explain them in the selected language rather than displaying an untranslated error as the whole customer reply.

A new-order conversation starts with package explanations and an immediate native selection question using the current entry copy. Only when that copy is absent, get the compact `order_design` prompt once; do not fetch a full schema, initialize an existing connection again or inspect service versions before the first question. After the package answer, call local input guidance with confirmed data. A Customized choice is immediately followed by its sample-form routing question; the customer-confirmed protein-property, binding and developability choices then join the next eligible independent-field batch. Antibody quantity is excluded from the public form and must not become a customer question or confirmation step; wait for the design workbook and derive it internally. Package and local-data questions need no credentials. Upon choosing our product library, check the current valid JWT or obtain missing Biointron Account/App Key values before its keyword question and search. External-link and manual modes defer authentication until submission. All modes perform the read-only company-eligibility/test-item preflight before design submission. A new-customer reset clears prior context without cancelling real orders. Never put account or App Key into `supplied`.

`get_order_input_requirements(stage, supplied=None, language="zh", detail="compact", mode="collect")` defaults to collection only. It returns `status=collecting|collected`, `validation_deferred=true`, `write_performed=false`, and a batch of independent questions. `collected` means the known branch has been collected, not that input is valid or a write is authorized. Ask routing decisions (package, Customized sample form, antigen source) separately before their dependent fields. Then invoke the returned `interaction.native_question.questions` in one native call for independent text and choice fields, using the selected language. Merge the whole batch before requesting the next branch or batch; do not call MCP, the model or full validation after every field. CLI prompts through the same batch sequentially without model/MCP round trips, rule rereads or business validation inside the batch. Missing or blank routing answers still need questions. Preserve real `false`, `0` and explicitly supplied `[]`; never invent defaults. Collection does not perform full business validation or scan XLSX contents.

| Stage | Shape of `supplied` |
| --- | --- |
| `design` | `{"data": <known design object>, "filename": <known filename>, "file_base64": <available original XLSX Base64>}` |
| `cart` | `{"cart_data": <known cart object>}` |

Omit unknown values or omit `supplied` entirely; never pass placeholder strings as actual data. `detail="compact"` omits the full schema and diagnostic inventory; `detail="full"` exposes them when explicitly needed. Collection returns the next routing question or independent-field batch in `interaction.native_question`, plus original option values and applicable action/catalog metadata. Follow `next_action` / `interaction.required_action` before asking dependent questions. Product search keeps its credential prerequisite and actual candidates/navigation; `contact_service_operator` is a configuration problem, not a customer field. A valid JWT already held by the client satisfies a generic credential reminder. Never put credential values in `supplied`.

Reuse existing information and collect independent fields in the same native `questions` array after the routing decisions. Do not validate each answer or ask the model/MCP to choose the next field within an already returned batch. CLI asks the same batch through consecutive terminal prompts. Explicit `false`, `0` and empty category arrays are answers, not missing values; whether they satisfy business constraints is checked at validation. Empty/absent branch choices still need questions. Examples are never defaults, shipping requires an actual choice, and `positiveControl` remains optional. Follow the native tool question-count limit by splitting locally if necessary.

Prefer native free-text input. Codex `request_user_input_async` uses `questions: [{title: "...", options?: ["..."]}]`; omit `options` for text fields, and use explicit options for selections. Both types require a real tool call. If another available question tool requires two or three choices and offers Other/custom text, direct the user to enter the actual field value in that text box. Required choices such as “填写此项” and “暂不提供” are UI actions only: do not store them as account/project/URL values, and do not invent actual accounts or links as choices. An action without a supplied value does not complete the question. Use only tools exposed and permitted in the current client and mode; do not switch to Plan mode for `request_user_input` or overlook another available native tool because that one is restricted. Never claim that a dialog appeared without invoking one.

The `design_workbook` question uses `input_type="text"`, `ui_only=true` and `client_action="read_local_design_workbook"` to collect the local `.xlsx` path through an actual native text question or terminal prompt, including CLI: “请输入本次抗体设计表（.xlsx）的本地文件路径” (`zh`) or “Please enter the local path to the antibody design workbook (.xlsx) for this order” (`en`). A client with a real file picker may invoke it instead, and an available original attachment for this order should be reused. Do not merely print “please upload” and wait without an input action. Although the question identifies the missing `file_base64` field, its answer is only a client-side path: read the original file locally, then supply its basename as `filename` and its bytes encoded as `file_base64`. Never put the path text into `file_base64` or send it to remote MCP as a readable path. On an actual file-read failure, or a violation of file-name, nonempty-file or size transport limits, explain the issue and repeat this file question while preserving other answers. Excel template/content recognition and quantity-range checks must not block locally. Do not rescan the workbook during MCP question routing: the actual `start_design` path attempts one count before writing. If no reliable count is available, omit the quantity field and let the API judge the unchanged file, without a quantity question or a replacement-file demand.

For example, after routing is settled, these independent fields may be requested in one `request_user_input_async` call. For `language="zh"`:

```json
{"questions":[{"title":"请输入本次项目名称"},{"title":"是否指定使用客户提供的 DNA？","options":["是","否"]},{"title":"请输入本次抗体设计表（.xlsx）的本地文件路径"}]}
```

For `language="en"`, use the corresponding single batch instead:

```json
{"questions":[{"title":"Please enter the project name for this order"},{"title":"Use the customer-provided DNA?","options":["Yes","No"]},{"title":"Please enter the local path to the antibody design workbook (.xlsx) for this order"}]}
```

Prefer the actual generated questions and omit already answered fields; these examples are tool arguments, not customer paste templates. The file answer is a UI-only local path: read it locally and send only `filename`/`file_base64` to MCP. Keep the question pending until actual answers arrive, then merge the batch. Do not search the repository or launch a business CLI merely to collect these values. If native questions are genuinely unavailable, explain that limitation and collect the same batch through the available text/terminal interface; there is no per-field model, MCP or validation round trip. MCP cannot force every client to render a popup.

When our product library is chosen, or at submission for other modes, reuse the current valid JWT or ask only for missing **Biointron Account** and then **App Key** as separate ordinary text fields. App Key does not require masking, hidden input or a separate secure dialog. Do not prefill or repeat a supplied value in later replies, logs or reports. Internal API fields remain `username` and `appkey`. Do not ask customers for the backend API address; it is provided by server config.

After a completed batch, merge known inputs and preserve real `false`, `0` and `[]`. Request collection guidance only when moving to a new branch/batch or resolving an unanswered routing choice, not after every field. Reuse the current language, valid JWT, answers and candidates. Do not insert planning, order recaps, discovery, reconnects, rule rereads or repeated authentication within collection. Keep pending questions active instead of ending with a missing-fields summary. These structural changes remove per-field round trips; they do not establish a measured or guaranteed response time.

Immediately before an actual design or cart write, call `get_order_input_requirements(..., mode="validate", language=language)` with all collected inputs. Validate the whole stage once; on `status=needs_input`, explain all discovered issues and invoke its native correction batch, preserving valid answers. Revalidate after the correction batch, not after each field. `status=ready` confirms local validity only. Compact validation retains all discovered issues and the question batch; use `detail="full"` only when a complete schema or diagnostic report is needed. Actual write-entry guards remain intact: authentication, file transport limits, company eligibility, live catalog and saved-context checks still precede the relevant API call. Keep credentials in client state; account, App Key and JWT never enter `supplied` or business DTOs. Collection and validation do not authorize a write. Missing ordinary top-level arguments at actual write entry also produce structured `needs_input`; authentication/configuration failures and uncertain post-write outcomes remain separate and never justify an automatic retry.

The local validator is `scripts/forms.py`; deploy it with `scripts/workbook.py` and the other scripts. Its routing order begins with package, Customized sample form when applicable, and antigen source before dependent fields; eligible independent fields are grouped into collection batches. MCP input guidance and write-entry form checks use `count_workbook=False`: filename/Base64/nonempty/size checks remain, while repeated workbook scans are skipped. The actual `start_design` path performs one best-effort count before writing. CLI consumes the same batch without invoking full validation or scanning XLSX between prompts. The count belongs to actual design execution, never a question or a user-entered value. Discard stale/manual counts. Count named sample rows, not the sheet's formatted row count or the number of sequence/chain cells; skip headers, blanks and known `AI spec`, `_mapping` and `_options` helper sheets without silently deduplicating names. A sample header must include `protein_name` and a recognized chain column, including `VH/Protein`; this recognition is only for statistics, not proof that the backend supports a template. If counting fails or multiple sample sheets make it uncertain, omit `antibodyProjectCount`; do not fill zero or another default. Do not locally reject a workbook for its template, helper sheets, content or quantity range, and do not run an independent content check that demands a replacement file. Send the unchanged original file and let the backend API return any business validation error. File reading/Base64/size/name transport protections and existing non-Excel business and identity checks remain. No new dependency is needed for XLSX counting.

## Reading MCP Responses

Use native MCP tools whenever available. A client-side parser failure is not evidence of a failed business API or an empty catalog. In particular, do not call `content.find` on an error envelope, a raw text wrapper or an absent result. Check `is_error` / `isError` first; SDK models use `structured_content`, while wire JSON can use `structuredContent`. Only fall back to JSON text blocks when they actually exist. Preserve all returned catalog candidates and pagination metadata.

In a full project environment without native MCP tools, use `scripts/mcp_client.py` instead of constructing a persistent Node/Python stdin queue for each conversation. It opens a session for one explicitly requested tool call and closes it afterward. The module function is `await call_mcp_tool(url, name, arguments, timeout=300.0)`. The corresponding CLI is:

```text
python -X utf8 -m skill.order_design.scripts.mcp_client
```

Send one JSON object to stdin, then close stdin: `{ "url": "<selected MCP endpoint>", "name": "search_order_antigens", "arguments": { "keyword": "<customer keyword>", "business_token": "<current verified JWT>", "page_no": 1, "page_size": 50, "language": "en" }, "timeout": 300 }`. These are placeholders, not executable order data. Use the MCP endpoint already chosen in the client setup, not `RUSHDATA_BASE_URL`; do not ask an ordering customer to discover either address. The service credential comes from existing `MCP_ACCESS_TOKEN` configuration, while `business_token` must be bound explicitly from this customer's successful `result.token`. Do not reference an undefined token variable, persist the request to a file or place credentials in command-line arguments.

The helper returns one JSON envelope: `{ "ok": true|false, "result": <decoded result or null>, "error": <error details or null> }`. It does not retry. When `ok=false`, inspect the failure stage and kind before reading results. A tool error can still carry a `needs_input` / `needs_credentials` result that requires the normal collection or correction batch flow; it is not a connection failure. A transport or response-format failure must not become “no products found.” Do not send the helper envelope through a second `CallToolResult` parser; its `result` is already decoded.

The process caller must capture stdout as UTF-8, handle nonzero exit and process-spawn errors, and stop waiting on process exit or deadline. Set the outer process/tool wait to cover the requested timeout, or use the host's running-process continuation mechanism; a shorter REPL deadline can reset the kernel and discard in-memory state. Retain the decoded result in memory and display the current question or real product choices rather than dumping tokens or the entire result into diagnostic logs. No stdout frame must be parsed as a product result until `ok` has been inspected. Preserve existing order answers and candidates on failure; report the observed failure stage without claiming an unverified network repair. Write-result uncertainty still requires state verification, never automatic resubmission. Using this helper does not authorize a business operation or change the selected MCP endpoint.

## Client-side Credential Exchange

Use an already provided valid JWT without asking again. Otherwise request only missing **Biointron Account**, then **App Key**, through separate ordinary text questions, never together, and link to [Biointron](https://os.biointron.com/). Do not ask ordinary customers to find JWT or invent an App Key website menu. For the product-library question marked `credential_check_required`, `get_order_input_requirements` returns `catalog_auth` with credential and exchange connection metadata. Use it directly without loading the full execution prompt; its generic `needs_credentials` hint does not override a valid JWT already available to the client. Use server-returned `connection_config` / `catalog_auth`; other credential responses expose `client_side_exchange.base_url` / `url`, and the later MCP `order_design(phase="execute", language=language)` prompt also includes server-configured connection metadata. The address comes from the server's `config` / `RUSHDATA_BASE_URL`, including the service prefix. An absent API address in the client's config does not mean the remote MCP server is missing it. Standalone scripts read their own config directly. Never ask the customer for an API address or guess an environment. Only if the server actually reports missing configuration, explain the backend configuration problem for the service operator, with no API-address questionnaire.

Map user-provided account labels (`account`, account/email) to the API's `username`; map an explicitly supplied App Key (including the user's label `apkey`) to `appkey`. Do not send `account`/`apkey` as API field names. Exchange before the first business tool, including read-only preflight. `business_token` is the returned JWT, never an account, App Key, `account:App Key`, another concatenation or a Base64 conversion. A 401 does not authorize guessing another token format or repeatedly trying those values; report the failure and verify the exchange/environment without automatic retries. If the client lacks HTTP/script execution, identify that concrete limitation instead of attempting the business tools with the wrong credential or asking the customer to determine a token format.

Through an available client HTTP or script tool, send:

```http
POST <confirmed-business-api-base>/customer/getAccessToken
Content-Type: application/json

{"appkey": "<customer-appkey>", "username": "<bound-account>"}
```

The placeholders are illustrative only. Use the confirmed HTTPS destination; do not follow redirects with credentials. This exchange does not require an `X-Access-Token` header or the MCP service's `Authorization` header. Continue only on HTTP 2xx, numeric `code=200`, `success=true`, and a nonempty JWT in `result.token`. An HTTP 200 alone is insufficient. On a rejected, malformed, or interrupted response, stop and report the failure without credentials; do not guess another environment or continue with the App Key as a token.

Keep the App Key, account, and returned JWT in invocation memory only; do not write them into source files, command files, configuration, logs, or reports, and do not echo them. Client tool history may retain request arguments. Put the returned JWT in the existing MCP `business_token` argument, without `Bearer`; do not add an account argument to MCP tools. MCP continues to forward this JWT to business APIs and does not perform the exchange. If the client lacks HTTP/script execution, explain the missing capability and help arrange an appropriate client integration or technical support. Do not default to asking an ordinary customer to retrieve JWT manually. A user who independently supplies a valid JWT can still use the unchanged MCP protocol.

Keep credentials and results paired with the current customer. Exchange once for the workflow and reuse the exact same JWT from design through cart insertion: saved-design receipts are JWT-bound. If it expires after saving, stop writes; obtain a fresh JWT only for read-only state checks and retain existing order identities. Do not recreate orders, retry uncertain writes, or fabricate receipts to recover.

## API Encoding

Every MCP business tool call must supply the current customer's raw JWT in the dedicated `business_token` argument, never their App Key. The adapter sends it as `X-Access-Token`; it never reads a fixed business token from FC or reuses a previous request's credentials. Keep it outside `data` and `query`, and do not include it in reports or diagnostics. Protected requests use `X-Access-Token`. Check both HTTP status and the business response. A numeric business `code` of `200` is required; an explicit `success=false` is a failure. Successful `startDesign` responses use SSE, not the ordinary JSON envelope.

| Stage | Method and path | Request requirements |
| --- | --- | --- |
| Company eligibility | `GET /customer/companyStatus` | No parameters; require `hasCompany=true` and `companyId>0`. |
| Test-item catalog | `GET /order/rushData/testItems` | Resolve each `id` by `itemCategory` and `itemKey` or `itemName`. |
| Our antigen library | `GET /order/rushData/getBaiYingAntigenList` | Query `keyWord`, `pageNo`, `pageSize`; the adapter defaults to page 1 / size 50 and merges up to five consecutive pages per read-only search call. |
| Design template | `GET /order/rushData/downloadTemplate` | Query `type=IgG` or `type=VHH`; success returns XLSX. |
| Create or redesign | `POST /order/rushData/startDesign` | Multipart; `Accept: text/event-stream`. |
| Saved design HTML | `GET /order/rushData/report` | Query `rushDataServiceId` from the verified signed saved-design context; the endpoint directly returns the actual `report.html` content extracted by the backend from its result ZIP. This is not the experimental `/inspectionReportHtml` endpoint. |
| Add to cart | `POST /order/rushData/addToCart` | JSON body only, no query parameters; use the verified cart contract below. |
| Read cart | `GET /order/rushData/orders` | Query `pageNo`, `pageSize=10`, and `orderStatus=00`. |
| Quote | `POST /order/rushData/price/calculate` | JSON `orderNos` contains the selected order numbers joined by commas. |
| Submit | `POST /order/rushData/submit/batch` | The same `orderNos` encoding; `Time-Zone` contains the configured IANA time zone. |

Paths are relative to the configured business API base, including its service prefix. Do not guess a base address. Do not assume cart queries support order-number filtering or put new records on the first page; use pagination metadata.

## Design Input

| Field | Required handling |
| --- | --- |
| `id` | Omit for new designs; use the existing `rushDataServiceId` for an authorized redesign. |
| `file` | The customer's original nonempty XLSX, at most 10 MiB. |
| `projectName` | Customer-provided project nickname, trimmed nonempty text of 1-100 characters. Preserve internal spaces, underscores and hyphens; it is not a system project number or unique order identity. |
| `catalogNumber` | `BRD101`, `BRD201`, `BRD301`, or `BRD401`. |
| `antibodyProjectCount` | Internal transport field, absent from the public form schema. Include the actual count as decimal text only when reliably read from the original workbook; otherwise omit it, clear stale/manual values and let the API decide. Do not enforce the service quantity range locally, invent a default, or ask the customer to enter/confirm a quantity. Billing remains the backend's responsibility. |
| `antigenCount` | Integer from 1 through 3; exactly 1 for `BRD101`; equal to the antigen-array length. |
| `sp` | Optional Signal Peptide field; omit or leave empty when not already supplied. Custom SP is not currently offered per the meeting; legacy accepted values remain compatible, not a promise of custom support. Do not request or generate a custom sequence. |
| `testItemIds` | Actual catalog IDs, each in a separate Multipart field with this same name; never a JSON-array string. |
| `usingdna` | Confirm whether the customer specifies use of their supplied DNA; per the meeting this skips the system's own codon optimization. Encode as lowercase `true`/`false`; clarify ambiguous input and never generate, convert or optimize sequences here. |
| `antigens` | A JSON-array string after the backend confirms the accepted structure and transport. |
| `positiveControls` | A JSON-array string using backend-confirmed fields and required conditions. |

The HTTP client generates the design Multipart boundary. Do not put cart shipping or address fields into that design request; cart shipping follows the separate JSON contract below. This workflow does not call an address-binding endpoint.

MCP input uses `testItems` as category-to-business-key arrays. The adapter resolves keys to IDs; callers must not manufacture IDs. Resolve every required item uniquely and stop on missing, duplicate, or ambiguous matches.

For `SAMPLE_TYPE`, keep the package shorthand in MCP input and use this explicit mapping when resolving the current catalog:

| Package / MCP shorthand | Catalog `itemKey` |
| --- | --- |
| `supernatant` | `SAMPLE_SUPERNATANT` |
| `purified antibody` | `SAMPLE_PURIFIED_ANTIBODY` |

Read actual IDs from the current preflight catalog. Match category `SAMPLE_TYPE` and the mapped `itemKey` uniquely; never copy example IDs. Display labels such as `Expression (supernatant)` are presentation text and must not be hard-coded as identity matches. Missing or duplicate mapped keys stop the workflow; do not silently select a similarly named item.

Backend template expectations are listed for reference only; do not enforce them locally or block the original workbook based on these columns:

- IgG: `protein_name`, `vh`, `vl`, `ch_isotype`, `cl_isotype`.
- VHH: `protein_name`, `vhh`, `fc_isotype`, `fc`, `sp`.

Use the customer's unchanged original file. The local reader only attempts to derive `antibodyProjectCount`; it does not validate or modify sequences or replace backend design validation. If sample sheets cannot be recognized or multiple sheets make the count uncertain, omit the field and continue the authorized API request rather than demanding another workbook. Only an explicit API business error should prompt the corresponding correction; omitting a count does not guarantee that the API will accept the file.

## Packages

Fixed packages require exactly these selections. Do not add, remove, or replace items.

| Package | SAMPLE_TYPE | PROTEIN_PROPERTY | BINDING | DEVELOPABILITY | Antigen count |
| --- | --- | --- | --- | --- | --- |
| BRD101 Basic | `supernatant` | `Titer` | `BLI_Octet_2_points` | Empty | 1 |
| BRD201 Standard | `purified antibody` | `cGE` | `SPR_Carterra` | Empty | 1-3 |
| BRD301 Premium | `purified antibody` | `cGE` | `SPR_Carterra` | All of `DSF`, `PSR ELISA_BVP`, `AC_SINS` | 1-3 |

BRD401 Customized requires exactly one sample type:

Ask sample form immediately after package selection, then collect independent detection categories in a batch. Require the customer to confirm each category; an empty Binding or Developability array is an explicit no-test choice, not an inferred default. At pre-write validation, identify all incompatible items and their sample-form restrictions, then request a correction batch while preserving other choices. Do not silently discard them.

- **supernatant:** Protein is exactly `Titer`. Select at least one of `FACS_iQue_1_point` and `ELISA_1_point`; both are allowed. Developability must be empty.
- **purified antibody:** Select at least one of `cGE`, `SEC_HPLC`, and `SEC_UPLC`; `Titer` is forbidden. Binding and Developability may each be empty or contain multiple allowed items, but cannot both be empty.

Allowed purified-antibody Binding items: `SPR_Carterra`, `SPR_Biacore`, `BLI_Octet_2_points`, `BLI_Octet_4_points`, `FACS_iQue_1_point`, `FACS_iQue_8_points`, `ELISA_1_point`, and `ELISA_8_points`.

Confirmed by the user on 2026-11-04: BLI 2/4-point, FACS 1/8-point and ELISA 1/8-point variants may each be selected together; SPR Carterra and Biacore may also be selected together. Do not invent mutual exclusion within Binding. This does not permit those assays for supernatant when the sample-form rules forbid them. Shared validation in `client.py` is retained for explicit pre-write validation and final design requests, returning specific incompatible-item messages; ordinary collection defers those business checks.

Allowed purified-antibody Developability items: `PSR ELISA_BVP`, `PSR ELISA_Insulin`, `PSR ELISA_dsDNA`, `AC_SINS`, `DSF`, `DLS_Rh`, `DLS_Tagg`, `PAIA_HIC`, `PAIA_Heparin`, `PAIA_OVA`, and `PAIA_BVP`.

Example selection structure, using business keys rather than IDs:

```json
{
  "testItems": {
    "SAMPLE_TYPE": ["supernatant"],
    "PROTEIN_PROPERTY": ["Titer"],
    "BINDING": ["FACS_iQue_1_point"],
    "DEVELOPABILITY": []
  }
}
```

## Antigens and Positive Controls

Prepare information before design. Offer these source choices verbatim in the selected language and in this order: “使用我们的产品库（无需提供链接）” / “Use our product catalog (no link required)” (`SUPPLIER_CATALOG`), “提供外部产品链接” / “Provide an external product link” (`CUSTOMER_URL`), “手动填写已有抗原资料” / “Enter existing antigen information manually” (`MANUAL`). Show only the selected language. For our product library, first check the current valid JWT or obtain missing Biointron Account/App Key values and exchange them. Then ask for an antigen keyword, such as CD2, using a native text question or one CLI prompt. Search our backend library and let the customer select an actual returned product and specification. Auto-populate supplier, SKU, specification and available product fields; do not ask for a supplier first. Only the external-link mode asks the customer for a link. When the customer has already requested our library, enter it directly without repeating the source question. Switching from a link to our library updates `sourceType`, cancels the pending URL question and revalidates using the library branch. Do not invent products or generate biological content. Backend support for design transport remains subject to the draft-contract gate:

| `sourceType` | Fields to validate once support is confirmed |
| --- | --- |
| `CUSTOMER_URL` | `referenceUrl` must use HTTPS; confirm whether an address alone is sufficient. |
| `MANUAL` | `sampleName`, `proteinTag`, `proteinConcentration`, `proteinMolecularWeight`, `proteinBuffer`. |
| `SUPPLIER_CATALOG` | “使用我们的产品库（无需提供链接）”: require `supplier`, `catalogNumber` and `specification` from the selected real search result. `referenceUrl` is optional; validate HTTPS when present, never invent a missing link or request it from the customer. |

The antigen-array length must equal `antigenCount`. Supplier prices are informational and must not be added to the RushData service total. Preserve missing prices as `null` and actual zero prices as `0`. Do not expose supplier credentials.

At the business level, recommend an optional positive reference selected by name from the customer's antibody list, without recollecting existing sequence/physical data or guaranteeing the highest affinity. The meeting allows multiple names, but their request encoding is not yet confirmed. Do not infer the fields, counts, required conditions, or applicable assays for design `positiveControls`. Do not reuse the antigen schema or assume an empty array is universally valid. Confirm these requirements before enabling `RUSHDATA_DRAFT_CONTRACT_CONFIRMED` and making a design write. Cart `positiveControl` remains the single string below; do not join multiple names using an invented delimiter.

These design fields are the earlier draft contract, not the cart DTO. They do not replace the verified `addToCart.antigens` or singular `addToCart.positiveControl` below; do not transfer or rename them automatically without confirmed field correspondence.

Product-library search belongs to information preparation, before design saving. Do not insert antigen-saving, address-binding, or additional catalog lookups between confirmed design saving and cart insertion; retain the selected product's verified cart data.

Call `search_order_antigens(keyword, business_token, page_no=1, page_size=50, language=language)` after keyword entry. Each call loads its first requested page to determine the page range, then requests up to four further pages concurrently within that same request client. The maximum remains five consecutive pages, with actual results merged and deduplicated by `(supplier, catalogNumber, specification)`. No credentials or results are cached across users, and failures are not automatically retried. Present `catalog_summary` and real catalog/specification choices through a native dialog or CLI numbered menu. Always offer changing the keyword; when `has_more=true`, also offer loading more products with the returned `next_page` and unchanged keyword/page size. Do not use the original `page_no+1`, which would revisit pages already merged. Keep previous candidates and merge additional results with the same deduplication key. With no matches, ask for another keyword. A failure on a later page retains successful earlier results with an explanation and continuation position; do not retry automatically or present a partial result as complete. No separate product-picker page is required. This is a read-only search, not permission to write an order.

Pass the search response's `catalog_options` and `catalog_search` alongside `data`, `filename` and `file_base64` to `get_order_input_requirements`. `catalog_search` contains only `keyword`, `page_size`, `total`, `has_more`, `next_page` and `catalog_summary`; preserve it so the native selection can offer continuation instead of silently dropping pagination. Navigation choices trigger another search or keyword question and never become a selected design antigen. Each product option represents one returned product/specification combination and includes `label`, `supplier`, `catalogNumber`, `specification`, optional `referenceUrl` and available sample fields. Select across suppliers without a supplier prerequisite. Selection supplies the design fields with `sourceType=SUPPLIER_CATALOG`; preserve that option's separate verified `cart_data` for later cart use. Candidate and search metadata stay outside design Multipart, and credentials never go to the local input tool. The local tool itself does not make the HTTP search; the dedicated MCP search tool or CLI client performs it.

Preserve all backend search candidates rather than silently filtering by exact keyword, supplier or species; obtain customer confirmation before filtering, explain that search may include fuzzy matches, and never equate similarly named products with the same antigen.

The search response distinguishes backend product totals from loaded choices: `total` is the matching product count reported by this source, `records_loaded` counts records read in this batch, `products_loaded` counts its distinct selectable products, and `options_count` counts selectable specifications. `first_page`, `last_page` and `pages_loaded` describe the fetched range; `next_page` identifies the next unfinished page. `complete=true` applies only when a search started at page 1 and loaded the full range successfully. Show skip/failure reasons from `catalog_issues`, including their page information; do not turn rejected data into fabricated selectable products or treat an unusable page as no matches. These counts cover this interface and environment only. Without comparing the actual webpage request, aggregated loading cannot establish that both clients search the same sources.

The product-search contract was read from the [test-environment OpenAPI](https://testmyorder-en.biointron.com.cn/byorderapi/by-order-client/v2/api-docs) on **2026-11-05**. This was schema inspection only, not a live product search or integration test. `GET /order/rushData/getBaiYingAntigenList` uses `X-Access-Token` and exact query names `keyWord`, `pageNo`, `pageSize`. Its response envelope contains `code`, `success` and `result`; the page has `records`, `current`, `pages`, `size` and `total`. Records contain `antigenName`, `catalogNo`, `supplierName`, optional `productUrl`, `sampleConcentration` (mg/ml), `sampleLabel`, `sampleMolecularWeight`, `sampleStorageBuffer` and `specsList` entries with `specs`, `rmb`, `usd`. Flatten actual specifications for selection. The selected cart mapping uses `specs` → `specification`, `rmb` → `price`, `usd` → `usdPrice` and the confirmed product/sample fields; preserve missing values and actual zero values. In product-details cart mode omit `productUrl`, even if its source URL is retained as the design's optional `referenceUrl`, because cart URL-only and product-details modes are mutually exclusive.

## SSE and Saved-Design Receipts

The workbook-path answer only initiates file reading, transport checks and non-blocking quantity counting; Excel content acceptance belongs to the API. After required inputs, current-customer permission preflight and existing design authorization are satisfied, send this complete progress message in commentary immediately before calling `start_order_design`, then continue execution and wait for the actual result:

> 正在进行订单设计，预计需要较长时间，请耐心等待。
>
> Biointron provides high-throughput antibody expression and profiling.
>
> - **10,000 / day** — Antibodies expressed
> - As fast as **3 days** — CHO cell expression
> - **30+** — Developability assay readouts
>
> 设计完成后，我会继续反馈结果。

For `language="en"`, send the English version instead:

> Your order design is in progress and may take some time. Please wait.
>
> Biointron provides high-throughput antibody expression and profiling.
>
> - **10,000 / day** — Antibodies expressed
> - As fast as **3 days** — CHO cell expression
> - **30+** — Developability assay readouts
>
> I will share the results when the design is complete.

Show the complete message once per design, not at every stage. It is a progress update, not a final answer or another approval request. The service figures do not promise this order's delivery date; do not add unsupported minutes or progress percentages. Missing inputs or failed preflight must not be described as design in progress. Report the actual success, failure or uncertain outcome afterward without automatic retries, and distinguish saved design from final order submission.

Consume SSE frames with `event:` and `data:` fields. Parse only supported structures; do not search arbitrary nested values for success indicators.

| Event | Required action |
| --- | --- |
| `order_created` | Retain order identity; design is not complete. |
| `stream_started`, `log`, `result_saving` | Continue waiting; these are not success evidence. |
| `completed` with `status=ok` | Calculation completed; continue waiting for saving. |
| `completed` with `status=failed` | Stop. |
| `result_saved` | Accept only after `completed.status=ok` and with a valid service ID. |
| `design_error`, `result_save_failed`, `proxy_error` | Stop. |

Supported identity fields and aliases:

| Field | Aliases |
| --- | --- |
| `orderNo` | `order_no` |
| `rushDataServiceId` | `rush_data_service_id`, `id` |
| `orderId` | `order_id` |

Keep identities consistent across frames. Do not invent missing identifiers or prefixes. Unknown events, a closed connection, or calculation success alone cannot authorize cart insertion.

If a previously received canonical `orderNo` starts with `RD-` and a later `order_no` exactly matches its suffix, retain the known canonical number. This narrow alias rule does not permit other identity changes or replace save confirmation.

`start_order_design` signs continuation only after confirmed saved SSE evidence. Return data includes `workflow_context={version:1, order_no, expires_at, next_tool:"add_order_to_cart", continuation_token:<full signed string>}` and a compatibility top-level `continuation_token`. The AI must retain this entire object and supply it unchanged on continuation; the server does not store or retrieve it. An order number alone is insufficient. The signed `next_tool` identifies the later cart write; first complete the saved-design result choice below without changing that context.

## Saved Design Result Choice and HTML Delivery

Only after the current design's `result_saved` is verified, and before collecting cart inputs or adding the design to cart, invoke a native single-choice card or CLI selection and wait for the actual answer. This is a client-side viewing preference, not a business-payload field or another design approval. For `language="zh"`, the native question arguments are:

```json
{"questions":[{"title":"设计已保存，是否查看本次设计结果？","options":["需要，查看HTML设计结果","不需要，继续下单"]}]}
```

For `language="en"`, invoke the same one-question flow with this copy instead:

```json
{"questions":[{"title":"The design has been saved. Would you like to view the design result?","options":["Yes, view the HTML design result","No, continue ordering"]}]}
```

Use the available native tool's actual schema, preferring returned `interaction.native_question` where supplied. These examples describe Codex `request_user_input_async` arguments; do not print them as a substitute for invoking the question. CLI uses the same selected-language question and choices, one terminal selection at a time. Keep asynchronous questions pending until answered. An existing signed continuation never authorizes bypassing this choice.

- **View:** Call `get_order_design_result` with the complete original signed context, current JWT and selected language, as detailed below. Save and deliver its actual HTML as a clickable file link or usable preview before collecting cart fields or adding to cart. Do not claim delivery based only on a success message, raw HTML code, order identity, login URL or a local path the customer cannot open. Continue the already-authorized cart workflow after actual delivery, without another general continue confirmation.
- **Skip:** Do not retrieve the design result or render HTML. Continue the existing authorized cart workflow directly, reusing known cart fields and collecting only missing ones.
- **Unavailable or failed delivery:** Explain the confirmed retrieval/rendering/delivery failure, preserve the saved design and ask one selected-language choice: “重试读取设计结果” / “继续下单” (`zh`), or “Retry reading the design result” / “Continue ordering” (`en`). The retry choice authorizes only retrying the failed step for this saved result: repeat the GET only for an actual read failure; for local save or delivery failure, reuse the already-returned HTML without another read. Do not retry automatically, recreate or redesign the order, or lose existing answers. Continue only when delivery succeeds or the customer selects continue.

The read-only MCP contract is `get_order_design_result(business_token, order_no="", continuation_token="", workflow_context=None, language="zh")`; explicitly pass the current `zh` or `en` language. Prefer the complete original `workflow_context`; any separately supplied order number or compatibility receipt must agree. The reader verifies the saved-design signature, exact JWT binding and saved order identity, then requests `GET /order/rushData/report?rushDataServiceId=<signed service ID>` and receives the actual `report.html` content directly; the backend extracts that content from its result ZIP, so the client does not receive or unzip a ZIP. Do not substitute a guessed service ID or reconstruct a context from an order number.

A successful read returns `status="design_result_ready"`, `orderNo`, `projectName`, `filename="RushData_Design_<safe order>.html"`, `mime_type="text/html"`, `html`, `report_type="design"`, `write_performed=false` and the unchanged full `workflow_context`. The host must write the returned `html` as UTF-8 with BOM (`utf-8-sig`) under the returned filename, preserving the HTML content while preventing its retained charset declaration from causing garbled display, then deliver an openable file link or preview before continuing cart work. The MCP response supplies HTML content; merely displaying that code is not artifact delivery. Keep credentials and signed context outside the HTML and ordinary customer output.

Do not invent HTML endpoints, guess URLs, or wrap an order receipt as the design result. `/inspectionReportHtml` and `get_report_results` concern experimental reports and are not sources for this design-view step. Only the actual saved-design HTML is delivered; labels and order metadata alone are not design content. Missing HTML support is a viewing limitation, not evidence that saving failed, and must lead to the explicit retry-or-continue choice.

Preserve the complete original signed `workflow_context`, saved identity and exact current JWT throughout. Keep the view preference, pending question, delivery outcome and cart readiness in the outer client/handoff record; never add them to `workflow_context` or the business payload. Viewing or skipping does not authorize final submission. The existing exact-order/quote/PO/company confirmation remains required before `submit_verified_order`.

## AI-held Signed Continuation

The active MCP workflow requires no Redis, database or shared session cache. Use `add_order_to_cart(business_token, cart_data, order_no="", continuation_token="", workflow_context=None, language=language)` with the complete returned context and the same JWT supplied separately. The optional order number, compatibility receipt and context must match when used together. MCP checks the signature, exact JWT binding, API environment, expiry, order metadata and `cart_data.projectNo`. Only saved SSE evidence can issue proof; detail lookup cannot reissue it or prove the current saved version. A missing main `orderId` cannot be replaced with a service ID. Before insertion, details must show draft (`-3`) or cart (`00`) status; submitted/unknown states are blocked. This is a read-only check, not an atomic guarantee.

Preserve the complete original `workflow_context` across context organization, memory compaction and chat/agent handoff: no shortened signatures, omitted fields, summary-only substitutions or reconstructed contexts. Keep private records separated by a secure customer-credential reference and `order_no`. Carry the stage, saved-design view preference and delivery status, pending question, confirmed `cart_data` (preserving real `false` and `0`), missing/invalid fields, authorized actions, last tool call and unresolved outcomes. Keep these notes outside `workflow_context`; do not add fields to the original object. This is a Skill/client requirement, not a promise that every client retains history; lost context stops continuation because the server has no copy. Never mix one customer's credential with another order's context.

Use secure references rather than JWT/App Key values in ordinary summaries or handoffs. Do not write credentials or signed receipts into repository memory, shareable documents or server storage. Retain the complete context only in private client continuity. If the same JWT cannot be accessed, securely obtain it; a different freshly exchanged JWT cannot continue the previous context. Credential validity remains at most one hour, without refresh or re-signing. Lost/expired proof stops continuation; never recreate an order as recovery.

`end_order_workflow(order_no, business_token, workflow_context=None, continuation_token="", language=language)` returns `status="discard_context"`, `server_revoked=false`, `client_action="delete_local_context"`, and `business_order_cancelled=false`. Delete the local context for that customer/order, not the real order. No server revocation, deletion of other copies, order cancellation or cart-item removal is performed. After confirmed cart success also stop using the local continuation proof, retaining order identity and outcome for reporting.

MCP no longer reserves shared design/submission fingerprints or atomically claims cart writes. A sequential cart call checks the cart read-only; an existing match returns `already_in_cart=true`, `write_performed=false`, and `cart_data_applied=false`, so newly supplied antigen/shipping fields were not applied. Concurrent cross-instance writes and identical designs still need backend idempotence. Never promise exactly-once behavior or automatically retry uncertain writes. Do not run concurrent writes for the same order; inspect the cart after an unknown result. For an authorized redesign discard the local old context, while acknowledging the server cannot revoke other copies or prove the current saved version merely from order details.

The standalone CLI calls business APIs directly. Do not switch to it or the website automatically after a failed MCP call; use it only when the user explicitly requests independent CLI execution and preserve its authorization and uncertainty rules.

## Verified Cart JSON Contract — 2026-11-03

Source: the test deployment's [OpenAPI document](https://testmyorder-en.biointron.com.cn/byorderapi/by-order-client/v2/api-docs), `RushDataAddToCartAntigenRequest` and `RushData选中抗原`, checked with the current web client on 2026-11-03. This confirms the request contract; it does not assert that a real cart write was performed. The older `RushData开放API下单接口文档_草案.md` statement that `addToCart` has no JSON body is outdated. Preserve that file as historical evidence, not as this endpoint's current contract.

`POST /order/rushData/addToCart` sends `Content-Type: application/json`, `X-Access-Token: <JWT>`, and **no query parameters**. Its required body fields are `antigens`, `orderNo`, `projectNo`, `rushDataServiceId`, and `shippingRequired`. `projectName` is optional; `positiveControl` is optional text in a single string, not a `positiveControls` array.

For `add_order_to_cart(business_token, cart_data, order_no="", continuation_token="", workflow_context=None, language=language)`, return the complete original `workflow_context`; a compatibility signed receipt may also be supplied, and all representations must match. Order number alone cannot recover proof. The client supplies only these `cart_data` fields:

| `cart_data` field | Required handling |
| --- | --- |
| `projectNo` | The real project number from design details. Do not derive it from `projectName`, `orderNo`, or a service ID; missing evidence stops cart insertion. |
| `shippingRequired` | An explicit user-selected Boolean. `false` removes any existing address binding and must not be a default. `true` requires an address already bound through the website; do not invent or create an address binding here. |
| `antigens` | 1–3 selected objects using only the 11 fields below. |
| `positiveControl` | Optional single string supplied or confirmed by the customer; do not convert the old design array automatically. |

The MCP service obtains `rushDataServiceId`, `orderNo`, and `projectName` from its verified design receipt. These identity fields, shipping addresses, and arbitrary extra keys cannot be overridden through `cart_data`. Missing required receipt identity stops the call rather than accepting a client-supplied replacement.

To obtain a missing `projectNo`, an available client HTTP/script tool can read `GET <confirmed-business-api-base>/order/rushData/detail?orderId=<saved-orderId>` with the same JWT in `X-Access-Token`. This read-only endpoint uses the saved master `orderId`, not `rushDataServiceId`. Require a successful business response and matching `result.orderId` and `result.orderNo` before taking `result.projectNo`. If the saved order ID is absent, details cannot be read, or identities conflict, stop and request verified details; do not guess IDs, use the first listed order, or create another design. This does not add a new MCP tool.

Each selected antigen has this current schema; unused fields are `null`:

| Field | Type / limit |
| --- | --- |
| `antigenName` | String, at most 255 characters |
| `catalogNo` | String, at most 128 characters |
| `specification` | String, at most 255 characters |
| `price` | Number or `null` |
| `usdPrice` | Number or `null` |
| `productUrl` | String, at most 1000 characters |
| `sampleLabel` | String, at most 255 characters |
| `sampleConcentration` | Number or `null` |
| `sampleMolecularWeight` | String, at most 200 characters; preserve supplied units or range text |
| `sampleStorageBuffer` | String, at most 1000 characters; use the supplier's Formulation, not Storage instructions |
| `supplierName` | String, at most 255 characters |

Reuse the selected library option's verified `cart_data` without asking the customer to choose or fill that product again. Otherwise offer cart-specific choices: “product link” (example format `https://supplier.example/product`) or “product details” (example format antigen name + catalog number + supplier). These examples are explanatory only. Ask for the chosen mode first, then only its required fields; this is distinct from the three design modes. For URL-only input, use `productUrl` and set the other ten fields to `null`. For a selected product, `antigenName`, `catalogNo`, and `supplierName` are required; fill other values only from confirmed product information. This DTO has no `sourceType`, `referenceUrl`, or `antigenProductId` field. Do not force the draft design antigen schema onto it or invent missing supplier data.

The direct `check.py` terminal entry defaults to `--auth appkey`. In `design`/`full` modes, introduce all four packages before local project, antigen and cart questions; attempt non-blocking antibody counting from the original workbook, omitting an uncertain count for API-side validation. Upon choosing our product library, obtain any missing Biointron Account and App Key with separate ordinary text inputs, exchange through the configured API address, then ask for a keyword and show actual paginated search choices. Reuse the selected product's cart data and current valid JWT later. External-link/manual modes wait until submission to request credentials. App Key is not masked. Advanced `--auth jwt` retains hidden JWT input. Read-only preflight and existing-order submit modes obtain credentials for their requested calls. Select antigen source before dependent fields, then prompt sequentially through each returned independent-field batch without intermediate MCP/model calls or business validation. Validate the whole stage before writing; explain all discovered issues and collect their correction batch. Answers remain in memory, never written back into request JSON. Do not default packages or shipping.

In `design` and `full`, retain any supplied top-level `cart_data` without putting it in Multipart design fields. After confirmed saving, complete the saved-design result choice and any selected HTML delivery before collecting missing cart fields. Obtain a real `cart_data.projectNo` from verified saved-order details if needed, then validate all required cart input before cart insertion. Do not guess a project number or recreate a saved design to recover missing metadata. MCP `start_order_design` keeps its signature and does not accept `cart_data` inside `data`.

`--non-interactive` disables all terminal input/getpass. Noninteractive `run(args, business_token)` requires explicit `--design-result view` or `--design-result skip` before any design write; a missing preference stops before writing and must never default to skip. The interactive CLI asks after confirmed saving. With `view`, the actual HTML is written to the optional `--design-result-dir` directory and its local artifact is delivered before cart continuation; `--report` still writes the JSON workflow outcome and is not a design HTML report. The CLI does not accept plaintext account/key flags or read a fixed business JWT from environment variables; without credentials it blocks immediately, so these flags are not authentication mechanisms. Automation supplies the current JWT explicitly and remains noninteractive. CLI execution still requires explicit authorization and must not become an automatic fallback after MCP failure.

## Cart, Quote, and Submission

1. Locate the saved design across cart pages by matching `record.id` to `rushDataServiceId`. If both sides contain an order number, require a match. Require one unambiguous record with `orderStatus=00`.
2. Retain that record's `orderNo`. Include other orders only when explicitly selected by the user. Never submit the entire cart by default.
3. Use `calculate_order_price` for an authoritative quote. MCP accepts an `order_nos` array; the adapter converts it to the upstream comma-separated `orderNos` string. Do not sum cart prices or add supplier antigen prices.
4. Require the quoted order set to match the selected set exactly. Partial quotes, duplicate entries, or unexpected orders must prevent submission, even when `canSubmit=true`.
5. Present the authoritative quote and obtain the customer's confirmation of the selected orders, price/discount and PO/company-information readiness. Unknown or missing prerequisites require human verification. There is currently no MCP PO field or PO-validity check; do not add a guessed request field or treat company eligibility and `canSubmit` as proof of PO validity. Then `submit_verified_order` requotes immediately before submission. It requires `canSubmit` to be exactly `true` and preserves the selected set. If blocked, report the backend's `submitMessage` when available.
6. Submit with the configured `Time-Zone`, then check the relevant cart pages. Distinguish a successful submission response from incomplete cart synchronization. Do not repeat submission because a record remains visible.

Existing selected orders can enter at the quote and submission stage without recreating a design. Submission is not payment: accepted orders enter human confirmation, and production requires Biointron's confirmation. Neither submission acceptance nor cart removal establishes production start or experimental completion. The six business stages and unresolved progress-field mapping are described in [business-context.md](business-context.md); `get_order_cart` only queries the cart.

## Reporting an Uncertain Result

Stop further writes on an uncertain outcome. Retain the order identity and last confirmed stage, then use available read-only checks. Report each stage as confirmed, failed, not attempted, or awaiting verification. Keep credentials, uploaded file contents, and raw biological sequences out of diagnostics.
