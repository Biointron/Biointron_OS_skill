<div align="center">

<p dir="ltr">
<a href="../../README.md" lang="en" dir="ltr">English</a> ·
<strong lang="zh-CN" dir="ltr">简体中文</strong> ·
<a href="README.zh-TW.md" lang="zh-TW" dir="ltr">繁體中文</a> ·
<a href="README.ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="README.ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="README.tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="README.ru.md" lang="ru" dir="ltr">Русский</a> ·
<a href="README.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="README.th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="README.de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="README.es.md" lang="es" dir="ltr">Español</a> ·
<a href="README.fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="README.uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="README.pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="README.pt-BR.md" lang="pt-BR" dir="ltr">Português (Brasil)</a> ·
<a href="README.fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="README.ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="README.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="README.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="README.el.md" lang="el" dir="ltr">Ελληνικά</a> ·
<a href="README.ml.md" lang="ml" dir="ltr">മലയാളം</a> ·
<a href="README.ur-Latn.md" lang="ur-Latn" dir="ltr">Roman Urdu</a> ·
<a href="README.ro.md" lang="ro" dir="ltr">Română</a>
</p>

# Biointron OS

### 让你的 AI Agent，连接百英服务。

从订单需求到结果获取，将百英服务融入你熟悉的 AI 工作方式。<br />
MCP 连接服务，Skills 引导流程，每一步由你掌握。

