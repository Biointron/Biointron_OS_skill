# Order Workflow Rules

## API Encoding

Protected requests use `X-Access-Token`. Check both HTTP status and the business response. A numeric business `code` of `200` is required; an explicit `success=false` is a failure. Successful `startDesign` responses use SSE, not the ordinary JSON envelope.

| Stage | Method and path | Request requirements |
| --- | --- | --- |
| Company eligibility | `GET /customer/companyStatus` | No parameters; require `hasCompany=true` and `companyId>0`. |
| Test-item catalog | `GET /order/rushData/testItems` | Resolve each `id` by `itemCategory` and `itemKey` or `itemName`. |
| Design template | `GET /order/rushData/downloadTemplate` | Query `type=IgG` or `type=VHH`; success returns XLSX. |
| Create or redesign | `POST /order/rushData/startDesign` | Multipart; `Accept: text/event-stream`. |
| Add to cart | `POST /order/rushData/addToCart` | Query `rushDataServiceId` and `projectName`; no JSON body. |
| Read cart | `GET /order/rushData/orders` | Query `pageNo`, `pageSize=10`, and `orderStatus=00`. |
| Quote | `POST /order/rushData/price/calculate` | JSON `orderNos` contains the selected order numbers joined by commas. |
| Submit | `POST /order/rushData/submit/batch` | The same `orderNos` encoding; `Time-Zone` contains the configured IANA time zone. |

Paths are relative to the configured business API base, including its service prefix. Do not guess a base address. Do not assume cart queries support order-number filtering or put new records on the first page; use pagination metadata.

## Design Input

| Field | Required handling |
| --- | --- |
| `id` | Omit for new designs; use the existing `rushDataServiceId` for an authorized redesign. |
| `file` | The customer's original nonempty XLSX, at most 10 MiB. |
| `projectName` | Trimmed, nonempty text of 1-100 characters; preserve it for cart insertion. |
| `catalogNumber` | `BRD101`, `BRD201`, `BRD301`, or `BRD401`. |
| `antibodyProjectCount` | Integer from 48 through 999, encoded as decimal text in Multipart. |
| `antigenCount` | Integer from 1 through 3; exactly 1 for `BRD101`; equal to the antigen-array length. |
| `sp` | A customer-selected value accepted by the adapter, or an empty string; do not generate a substitute sequence. |
| `testItemIds` | Actual catalog IDs, each in a separate Multipart field with this same name; never a JSON-array string. |
| `usingdna` | The customer's choice, encoded as lowercase `true` or `false`. |
| `antigens` | A JSON-array string after the backend confirms the accepted structure and transport. |
| `positiveControls` | A JSON-array string using backend-confirmed fields and required conditions. |

The HTTP client generates the Multipart boundary. Do not include shipping, address, or address-binding fields.

MCP input uses `testItems` as category-to-business-key arrays. The adapter resolves keys to IDs; callers must not manufacture IDs. Resolve every required item uniquely and stop on missing, duplicate, or ambiguous matches.

Files must contain at least one nonempty record and the applicable template columns:

- IgG: `protein_name`, `vh`, `vl`, `ch_isotype`, `cl_isotype`.
- VHH: `protein_name`, `vhh`, `fc_isotype`, `fc`, `sp`.

Use customer-supplied files that have passed applicable business validation. Extension and size checks do not validate workbook contents. Do not assume the record count must equal `antibodyProjectCount` unless the backend confirms that rule.

## Packages

Fixed packages require exactly these selections. Do not add, remove, or replace items.

| Package | SAMPLE_TYPE | PROTEIN_PROPERTY | BINDING | DEVELOPABILITY | Antigen count |
| --- | --- | --- | --- | --- | --- |
| BRD101 Basic | `supernatant` | `Titer` | `BLI_Octet_2_points` | Empty | 1 |
| BRD201 Standard | `purified antibody` | `cGE` | `SPR_Carterra` | Empty | 1-3 |
| BRD301 Premium | `purified antibody` | `cGE` | `SPR_Carterra` | All of `DSF`, `PSR ELISA_BVP`, `AC_SINS` | 1-3 |

