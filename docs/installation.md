# Installation / 安装指南

[Home](../README.md) · [中文首页](readme/README.zh-CN.md) · [Tools / 工具](tool-catalog.md) · [Skills](../skills/README.md)

## Before you start / 开始之前

The MCP service and Skill packages are separate. Both Skills are included in this repository. Order Design uses a supported MCP client for business operations. HTML Report generates reports from actual result JSON; it can use an existing file or, with authorization and the current customer's JWT, retrieve the results first. Generating HTML from supplied JSON needs no credentials or MCP connection.

MCP 连接与 Skill 安装是两件事，两个 Skill 均已包含在仓库中。订单 Skill 通过支持 MCP 的客户端执行业务操作；报告 Skill 根据真实结果 JSON 生成报告，可以使用已有文件，也可在授权范围内用当前客户 JWT 先查询结果。已有 JSON 时，生成 HTML 无需凭据或 MCP 连接。

<a id="mcp"></a>

## Connect MCP / 连接 MCP

### Access / 获取接入信息

Use the Beta MCP address below. Ask your Biointron contact for a service access token and the capabilities enabled for your account. Account-registration and self-service API-key links have not yet been published here.

使用下方 Beta MCP 地址，并向百英对接人获取 MCP 服务访问令牌和账号可用能力。本资料尚未公布账号注册或自助 API Key 获取链接。

| Setting / 配置项 | Value / 值 |
| --- | --- |
| Name / 名称 | `BiointronOS_MCP` |
| Transport / 传输 | Streamable HTTP |
| URL / 地址 | `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp` |
| Header / 请求头 | `Authorization: Bearer <MCP_ACCESS_TOKEN>` |

A client must support Streamable HTTP and the configured authorization header. OAuth-only connections are not automatically compatible. Keep the MCP service token separate from any business API token. See [API notes](api.md).

客户端需要支持 Streamable HTTP 和对应认证头，仅支持 OAuth 的连接不能直接视为兼容。MCP 服务令牌与业务 API 凭据彼此独立，详见 [API 说明](api.md)。

### Business calls / 业务调用

The connection header above remains unchanged. Once connected, supply the current customer's raw JWT as `business_token` on each of the ten customer-related report/order/workflow tools. The local `get_order_input_requirements` tool needs no business JWT. Do not add `Bearer`, put the JWT inside `query`/`data`, or place it in the MCP connection configuration. Missing tokens do not fall back to a server credential or the previous customer. Do not echo tokens in replies or reports; client tool history may retain arguments. Refresh the tool schemas after the service update. See the [tool catalog](tool-catalog.md).

上面的 MCP 入口认证头保持不变。连接后，十个客户相关的报告、下单及流程工具每次都需在独立参数 `business_token` 中传入当前客户的原始 JWT；本地工具 `get_order_input_requirements` 无需业务 JWT。不加 `Bearer`，不放进 `query`/`data` 或 MCP 连接配置。缺少时不会回退到服务器固定凭据或上一客户的 Token；不要在普通回复或报告中回显，客户端可能保存工具调用历史。服务更新后刷新工具 schema，详见[工具目录](tool-catalog.md)。

### Conversation language / 会话语言

