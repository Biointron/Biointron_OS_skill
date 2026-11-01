---
name: order-design
description: Create or redesign RushData orders, verify saved designs, add orders to the cart, obtain authoritative quotes, and submit selected orders for experimental work. Use for this order workflow, not for generating biological sequences, experimental protocols, or reports.
---

# RushData Order Design

Use customer-provided project data and design files to complete the authorized order workflow. Submitting an order for experimental work means calling `submit/batch`; it does not mean the experiment has completed.

Use `references/workflow.md` for input and API rules. Prefer MCP tools for normal execution.

## Tools

| Tool | Purpose |
| --- | --- |
| `order_design_preflight()` | Read company eligibility and the current test-item catalog. |
| `start_order_design(data, file_base64, filename)` | Submit a design, wait for confirmed saving, and return a `continuation_token`. |
| `add_order_to_cart(continuation_token)` | Add the verified design and locate its cart record; success returns `status=cart_confirmed`. |
| `get_order_cart(page_no=1)` | Read one cart page; follow pagination when checking an order. |
| `calculate_order_price(order_nos)` | Obtain an authoritative quote without submitting orders. |
| `submit_verified_order(order_nos)` | Requote, validate the exact selection, submit once, and check the cart afterward. |

`order_nos` is an array of order-number strings. Tools perform the upstream encoding. Do not expand the selection beyond the orders authorized by the user.

## Server Settings

The server uses `RUSHDATA_BASE_URL`, `RUSHDATA_ACCESS_TOKEN`, `RUSHDATA_API_TIMEOUT`, `RUSHDATA_DESIGN_TIMEOUT`, and `RUSHDATA_TIME_ZONE`. Business authentication uses `X-Access-Token`, separately from MCP authentication. Keep credentials out of tool arguments, request data, skill files, and logs.

`RUSHDATA_CONTINUATION_SECRET` must be an independent random server secret of at least 32 characters, different from both access tokens. It signs saved-design receipts and must remain on the server.

Set `RUSHDATA_DRAFT_CONTRACT_CONFIRMED=true` only after the backend confirms the antigen and positive-control fields, their encoding, required conditions, and applicable response structures. The setting itself is not evidence of support. Stop design writes while this contract is unresolved; do not remove required data to bypass the check.

## Execute

For existing orders that only need submission, start at step 6. Do not request another design file or recreate the orders.

1. Obtain the user's project data and original IgG or VHH XLSX. Check package, counts, and supplied antigen and positive-control data using `references/workflow.md`. Do not generate or alter biological sequences.
2. Call `order_design_preflight`. Require `hasCompany=true` and a positive `companyId`. Resolve test-item IDs from the current catalog; stop on missing or ambiguous matches.
3. Call `start_order_design` with the request object, standard Base64 of the original XLSX, and its filename. The file must be nonempty, have an `.xlsx` filename, and be at most 10 MiB. Do not pass a server file path or download address. Omit `data.id` for a new design; for an explicitly requested redesign, use the existing `rushDataServiceId`.
4. Only after saving is confirmed, pass the unchanged `continuation_token` to `add_order_to_cart`. This continues the saved design without running design again.
5. Require `status=cart_confirmed` and retain the matching `orderNo`. Use `get_order_cart` for further read-only checks. Never select an order by project name or list position alone.
6. When submission is authorized, use `calculate_order_price` to inspect the quote if needed, then call `submit_verified_order` with the same selected order numbers. It requotes and requires `canSubmit` to be exactly `true` and the quoted order set to match exactly.
7. Report the submission result and cart synchronization separately. Submission acceptance does not establish that an experiment has completed.

The request object uses `projectName`, `catalogNumber`, `antibodyProjectCount`, `antigenCount`, `usingdna`, `sp`, `antigens`, and `positiveControls`. For custom packages, `testItems` maps categories to arrays of business keys. Fixed packages may omit it. Never invent IDs or copy placeholder IDs.

## Failure and Continuation

Stop subsequent writes on design or save failure, conflicting identities, ambiguous cart matches, or an invalid quote. Preserve any received `orderNo`, `rushDataServiceId`, and the last confirmed stage. A write timeout or disconnected stream can leave a real order behind; do not report it as never created.

A `continuation_token` lasts one hour and is bound to the signing secret, business API environment, and business access token. It proves that this service confirmed saving; it does not make cart insertion idempotent. After an uncertain write, check state read-only instead of automatically repeating design, cart insertion, or submission.

Without a valid receipt, an existing draft requires a supported backend save-status check before continuation. That recovery capability is unavailable here. `designStatus=ok`, an absent cart record, or `completed.status=ok` alone cannot replace `result_saved`. Do not fabricate a receipt, redesign, or create another order to bypass this limitation.