[![MCP 工具目录](https://img.shields.io/badge/MCP-tool_catalog-087F8C?style=flat-square)](../tool-catalog.md)
[![Skills](https://img.shields.io/badge/Agent-Skills-234E70?style=flat-square)](../../skills/README.md)
[![非商业许可证](https://img.shields.io/badge/License-Noncommercial-6B7280?style=flat-square)](../../LICENSE)
[![Beta Playground](https://img.shields.io/badge/Release-Beta_Playground-D7A345?style=flat-square)](#beta)

<br />

<!-- HERO: Keep the artwork path in sync across all language versions. -->
<img src="../../assets/biointron-os-hero.png" alt="Biointron OS" width="1000" />

<br />

**[快速开始](#get-started) · [MCP 工具](../tool-catalog.md) · [Skills](../../skills/README.md) · [API 与示例](../api.md) · [在线平台](#online-platform) · [常见问题](#faq)**

</div>

---

## 一个平台，三种连接方式。

Biointron OS 面向 AI Agent、模型与用户，提供连接百英服务的统一入口。通过服务接口与工作流指引，逐步串联下单、设计提交、进度查询与结果获取。

| 面向 Agent | 面向模型 | 面向用户 |
| :--- | :--- | :--- |
| 通过 **MCP** 发现和调用服务。 | 通过**结构化数据**与接口说明连接流程。 | 通过**可交互界面**使用业务服务。 |
| 配合 Skills 理解任务步骤。 | Beta 阶段持续完善数据约定。 | 网页端独立于本仓库提供。 |

本仓库集中提供 Skills、连接指南、工具目录和示例；百英业务服务独立运行。

<a id="get-started"></a>

## 快速开始

### 1 · 连接 MCP

向你的百英对接人获取服务访问令牌并确认账号权限。在支持 **Streamable HTTP** 和 **Bearer 认证**的 MCP 客户端中添加：

| 配置项 | 内容 |
| :--- | :--- |
| 名称 | `BiointronOS_MCP` |
| 连接方式 | Streamable HTTP |
| 地址 | `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp` |
| 认证 | `Authorization: Bearer <MCP_ACCESS_TOKEN>` |

支持 `mcpServers` 配置格式的客户端，可将下面的示例合并到现有设置中，并将 `<MCP_ACCESS_TOKEN>` 替换为自己的服务访问令牌：

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

`START_MCP_TIMEOUT_MS` 和 `RUN_MCP_TIMEOUT_MS` 是参考配置中的自定义请求头，数值分别为 **60 秒**和 **11 分钟**。它们不是 MCP 标准超时配置，须由客户端或服务明确支持；仅放入 `headers` 不能保证改变客户端等待时间，具体按客户端文档设置。更多说明见[安装指南](../installation.md#mcp)。

### 2 · 安装 Skills

从 [Skills 目录](../../skills/README.md)选择 Skill，下载包含参考文件和配套脚本在内的完整文件夹，放入 AI 客户端的 Skill 目录。Codex 与 Claude Code 的位置见 [Skill 安装说明](../installation.md#skills)。

两个 Skill 文件夹均已包含：`skills/order_design`（`order-design`）和 `skills/auto_html_report`（`auto-html-report`）。订单 Skill 引导套餐选择、资料收集、可选的设计 HTML 交付和授权下单；报告 Skill 可直接根据已有 JSON 生成多语言报告，无需凭据或 MCP。缺少 JSON 时，可按已确认的订单号和当前客户 JWT，通过 `get_report_results` 查询已获授权的结果，再生成报告。接入要求见 [Skills 目录](../../skills/README.md)。

### 3 · 从只读体验开始

```text
请列出本会话可用的 Biointron MCP 工具，说明每个工具的用途。
告诉我哪些能力已就绪、哪些仍处于 Beta 阶段。
暂时不要创建或提交订单。
```

发现工具是连接验证的第一步。具体业务操作能否完成，还需要验证对应的后端接入。

## MCP 工具目录

| 工具 | 用途 | 操作性质 |
| :--- | :--- | :--- |
| `get_order_input_requirements` | 默认分批收集资料，设计或购物车写入前统一校验；无需业务 JWT。 | 只读 |
| `search_order_antigens` | 按关键词查询百英产品库，返回真实货号、规格及分页选项。 | 只读 |
| `order_design_preflight` | 检查公司资格和可用检测项目。 | 只读 |
| `start_order_design` | 提交客户 XLSX 并等待设计保存确认。 | 写入业务数据 |
| `get_order_design_result` | 客户选择查看后读取并交付已保存设计的 HTML。 | 只读 |
| `add_order_to_cart` | 将已确认保存的设计加入购物车。 | 写入业务数据 |
| `end_order_workflow` | 指导客户端丢弃本地上下文，不撤销签名或取消订单。 | 仅客户端指令 |
| `get_order_cart` | 查询订单购物车。 | 只读 |
| `calculate_order_price` | 获取指定订单的报价。 | 只读 |
| `submit_verified_order` | 核验报价后提交选定订单，等待人工确认。 | 写入业务数据 |
| `get_report_results` | 读取已有报告的 JSON 结果。 | 只读 |

十个客户相关工具（含产品库查询、设计 HTML 读取及 `end_order_workflow`）需要当前客户的 JWT 作为 `business_token`；本地输入说明工具无需业务 JWT，MCP 入口认证不变。详见[工具参数](../tool-catalog.md)和[凭据说明](../api.md)。

当前本地清单为 **11 个工具、5 个资源、2 个提示词**；本轮未部署，未执行真实产品查询或联调测试，完整业务链路仍待验证。查看[工具签名、接入状态与使用边界](../tool-catalog.md)。

新单先介绍并选择套餐。选择产品库后，依据本地输入工具的 `catalog_auth` 复用有效 JWT，或补齐 **Biointron Account** 和 **App Key** 后兑换，无需加载完整执行提示词。再通过原生文本弹窗或 CLI 输入关键词（如 CD2），展示后台真实货号和规格供选择，支持翻页、无结果时换词；选中后复用 `cart_data`，不询问供应商或补链接。外部链接和手动资料仍在提交设计前认证。

## Skills

| Skill | 用途 | 发布状态 |
| :--- | :--- | :--- |
| [订单设计 · `order-design`](../../skills/order_design/SKILL.md) | 引导套餐及产品选择、分批收集资料、可选交付已保存的设计 HTML，核对购物车与报价后提交选定订单供人工确认。 | 已包含 |
| [HTML 结果报告 · `auto-html-report`](../../skills/auto_html_report/SKILL.md) | 根据已有或授权查询所得的 JSON 生成独立的多语言 HTML 报告，包含完整汇总、样本对比图、SPR/BLI 动力学图和可用图片。 | 已包含 |

MCP 提供可调用操作，Skills 说明如何按任务使用这些能力。安装 Skill 不等于获得服务权限，也不会自动注册 MCP。[查看完整目录 →](../../skills/README.md)

提交订单后仍需百英人工确认，不代表已投产或实验完成。已保存的设计 HTML 与实验结果报告是两种不同交付物。

<a id="beta"></a>

## Beta Playground

Biointron OS 当前以 Beta Playground 形式逐步开放，部分接口仍在接入中。每一步都应依据实际返回结果说明状态；HTTP 成功或工具名称可见，不代表业务已经完成。

创建和提交订单须处于用户授权范围内。写操作超时后，应先核查已有订单状态，再决定下一步。需要开通权限或遇到尚未开放的能力时，请联系为你提供账号的百英对接人。

<a id="online-platform"></a>

## Biointron 在线平台

在浏览器中使用百英服务。Biointron 在线平台提供 RushDATA 项目工作区，集中展示项目草稿、购物车与订单，并设有 AI 助手入口。通过平台了解可用服务、查看项目信息，让项目管理更加直观。

**[访问 Biointron 在线平台 →](https://ai.biointron.com/#/landing)**

<a href="https://ai.biointron.com/#/landing"><img src="../../assets/Biointron_Rushdata.png" alt="Biointron 在线平台：RushDATA 工作区、项目导航与 AI 助手" width="1000" /></a>

<a id="faq"></a>

## 常见问题

<details>
<summary><strong>MCP 和 Skill 都需要安装吗？</strong></summary>

MCP 提供工具连接，Skill 提供任务流程指引，也可能有独立依赖。请以已发布 Skill 的要求为准；仅下载 Skill 不会自动连接业务服务。

</details>

<details>
<summary><strong>能看到工具，是否就能完成业务？</strong></summary>

工具可见只表示它已注册。还需确认后端配置、账号权限和具体操作的验证情况，工具目录会区分这些状态。

</details>

<details>
<summary><strong>服务端和业务代码在哪里？</strong></summary>

本仓库发布公开接入资料与 Skills。云端服务和内部业务实现独立维护。

</details>

## 文档导航

| 开始使用 | 参考资料 |
| :--- | :--- |
| [安装 MCP 与 Skills](../installation.md) | [MCP 工具目录](../tool-catalog.md) |
| [Skills 目录](../../skills/README.md) | [API 与 JSON 示例](../api.md) |
| [参与贡献](../../CONTRIBUTING.md) | [许可证状态](../license.md) |

详细指南采用中英双语。

## License

采用 [PolyForm Noncommercial 1.0.0](../../LICENSE)。**本许可证不允许商业使用**。仓库内容源码可见，限非商业使用，具体范围以[完整条款及说明](../license.md)为准。

---

<div align="center">
<sub>Biointron OS · For Agents. For Models. For People.</sub>
</div>