Pass `language="en"` or `language="zh"` on each order tool call and `order_design` prompt according to the customer's natural-language instructions; do not put it in the connection configuration or business payload. Keep it through keywords, SKUs, credentials and paths until the customer changes language. All customer-facing order text uses that language. Omitted language defaults to `zh` for older callers; the source project's CLI accepts `--language en`/`--language zh`. See [language handling](api.md#conversation-language--会话语言).

按客户自然语言指令在每次下单工具和 `order_design` 提示词中传入 `language="zh"` 或 `language="en"`，不写入连接配置或业务资料。关键词、货号、凭据和路径不改变语言；套餐、提问、选项、说明、错误与等待消息均沿用会话语言。省略时默认 `zh` 兼容旧调用，源项目 CLI 使用 `--language zh`/`--language en`。

### JSON configuration / JSON 配置

For clients that support this `mcpServers` configuration format, merge the following connection into the existing configuration. Replace `<MCP_ACCESS_TOKEN>` with your issued token only in your local client settings. Keep existing connections and never commit the real token. The downloadable example is [mcp-servers.example.json](../examples/mcp-servers.example.json).

如果客户端支持以下 `mcpServers` 配置格式，可将此连接合并到已有配置。在本地客户端设置中将 `<MCP_ACCESS_TOKEN>` 替换为已获得的令牌，保留其他连接，不要把真实令牌提交到仓库。可下载 [mcp-servers.example.json](../examples/mcp-servers.example.json)。

```json
{
  "mcpServers": {
    "BiointronOS_MCP": {
      "url": "https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp",
      "headers": {
        "Authorization": "Bearer <MCP_ACCESS_TOKEN>",
        "START_MCP_TIMEOUT_MS": "60000",
        "RUN_MCP_TIMEOUT_MS": "660000"
      }
    }
  }
}
```

`BiointronOS_MCP` is a configurable connection name, not a tool identifier. The Codex example below uses `biointron` as its connection name. This JSON format is client-specific; it is not a configuration format guaranteed by the MCP protocol.

`BiointronOS_MCP` 是可自定义的连接名称，不是工具标识。下方 Codex 示例使用 `biointron` 作为连接名称。此 JSON 属于客户端配置格式，MCP 协议不保证所有客户端都支持它。

The two timeout-named headers are retained from the supplied configuration as **custom client/service fields**, not standard MCP timeout settings. `60000` milliseconds equals **60 seconds**; `660000` milliseconds equals **11 minutes**. Putting these values in `headers` alone does not guarantee a change to the client's waiting time. Configure actual startup and operation timeouts according to your client's documentation; a client or service must explicitly support these custom fields for them to have an effect. See the [official MCP transport specification](https://modelcontextprotocol.io/specification/latest/basic/transports).

两个带有 timeout 名称的请求头按提供的配置保留，属于**客户端或服务的自定义项**，不是 MCP 标准超时配置。`60000` 毫秒为 **60 秒**，`660000` 毫秒为 **11 分钟**。仅放在 `headers` 中不能保证改变客户端等待时间；实际启动和操作超时应按客户端文档配置，这些自定义字段也需要客户端或服务明确支持才会生效。参见 [MCP 官方传输规范](https://modelcontextprotocol.io/specification/latest/basic/transports)。

### Codex

Merge the following table into your existing `~/.codex/config.toml`; do not replace the entire file. It uses the same service address as the JSON example. A downloadable example is in [codex-mcp.example.toml](../examples/codex-mcp.example.toml).

将以下配置节合并到现有 `~/.codex/config.toml`，不要覆盖整份配置。服务地址与上方 JSON 示例一致：

```toml
[mcp_servers.biointron]
url = "https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp"
bearer_token_env_var = "BIOINTRON_MCP_TOKEN"
```

Set `BIOINTRON_MCP_TOKEN` in the environment of the process that launches Codex. The variable's value must be the issued MCP access token. Restart Codex from that environment, then check its MCP connection status. Setting a variable in an unrelated terminal does not update an already running desktop app.

在启动 Codex 的进程环境中设置 `BIOINTRON_MCP_TOKEN`，值为已获得的 MCP 访问令牌，然后从该环境重启 Codex 并检查 MCP 状态。单独在另一个终端设置变量，不会更新已运行的桌面应用。不要将真实令牌写入仓库。

Reference / 依据：[Official Codex MCP documentation](https://developers.openai.com/codex/mcp).

### Other MCP clients / 其他客户端

Use the connection fields above in your client's remote MCP settings. Configuration formats differ: do not assume one JSON file works in every client. If the client cannot supply the required header, use a supported client or ask the provider for an alternative authentication option.

在客户端远程 MCP 设置中填写上表信息。各客户端配置格式不同，不能把某个 JSON 当作通用安装文件。若无法提供所需认证头，请改用支持的客户端或向服务方确认其他认证方式。

<a id="skills"></a>

## Install Skills / 安装 Skills

### Choose a package / 选择发布包

Check the [Skills catalog](../skills/README.md). Download the repository ZIP or obtain the selected Skill's complete folder from `skills/`. Keep `SKILL.md`, `references/`, any scripts and required assets together. A link to `SKILL.md` alone does not install its dependencies.

先查看 [Skills 目录](../skills/README.md)。下载仓库 ZIP，或取得 `skills/` 下指定 Skill 的完整文件夹。保留 `SKILL.md`、`references/`、脚本及其必需资源；只复制一个 `SKILL.md` 地址不会安装全部依赖。

| Skill name / 名称 | Folder to copy / 复制的文件夹 | Required input or connection / 使用前提 |
| --- | --- | --- |
| [`order-design`](../skills/order_design/SKILL.md) | `skills/order_design/` | Authorized MCP order tools and customer-supplied project inputs / 已授权的 MCP 订单工具及客户提供的项目资料。 |
| [`auto-html-report`](../skills/auto_html_report/SKILL.md) | `skills/auto_html_report/` | Actual JSON, or an authorized result query followed by generation; an agent that can create HTML and charts / 真实 JSON，或先授权查询再生成；Agent 需能生成 HTML 和图表。 |

| Client / 客户端 | Project scope / 当前项目 | Personal scope / 当前用户 |
| --- | --- | --- |
| Codex | `.agents/skills/<skill-folder>/SKILL.md` | `~/.agents/skills/<skill-folder>/SKILL.md` |
| Claude Code | `.claude/skills/<skill-folder>/SKILL.md` | `~/.claude/skills/<skill-folder>/SKILL.md` |

`<skill-folder>` is `order_design` or `auto_html_report`; `~` means your user home directory. Choose one scope and copy the entire folder there. Review any existing installation before replacing it. Follow the package's dependency and configuration instructions, then reopen the client or a session and check its available Skills.

`<skill-folder>` 为 `order_design` 或 `auto_html_report`，`~` 指当前用户主目录。选择一种范围并复制整个文件夹；已有同名安装时先核对版本。按包内说明配置依赖和服务连接，重新打开客户端或会话，再确认 Skill 是否可见。

References / 依据：[Official Codex Skills documentation](https://developers.openai.com/codex/skills) · [Claude Code Skills documentation](https://code.claude.com/docs/en/skills).

The report Skill's declared name is `auto-html-report`; its repository folder and MCP prompt are still named `auto_html_report`. Use the declared name to request the local Skill, and keep the existing folder and MCP identifiers when installing or calling tools.

报告 Skill 声明名称为 `auto-html-report`，仓库文件夹及 MCP 提示词仍为 `auto_html_report`。调用本地 Skill 时使用声明名称，安装目录和 MCP 调用标识保留原名称。

### Install with an AI assistant / 让 AI 帮你安装

In an AI tool that supports local Skill installation, send the following instruction. It points to the [public repository](https://github.com/Biointron/Biointron_OS_skill); the assistant should use the current client's supported installation method and report whether a restart or additional setup is required.

在支持本地 Skill 安装的 AI 工具中发送以下指令。指令引用[公开仓库](https://github.com/Biointron/Biointron_OS_skill)，由 AI 按当前客户端支持的方式安装，并说明是否需要重启或额外配置。

```text
Please follow the installation instructions in https://github.com/Biointron/Biointron_OS_skill to install both Skills from skills/order_design and skills/auto_html_report for the AI tool I am currently using. Include all reference files and supporting scripts, preserve my existing configuration, and verify that both Skills are recognized after installation. Then explain how to use them and identify any additional setup required.
```

```text
请阅读 https://github.com/Biointron/Biointron_OS_skill 的安装说明，为当前 AI 工具安装 skills/order_design 和 skills/auto_html_report 两个 Skill，完整保留参考文件、配套脚本及已有配置，安装后确认是否加载成功，并说明如何使用及是否需要额外配置。
```

### Requirements by Skill / 各 Skill 的使用要求

**Order Design:** connect MCP for tool use. Package introductions and local batch collection need no business JWT; product-library queries and business operations need the current customer's JWT. Validate completed design/cart input before writing. After verified saving, the customer can choose whether to view the actual design HTML. Selected orders are submitted for human confirmation, not immediate production. The bundled Python helpers still require the source project's configuration, package layout and dependencies; copying the folder does not make them standalone programs. See the [Skill catalog](../skills/README.md).

**订单设计：**调用工具时连接 MCP。套餐介绍和本地分批收集无需业务 JWT，产品库查询与业务操作需要当前客户 JWT；设计或购物车写入前统一校验完整资料。核实设计已保存后，由客户选择是否查看实际设计 HTML。选单提交用于人工确认，不代表立即投产。附带 Python 辅助脚本仍需要源项目配置、包结构和依赖，复制文件夹不会使其成为独立程序，详见 [Skill 目录](../skills/README.md)。

**HTML Report:** provide actual JSON, optionally with a report language, branding and associated images. The agent creates a standalone HTML file using `SKILL.md` and `references/result-schema.md`. No credentials or MCP are needed for supplied JSON. If results must be fetched and the query is authorized, use `get_report_results(query={"orderNo": "<order-number>"}, business_token=<JWT>, language=<zh-or-en>)` first. Reuse a valid JWT; otherwise collect only missing **Biointron Account** and **App Key** values separately, and exchange them using server-provided connection metadata. The App Key is not `business_token`. When connection information is missing, an available `order_design(phase="execute", detail="compact", language=<zh-or-en>)` prompt is used solely to obtain that information, without starting an order. Query language (`zh`/`en`) is separate from the requested report language; reports default to English and support other requested languages. The Skill package itself is written in English.

**HTML 报告：**提供真实 JSON，可选提供报告语言、品牌信息及对应图片；Agent 按 `SKILL.md` 和 `references/result-schema.md` 生成独立 HTML。已有 JSON 时无需凭据或 MCP；缺少结果且已获查询授权时，先调用 `get_report_results(query={"orderNo": "<order-number>"}, business_token=<JWT>, language=<zh-or-en>)`。优先复用有效 JWT，否则分别补齐缺少的 **Biointron Account** 与 **App Key**，按服务端连接元数据兑换；App Key 不能直接作为 `business_token`。缺少连接信息时，可用的 `order_design(phase="execute", detail="compact", language=<zh-or-en>)` 提示词仅用于读取连接信息，不启动下单。查询交互语言（`zh`/`en`）与报告语言独立，报告默认英文并支持其他所需语言；Skill 包本身使用英文编写。

### First use / 首次使用

```text
Show me the Biointron Skills and MCP tools available in this session.
Explain the required inputs and which steps change business data.
Do not create, modify or submit an order yet.
```

```text
请列出本会话可用的 Biointron Skills 和 MCP 工具。
说明各流程需要什么输入，哪些步骤会改动业务数据。
暂时不要创建、修改或提交订单。
```

For a local report, attach the result JSON and ask: "Use auto-html-report to create an English HTML report from this JSON, with the complete Data Summary, charts and available images."

生成本地报告时，附上结果 JSON 并提出：“请使用 auto-html-report，将这份 JSON 生成为英文 HTML 报告，保留完整数据汇总、图表和可用图片。”

Only proceed with a business workflow within the user's authorization and the Skill's requirements. Installing instructions does not grant API access, install missing private modules, or verify a deployed service.

在用户授权和 Skill 的使用要求范围内继续业务操作。安装规则本身不会授予 API 权限、补齐内部模块或验证线上服务。

## Troubleshooting / 常见问题

| Symptom / 现象 | Check / 检查方向 |
| --- | --- |
| Cannot connect / 无法连接 | Verify the issued URL and Streamable HTTP support / 核对实际地址和协议支持。 |
| `401` | Check the token and client-process environment / 核对令牌及客户端进程环境。 |
| Tools appear but calls fail / 有工具但调用失败 | Supply the required `business_token`, read the returned status and confirm API permissions / 提供必填 `business_token`，查看实际错误并确认业务权限。 |
| `reading 'find'`, undefined token variable, or a stopped script bridge / 临时连接脚本读取失败 | This is a client-side failure, not proof that the catalog API failed. Prefer native MCP tools; in the full project, use the Skill's single-call client helper. Check the error envelope before reading results and stop waiting when the process exits. / 这是客户端故障，不能据此判断产品库 API 失败。优先使用原生 MCP 工具；完整项目中使用 Skill 的单次调用入口。先检查错误，再读结果；进程退出后不继续空等。 |
| Skill is missing / Skill 不可见 | Check the directory, `SKILL.md` and client reload / 核对目录、文件名及客户端是否重新加载。 |
| Missing module or reference / 缺少模块或引用文件 | Check package completeness with the maintainer / 联系维护者确认发布包完整性。 |
| Write timed out / 写操作超时 | Check the existing business state before another submission / 先核查已有业务状态再决定后续操作。 |

For access problems, contact the Biointron representative who supplied your account. Share sanitized errors and the last confirmed step; do not post credentials or customer data in public issues.

权限问题请联系提供账号的百英对接人，提供脱敏错误和最后确认的步骤；不要在公开 Issue 中贴凭据或客户数据。
