# Skills

[Home](../README.md) · [中文首页](../docs/readme/README.zh-CN.md) · [Installation / 安装](../docs/installation.md#skills)

Both Skill folders are included in this repository. Download each complete folder and follow the [installation guide](../docs/installation.md#skills).

本仓库已包含以下两个 Skill。请下载完整文件夹，并按[安装指南](../docs/installation.md#skills)配置。

| Skill | Workflow / 用途 | Folder / 文件夹 |
| --- | --- | --- |
| [`order-design` · 订单设计](order_design/SKILL.md) | Guide package selection, order preparation, optional design HTML delivery and submission for human confirmation / 引导套餐选择、订单资料准备、可选设计 HTML 交付及提交人工确认。 | `order_design/` |
| [`auto-html-report` · HTML 结果报告](auto_html_report/SKILL.md) | Create multilingual HTML reports from supplied JSON or results retrieved with authorization / 根据已有或授权查询所得的 JSON 生成多语言 HTML 报告。 | `auto_html_report/` |

The Skill names above match each `SKILL.md` file's `name` field. Folder names remain `order_design` and `auto_html_report`; the MCP prompt names remain `order_design` and `auto_html_report`. Use `auto-html-report` when asking an installed local Skill to generate a report.

上表 Skill 名称来自各 `SKILL.md` 的 `name` 字段。文件夹仍为 `order_design` 和 `auto_html_report`，MCP 提示词名称也仍为 `order_design` 和 `auto_html_report`；调用本地已安装的报告 Skill 时使用 `auto-html-report`。

## Order Design / 订单设计

Start with Basic, Standard, Premium or Customized, then collect information in batches after each branching choice. The Skill supports product-library selection, customer-provided antigen information and the original design XLSX. It validates the completed stage before a write, verifies that the design was saved, and offers the actual saved-design HTML when requested. It then guides cart details, authoritative quotes and authorized submission of selected orders for human confirmation. Production begins only after Biointron confirms the order; submission is not payment or evidence of experimental completion.

先选择 Basic、Standard、Premium 或 Customized，再按分支分批收集资料。支持产品库选择、客户提供的抗原资料和原始设计 XLSX；写入前统一校验本阶段资料，核实设计已保存后，可按客户选择交付实际设计 HTML。随后引导购物车资料、权威报价及授权范围内的选单提交，等待人工确认。百英确认后才进入生产；提交不代表付款或实验完成。

Customer-facing order interactions follow the requested Chinese or English conversation language. The client reuses valid credentials and asks only for missing information. Package introductions and local collection need no business JWT. Product-library queries and business operations require the current customer's JWT, obtained from a supplied valid token or the configured account/App Key exchange. Order creation, cart writes and submission stay within the user's authorization.

下单交互沿用客户选择的中文或英文，复用有效凭据，只补问缺失资料。套餐介绍和本地资料收集无需业务 JWT；产品库查询及业务操作需要当前客户 JWT，可复用已有有效令牌，或按配置使用账号和 App Key 兑换。设计、购物车写入和提交均在用户授权范围内执行。

Read the [business context](order_design/references/business-context.md) for terminology and the [workflow reference](order_design/references/workflow.md) for input, authorization and signed-continuation rules. The Skill does not generate biological sequences, experimental protocols or measured results. A design HTML file describes the saved design; experimental results are handled by the report Skill.

业务术语见[业务背景](order_design/references/business-context.md)，输入、授权及签名上下文规则见[工作流参考](order_design/references/workflow.md)。此 Skill 不生成生物序列、实验方案或测量结果。设计 HTML 用于展示已保存的设计，实验结果由报告 Skill 处理。

Normal use follows the hosted MCP tools. The included Python helpers depend on the source project's configuration, package layout and dependencies, including `httpx`, `jsonschema` and the MCP client library. They are not a standalone installer. Copy the complete folder, and use the matching source project only when running those helpers directly. See the [installation requirements](../docs/installation.md#skills).

常规使用通过托管 MCP 工具执行。附带 Python 辅助脚本依赖源项目配置、包结构及 `httpx`、`jsonschema`、MCP 客户端库等依赖，不是独立安装器。安装时复制完整文件夹；只有直接运行辅助脚本时才需要匹配的源项目环境。详见[安装要求](../docs/installation.md#skills)。

## HTML Report / HTML 结果报告

Create a standalone HTML report from actual RushData result JSON. With usable JSON already supplied, generation needs no credentials, MCP connection or another Skill. If data is missing and a query is authorized, the Skill can first obtain results through `get_report_results` using the confirmed order number and the current customer's JWT, then generate the report. An order number alone is not result data.

根据真实 RushData 结果 JSON 生成独立 HTML 报告。已有可用 JSON 时，无需凭据、MCP 连接或其他 Skill；缺少数据且已获查询授权时，可先用已确认的订单号和当前客户 JWT，通过 `get_report_results` 取得结果，再生成报告。订单号本身不能代替结果数据。

Reuse a valid JWT. Otherwise request only the missing **Biointron Account** and **App Key**, one field at a time, and exchange them through the server-provided connection information. Use the verified `result.token` for the query; the App Key is not a JWT. If metadata is missing, an available `order_design(phase="execute", detail="compact", language=<zh-or-en>)` prompt may supply connection information only, without starting an order. Credentials and internal transport details stay out of the delivered report.

优先复用有效 JWT；否则逐项补齐缺少的 **Biointron Account** 和 **App Key**，依据服务端提供的连接信息兑换后，用核实的 `result.token` 查询，不能把 App Key 当作 JWT。缺少连接元数据时，可通过可用的 `order_design(phase="execute", detail="compact", language=<zh-or-en>)` 提示词仅读取连接信息，不启动下单。交付报告不包含凭据或内部传输信息。

| Report feature / 报告能力 | Behavior / 说明 |
| --- | --- |
| Complete Data Summary / 完整数据汇总 | Preserve source rows, declared fields, units and precision; provide search and CSV export / 保留原始样本行、声明字段、单位与精度，支持搜索及 CSV 导出。 |
| Ordinary comparison charts / 普通对比图 | Provide sample-name and numeric high-to-low views / 同时提供按样本名排序和按数值降序排列的视图。 |
| SPR/BLI kinetics / SPR/BLI 动力学 | Use paired rate data for kinetic plots; do not substitute sample-versus-K_D charts / 根据成对速率数据绘制动力学图，不以样本与 K_D 对比图替代。 |
| Experimental images / 实验图片 | Include available images with their matching sample/assay; do not invent missing images / 有图片时按样本与检测项目匹配展示，不编造缺失图片。 |
| Languages and delivery / 语言与交付 | Default to English; create a separate standalone HTML file per order and requested language / 默认英文，每个订单及所需语言分别交付独立 HTML 文件。 |

The report Skill package is written in English; customer reports still support Chinese, Japanese and other requested languages. The agent needs file-writing and chart-generation capabilities. Read the [result schema reference](auto_html_report/references/result-schema.md) for supported structures and matching rules. Order submission or a design report cannot substitute for experimental data.

报告 Skill 包使用英文编写，客户报告仍支持中文、日文等所需语言。Agent 需要具备文件写入和图表生成能力；数据结构和匹配规则见[结果结构参考](auto_html_report/references/result-schema.md)。订单提交回执或设计报告不能代替实验数据。

## Package contents / 文件组成

```text
skills/
├── order_design/
│   ├── SKILL.md
│   ├── references/
│   │   ├── business-context.md
│   │   └── workflow.md
│   └── scripts/
│       ├── auth.py
│       ├── check.py
│       ├── client.py
│       ├── forms.py
│       ├── interactive.py
│       ├── localization.py
│       ├── mcp_client.py
│       └── workbook.py
└── auto_html_report/
    ├── SKILL.md
    └── references/result-schema.md
```

Copy the selected Skill folder, including its references and any scripts; this catalog is not itself a Skill. See [installation instructions](../docs/installation.md#skills) for destination directories. Installing a Skill does not grant service access or verify the live business workflow.

Keep `scripts/forms.py` with the order helper scripts: it provides the local schema and input checks used by `get_order_input_requirements` and the write tools. It needs `jsonschema`, already included in the source project's existing MCP 2.3 dependency set. The local input tool needs no business JWT, but it neither authorizes writes nor restores missing saved-design proof.

订单包须保留 `scripts/forms.py`：本地输入说明工具与写入工具共用其 schema 和输入检查。它使用源项目现有 MCP 2.3 依赖已提供的 `jsonschema`。本地输入工具无需业务 JWT，但不能授权写入或恢复缺失的设计保存证明。

复制选定 Skill 的完整文件夹，保留参考文件和配套脚本；本目录说明本身不是 Skill。目标目录见[安装说明](../docs/installation.md#skills)。安装 Skill 不会自动获得服务权限，也不代表线上业务流程已经验证。

The repository uses a [noncommercial license](../docs/license.md). Service access remains subject to account permissions and service terms.

本仓库采用[非商业许可证](../docs/license.md)，服务访问仍受账号权限及服务条款约束。
