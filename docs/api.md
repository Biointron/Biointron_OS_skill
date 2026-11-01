# API notes / API 说明

[Home](../README.md) · [中文首页](readme/README.zh-CN.md) · [Installation / 安装](installation.md) · [Tool catalog / 工具目录](tool-catalog.md)

## Connection / 连接

Biointron OS exposes its agent-facing tools through remote **MCP Streamable HTTP** at `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp`. Obtain access credentials from the service provider, then follow the [installation guide](installation.md). Account-registration and self-service API-key issuance links have not yet been published here. Documenting the address does not establish that all business operations are ready.

Biointron OS 通过远程 **MCP Streamable HTTP** 提供 Agent 工具，地址为 `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp`。请向服务提供方获取访问凭据，再按 [安装说明](installation.md) 配置。本资料尚未公布账号注册或自助 API Key 获取链接；提供服务地址不代表所有业务操作已就绪。

The reference service accepts `Authorization: Bearer <MCP_ACCESS_TOKEN>`. A client must support the configured authentication mechanism; a client that only supports OAuth cannot be assumed compatible with this static-token setup.

参考服务使用 `Authorization: Bearer <MCP_ACCESS_TOKEN>`。客户端须支持对应认证方式；仅支持 OAuth 的客户端不能直接视为兼容此静态令牌配置。

The [JSON connection example](../examples/mcp-servers.example.json) uses the configurable name `BiointronOS_MCP`. Its `mcpServers` structure must be supported by the client. `START_MCP_TIMEOUT_MS` and `RUN_MCP_TIMEOUT_MS` are custom client/service headers, not standard MCP timeout settings. Their example values are 60,000 milliseconds (60 seconds) and 660,000 milliseconds (11 minutes). Merely sending these headers does not guarantee that the client will wait that long; configure its actual timeouts according to the client's documentation. See the [MCP transport specification](https://modelcontextprotocol.io/specification/latest/basic/transports).

[JSON 连接示例](../examples/mcp-servers.example.json)使用可自定义的连接名 `BiointronOS_MCP`，客户端须支持其 `mcpServers` 结构。`START_MCP_TIMEOUT_MS` 和 `RUN_MCP_TIMEOUT_MS` 是客户端或服务的自定义请求头，不是 MCP 标准超时配置。示例分别为 60,000 毫秒（60 秒）和 660,000 毫秒（11 分钟）；仅发送这些头不能保证客户端等待相应时长，实际超时需按客户端文档配置。参见 [MCP 传输规范](https://modelcontextprotocol.io/specification/latest/basic/transports)。

## Credentials / 凭据

| Credential | Purpose / 用途 | Where configured / 配置位置 |
| --- | --- | --- |
| MCP access token / MCP 访问令牌 | Authenticate the client to the MCP service / 验证客户端对 MCP 的访问 | Client connection and MCP service / 客户端连接与 MCP 服务 |
| Business API credential / 业务 API 凭据 | Authenticate requests to upstream business APIs / 验证对后端业务 API 的访问 | Service-side configuration; a directly connected Skill follows its own setup / 服务端配置；直连业务 API 的 Skill 按自身说明配置 |

These are separate credentials. Do not reuse one as the other or place real values in tool arguments, documentation, examples, or repository files. The reference MCP service uses a shared service identity; it does not provide per-customer OAuth or tenant isolation.

这两类凭据彼此独立，不能互相替代，也不应把真实值放入工具参数、文档、示例或仓库文件。参考 MCP 服务使用共享服务身份，尚未提供按客户区分的 OAuth 或租户隔离。

## Business contracts / 业务契约

The [tool catalog](tool-catalog.md) documents the MCP entry points and their parameter containers. It does not define the upstream business API. A public, versioned contract is still needed for:

工具目录描述的是 MCP 入口及参数容器。后端业务 API 的以下内容仍需在正式公开、带版本的契约中提供：

- Required fields and identifiers / 必填字段与标识含义。
- Authentication, authorization, and account eligibility / 认证、授权及账户资格。
- Response fields, business success criteria, and error codes / 返回字段、业务成功判定和错误码。
- Order-state queries and recovery after an uncertain write / 订单状态查询及写入结果不确定时的核查方式。
- Report data definitions and file-access rules / 报告数据定义及文件访问规则。

An installation example cannot substitute for these definitions. The bundled Skills include an [order workflow reference](../skills/order_design/references/workflow.md) and a [report result schema](../skills/auto_html_report/references/result-schema.md). These describe the current Skills; they do not replace a versioned upstream API contract. See [installation requirements](installation.md#skills) for the MCP connection and the limits of the bundled Python helpers.

安装示例不能替代业务字段定义。两个 Skill 已随包提供[订单工作流参考](../skills/order_design/references/workflow.md)和[报告结果结构](../skills/auto_html_report/references/result-schema.md)，用于说明当前 Skill，并不替代带版本的后端 API 契约。MCP 连接要求及附带 Python 脚本的依赖限制见[安装说明](installation.md#skills)。

## Adapter result / 适配器返回

[tool-result.example.json](../examples/tool-result.example.json) illustrates the `get_report_results` adapter's wrapper:

| Field | Meaning / 含义 |
| --- | --- |
| `http_status` | Upstream HTTP status / 后端 HTTP 状态码 |
| `data` | Parsed upstream JSON, or `null` when the response body is empty / 解析后的后端 JSON；空响应体时为 `null` |

The sample deliberately uses `data: null` and contains no report schema. It demonstrates an empty upstream response, **not a successful business operation**. This is an application-level adapter result, not the full MCP `tools/call` result or a JSON-RPC response. An MCP client may expose it inside its tool-result content. Order tools return stage-specific status and identity fields; see the [tool catalog](tool-catalog.md).

示例使用 `data: null`，不包含报告 schema，表示后端响应体为空，**不表示业务执行成功**。它是 `get_report_results` 的应用层适配器结果，不是完整的 MCP `tools/call` 返回体或 JSON-RPC 响应；客户端可能将它呈现在工具返回内容中。订单工具按阶段返回状态和身份字段，详见[工具目录](tool-catalog.md)。

## Beta behavior / Beta 行为

An unconfigured endpoint is unavailable even when its tool is listed. Connection failures, HTTP errors, or invalid responses must be reported accurately. For write operations, a timeout can leave the actual business outcome uncertain: retain known identifiers and check the state before any repeat submission. Experimental availability is not a substitute for a confirmed result.

即使工具已经列出，未配置的业务接口仍不可用。连接失败、HTTP 错误及无效响应应如实说明。写请求超时可能使实际业务结果无法确认，应保留已知标识，核查状态后再决定是否重试，不能把测试状态解释为业务已成功。
