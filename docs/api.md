# API notes / API 说明

[Home](../README.md) · [中文首页](readme/README.zh-CN.md) · [Installation / 安装](installation.md) · [Tool catalog / 工具目录](tool-catalog.md)

## Connection / 连接

Biointron OS exposes its agent-facing tools through remote **MCP Streamable HTTP** at `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp`. Obtain access credentials from the service provider, then follow the [installation guide](installation.md). For the customer account/AppKey entry point, use the [Biointron website](https://os.biointron.com/); do not invent an unverified AppKey menu or issuance path. Documenting the address does not establish that all business operations are ready.

Biointron OS 通过远程 **MCP Streamable HTTP** 提供 Agent 工具，地址为 `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp`。请向服务提供方获取访问凭据，再按 [安装说明](installation.md) 配置。客户账号与 AppKey 可从[百英网站入口](https://os.biointron.com/)开始，未经核实不得编造具体菜单或发放路径；提供服务地址不代表所有业务操作已就绪。

The reference service accepts `Authorization: Bearer <MCP_ACCESS_TOKEN>`. A client must support the configured authentication mechanism; a client that only supports OAuth cannot be assumed compatible with this static-token setup.

参考服务使用 `Authorization: Bearer <MCP_ACCESS_TOKEN>`。客户端须支持对应认证方式；仅支持 OAuth 的客户端不能直接视为兼容此静态令牌配置。

The [JSON connection example](../examples/mcp-servers.example.json) uses the configurable name `BiointronOS_MCP`. Its `mcpServers` structure must be supported by the client. `START_MCP_TIMEOUT_MS` and `RUN_MCP_TIMEOUT_MS` are custom client/service headers, not standard MCP timeout settings. Their example values are 60,000 milliseconds (60 seconds) and 660,000 milliseconds (11 minutes). Merely sending these headers does not guarantee that the client will wait that long; configure its actual timeouts according to the client's documentation. See the [MCP transport specification](https://modelcontextprotocol.io/specification/latest/basic/transports).

[JSON 连接示例](../examples/mcp-servers.example.json)使用可自定义的连接名 `BiointronOS_MCP`，客户端须支持其 `mcpServers` 结构。`START_MCP_TIMEOUT_MS` 和 `RUN_MCP_TIMEOUT_MS` 是客户端或服务的自定义请求头，不是 MCP 标准超时配置。示例分别为 60,000 毫秒（60 秒）和 660,000 毫秒（11 分钟）；仅发送这些头不能保证客户端等待相应时长，实际超时需按客户端文档配置。参见 [MCP 传输规范](https://modelcontextprotocol.io/specification/latest/basic/transports)。

## Conversation language / 会话语言

Select `language="en"` or `language="zh"` from the customer's natural-language instructions and pass it explicitly to `order_design` and every order tool call. Keep it through CD2, SKUs, paths, credentials, numbers and short selections; follow a clear later language change. All customer-facing package copy, questions/options, guidance, validation/errors, catalog navigation and progress use the selected language verbatim where fixed copy is supplied. The compatibility default is `zh`, not automatic language detection. CLI callers use `--language en` or `--language zh`. Keep language in outer client context, never in `data`, `supplied`, upstream business payloads or signed `workflow_context`; the server has no global language state. API field names/enums and original customer/product data remain unchanged; explain raw backend errors in the chosen language.

按客户自然语言指令选定 `language="zh"` 或 `language="en"`，每次 `order_design` 和下单工具调用显式传入；CD2、货号、路径、凭据、数字和简短选择不改变语言，客户明确换语言时再切换。套餐、问题/选项、说明、校验/错误、产品库导航及进度都使用所选语言，固定文案保留对应语言原文。默认 `zh` 仅兼容旧调用，CLI 用 `--language zh`/`--language en`。语言只在客户端外层上下文保留，不进入 `data`、`supplied`、业务请求或签名上下文，服务器不保存全局语言；业务键、枚举和原始资料不改写，后端错误用会话语言解释。

## Credentials / 凭据

| Credential | Purpose / 用途 | Where configured / 配置位置 |
| --- | --- | --- |
| MCP access token / MCP 访问令牌 | Authenticate the client to the MCP service / 验证客户端对 MCP 的访问 | Client connection and MCP service / 客户端连接与 MCP 服务 |
| Business API credential / 业务 API 凭据 | Identify the customer and check access at the business API / 由业务 API 识别客户并校验权限 | Required `business_token` argument on every business tool call / 每次业务工具调用的必填参数 `business_token` |

Keep these credentials separate. The MCP connection still uses the shared service token. Every business tool requires the current customer's raw `business_token`, without a `Bearer` prefix; report and order tools use the same parameter. The server does not fall back to `BIOINTRON_API_AUTH_VALUE`, `RUSHDATA_ACCESS_TOKEN`, or a previous call's token. Requests use separate credentials and Cookie state; business APIs enforce the supplied customer token's permissions. This is not an OAuth login or token-refresh flow.

Provide a business token only in its dedicated argument, never in `query`, `data`, MCP prompt arguments, files, ordinary replies or generated reports. Client tool history may retain arguments. Do not write real credentials into examples, documentation or repository files. Saved-design receipts are bound to the supplied business token and cannot be continued with another customer's token.

两类凭据不能互相替代。MCP 入口继续使用共享服务令牌；每个业务工具每次都要求当前客户的原始 `business_token`，不加 `Bearer`，报告与下单使用同一个参数。服务端不回退到 `BIOINTRON_API_AUTH_VALUE`、`RUSHDATA_ACCESS_TOKEN` 或前一次调用的 Token。请求凭据和 Cookie 状态按调用隔离，业务 API 根据本次 Token 校验客户权限；这不是 OAuth 登录或令牌自动续期功能。

业务 Token 只放在专用参数中，不放入 `query`、`data`、MCP Prompt 参数、文件、普通回复或生成报告。客户端可能保存工具调用历史。示例、文档和仓库文件不能保存真实凭据。设计保存凭证绑定本次业务 Token，不能换成另一客户的 Token 续接。

When a business request needs credentials, reuse the current customer's valid JWT. Otherwise ask only for the missing **Biointron Account**, then **App Key**, as separate text fields and keep the task pending. Map user labels `account`/`apkey` to the exchange JSON fields `username`/`appkey`. The client posts those fields to the configured `client_side_exchange.url`, using available server connection metadata; require HTTP 2xx, numeric `code=200`, `success=true`, and a nonempty `result.token` before passing that JWT as `business_token`. MCP does not perform the exchange or accept an account/App Key in place of JWT. Do not hardcode an authentication address, guess an environment, follow credential-bearing redirects, or automatically retry a failed exchange. Follow the [exchange rules](../skills/order_design/references/workflow.md#client-side-credential-exchange). If the client lacks HTTP/script execution, explain that capability gap rather than asking ordinary customers to retrieve JWT manually. Generating a report from already supplied result JSON bypasses credentials entirely.

In every client and CLI, resolve routing choices before dependent fields, then invoke the generated independent-field batch through an available native question tool. Omit `options` for text fields; when a tool requires choices and offers Other/custom text, collect the actual value there. UI actions such as “填写此项” or “暂不提供” are not business values. Merge the completed batch without per-field MCP/model or validation calls. CLI asks the same batch sequentially; complete business checks happen before writing. Credentials remain separate ordinary text fields labelled **Biointron Account** and **App Key**, following existing credential guidance. Do not prefill/echo secrets or put them in URLs, logs, reports or business DTOs. If native questions are genuinely unavailable, explain the limitation and use the available text/terminal interface. Use only tools permitted in the current mode; never pretend a dialog opened.

实际业务请求需要凭据时，先复用当前客户有效 JWT；否则仅按顺序单独补问缺失的 **Biointron Account**、**App Key**，等待真实回答。用户的 `account`/`apkey` 映射为兑换 JSON 的 `username`/`appkey`，由客户端按服务连接元数据中的 `client_side_exchange.url` 发起 POST；只有 HTTP 2xx、数值 `code=200`、`success=true` 且 `result.token` 非空才使用该 JWT。MCP 不负责兑换，也不接受账号或 App Key 代替 JWT。不固定认证地址、不猜环境、不跟随携带凭据的重定向、不自动重试失败兑换，详见[兑换规则](../skills/order_design/references/workflow.md#client-side-credential-exchange)。没有 HTTP/脚本能力时说明能力缺口，不让普通客户手动寻找 JWT。已有结果 JSON 的本地报告生成完全不需要凭据。业务资料先选分支，再把独立文本及选择题放在同一个原生 `questions` 数组；文本项省略 `options`，UI 动作不是业务值。CLI 顺序收集同批答案，批内不调用模型、MCP 或完整校验，写入前集中检查。凭据使用普通文本，不预填、回显或放入 URL、日志、报告、`supplied` 或业务 DTO。没有原生提问能力时才说明限制，用可用文字/终端完成同批资料；不依赖 Plan 专用工具，不假装弹窗。

Start new orders with package introductions and selection, without authentication. Upon choosing our product library, local input guidance returns `catalog_auth` for a question marked `credential_check_required`; use its configured exchange metadata without loading the full execution prompt. Prefer an existing valid JWT even when this guidance says `needs_credentials`; otherwise collect only missing Biointron Account/App Key values. Ask for a keyword such as CD2 through a native text dialog or CLI, then call `search_order_antigens(keyword, business_token, page_no=1, page_size=50, language=language)`. The query merges up to five pages, deduplicating by supplier, catalog number and specification. Preserve all returned candidates; do not silently apply exact-keyword, supplier or species filters. Ask the customer before narrowing the results and distinguish similarly named antigens. Show `catalog_summary` and pass both `catalog_options` and `catalog_search` to local input guidance. When `has_more` is true, offer a load-more action using `next_page`, preserve earlier candidates, and distinguish product counts from specification counts. Partial page failures remain visible and must not be described as complete results. Retain the chosen option's `cart_data`. Do not ask for a supplier or a missing product link. External-link/manual branches authenticate before design submission. API addresses come from config, never a customer question.

新单先介绍并选择套餐，不先认证。选择产品库后，本地输入说明在 `credential_check_required` 问题中返回 `catalog_auth`，直接使用其中的配置连接信息，无需加载完整执行提示词；即使提示 `needs_credentials`，客户端已有有效 JWT 仍优先复用，否则只补问缺失的 Biointron Account 和 App Key。随后通过原生文本弹窗或 CLI 输入关键词（如 CD2），调用 `search_order_antigens(keyword, business_token, page_no=1, page_size=50, language=language)`，每次最多合并5页并按供应商、货号、规格去重。完整保留后台候选，未经客户确认不按精确关键词、供应商或物种二次筛选，也不将相似名称当作同一抗原。展示 `catalog_summary`，将 `catalog_options` 与 `catalog_search` 一起交给输入说明工具；有更多结果时提供继续加载入口并使用 `next_page`，保留已加载候选，分别显示产品数和规格数。后页失败须说明未完成；无结果可换词，选中后保留 `cart_data`，不询问供应商或补链接。外部链接、手动资料分支仍在提交设计前认证，API 地址从 config 读取，不向客户提问。

The local catalog contains **11 tools, 5 resources and 2 prompts**: ten customer-related tools require JWT, and the local input-requirements tool does not. These declarations were inspected read-only; this documentation update was not deployed and no live business request or integration test was run. / 本地清单为 **11 个工具、5 个资源、2 个提示词**：十个客户业务或续办工具需要 JWT，一个本地输入说明工具无需业务 JWT。本轮仅只读核对声明，未部署、未调用真实业务或执行联调测试。

## Business contracts / 业务契约

### Report generation and optional retrieval / 报告生成与可选取数

The report Skill's metadata name is **`auto-html-report`**. Its folder and MCP prompt remain **`auto_html_report`**, and its resource identifiers retain that underscore spelling. The [Skill](../skills/auto_html_report/SKILL.md) turns supplied experimental result JSON into a standalone HTML report with a complete Data Summary, sample comparison charts, SPR/BLI kinetic plots, and available experimental images. This local path needs no credentials, MCP connection, or order Skill. An order number, schema example, or empty response is not result data.

报告 Skill 的元数据名称为 **`auto-html-report`**，文件夹和 MCP 提示词仍为 **`auto_html_report`**，资源标识也保留下划线拼写。[报告 Skill](../skills/auto_html_report/SKILL.md) 从已提供的实验结果 JSON 制作独立 HTML，包含完整 Data Summary、样本对比图、SPR/BLI 动力学图及实际提供的实验图片。此本地流程无需凭据、MCP 连接或订单 Skill；订单号、结构示例、空响应都不能代替结果数据。

If result JSON is missing and the user authorizes retrieval, use the confirmed order number and current customer's JWT with `get_report_results(query={"orderNo": "<order-number>"}, business_token=<JWT>, language=<interaction-language>)`. Tool interaction supports `zh` or `en`, independently of the requested report language. Reuse a valid JWT or complete the client-side exchange above. Reuse existing connection metadata first; only if it is missing, request `order_design(phase="execute", detail="compact", language=<interaction-language>)` solely for `connection_config`. Do not use the default `start` phase for report preparation or follow unrelated ordering instructions. Standalone clients use their existing configuration; missing configuration belongs to service maintenance. Check HTTP status, business status and actual result content before generating HTML. Loading the report prompt only supplies instructions and does not query results, read image paths, or authorize any order write.

缺少 JSON 且用户授权查询时，用已确认订单号和当前客户 JWT 调用 `get_report_results(query={"orderNo": "<order-number>"}, business_token=<JWT>, language=<interaction-language>)`。工具交互支持 `zh`/`en`，与用户要求的报告语言分开。复用有效 JWT；无 JWT 时先按上节完成客户端兑换。优先使用已有连接元数据，仅缺少时才调用 `order_design(phase="execute", detail="compact", language=<interaction-language>)` 获取 `connection_config`，不使用默认 `start` 阶段或执行无关下单指令。独立客户端使用已有连接配置，缺配置交维护方处理。查询后核对 HTTP、业务状态及实际结果，再生成 HTML。加载报告提示词只提供说明，不自动查询结果、读取图片路径或授权写订单。

### Final order submission / 最终订单提交

The order Skill (`order-design`, folder/prompt `order_design`) collects independent question batches, validates the complete design/cart stage before writing, and offers the saved-design HTML choice below. Before final submission, obtain an authoritative quote and the customer's confirmation of the exact orders, quote/discount, and readiness of PO and real company information. Unknown prerequisites require human verification; `hasCompany` and `canSubmit` do not verify PO validity. `submit_verified_order` requotes the exact selection and submits it for **Biointron's human confirmation**. Report submission acceptance and cart synchronization separately. Acceptance is not payment, production confirmation, experimental completion, or a guarantee that results are available; production begins only after Biointron's confirmation.

订单 Skill（名称 `order-design`，目录/提示词 `order_design`）按独立问题批次收集资料，在设计或购物车写入前统一校验，并提供下节的设计 HTML 查看选择。最终提交前，先取得权威报价，由客户确认准确订单、报价/折扣及 PO、真实公司资料已具备；未知条件需人工核实，`hasCompany`、`canSubmit` 不能证明 PO 有效。`submit_verified_order` 对准确订单集合重新报价并提交，**等待百英人工确认**。提交受理与购物车同步分别反馈；受理不表示付款、确认生产、实验完成或结果可用，生产仅在百英确认后开始。

### Optional saved-design HTML / 可选设计结果查看

Immediately after verified design storage, follow `start_order_design.interaction` to ask whether the customer wants the HTML design result, before collecting cart details or adding to cart. Yes: call `get_order_design_result` with the same `business_token` and complete original `workflow_context`, save its actual `html` using `utf-8-sig` without rewriting the content or overwriting an existing file, and deliver a file link or attachment before continuing. No: skip retrieval and continue the existing cart workflow. Read failures offer retry-read or continue, preserving the saved design and context; never redesign or automatically repeat a write. Local delivery failures reuse the already-read HTML. Viewing a report is not final-submit consent.

设计确认保存后，先按 `start_order_design.interaction` 弹出“是否查看设计结果”选择，再收集购物车资料或加购。需要时，以相同 `business_token` 和完整原始 `workflow_context` 调用 `get_order_design_result`，将真实 `html` 原文以带 BOM 的 UTF-8（`utf-8-sig`）保存为新文件并交付文件链接或附件，再继续；不需要时跳过读取。读取失败先询问重试读取还是继续，保留已保存设计与上下文，不重新设计或自动重复写入。仅本地交付失败则复用已读 HTML。查看结果不代表授权最终提交。

The reader uses the verified `rushDataServiceId` with `GET /order/rushData/report` (ZIP `report.html`). It is distinct from experimental report JSON/HTML and does not use `get_report_results` or `auto_html_report`. Success returns `status=design_result_ready`, `report_type=design`, `filename`, `mime_type=text/html`, `html`, and the unchanged context. CLI asks after saving; noninteractive `run(args, business_token)` requires an explicit `--design-result view|skip` before design starts. `--design-result-dir` chooses the HTML folder; `--report` remains the JSON outcome file.

读取接口使用已验证的 `rushDataServiceId` 调用 `GET /order/rushData/report`，读取结果 ZIP 中的 `report.html`，与实验结果报告分开。成功返回实际 HTML、文件名及原始上下文。CLI 在保存后询问；非交互调用需在设计前明确指定 `--design-result view|skip`，`--design-result-dir` 设置 HTML 目录，`--report` 仍是 JSON 执行结果。

### Local input requirements / 本地输入说明

`get_order_input_requirements(stage, supplied=None, language="zh", detail="compact", mode="collect")` defaults to collection only. It returns `status=collecting|collected`, `validation_deferred=true`, `write_performed=false`, and a batch of independent questions. `collected` means the known branch has been collected, not that input is valid or a write is authorized. Ask routing decisions (package, Customized sample form, antigen source) separately before their dependent fields. Then invoke the returned `interaction.native_question.questions` in one native call for independent text and choice fields, using the selected language. Merge the whole batch before requesting the next branch or batch; do not call MCP, the model or full validation after every field. CLI prompts through the same batch sequentially without model/MCP round trips, rule rereads or business validation inside the batch. Missing or blank routing answers still need questions. Preserve real `false`, `0` and explicitly supplied `[]`; never invent defaults. Collection does not perform full business validation or scan XLSX contents. Immediately before an actual design or cart write, call `get_order_input_requirements(..., mode="validate", language=language)` with all collected inputs. Validate the whole stage once; on `status=needs_input`, explain all discovered issues and invoke its native correction batch, preserving valid answers. Revalidate after the correction batch, not after each field. `status=ready` confirms local validity only. Compact validation retains all discovered issues and the question batch; use `detail="full"` only when a complete schema or diagnostic report is needed. Actual write-entry guards remain intact: authentication, file transport limits, company eligibility, live catalog and saved-context checks still precede the relevant API call. Keep credentials in client state; account, App Key and JWT never enter `supplied` or business DTOs. Collection and validation do not authorize a write. Reuse the current language, valid JWT and catalog candidates. Do not insert planning, recaps, tool discovery, reconnection or repeated authentication between questions. Design `supplied` contains known `data`, `filename`, and `file_base64`; cart contains known `cart_data`. UI-only paths must be read locally and converted to filename/Base64, never sent as remote paths. This tool takes no business JWT and calls no business API; MCP authentication remains unchanged.

The local validator remains `skill/order_design/scripts/forms.py`, using the existing `jsonschema` dependency. Explicit validation reports all discovered issues, with a native correction batch; complete `schema` and diagnostic inventory are available through `detail="full"`. Actual design/cart entry checks still return structured `needs_input` for ordinary missing/invalid top-level input. Authentication/configuration failures and uncertain write outcomes remain separate and never justify automatic retries. Include the validator in deployment/public packages; no new environment variable or Redis is required.

`get_order_input_requirements(stage, supplied=None, language=language, detail="compact", mode="collect")` 默认只收集资料：返回 `status=collecting|collected`、`validation_deferred=true`、`write_performed=false` 及当前可独立填写的问题批次。`collected` 仅表示本轮资料已收集，不表示输入正确、已获授权或可写入。套餐、Customized 样本形式、抗原来源等决定后续分支的问题先单独选择；分支确定后，将独立文本及选择题放在同一次 `interaction.native_question.questions` 中实际调用原生工具。合并整批真实答案后再推进下一分支或批次，不对每个字段重新调用 MCP、模型或完整校验。CLI 顺序询问同一批字段，批内不回到模型、不重读规则、不调用输入说明或业务校验。缺失或空白的分支答案仍需询问；保留 `false`、`0` 和客户明确给出的 `[]`，不补默认值。收集阶段不运行完整业务校验或扫描 XLSX。 资料收齐、准备实际设计或购物车写入时，显式调用 `get_order_input_requirements(..., mode="validate", language=language)`，一次检查本阶段全部资料。`status=needs_input` 时汇总全部已发现问题，并用返回的原生问题批次收集修正；保留其他有效答案，整批修改后再校验。`status=ready` 仅表示本地检查通过。`detail="compact"` 保留当前动作、问题批次及全部校验问题；仅需完整 schema 与诊断时用 `detail="full"`。实际写入入口的完整保护保留，认证、文件传输限制、公司权限、产品目录与签名上下文等检查均须在相应 API 调用前通过。凭据只留客户端，App Key、账号和 JWT 不进入 `supplied` 或业务 DTO；收集或校验完成均不新增写入授权。 设计 `supplied` 为已知 `data`、`filename`、`file_base64`，购物车为 `cart_data`；文件路径只在客户端读取转换，不传给远程 MCP。部署及公开包保留 `scripts/forms.py`，其 `jsonschema` 已由 MCP 2.3 提供，不新增环境变量或 Redis。

Across all branches, advance after completed batches rather than after each changed field. Keep credentials in client state, reuse a valid JWT and exchange only after missing credentials are complete. Do not insert plans, recaps, discovery, bridges, reconnects or rule rereads inside a batch. Load `order_design(phase="execute", language=language)` once before execution; reuse compact rules and connection metadata, with full references reserved for specific diagnostics. Collection does not scan XLSX. Actual design execution performs one advisory count from the original workbook; an unreliable count is omitted. File transport checks and pre-write business/permission guards remain, and the backend decides workbook acceptability.

所有分支在整批答案完成后推进，批内不逐字段调用 MCP/模型或校验。凭据保留客户端，有效 JWT 直接复用，缺项补齐后才兑换。执行规则 `order_design(phase="execute", language=language)` 只加载一次，具体排查才读取完整参考。收集阶段不扫描 XLSX；实际设计执行时从原文件尽力统计一次，不可靠则省略。文件读取/传输检查及写入前业务、权限保护保留，Excel 内容是否合格交后端判断。

Catalog searches use one HTTP client local to the call with the same customer JWT. The first requested page establishes bounds; up to four following known pages are read concurrently and all launched reads finish before the client closes. Merge in page order with the existing five-page/50-record limits, deduplication, output byte cap, changed-pagination/repeated-page checks and first-failed-page `next_page` behavior. There is no cross-customer cache or automatic retry. These changes reduce repeated work; no end-to-end latency was measured and model/backend response within a few seconds is not guaranteed.

产品库每批复用一个仅属于本次调用、使用同一客户 JWT 的 HTTP 客户端；首个请求页确认范围后，并发读取后续已知的最多 4 页，全部读取完成后关闭客户端。按页序合并，保留最多 5 页、每页最多 50 条、去重、输出大小上限、分页变化/重复页检查及首个失败页的 `next_page` 规则，不跨客户缓存或自动重试。这些调整减少重复工作，未实测端到端耗时，不保证模型或后端在数秒内返回。

This local input tool does not recover designs or reissue save receipts. Continuation requires the original complete signed context or compatible receipt, the same JWT and a valid expiry; order number alone cannot recover missing proof. The server has no saved copy.

本地输入说明工具不恢复设计、不补签凭证；续办须有完整原签名上下文或兼容回执、原 JWT 且尚未过期。只有订单号不能恢复，服务端没有副本。

The [tool catalog](tool-catalog.md) documents the MCP entry points and their parameter containers. It does not define the upstream business API. A public, versioned contract is still needed for:

工具目录描述的是 MCP 入口及参数容器。后端业务 API 的以下内容仍需在正式公开、带版本的契约中提供：

- Required fields and identifiers / 必填字段与标识含义。
- Authentication, authorization, and account eligibility / 认证、授权及账户资格。
- Response fields, business success criteria, and error codes / 返回字段、业务成功判定和错误码。
- Order-state queries and recovery after an uncertain write / 订单状态查询及写入结果不确定时的核查方式。
- Report data definitions and file-access rules / 报告数据定义及文件访问规则。

An installation example cannot substitute for these definitions. The bundled Skills include an [order workflow reference](../skills/order_design/references/workflow.md) and a [report result schema](../skills/auto_html_report/references/result-schema.md). These describe the current Skills; they do not replace a versioned upstream API contract. The order Python helpers still require the source project's configuration, Python package layout and dependencies; their inclusion does not make this documentation bundle a standalone business application. See [installation requirements](installation.md#skills).

安装示例不能替代业务字段定义。两个 Skill 已随包提供[订单工作流参考](../skills/order_design/references/workflow.md)和[报告结果结构](../skills/auto_html_report/references/result-schema.md)，用于说明当前 Skill，并不替代带版本的后端 API 契约。订单 Python 辅助脚本仍需要源项目配置、Python 包结构及依赖；随包提供不代表本展示包是独立业务程序，详见[安装说明](installation.md#skills)。

## Temporary workflow state / 临时工作流状态

The active workflow has no Redis/database/session-cache dependency. Design success returns `workflow_context={version:1, order_no, expires_at, next_tool:"add_order_to_cart", continuation_token:<full signed string>}`. The AI retains and returns the complete original object; the top-level receipt remains compatible. Prefer `add_order_to_cart(business_token, cart_data, workflow_context=<original>, language=language)`; optional `order_no` and `continuation_token` must agree with that context. Order number alone cannot recover missing proof. MCP checks the signature, exact JWT, API environment, expiry, order metadata and `projectNo`; a missing main order ID cannot be replaced by a service ID. Details must show draft (`-3`) or cart (`00`) status before insertion; submitted/unknown states are blocked. This read-only check is not atomic.

During context organization, memory compaction or chat/agent handoff, preserve the full object verbatim, never a truncated signature or summary-only substitute. Keep each order under its customer-credential secure reference and order number. Retain phase, confirmed cart fields including real `false`/`0`, outstanding inputs, user authorization, last call and unresolved results in an outer handoff record, never by adding fields to `workflow_context`. JWT/AppKey values stay out of ordinary summaries, repository memory, shareable documents and server storage; use secure references. These are Skill/client instructions, not a guarantee that every client preserves history. If proof is lost, stop: the server has no copy.

`end_order_workflow(order_no, business_token, workflow_context=None, continuation_token="", language=language)` returns `status="discard_context"`, `server_revoked=false`, `client_action="delete_local_context"`, and `business_order_cancelled=false`. It instructs the AI to discard its local context, not revoke a signature or cancel/delete an actual order. It cannot erase other copies. Credential validity remains one hour, without refresh/reissue. A different JWT cannot continue old proof. After an authorized redesign discard the old local context; metadata lookup cannot establish the current saved version or revoke other copies.

There is no shared design/submission deduplication or atomic cart claim. Sequential cart insertion first reads the cart; an existing match returns `already_in_cart=true`, `write_performed=false`, `cart_data_applied=false`. This means the submitted cart fields were not rewritten; do not claim new antigen/shipping choices were applied. Cross-FC concurrency and duplicate designs need backend idempotence. AI must not auto-retry or concurrently write the same order; unknown results require read-only checks. Do not fall back automatically to CLI/website operations after an MCP failure.

当前由 AI 携带完整签名 `workflow_context`，没有 Redis、数据库或会话缓存运行依赖。设计成功返回 `version:1`、订单号、到期时间、下一工具和完整签名字符串；AI 原样回传，JWT 单独传入。多个表示须一致，只有订单号不能恢复。MCP 验签并核对原 JWT、环境、期限、订单元数据与 `projectNo`。 加购前只接受详情中的草稿（`-3`）或购物车（`00`）状态，已提交/未知状态停止；读取核对不保证原子性。

整理、压缩或跨聊天交接时，完整对象不能截断或用总结替代；按凭据安全引用＋订单号分别保留。阶段、已填购物车资料（真实 false/0）、缺项、授权、最后调用及未知结果放在外层续办记录，不往原 `workflow_context` 加字段。JWT/AppKey 不进入普通摘要、仓库记忆、可分享文档或服务器存储。此为 Skill 对客户端的要求，不能保证所有客户端一定保留；丢失必须停，服务端没有副本。

结束工具只返回丢弃本地上下文指令，`server_revoked=false`、`business_order_cancelled=false`，不撤销签名或后台订单，也不能删除其他副本。凭证最多有效 1 小时，不补签续期。重设计时丢弃本地旧上下文，详情不能证明当前保存版本。顺序加购发现已在购物车时返回 `already_in_cart=true`、`write_performed=false`、`cart_data_applied=false`，不能声称本次已更新抗原或发货选择。无共享去重/原子领取，跨 FC 并发与重复设计依赖后端幂等；不自动重试或并发写同单，未知结果先查询。

## Adapter result / 适配器返回

### Verified cart request / 已核对的购物车请求

Checked on **2026-11-03** against the test environment's [OpenAPI document](https://testmyorder-en.biointron.com.cn/byorderapi/by-order-client/v2/api-docs) and current web client: `POST /order/rushData/addToCart` takes JSON only, with no query parameters. Required fields are `antigens`, `orderNo`, `projectNo`, `rushDataServiceId`, and `shippingRequired`; optional fields include `projectName` and singular string `positiveControl`. The older draft's no-body description is outdated. This is contract verification, not a completed live write test.

The MCP tool accepts `cart_data` containing only `projectNo`, `shippingRequired`, `antigens`, and optional `positiveControl`. It obtains order identity from its verified continuation receipt. Confirm the actual project number and explicit shipping choice; `false` unbinds an address, while `true` needs a website-bound address. The design's antigen and positive-control fields do not substitute for this cart DTO. See the [11-field antigen schema and workflow](../skills/order_design/references/workflow.md).

**2026-11-03** 已对照测试环境 OpenAPI 与当前网页核对：`addToCart` 只接收 JSON，不带 Query。必填 `antigens`、`orderNo`、`projectNo`、`rushDataServiceId`、`shippingRequired`；`projectName` 和单数字符串 `positiveControl` 可选。MCP 的 `cart_data` 仅接收 `projectNo`、`shippingRequired`、`antigens` 和可选 `positiveControl`，订单身份由保存凭证取得。必须核实真实项目编号及用户发货选择；`false` 会解绑地址，`true` 需要网页已绑定地址。旧草案无请求体说明已过期，设计字段不能替代当前购物车 DTO。此为契约核对，尚不表示真实写入测试完成；字段详见[工作流规则](../skills/order_design/references/workflow.md)。

### Report wrapper / 报告包装

[tool-result.example.json](../examples/tool-result.example.json) illustrates the `get_report_results` adapter's wrapper:

| Field | Meaning / 含义 |
| --- | --- |
| `http_status` | Upstream HTTP status / 后端 HTTP 状态码 |
| `data` | Complete parsed upstream API envelope, with business results under `data.result`; `null` when the response body is empty / 完整解析后的后端 API 包装，业务结果位于 `data.result`；空响应体时为 `null` |

The sample deliberately uses `data: null` and contains no report schema. It demonstrates an empty upstream response, **not a successful business operation**. This is an application-level adapter result, not the full MCP `tools/call` result or a JSON-RPC response. An MCP client may expose it inside its tool-result content. Order tools return stage-specific status and identity fields; see the [tool catalog](tool-catalog.md).

示例使用 `data: null`，不包含报告 schema，表示后端响应体为空，**不表示业务执行成功**。它是 `get_report_results` 的应用层适配器结果，不是完整的 MCP `tools/call` 返回体或 JSON-RPC 响应；客户端可能将它呈现在工具返回内容中。订单工具按阶段返回状态和身份字段，详见[工具目录](tool-catalog.md)。

## Beta behavior / Beta 行为

An unconfigured endpoint is unavailable even when its tool is listed. Connection failures, HTTP errors, or invalid responses must be reported accurately. For write operations, a timeout can leave the actual business outcome uncertain: retain known identifiers and check the state before any repeat submission. Experimental availability is not a substitute for a confirmed result.

即使工具已经列出，未配置的业务接口仍不可用。连接失败、HTTP 错误及无效响应应如实说明。写请求超时可能使实际业务结果无法确认，应保留已知标识，核查状态后再决定是否重试，不能把测试状态解释为业务已成功。
