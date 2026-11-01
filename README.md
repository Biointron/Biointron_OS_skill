<div align="center">

<p dir="ltr">
<strong lang="en" dir="ltr">English</strong> ·
<a href="docs/readme/README.zh-CN.md" lang="zh-CN" dir="ltr">简体中文</a> ·
<a href="docs/readme/README.zh-TW.md" lang="zh-TW" dir="ltr">繁體中文</a> ·
<a href="docs/readme/README.ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="docs/readme/README.ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="docs/readme/README.tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="docs/readme/README.ru.md" lang="ru" dir="ltr">Русский</a> ·
<a href="docs/readme/README.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="docs/readme/README.th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="docs/readme/README.de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="docs/readme/README.es.md" lang="es" dir="ltr">Español</a> ·
<a href="docs/readme/README.fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="docs/readme/README.uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="docs/readme/README.pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="docs/readme/README.pt-BR.md" lang="pt-BR" dir="ltr">Português (Brasil)</a> ·
<a href="docs/readme/README.fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="docs/readme/README.ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="docs/readme/README.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="docs/readme/README.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="docs/readme/README.el.md" lang="el" dir="ltr">Ελληνικά</a> ·
<a href="docs/readme/README.ml.md" lang="ml" dir="ltr">മലയാളം</a> ·
<a href="docs/readme/README.ur-Latn.md" lang="ur-Latn" dir="ltr">Roman Urdu</a> ·
<a href="docs/readme/README.ro.md" lang="ro" dir="ltr">Română</a>
</p>

# Biointron OS

### Connect your AI agent to Biointron services.

From order requests to reported results, bring Biointron workflows into the tools you already use.<br />
MCP provides the connection. Skills guide the workflow. You stay in control.

