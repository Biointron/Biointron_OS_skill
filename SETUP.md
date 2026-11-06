# GitHub 展示包交接说明

本目录是公开仓库 [Biointron/Biointron_OS_skill](https://github.com/Biointron/Biointron_OS_skill) 的展示内容根目录。将**目录内的文件**放到仓库根目录，GitHub 会自动在代码列表下显示 `README.md`。不要在远端再套一层 `modules/github`。

## 已准备的内容

| 文件 | 用途 |
| --- | --- |
| [README.md](README.md) | 英文默认首页。 |
| [docs/readme/README.zh-CN.md](docs/readme/README.zh-CN.md) | 简体中文首页。 |
| [docs/readme/README.ja.md](docs/readme/README.ja.md) | 日文首页。 |
| `docs/readme/README.<语言代码>.md` | 全部 22 种非英文首页集中放在此目录；顶部语言栏可切换全部 23 种语言。 |
| [assets/](assets/README.md) | 已使用用户提供的 `最终logo.png`，以及后续更新说明。 |
| [工具目录](docs/tool-catalog.md) | 十一个 MCP 工具：十个客户业务/续办工具需要 JWT，一个本地输入说明工具无需业务 JWT；另有五个资源、两个提示词。 |
| [安装指南](docs/installation.md) | MCP 连接、JSON / Codex 示例、Codex / Claude Code Skill 安装位置。 |
| [JSON 连接示例](examples/mcp-servers.example.json) | `BiointronOS_MCP` 配置，使用已提供的服务地址与令牌占位符。 |
| [Skills 目录](skills/README.md) | Skill 名称为 `order-design` 和 `auto-html-report`，文件夹分别为 `skills/order_design` 和 `skills/auto_html_report`；配套参考文件及订单辅助脚本已随包提供。 |
| [API 说明](docs/api.md) | 认证边界、公开契约状态、JSON 示例说明。 |
| [LICENSE](LICENSE) | 未修改的 PolyForm Noncommercial 1.0.0 正文。 |
| [贡献说明](CONTRIBUTING.md) | 文档贡献与本地检查方式。 |
| `scripts/check_docs.py` | 无依赖的本地链接、锚点、JSON / SVG 检查。 |
| `scripts/build_preview.py` | 从 Markdown 生成便于本地查看的网页预览。 |

## 多语言首页

首页提供与参考截图一致的 23 种语言：English、简体中文、繁體中文、日本語、한국어、Türkçe、Русский、Tiếng Việt、ไทย、Deutsch、Español、Français、Українська、Polski、Português (Brasil)、فارسی、العربية、Bahasa Indonesia、Italiano、Ελληνικά、മലയാളം、Roman Urdu、Română。

各入口对应完整翻译的 README，当前语言加粗，语言栏会随页面宽度自动换行。根目录只保留英文默认首页 `README.md`，其余 22 种语言（含简体中文和日文）集中放在 `docs/readme/`。语言切换、文档入口和图片链接均使用对应位置的相对路径。阿拉伯语和波斯语正文按从右到左阅读的方向显示，技术标识和配置保持原文。详细安装、工具及 API 文档仍为中英双语。

## 首页顺序

语言选择 → Biointron OS 标题和介绍 → MCP / Skills / License / Beta 徽章 → 正式宣传图 → 横向导航 → 三层定位 → MCP 与 Skill 安装 → 工具、Skill 介绍 → Beta Playground → 在线平台介绍与宣传图 → FAQ / 文档 / License。

宣传图已采用项目 `static/最终logo.png`，在展示包中保存为 `assets/biointron-os-hero.png`。所有语言首页按原始宽高比例展示；后续替换同名 PNG 即可更新图片，详见 [assets 说明](assets/README.md)。

在线平台介绍使用 `assets/Biointron_Rushdata.png`，位于 Beta Playground 之后、FAQ 之前；文字入口和图片均可点击访问 [Biointron 在线平台](https://ai.biointron.com/#/landing)。全部 23 种语言的首页导航已增加对应入口。

版式参考 [morluto/rea](https://github.com/morluto/rea) 的语言入口、居中品牌区、徽章、图文导航和分层文档。文案与产品说明均按 Biointron OS 编写，宣传图使用用户提供的素材，没有复制参考仓库的品牌素材或安装命令。

## MCP 连接配置 / MCP connection configuration

已加入服务地址 `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp`。JSON 示例以 `BiointronOS_MCP` 为连接名，Codex 示例沿用 `biointron`；两者均为可自定义名称，不是工具标识。JSON 格式仅适用于明确支持该 `mcpServers` 结构的客户端。公开配置只保留 `Bearer <MCP_ACCESS_TOKEN>`，真实令牌由使用者在本地填写。

The supplied service address is now included. The JSON example uses `BiointronOS_MCP`, while Codex uses `biointron`; both are configurable connection names, not tool identifiers. Use the JSON only with a client that supports its `mcpServers` structure. Public examples retain `Bearer <MCP_ACCESS_TOKEN>`; users supply their real token locally.

配置中的 `START_MCP_TIMEOUT_MS: 60000` 和 `RUN_MCP_TIMEOUT_MS: 660000` 按用户提供的内容保留，分别表示 60 秒和 11 分钟。这两个头属于客户端或服务自定义项，不是 MCP 标准超时配置；仅放在 `headers` 中不能保证延长客户端等待时间。请按实际客户端文档设置超时，详见[安装指南](docs/installation.md)。本次文档更新未调用真实服务。

The supplied `START_MCP_TIMEOUT_MS: 60000` and `RUN_MCP_TIMEOUT_MS: 660000` headers are retained, representing 60 seconds and 11 minutes. They are custom client/service fields, not standard MCP timeout settings. Putting them in `headers` alone does not guarantee a longer client wait. Configure timeouts according to the actual client's documentation; see the [installation guide](docs/installation.md). This documentation update did not call the live service.

十个涉及客户业务或临时续办状态的工具要求每次调用传入 `business_token`（客户原始业务 Token，无 `Bearer` 前缀），报告查询、产品库查询和下单共用此参数。MCP 入口令牌不变；服务端不再读取 `BIOINTRON_API_AUTH_VALUE`、`RUSHDATA_ACCESS_TOKEN`。发布前先同步后端和两个 Skill 的最新版本，再刷新客户端工具 schema；GitHub 文档更新本身不会更新 FC。文档和示例只写占位符，真实业务 Token 不进入仓库或生成报告。

All ten customer-related business/workflow tools, including saved-design HTML retrieval and product-library search, require the current customer's raw `business_token` on each call. The MCP connection credential is unchanged. Publish the matching backend and Skill versions before refreshing clients; updating this repository does not deploy FC. Keep real business tokens out of repository files and generated reports.

另有无需业务 JWT 的本地工具 `get_order_input_requirements`，用于分阶段补齐输入，不调用业务 API，也不代表已授权执行。默认 `mode="collect"` 返回互不依赖的问题批次，普通答案先收集；设计或购物车写入前以 `mode="validate"` 统一检查、集中修正。`detail="compact"` 只保留当前动作、问题批次和相关诊断；`detail="full"` 才提供完整 `schema`、`missing_fields` 供排查。当前合计 **11 个工具、5 个资源、2 个提示词**。保留公开订单包的 `scripts/forms.py`；其 `jsonschema` 使用已有 MCP 2.3 依赖，不新增环境变量。本轮未部署 FC，未执行真实产品查询或联调测试。

The local `get_order_input_requirements` tool needs no business JWT and makes no business API requests; input readiness is not permission to execute. Default `mode="collect"` batches independent questions without validating each ordinary answer; `mode="validate"` checks completed design/cart data and returns repair batches before writes. `detail="compact"` retains the current action, native question batch and relevant diagnostics; `detail="full"` adds the full `schema` and `missing_fields` for diagnostics. The current total is **11 tools, 5 resources and 2 prompts**. Keep the public order package's `scripts/forms.py`; `jsonschema` is supplied by existing MCP 2.3 dependencies. The input validator adds no environment variables; AI-held signed continuation requires no Redis configuration. No FC deployment, live product query or integration test is part of this update.

所有下单分支先完成当前整批填写，再合并资料获取下一批；不每答一项就调用 MCP 或校验。套餐、样本形式和抗原来源先确定依赖分支；收齐后才统一检查并只补问修正批次。复用有效 JWT，Biointron Account 与 App Key 之间不插入请求，逐题转换不插入计划、复述、工具发现、桥接进程、重连或规则重读。执行前只加载一次 `order_design(phase="execute", language=language)`，默认 `detail="compact"` 返回精简执行规则和连接信息；仅具体排查使用 `detail="full"` 完整参考。表格数量在实际设计适配器中尽力统计一次，不在每轮 MCP/CLI 提问时重复解析；传输与业务检查保留。产品库每批用同一调用内的 HTTP 客户端先读一页、再并发读取后续最多 4 个已知页面，等待全部读取后按页序合并；5 页/每页 50 条、去重、大小上限和失败续查规则不变，不跨客户缓存或自动重试。未实测端到端耗时，不保证模型或后端数秒返回，详见 [API 说明](docs/api.md#local-input-requirements--本地输入说明)。

Across all branches, finish the current question batch before merging answers and obtaining the next batch; do not call MCP or validation for each answer. Resolve package/sample/source branches before their dependent fields, then validate completed data and ask only for repairs. Reuse valid JWTs, place no requests between Biointron Account and App Key questions, and insert no plans, recaps, discovery, bridge processes, reconnects or rule rereads between questions. Load `order_design(phase="execute", language=language)` once before execution; default `detail="compact"` supplies concise rules and connection information, while `detail="full"` retains complete references for specific diagnostics. The actual design adapter counts workbook rows once on a best-effort basis rather than on every MCP/CLI question; transport and business checks remain. Catalog search uses one call-local HTTP client to read one page, then up to four known pages concurrently, awaiting all reads and merging in order with unchanged five-page/50-record, deduplication, byte-cap and failure-continuation rules. No cross-customer cache or automatic retry is added. No end-to-end timing was measured or few-second model/backend response guaranteed; see [API details](docs/api.md#local-input-requirements--本地输入说明).

套餐开场不认证。选择产品库后使用本地输入工具的 `catalog_auth` 检查凭据：已有有效 JWT 直接复用，否则只补问缺失的 Biointron Account 和 App Key 并兑换；不用先加载完整执行提示词。再以原生文本弹窗或 CLI 输入关键词，调用 `search_order_antigens(keyword, business_token, page_no=1, page_size=50)`，每次最多合并5页并去重，展示 `catalog_summary`；`has_more` 时提供继续加载选项并按 `next_page` 继续，同时支持换词。产品数和规格数分别显示，未完成不能声称全部已加载。选中后保留返回的 `cart_data`；不询问供应商或补链接。其他来源仍在提交设计前认证。

Keep package selection first. Our library branch uses the local input response's `catalog_auth` to reuse a valid JWT or obtain missing Biointron Account/App Key values, without loading the full execution prompt. Ask for a keyword through a native text dialog or CLI, call `search_order_antigens`, and show real catalog numbers/specifications with pagination or another keyword when empty. Reuse the selected `cart_data`; do not request a supplier or missing link. Other source modes authenticate before design submission.

新增只读工具 `get_order_design_result(business_token, order_no="", continuation_token="", workflow_context=None, language="zh")`。确认 `result_saved` 后、收集购物车资料或加入购物车前，用会话语言实际询问是否查看 HTML 设计结果。选择查看才使用原完整签名上下文和同一 JWT 读取本次设计：`GET /order/rushData/report?rushDataServiceId=<签名中的服务 ID>` 直接返回后台 ZIP 中的 `report.html` 内容，客户端不接收或解压 ZIP。按返回 `filename` 将 `html` 以 `utf-8-sig` 保存，交付可点击文件或预览后继续原授权流程；选择跳过则不读取或渲染。失败时让客户选择重试或继续，只有读取失败才重发请求，保存或交付失败复用已返回 HTML。不自动重试或重新设计，两种查看选择都不替代最终提交确认。实验报告 `/inspectionReportHtml` 和 `get_report_results` 不用于此步骤。

The new read-only `get_order_design_result` uses the original signed context and exact JWT to return the saved design's actual HTML. After verified saving and before collecting cart fields or adding to cart, ask the selected-language view-or-skip question through a native card or interactive CLI. The report endpoint directly returns HTML extracted by the backend from its result ZIP; the client does not receive or unzip a ZIP. Save the returned `html` under `filename` with `utf-8-sig`, deliver a clickable file or preview, then resume the authorized cart flow. Skip performs no result read or rendering. On failure, ask retry or continue; repeat the GET only for a read failure, reusing returned HTML for local save/delivery failures. Preserve context and credentials, never redesign or automatically retry, and retain final-submit confirmation. Experimental report endpoints are separate.

独立 CLI 的交互式流程在保存设计后提问；非交互 `run(args, business_token)` 必须在设计写入前显式给出 `--design-result view` 或 `--design-result skip`，缺少选择即停止，且请求仍需预先提供顶层 `cart_data`。`--design-result-dir` 可指定 HTML 目录，`--report` 仍是 JSON 执行结果。设计保存及查看步骤完成后，再补齐并校验购物车资料；`projectNo` 以真实已保存订单详情为准。

Interactive CLI asks after design saving. Noninteractive `run(args, business_token)` requires an explicit `--design-result view` or `--design-result skip` before any design write, plus pre-supplied top-level `cart_data`. Missing choice stops execution. `--design-result-dir` selects the local HTML directory; `--report` remains a JSON workflow outcome. Complete the saved-design viewing step before cart collection and validation, using the real project number from saved-order details.

最终提交前须取得权威报价，并由客户确认准确订单、报价/折扣及 PO、真实公司资料已具备；未知条件需人工核实，`hasCompany` 或 `canSubmit` 不代表 PO 已验证。`submit_verified_order` 重新报价后提交选定订单，等待百英人工确认。提交受理、购物车同步分别反馈；受理不表示付款、确认生产、实验完成或结果已可用，生产仅在百英确认后开始。

Before final submission, obtain an authoritative quote and the customer's confirmation of the exact orders, quote/discount, and readiness of PO and real company information. Unknown prerequisites need human verification; `hasCompany` and `canSubmit` do not verify PO validity. `submit_verified_order` requotes and submits the selection for Biointron's human confirmation. Report acceptance and cart synchronization separately; acceptance is not payment, production confirmation, experimental completion, or available results. Production begins only after Biointron's confirmation.

## 两个 Skill 的名称与使用边界

维护者已将两个 Skill 放入 `skills/order_design` 和 `skills/auto_html_report`，参考文件已随包提供。订单 Skill 元数据名称为 `order-design`，MCP 提示词为 `order_design`；报告 Skill 元数据名称为 `auto-html-report`，文件夹、MCP 提示词和资源标识继续使用 `auto_html_report`。不要因 Skill 名称使用连字符而改动现有目录或提示词标识。

报告 Skill 支持直接从已有实验结果 JSON 在本地生成独立 HTML，包括完整 Data Summary、样本对比图、SPR/BLI 动力学图及实际提供的实验图片；此路径无需凭据、MCP 连接或订单 Skill。只有订单号时，必须先有结果数据：用户授权查询后，以已确认订单号和当前客户 JWT 调用 `get_report_results(query={"orderNo": "<order-number>"}, business_token=<JWT>, language=<interaction-language>)`，检查 HTTP、业务状态与真实结果后再生成。工具交互语言为 `zh`/`en`，与报告语言分开；加载 `auto_html_report` 提示词本身不查询结果或读取图片。

无 JWT 时，复用已有账号/App Key，只按顺序单独补问缺失的 Biointron Account、App Key；由客户端按服务元数据中的 `client_side_exchange.url` POST `username`/`appkey`，核实 HTTP 2xx、数值 `code=200`、`success=true` 和非空 `result.token` 后使用该 JWT。已有有效 JWT 直接复用。优先使用现有连接元数据，只有缺少时才调用 `order_design(phase="execute", detail="compact", language=<interaction-language>)` 获取 `connection_config`；报告准备不能使用默认 `start` 阶段或启动下单。独立客户端使用已有配置，缺配置由维护方处理；不在公开文档写固定认证地址，也不让客户猜 JWT 或 API 地址。真实凭据只留调用上下文，不写入报告、文档或仓库；失败不自动重试。

订单附带 Python 脚本仍依赖源项目的 `config.order_design`、`skill.order_design` 包结构及第三方依赖，不能将本公开包当作独立业务程序或安装器；常规订单流程通过托管 MCP 使用。报告 Skill 是由 Agent 执行的指令与字段说明，随包提供不代表已经在本地或云端验证所有业务。详细边界见 [API 说明](docs/api.md) 和 [Skill 目录](skills/README.md)。本轮只更新 GitHub 文档，未部署 FC、未调用真实业务服务。

## 发布时补齐

| 内容 | 修改位置 |
| --- | --- |
| 账号 / API Key 获取链接 | `docs/installation.md` 的接入信息段落；未确认前使用百英对接人入口。 |
| 支持渠道 | 在线平台已加入首页；专用支持地址确认后补入导航和安装文档。 |
| 订单辅助脚本的独立运行支持（可选） | 当前按托管 MCP 方式使用；若需独立运行 `check.py`，还需提供源项目服务配置、正确包结构及依赖说明；产品库查询前或其他分支提交设计前，以普通文本逐项补齐 Biointron Account 和 App Key 后兑换 JWT；普通资料连续完成当前批次后才统一校验，不逐字段调用 MCP；修正也按批次完成，`--auth jwt` 可隐藏输入已有 JWT；自动化用非交互 `run(args, business_token)`，不读取固定环境凭据。 |
| 版权主体 | 由权利人确认准确公司或个人名称后另加版权声明；不修改标准许可条款。 |

公开仓库 URL 已确定为 [https://github.com/Biointron/Biointron_OS_skill](https://github.com/Biointron/Biointron_OS_skill)。内部导航继续使用可移植相对链接，便于本地查看与复制；没有伪造下载量、Stars、在线服务状态或一键安装命令。

## GitHub 的 About 栏

建议 Description：

```text
Two Biointron Skills: guided RushData ordering with human confirmation and multilingual HTML reports from result JSON. MCP support · Beta · Noncommercial use.
```

建议 Topics：

```text
biointron mcp model-context-protocol agent-skills ai-agents research-workflow noncommercial
```

Website 可填写 `https://ai.biointron.com/#/landing`。首页徽章通过 shields.io 展示，点击目标均为本地文档。

## 非商业许可证

已按“不允许商用”要求使用 PolyForm Noncommercial 1.0.0，许可证原文来自 [PolyForm 官方下载](https://polyformproject.org/licenses/noncommercial/1.0.0.txt)。该许可证对非商业组织和个人用途有自己的明确定义，适用范围见 [许可证说明](docs/license.md)。页面统一写为“非商业使用 / source-available”，不标为允许商用的 MIT 或 Apache-2.0。

## 预览与检查

在本目录运行（需要 Python 3.11+）：

```sh
python scripts/check_docs.py
python -m unittest discover -s scripts -p "test_*.py"
```

可选网页预览：

```sh
python -m pip install Markdown
python scripts/build_preview.py
```

用浏览器打开生成的 `preview/README.html`（英文）或 `preview/docs/readme/README.zh-CN.html`（简体中文）。这是从同一份 Markdown 生成的静态预览，实际效果以 GitHub 渲染为准。`preview/` 已忽略，无需上传。

只上传本目录中的公开资料与已加入的两个 Skill 文件夹；不要把整个后端项目上传。环境配置、凭据、客户数据和会议纪要不属于本展示包。`preview/` 和各层 `__pycache__/` 是本地生成文件，已通过 `.gitignore` 排除。

本轮未创建或推送远端仓库、未部署服务，也未执行 `git commit`。

当前采用 AI 原样携带签名 `workflow_context`，无 Redis 运行依赖。压缩/交接时保留完整对象，JWT 使用安全引用；结束工具仅指导丢弃本地上下文，不撤销签名或取消订单。只有订单号不能恢复丢失凭证，详见 [API 状态说明](docs/api.md#temporary-workflow-state--临时工作流状态)。