BRD401 Customized requires exactly one sample type:

- **supernatant:** Protein is exactly `Titer`. Select at least one of `FACS_iQue_1_point` and `ELISA_1_point`; both are allowed. Developability must be empty.
- **purified antibody:** Select at least one of `cGE`, `SEC_HPLC`, and `SEC_UPLC`; `Titer` is forbidden. Binding and Developability may each be empty or contain multiple allowed items, but cannot both be empty.

Allowed purified-antibody Binding items: `SPR_Carterra`, `SPR_Biacore`, `BLI_Octet_2_points`, `BLI_Octet_4_points`, `FACS_iQue_1_point`, `FACS_iQue_8_points`, `ELISA_1_point`, and `ELISA_8_points`.

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

Prepare all required information before design. The backend must confirm support for each requested antigen source mode:

| `sourceType` | Fields to validate once support is confirmed |
| --- | --- |
| `CUSTOMER_URL` | `referenceUrl` must use HTTPS; confirm whether an address alone is sufficient. |
| `MANUAL` | `sampleName`, `proteinTag`, `proteinConcentration`, `proteinMolecularWeight`, `proteinBuffer`. |
| `SUPPLIER_CATALOG` | `supplier`, `catalogNumber`, `specification`, `referenceUrl`; use actual supplier data for additional fields. |

The antigen-array length must equal `antigenCount`. Supplier prices are informational and must not be added to the RushData service total. Preserve missing prices as `null` and actual zero prices as `0`. Do not expose supplier credentials.

Do not infer the fields, counts, required conditions, or applicable assays for `positiveControls`. Do not reuse the antigen schema or assume an empty array is universally valid. Confirm these requirements before enabling `RUSHDATA_DRAFT_CONTRACT_CONFIRMED` and making a design write.

Supplier lookup is optional preparation. Do not insert antigen-saving, address-binding, or supplier-lookup calls between confirmed design saving and cart insertion.

## SSE and Saved-Design Receipts

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

`start_order_design` issues a `continuation_token` only after this service confirms saving. Immediately pass it unchanged to `add_order_to_cart`. The receipt expires after one hour and is bound to the signing secret, business API environment, and business access token.

A receipt does not guarantee idempotence. Do not automatically repeat cart insertion after a timeout. An expired or missing receipt requires a supported backend save-status check before continuing an existing draft; that capability is unavailable here. `designStatus=ok` and an absent cart record cannot replace a confirmed save event. Do not redesign or create another order to work around missing evidence.

## Cart, Quote, and Submission

1. Locate the saved design across cart pages by matching `record.id` to `rushDataServiceId`. If both sides contain an order number, require a match. Require one unambiguous record with `orderStatus=00`.
2. Retain that record's `orderNo`. Include other orders only when explicitly selected by the user. Never submit the entire cart by default.
3. Use `calculate_order_price` for an authoritative quote. MCP accepts an `order_nos` array; the adapter converts it to the upstream comma-separated `orderNos` string. Do not sum cart prices or add supplier antigen prices.
4. Require the quoted order set to match the selected set exactly. Partial quotes, duplicate entries, or unexpected orders must prevent submission, even when `canSubmit=true`.
5. `submit_verified_order` requotes immediately before submission. It requires `canSubmit` to be exactly `true` and preserves the selected set. If blocked, report the backend's `submitMessage` when available.
6. Submit with the configured `Time-Zone`, then check the relevant cart pages. Distinguish a successful submission response from incomplete cart synchronization. Do not repeat submission because a record remains visible.

Existing selected orders can enter at the quote and submission stage without recreating a design. Neither submission acceptance nor cart removal establishes that an experiment has finished.

## Reporting an Uncertain Result

Stop further writes on an uncertain outcome. Retain the order identity and last confirmed stage, then use available read-only checks. Report each stage as confirmed, failed, not attempted, or awaiting verification. Keep credentials, uploaded file contents, and raw biological sequences out of diagnostics.
