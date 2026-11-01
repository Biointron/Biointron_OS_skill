# Skills

[Home](../README.md) · [中文首页](../docs/readme/README.zh-CN.md) · [Installation / 安装](../docs/installation.md#skills)

Both Skill folders are included in this repository. Download each complete folder and follow the [installation guide](../docs/installation.md#skills).

本仓库已包含以下两个 Skill。请下载完整文件夹，并按[安装指南](../docs/installation.md#skills)配置。

| Skill | Workflow / 用途 | Folder / 文件夹 |
| --- | --- | --- |
| [`order-design` · 订单设计](order_design/SKILL.md) | Guide design submission, cart and quotation checks, and authorized order submission / 引导设计提交、购物车和报价核查，以及授权范围内的下单。 | `order_design/` |
| [`auto_html_report` · HTML 结果报告](auto_html_report/SKILL.md) | Create standalone multilingual HTML reports from supplied result JSON / 根据已有结果 JSON 生成独立的多语言 HTML 报告。 | `auto_html_report/` |

The identifiers above come from each `SKILL.md` file's `name` field. Keep the folder names shown here when copying the packages.

上表标识来自各 `SKILL.md` 的 `name` 字段。复制安装时保留表中的文件夹名称。

## Order Design / 订单设计

Use the customer's supplied business inputs and original files to guide an authorized order workflow through MCP. The Skill checks stage results and does not generate biological sequences, experimental protocols or measurements. Read the included [workflow reference](order_design/references/workflow.md) for its input and continuation rules.

依据客户提供的业务资料和原始文件，通过 MCP 引导已授权的订单流程，核对各阶段结果。不生成生物序列、实验方案或测量数据。输入和流程衔接要求见随包提供的[工作流参考](order_design/references/workflow.md)。

Normal use requires an authorized MCP connection with the order tools enabled. The bundled Python scripts are source-project helpers, not standalone installers: `check.py` imports `config.order_design` and `skill.order_design.scripts.client`, and the client requires `httpx`. This public bundle does not include that project configuration or Python package layout. Use the hosted MCP tools for the documented installation; running the helpers directly requires the matching source project and its dependencies.

正常使用需要已授权、已开放订单工具的 MCP 连接。附带 Python 脚本是源项目辅助代码，不是独立安装器：`check.py` 依赖 `config.order_design` 与 `skill.order_design.scripts.client`，客户端依赖 `httpx`。本公开包未包含对应项目配置和 Python 包结构。按本指南安装时使用托管 MCP 工具；直接运行这些脚本需要匹配的源项目与依赖。

## HTML Report / HTML 结果报告

Turn supplied RushData result JSON into a standalone HTML file with a complete Data Summary, sample comparison charts, assay tables and available images. The Skill supports multiple languages and defaults to English. Its [result schema reference](auto_html_report/references/result-schema.md) defines the supported structures and field-matching rules.

将已提供的 RushData 结果 JSON 生成为独立 HTML 文件，包含完整数据汇总、样本对比图、检测明细表和可用图片。支持多种语言，默认英文。支持的数据结构和字段匹配规则见[结果结构参考](auto_html_report/references/result-schema.md)。

Supply actual result JSON and use an agent that can write HTML files. An order number alone is insufficient. If results must be fetched first, use the separate `get_report_results` MCP tool, then provide its result JSON to this Skill. Generating a report from an existing local JSON file does not require an MCP connection. The Skill does not create orders, design experiments or invent measured results.

需要提供真实结果 JSON，并使用能够生成 HTML 文件的 Agent。只有订单号不足以生成报告；如需先查询结果，可通过独立的 `get_report_results` MCP 工具获取，再把结果 JSON 交给此 Skill。已有本地 JSON 时，生成报告无需 MCP 连接。不创建订单、设计实验或编造测量结果。

## Package contents / 文件组成

```text
skills/
├── order_design/
│   ├── SKILL.md
│   ├── references/workflow.md
│   └── scripts/
│       ├── check.py
│       └── client.py
└── auto_html_report/
    ├── SKILL.md
    └── references/result-schema.md
```

Copy the selected Skill folder, including its references and any scripts; this catalog is not itself a Skill. See [installation instructions](../docs/installation.md#skills) for destination directories. Installing a Skill does not grant service access or verify the live business workflow.

复制选定 Skill 的完整文件夹，保留参考文件和配套脚本；本目录说明本身不是 Skill。目标目录见[安装说明](../docs/installation.md#skills)。安装 Skill 不会自动获得服务权限，也不代表线上业务流程已经验证。

The repository uses a [noncommercial license](../docs/license.md). Service access remains subject to account permissions and service terms.

本仓库采用[非商业许可证](../docs/license.md)，服务访问仍受账号权限及服务条款约束。
