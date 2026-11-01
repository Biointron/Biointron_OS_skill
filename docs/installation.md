# Installation / 安装指南

[Home](../README.md) · [中文首页](readme/README.zh-CN.md) · [Tools / 工具](tool-catalog.md) · [Skills](../skills/README.md)

## Before you start / 开始之前

The MCP service and Skill packages are separate. Both Skills are included in this repository. Order Design needs a supported MCP client and service access; HTML Report needs supplied result JSON and an agent that can create HTML files. Reporting from an existing local JSON file does not require MCP access.

MCP 连接与 Skill 安装是两件事，两个 Skill 均已包含在仓库中。订单设计需要支持 MCP 的客户端和服务权限；HTML 报告需要已有结果 JSON，以及能够生成 HTML 文件的 Agent。已有本地 JSON 时，生成报告无需 MCP 权限。

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
| [`auto_html_report`](../skills/auto_html_report/SKILL.md) | `skills/auto_html_report/` | Actual result JSON and an agent that can generate HTML and charts / 真实结果 JSON，以及能生成 HTML 和图表的 Agent。 |

| Client / 客户端 | Project scope / 当前项目 | Personal scope / 当前用户 |
| --- | --- | --- |
| Codex | `.agents/skills/<skill-folder>/SKILL.md` | `~/.agents/skills/<skill-folder>/SKILL.md` |
| Claude Code | `.claude/skills/<skill-folder>/SKILL.md` | `~/.claude/skills/<skill-folder>/SKILL.md` |

`<skill-folder>` is `order_design` or `auto_html_report`; `~` means your user home directory. Choose one scope and copy the entire folder there. Review any existing installation before replacing it. Follow the package's dependency and configuration instructions, then reopen the client or a session and check its available Skills.

`<skill-folder>` 为 `order_design` 或 `auto_html_report`，`~` 指当前用户主目录。选择一种范围并复制整个文件夹；已有同名安装时先核对版本。按包内说明配置依赖和服务连接，重新打开客户端或会话，再确认 Skill 是否可见。

References / 依据：[Official Codex Skills documentation](https://developers.openai.com/codex/skills) · [Claude Code Skills documentation](https://code.claude.com/docs/en/skills).

### Requirements by Skill / 各 Skill 的使用要求

**Order Design:** connect MCP first and confirm that the order tools are available to your account. Normal use follows `SKILL.md` through those tools. Its bundled Python helpers depend on the source project's `config.order_design` and `skill.order_design` package layout, plus `httpx`; that configuration and package layout are not included here. Copying the Skill folder does not make those helpers standalone programs. See the [Skill catalog](../skills/README.md) for details.

**订单设计：**先连接 MCP，确认账号已开放对应订单工具；正常使用按 `SKILL.md` 通过工具执行。附带 Python 辅助脚本依赖源项目的 `config.order_design`、`skill.order_design` 包结构和 `httpx`，本目录未附带对应项目配置及包结构。复制 Skill 文件夹不会使这些脚本变成独立程序，详见 [Skill 目录](../skills/README.md)。

**HTML Report:** provide actual result JSON, optionally with a report language, branding and associated images. Keep `references/result-schema.md` with the Skill. The package supplies instructions and a schema reference, not a standalone report generator; your agent creates the HTML and charts. An order number alone is insufficient. Fetch results separately with `get_report_results` when needed, then supply the returned result JSON to this Skill.

**HTML 报告：**提供真实结果 JSON，可选提供报告语言、品牌信息及对应图片；保留随包的 `references/result-schema.md`。此包提供规则和结构参考，HTML 与图表由 Agent 生成，不附带独立报告生成器。只有订单号不足以生成报告；需要查询时先通过 `get_report_results` 获取结果，再交给此 Skill。

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

For a local report, attach the result JSON and ask: "Use auto_html_report to create an English HTML report from this JSON, with the complete Data Summary, charts and available images."

生成本地报告时，附上结果 JSON 并提出：“请使用 auto_html_report，将这份 JSON 生成为英文 HTML 报告，保留完整数据汇总、图表和可用图片。”

Only proceed with a business workflow within the user's authorization and the Skill's requirements. Installing instructions does not grant API access, install missing private modules, or verify a deployed service.

在用户授权和 Skill 的使用要求范围内继续业务操作。安装规则本身不会授予 API 权限、补齐内部模块或验证线上服务。

## Troubleshooting / 常见问题

| Symptom / 现象 | Check / 检查方向 |
| --- | --- |
| Cannot connect / 无法连接 | Verify the issued URL and Streamable HTTP support / 核对实际地址和协议支持。 |
| `401` | Check the token and client-process environment / 核对令牌及客户端进程环境。 |
| Tools appear but calls fail / 有工具但调用失败 | Read the returned Beta status and confirm backend availability / 查看实际错误，确认后端接入状态。 |
| Skill is missing / Skill 不可见 | Check the directory, `SKILL.md` and client reload / 核对目录、文件名及客户端是否重新加载。 |
| Missing module or reference / 缺少模块或引用文件 | Check package completeness with the maintainer / 联系维护者确认发布包完整性。 |
| Write timed out / 写操作超时 | Check the existing business state before another submission / 先核查已有业务状态再决定后续操作。 |

For access problems, contact the Biointron representative who supplied your account. Share sanitized errors and the last confirmed step; do not post credentials or customer data in public issues.

权限问题请联系提供账号的百英对接人，提供脱敏错误和最后确认的步骤；不要在公开 Issue 中贴凭据或客户数据。