[![MCP tool catalog](https://img.shields.io/badge/MCP-tool_catalog-087F8C?style=flat-square)](docs/tool-catalog.md)
[![Skills](https://img.shields.io/badge/Agent-Skills-234E70?style=flat-square)](skills/README.md)
[![Noncommercial license](https://img.shields.io/badge/License-Noncommercial-6B7280?style=flat-square)](LICENSE)
[![Beta Playground](https://img.shields.io/badge/Release-Beta_Playground-D7A345?style=flat-square)](#beta)

<br />

<!-- HERO: Keep the artwork path in sync across all language versions. -->
<img src="assets/biointron-os-hero.png" alt="Biointron OS" width="1000" />

<br />

**[Get started](#get-started) · [MCP tools](docs/tool-catalog.md) · [Skills](skills/README.md) · [API & examples](docs/api.md) · [Online platform](#online-platform) · [FAQ](#faq)**

</div>

---

## One platform. Three ways to connect.

Biointron OS is an interface to Biointron services for AI agents, models and people. It brings service access and workflow guidance together, with a roadmap spanning orders, submitted designs, progress and results.

| For Agents | For Models | For People |
| :--- | :--- | :--- |
| Discover and call services through **MCP**. | Work with **structured data** and documented interfaces. | Access workflows through an **interactive interface**. |
| Pair tool calls with task-specific Skills. | Data conventions are being aligned during Beta. | The web experience is provided separately from this repository. |

This repository is the public home for Skills, connection guides, the tool catalog and examples. Biointron business services run separately.

<a id="get-started"></a>

## Get started

### 1 · Connect MCP

Obtain a service access token and confirm your account permissions with your Biointron contact. In an MCP client that supports **Streamable HTTP** and **Bearer authentication**, add:

| Setting | Value |
| :--- | :--- |
| Name | `BiointronOS_MCP` |
| Transport | Streamable HTTP |
| URL | `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp` |
| Authentication | `Authorization: Bearer <MCP_ACCESS_TOKEN>` |

For clients that support the `mcpServers` configuration format, merge this example into your existing settings and replace `<MCP_ACCESS_TOKEN>` with your issued service access token:

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

`START_MCP_TIMEOUT_MS` and `RUN_MCP_TIMEOUT_MS` are custom request headers from the reference configuration, representing **60 seconds** and **11 minutes**. They are not standard MCP timeout settings and require explicit client or service support. Adding them to `headers` alone does not guarantee a change to client wait limits; follow your client's documentation. See the [installation guide](docs/installation.md#mcp).

### 2 · Add Skills

Choose a Skill from the [Skills catalog](skills/README.md). Download its complete folder, including references and any scripts, and place it in your agent's Skill directory. See [Skill installation](docs/installation.md#skills) for Codex and Claude Code.

Both Skill folders are included: `skills/order_design` (`order-design`) and `skills/auto_html_report` (`auto_html_report`). Order Design uses the MCP service; HTML Report works from supplied result JSON and does not retrieve results itself.

### 3 · Try a read-only introduction

```text
List the Biointron MCP tools available in this session and explain what each one does.
Tell me which capabilities are ready and which remain in Beta.
Do not create or submit an order.
```

Tool discovery is the first connection check. A successful business operation requires its own validated backend connection.

## MCP tool catalog

| Tool | Purpose | Effect |
| :--- | :--- | :--- |
| `order_design_preflight` | Check company eligibility and available test items. | Read only |
| `start_order_design` | Submit the supplied XLSX and wait for confirmed design storage. | Writes business data |
| `add_order_to_cart` | Add a confirmed saved design to the cart. | Writes business data |
| `get_order_cart` | Read the order cart. | Read only |
| `calculate_order_price` | Get a quote for selected orders. | Read only |
| `submit_verified_order` | Verify the quote and submit selected orders. | Writes business data |
| `get_report_results` | Retrieve existing report results as JSON. | Read only |

These seven tools are registered in the current MCP implementation. End-to-end business readiness remains to be verified. See [signatures, status and limits](docs/tool-catalog.md).

## Skills

| Skill | Purpose | Release status |
| :--- | :--- | :--- |
| [Order Design · `order-design`](skills/order_design/SKILL.md) | Guide design submission, cart and quotation checks, and authorized order submission. | Included |
| [HTML Report · `auto_html_report`](skills/auto_html_report/SKILL.md) | Turn supplied result JSON into standalone multilingual HTML reports with summary tables, charts and available images. | Included |

MCP exposes operations; Skills describe how an agent uses them within a task. Installing a Skill does not grant service access or automatically register MCP. [Browse the catalog →](skills/README.md)

<a id="beta"></a>

## Beta Playground

Biointron OS is being introduced as a Beta Playground. Some connections may still be unavailable. Report the actual result of each step; an HTTP success or a visible tool name does not establish that a business operation completed.

Order creation and submission require user authorization. If a write times out, check the existing order status before retrying. For access or an unavailable capability, contact the Biointron representative who provided your account.

<a id="online-platform"></a>

## Biointron Online Platform

Access Biointron services in your browser. The online platform brings RushDATA project workflows together, with access to project drafts, the shopping cart, orders and an AI assistant. Explore available services and view your project information in one place.

**[Visit the Biointron online platform →](https://ai.biointron.com/#/landing)**

<a href="https://ai.biointron.com/#/landing"><img src="assets/Biointron_Rushdata.png" alt="Biointron online platform with the RushDATA workspace, project navigation and AI assistant" width="1000" /></a>

<a id="faq"></a>

## FAQ

<details>
<summary><strong>Do I need both MCP and Skills?</strong></summary>

MCP supplies callable tools. Skills add workflow instructions and may have their own dependencies. Use the requirements in each released Skill; a Skill download alone does not connect a service.

</details>

<details>
<summary><strong>Does listing a tool mean it is ready for business use?</strong></summary>

No. Discovery confirms that the tool is registered. Backend configuration, account access and the requested operation must also be validated. The catalog records that distinction.

</details>

<details>
<summary><strong>Where are the server and business implementation?</strong></summary>

This repository distributes public integration materials and Skills. The hosted service and private business implementation are maintained separately.

</details>

## Documentation

| Start here | Reference |
| :--- | :--- |
| [Install MCP & Skills](docs/installation.md) | [MCP tool catalog](docs/tool-catalog.md) |
| [Skills catalog](skills/README.md) | [API & JSON examples](docs/api.md) |
| [Contribute](CONTRIBUTING.md) | [License status](docs/license.md) |

Detailed guides are provided in Chinese and English.

## License

Licensed under [PolyForm Noncommercial 1.0.0](LICENSE). **Commercial use is not permitted under this license.** This repository is source-available for noncommercial use. See [scope and terms](docs/license.md).

---

<div align="center">
<sub>Biointron OS · For Agents. For Models. For People.</sub>
</div>
