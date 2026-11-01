# MCP tool catalog / MCP 工具目录

[Home](../README.md) · [中文首页](readme/README.zh-CN.md) · [Installation / 安装](installation.md) · [API notes / API 说明](api.md)

Biointron OS is a **Beta / Playground** integration. This catalog covers seven business tools for RushData orders and reports. The MCP service is deployed on Alibaba Cloud FC; tool discovery and the resources and prompts for both Skills were verified on 2026-11-01. Full business workflows still require live validation. The connected server's returned tool schemas are the authority for that deployment.

Biointron OS 当前为 **Beta / Playground** 接入版本。本目录展示 RushData 订单与报告相关的七个业务工具。MCP 已部署到阿里云 FC，工具发现及两个 Skill 的资源、提示词已于 2026-11-01 通过云端验证；完整业务流程仍需真实联调。实际部署的参数以连接后返回的工具 schema 为准。

This tool-list update must be published to the existing cloud service, then refreshed in the client. The earlier cloud verification does not confirm that this later update is already live.

本次工具清单调整需同步更新已部署的云端服务，再刷新客户端；此前的云端验证不表示本次调整已经发布。

## Tools / 工具

| Tool | Required input / 必填输入 | Purpose / 用途 | Effect / 操作类型 | Integration status / 接入状态 |
| --- | --- | --- | --- | --- |
| `order_design_preflight` | None / 无 | Check company eligibility and available test items / 检查公司资格及可用检测项目 | Read-only / 只读 | Registered / 已注册 |
| `start_order_design` | `data: object`, `file_base64: string`, `filename: string` | Submit the supplied XLSX and wait for confirmed design storage / 提交客户 XLSX 并等待设计保存确认 | Writes business data / 写入 | Registered / 已注册 |
| `add_order_to_cart` | `continuation_token: string` | Add a confirmed saved design to the cart / 将已确认保存的设计加入购物车 | Writes business data / 写入 | Registered / 已注册 |
| `get_order_cart` | Optional `page_no: integer`, default `1` / 可选页码，默认 `1` | Read one page of the order cart / 分页查询订单购物车 | Read-only / 只读 | Registered / 已注册 |
| `calculate_order_price` | `order_nos: string[]` | Get a quote for selected orders / 获取指定订单的报价 | Read-only / 只读 | Registered / 已注册 |
| `submit_verified_order` | `order_nos: string[]` | Recheck the quote, submit selected orders and verify cart state / 重新核验报价、提交选定订单并检查购物车状态 | Writes business data / 写入 | Registered / 已注册 |
| `get_report_results` | `query: object` with string, integer, number, or boolean values / 值为字符串、整数、数值或布尔值的对象 | Retrieve existing report JSON / 查询已有报告 JSON | Read-only / 只读 | Registered; report endpoint and query contract required / 已注册，需配置报告接口并确认查询契约 |

Load the `order_design` prompt before using the order tools. Supply the customer's original XLSX as standard Base64, with its filename; the original file must be nonempty and no larger than 10 MiB. Use the `continuation_token` returned after confirmed storage to add that design to the cart. For report retrieval, call `get_report_results` with the actual order number in `query.orderNo`. Once result JSON is available, use the `auto_html_report` Skill or prompt if an HTML report is requested. Business fields must follow the corresponding Skill references and confirmed service contract.

订单工具使用前先加载 `order_design` 提示词。客户原始 XLSX 以标准 Base64 和文件名传入；原文件须非空且不超过 10 MiB。设计确认保存后，用返回的 `continuation_token` 将该设计加入购物车。报告查询通过 `get_report_results` 完成，将实际订单号填入 `query.orderNo`；取得结果 JSON 后，如需 HTML 报告，再使用 `auto_html_report` Skill 或提示词。业务字段遵循对应 Skill 参考和已确认的服务契约。

## Discover tools / 获取工具列表

After the MCP client has completed initialization and sent `notifications/initialized`, it can send the illustrative [tools/list request](../examples/tools-list.request.json). Let the client handle the negotiated protocol version and HTTP transport headers. This JSON is a request body, not a complete connection configuration.

MCP 客户端完成初始化并发送 `notifications/initialized` 后，可发送 [tools/list 请求示例](../examples/tools-list.request.json)。协议版本协商和 HTTP 请求头由客户端处理；此 JSON 仅为请求体，不是完整连接配置。

Inspect the returned schemas before invoking tools. Listing tools does not create an order. Design submission, adding to the cart and submitting selected orders change business data; invoke them only within the user's authorized scope. If a write result is uncertain, retain known identifiers and check the existing state before any further write.

调用前查看实际返回的 schema。列出工具不会创建订单；设计提交、加入购物车和提交选定订单会修改业务数据，只能在用户授权范围内使用。写操作结果不确定时，保留已知标识，先核查已有状态再继续写入。

## Results / 返回结果

`get_report_results` returns a wrapper with `http_status` and `data`. See the [illustrative adapter result](../examples/tool-result.example.json) and [API notes](api.md). Order tools return stage-specific status and identity fields; confirmed design storage also returns `continuation_token`. HTTP success alone does not establish business success, experiment completion, or report availability.

`get_report_results` 返回包含 `http_status` 与 `data` 的包装对象，见 [适配器返回示例](../examples/tool-result.example.json) 和 [API 说明](api.md)。订单工具按阶段返回状态和身份字段；设计确认保存后还会返回 `continuation_token`。HTTP 成功不能单独证明业务成功、实验完成或报告可用。

## Skills and availability / Skill 与可用性

This code version provides `order_design` and `auto_html_report` prompts, plus the Skill and reference resources for each workflow. Publish this naming update to the existing cloud service before refreshing clients. The local folders are included at [order_design](../skills/order_design/SKILL.md) (Skill name: `order-design`) and [auto_html_report](../skills/auto_html_report/SKILL.md). Installing a local Skill does not configure a business endpoint or prove the matching workflow works. See the [Skill directory](../skills/README.md) for package contents and dependencies.

本版代码提供 `order_design`、`auto_html_report` 两个提示词，以及每个流程对应的 Skill 和参考资源。本次名称更新需同步到已有云端服务，再刷新客户端。本地包已包含在 [order_design](../skills/order_design/SKILL.md)（Skill 名称为 `order-design`）和 [auto_html_report](../skills/auto_html_report/SKILL.md) 文件夹中。本地安装 Skill 不会自动完成业务接口配置，也不能证明对应流程已跑通。文件组成与依赖见 [Skill 目录](../skills/README.md)。
