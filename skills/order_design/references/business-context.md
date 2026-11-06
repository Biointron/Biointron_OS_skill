# 下单业务背景与客户说明

用于解释套餐、检测项、信息采集和人工确认流程；执行接口仍遵循 [workflow.md](workflow.md)。业务要求来自 2026-11-04 会议纪要，当前字段限制来自本项目适配器及工作流中记录的 2026-11-03 购物车契约核对。下列官网资料于 2026-11-04 查阅，用于解释科学概念，不替代当前 API 契约或实际报价。

## 对话起点

按客户自然语言指令选定 `language="zh"` 或 `language="en"`，后续问答、套餐选项、帮助、校验错误、产品库导航和等待消息均使用该语言；客户明确换语言时再切换。CD2、货号、路径、凭据、数字和简短选项不改变会话语言。本文件中文仅为业务参考，不能让英文会话回退中文。客户端显式把语言传给 `order_design` 和每个下单 MCP 工具，CLI 传 `--language zh`/`--language en`；省略时默认 `zh` 只兼容旧调用，服务器不保留全局语言。固定文案使用所选语言原文，业务键、枚举、品牌和原始资料不翻译；语言不写入业务对象或签名上下文。

首次下单先介绍并选择套餐；Customized 先单独选择样本形式，抗原来源先确定分支，再把已可独立填写的项目、检测、抗原资料与设计表路径合并为问题批次。资料收齐后，在真正设计前集中校验、批量修正，再确认权限并执行已授权设计。介绍套餐和本地资料收集不要求账号；产品库查询前仍须复用有效 JWT 或补齐 Biointron Account / App Key 并兑换，真实查询和产品选择不省略。外部链接和手动分支在提交前认证。所有分支在写入前核实公司资格。按全新用户开始时不沿用旧凭据和订单资料，也不因此取消真实订单。

介绍套餐时说明样本形式、检测内容和预期数据，再让用户选择；不是仅列出名称。抗体数量从对外表单中移除，不作为客户填写或确认的问题；未上传表格时等待上传，读取原始样本表后由系统自动判断。其他相互独立的必要信息合并提问，已有答案不重复询问。接口编码由 AI 在内部映射。

开场直接使用当前入口已有的四档套餐文案并立即调用原生单选工具，不要求先读完本文件、Skill 和接口参考。缺少文案时只获取一次默认 `order_design` 精简提示词；用户选定套餐后再收集后续资料。产品库查询直接使用当前工具说明及输入工具的 `catalog_auth` 凭据/连接说明，已有有效 JWT 优先复用，不为关键词输入或查询加载整套规则。首次准备设计、购物车、报价或提交时，获取一次 `order_design(phase="execute", language=language)` 的默认精简执行说明和连接元数据，后续阶段复用；具体问题确需完整参考时才用 `detail="full"` 或读取相关段落。避免排查无关版本或重复初始化已有连接。

`get_order_input_requirements(stage, supplied=None, language=language, detail="compact", mode="collect")` 默认只收集资料：返回 `status=collecting|collected`、`validation_deferred=true`、`write_performed=false` 及当前可独立填写的问题批次。`collected` 仅表示本轮资料已收集，不表示输入正确、已获授权或可写入。套餐、Customized 样本形式、抗原来源等决定后续分支的问题先单独选择；分支确定后，将独立文本及选择题放在同一次 `interaction.native_question.questions` 中实际调用原生工具。合并整批真实答案后再推进下一分支或批次，不对每个字段重新调用 MCP、模型或完整校验。CLI 顺序询问同一批字段，批内不回到模型、不重读规则、不调用输入说明或业务校验。缺失或空白的分支答案仍需询问；保留 `false`、`0` 和客户明确给出的 `[]`，不补默认值。收集阶段不运行完整业务校验或扫描 XLSX。 资料收齐、准备实际设计或购物车写入时，显式调用 `get_order_input_requirements(..., mode="validate", language=language)`，一次检查本阶段全部资料。`status=needs_input` 时汇总全部已发现问题，并用返回的原生问题批次收集修正；保留其他有效答案，整批修改后再校验。`status=ready` 仅表示本地检查通过。`detail="compact"` 保留当前动作、问题批次及全部校验问题；仅需完整 schema 与诊断时用 `detail="full"`。实际写入入口的完整保护保留，认证、文件传输限制、公司权限、产品目录与签名上下文等检查均须在相应 API 调用前通过。凭据只留客户端，App Key、账号和 JWT 不进入 `supplied` 或业务 DTO；收集或校验完成均不新增写入授权。 所有输入路径复用已答资料、语言、有效 JWT 和候选，不在批内重读规则或认证；不承诺未经实测的固定秒数。

收集阶段不扫描 XLSX 或重复校验业务字段；本地读文件及写入前保留文件名、Base64、非空和大小检查。实际 `start_design` 时尽力统计一次，不能可靠统计就省略数量，原文件交后台判断，不另问数量。CLI 按同一批次连续询问，批内不调用模型、MCP 或完整校验。

靶点目前是对话背景，不能自行新增 `target` 等请求字段。下单以客户提供的原始 Excel 和 JSON 业务资料配合完成；不在此流程中生成或修改生物序列。

## 套餐：如何向客户介绍

英文开场使用以下固定文案，不能从内部检测键重新翻译；中文开场使用当前入口或 `package_display_text` 的中文原文。下面的详细解释仅用于客户需要进一步说明时。

- **Basic: Supernatant expression, antibody expression level (supernatant antibody concentration) measurement, and two-point BLI binding analysis.**
- **Standard: Purified antibodies with purity and SPR binding characterization.**
- **Premium: Standard plus thermal stability, polyreactivity, and self-interaction assays.**
- **Customized: Choose the sample type, then select protein property, binding, and developability assays.**

| 客户名称 | 通俗说明与预期数据 | 当前适配器映射（内部使用） |
| --- | --- | --- |
| Basic | 上清表达、抗体表达量（上清抗体浓度）检测和 BLI 两点结合检测；不包含蛋白纯化。 | `BRD101`：Titer、BLI Octet 2-points；只支持 1 个抗原。 |
| Standard | 使用纯化抗体，进一步了解纯度和结合特性。 | `BRD201`：cGE、SPR Carterra；1–3 个抗原。 |
| Premium | 在 Standard 的基础上，增加热稳定性、多反应性和自身相互作用信息，辅助评估后续开发风险。 | `BRD301`：再增加 DSF、PSR ELISA_BVP、AC_SINS；1–3 个抗原。 |
| Customized | 选择后立即确认表达上清或纯化抗体，再由客户在同一批次分别选择蛋白性质、结合和开发性检测；不能跳过或代选。 | `BRD401`：使用 `testItems`，不能推测目录 ID 或额外互斥规则。 |

前三档的服务定位参考 [Biointron RushData 官网](https://www.biointron.com/antibody-production/rushdata.html)。官网介绍 Standard 可使用 BLI 或 SPR，并包含浓度读数；当前适配器的固定选择是 `cGE` 和 `SPR_Carterra`。不得因此自行改写固定套餐、增加检测键或保证未确认的交付字段。Customized 的执行规则来自当前适配器，不声称官网已列出其全部选项。

可以按客户目的解释和推荐，但需由客户选定套餐，不默认最高档或擅自替换。价格、折扣以后台权威报价为准，项目周期需确认；不沿用官网促销数字推算订单价格。

## 检测项：面向客户的简明解释

以下说明介绍“测什么”，不包含实验操作方案、判定阈值或结果承诺。具体能否出数，以已选套餐、实际报告和检测条件为准。

| 术语 / 当前业务键 | 可使用的解释 | 资料来源 |
| --- | --- | --- |
| Titer | 此处为抗体表达量（上清抗体浓度），按报告给出的浓度读数说明，与结合能力分别介绍；内部键仍用 Titer。 | [Biointron 对 Titer 的说明](https://www.biointron.com/blog/rapid-screening-binding-characterization-or-developability-profiling.html) |
| BLI / Octet | BLI 是生物层干涉检测技术，可观察分子结合与分离；Octet 是使用该技术的仪器平台。 | [Sartorius Octet 说明](https://www.sartorius.com/en/products/biolayer-interferometry/bli-resources/biomolecular-binding-kinetics-assays-on-the-octet-platform) |
| 2-points / 4-points | 当前服务的检测点位档位。官网将两点评估用于初筛；不能解释成“两个数值即可确定完整亲和力”。点位是否指浓度、重复或其他设计，需由百英确认。 | [Biointron 套餐说明](https://www.biointron.com/blog/which-rushdata-package-fits-your-program.html)；4-points 的具体定义待确认 |
| SPR / SPR_Carterra / SPR_Biacore | SPR 是表面等离子体共振技术，用于实时观察结合；Carterra 和 Biacore 是平台名称。高通量 SPR 可同时比较较多样本，具体数据依赖服务配置。 | [Carterra 高通量 SPR](https://carterra-bio.com/general-faqs/)、[Cytiva Biacore 官方说明](https://d3.cytivalifesciences.com/prod/IFU/29706293.pdf) |
| CE / cGE | CE 是毛细管电泳，cGE 是其中的凝胶电泳形式，可用于观察蛋白纯度和相关组分；当前套餐键是 `cGE`。 | [SCIEX 纯度分析说明](https://sciex.com/tech-notes/biopharma/multi-capillary-gel-electrophoresis-to-increase-throughput-for-t) |
| HPLC / SEC_HPLC / SEC_UPLC | HPLC 是液相色谱技术类别；这里的 SEC 按分子在溶液中的大小进行分离，用于观察单体、聚集体和片段。不能把所有 HPLC 检测都当成同一项。 | [Agilent SEC 说明](https://www.agilent.com/cs/library/eseminars/public/Introduction-to-HPLC-Separation-Principles-for-Biomolecules-05112020.pdf) |
| FACS_iQue | 使用流式细胞分析观察抗体与细胞的结合；iQue 是高通量平台。不能将此类结合信号直接承诺为 SPR/BLI 动力学参数。 | [Sartorius 细胞结合检测](https://www.sartorius.com/en/applications/life-science-research/high-throughput-screening-by-cytometry/antibody-binding-assays) |
| ELISA | 酶联免疫检测，通过检测信号反映指定条件下的结合；单点和多点档位的具体定义仍需服务方确认。 | [Sartorius 生物测定概述](https://www.sartorius.com/en/applications/quality-control-testing/sample-preparation-qc/bioassays-serial-dilutions-application-guide) |
| DSF | 提供热稳定性相关读数，如开始发生变化的温度和熔解温度。 | [Biointron 开发性检测说明](https://www.biointron.com/blog/beyond-fast-expression-scaling-antibody-validation-to-thousands-of-candidates.html) |
| PSR ELISA_BVP / AC_SINS | 前者用于了解多反应性，后者用于了解抗体自身相互作用；它们提供不同维度的信息。 | [Biointron 开发性检测说明](https://www.biointron.com/blog/beyond-fast-expression-scaling-antibody-validation-to-thousands-of-candidates.html) |
| DLS_Rh / DLS_Tagg | 动态光散射提供溶液中表观粒径信息；Rh 是水动力半径，Tagg 是聚集开始明显可检测时的温度，不能与 DSF 的 Tm 混用。 | [Malvern Rh 说明](https://www.malvernpanalytical.com/kr/learn/knowledge-center/whitepapers/wp140404applicdlsprotein4faq)、[Malvern Tagg 说明](https://www.malvernpanalytical.com/en/learn/knowledge-center/insights/aggregation-temperature-tagg-what-is-it-and-how-can-we-calculate-it?lang=ko) |
| PAIA_HIC / PAIA_Heparin / PAIA_OVA / PAIA_BVP | PAIA 检测组合涵盖疏水性及非特异相互作用等维度。厂商公开的 BVP 模拟试剂不能直接当作本系统 `PAIA_BVP` 的已确认定义；具体对应和输出需核实。 | [PAIA 厂商说明](https://www.paiabio.com/developability) |

`PSR ELISA_Insulin`、`PSR ELISA_dsDNA` 的服务定义、各点位档位、PAIA 的具体映射和全部项目的单位/阈值，仍需 Rush Data 知识库或百英确认。纪要中的 “Catalyst / SPR_Catalyst” 与代码中的 `SPR_Carterra` 不同，暂不建立别名，也不据此增加一个可选项目。

## Customized 的选择与冲突

完整可选键和当前约束见 [工作流套餐规则](workflow.md#packages)。现有明确约束包括：只能选一种样本形式；上清使用 Titer 且不能带开发性检测；纯化抗体不能选择 Titer。其他组合按该规则和本地校验执行。不能仅因两个检测都描述亲和力，就自行认定它们互斥。

业务方于 2026-11-04 明确：BLI 2 点和 4 点、FACS 单点和 8 点、ELISA 单点和 8 点各自可以同时选，SPR-Carterra 和 SPR-Biacore 也可以同时选。这些结合项目在纯化抗体模式下不互斥，不能因为“看起来重复”而删选。表达上清模式仍只允许 FACS 单点和 ELISA 单点，两项可并选，不能展示全部纯化检测作为可选项。

Customized 样本形式必须紧接套餐选择单独确认，之后把检测类别作为独立问题放在同一批次；允许不检测的类别仍需客户明确选择。不让客户填写 API 字段或 JSON。业务冲突留到设计前集中校验：指出所有已选项目与样本形式不兼容的具体原因，再通过修正批次更正；不能只说“组合错误”，也不默默改选、删除或更换套餐。未知规则仍由业务方核实。

## 抗原来源与信息完整性

抗原资料的三个选项按顺序使用所选语言原样展示：中文为 **使用我们的产品库（无需提供链接）**、**提供外部产品链接**、**手动填写已有抗原资料**；英文为 **Use our product catalog (no link required)**、**Provide an external product link**、**Enter existing antigen information manually**。第一项对应 `SUPPLIER_CATALOG`，由客户在百英系统提供的产品中选择；第二项对应 `CUSTOMER_URL`，才要求客户提供具体产品的 HTTPS 链接；第三项对应 `MANUAL`。不能把产品库选项写成“提供供应商名称和货号”。客户已经表示使用产品库时，直接进入该分支；此前选择过链接时切换来源并取消旧链接问题，不重复问来源。

产品库模式先检查当前账号凭据，再用原生文本弹窗或 CLI 输入询问抗原关键词，例如 CD2。随后调用 `search_order_antigens` 查询百英产品库，默认每页 50 条、每次最多合并 5 个连续页：先取首个请求页，再在同一次请求客户端内并行读取后续最多 4 页，按供应商、货号和规格去重后供客户选择；不跨用户缓存凭据或结果。展示 `catalog_summary`，区分后台总产品数、本批已加载产品数和可选规格数。原生弹窗和 CLI 都提供“更换关键词”，有更多结果时提供“继续加载更多产品”，按返回的 `next_page` 续查并保留已有候选，不能将本批数量说成全部结果。后续页失败时保留已加载结果、说明原因及未完成状态，不自动重试；没有匹配结果时请客户重新输入关键词。不同网页可能使用不同来源或环境，不能仅凭增加分页宣称两边产品已对齐。

完整保留后台搜索候选，不擅自按关键词精确匹配、供应商或物种缩减；筛选前先取得客户确认，可以解释模糊匹配，但不能把相似名称当作同一抗原。

无需独立产品选择页面，也不先让客户填写或选择供应商。选中后自动带回资料，保留返回的 `cart_data` 供购物车复用；后台未返回链接时不补问、不编造。客户端将 `catalog_options` 与 `catalog_search` 一同传给本地输入工具生成选择和续载动作，搜索及导航信息不进入设计资料。查询由专用 MCP 工具或 CLI 客户端完成；不能用示例产品充数、要求客户提供产品库 JSON，或改问链接和货号。具体分页、字段和来源核对见[工作流产品库规则](workflow.md#antigens-and-positive-controls)。

按纪要需要确认物种来源、标签、是否突变、缓冲液、分子量和浓度。向客户解释这些属性有助于识别产品并安排后续检测；未知信息记录为待补充，不推断物种、猜浓度、替换标签、建议或生成突变。缓冲液取产品的配方/溶液信息，不能拿储存温度等说明代替。

这份业务清单不等于现有 DTO 的必填字段：设计草案有三种来源模式，购物车只有产品链接和产品信息两种模式。当前购物车允许仅 `productUrl` 有值，其余字段为 null；不能往 URL 模式强塞其他字段或自行新增 `species`、`mutation`。完整属性由对话或后端补全；需要人工核实的缺项不能说成已经确认。是否将其升级为写入前强制校验，须先确认字段、单位、补全责任及接口支持。

纪要“5 个手工字段”与后文属性数量不一致，不按数字臆造表单。抗原 JSON 条目数必须等于 `antigenCount`，一致性校验在设计前集中检查及实际写入入口继续生效。

## 阳性参考

建议客户从本次抗体清单中选定已知可作为比较基准的抗体，可在业务层记录多个名称；不是必须添加，也不保证它一定具有最高亲和力。只确认名称及其与本次样本的对应关系，不重复收集已有序列和理化信息，不代客户挑选。

当前购物车 `positiveControl` 是可选单字符串，设计 `positiveControls` 是契约仍待确认的对象数组。不能自动把名称列表改成该数组或用逗号拼接多个名称传入单字符串；多个阳参的编码和后台关联方式须确认。确认之前保留客户意愿，说明当前限制。

## 模板字段与数量

- `projectName`：客户给项目起的昵称；去除首尾空白后保留内部空格、下划线和横杠，不把它当作系统项目编号、靶点或唯一订单身份。
- `antibodyProjectCount`：从客户之后上传的原始设计表尽力统计，不是客户问答或确认字段。统计样本名称对应的数据行，跳过表头、空行及 `AI spec`、`_mapping`、`_options` 等已知辅助表，不按格式化行数、链条数或单元格数统计，也不擅自去重。无法识别模板、多个样本表使范围不明或其他计数失败时，省略数量并清除旧手填数，不要求换表、不填默认值；原文件不改动，交给后端 API 判断。仅实际文件读取或传输失败时重新收集路径；本地不因模板、内容、辅助表或数量范围阻断，也不另行运行内容校验。只有 API 明确返回业务错误时才说明并收集对应修正资料。
- `usingdna`：是否指定直接使用客户提供的 DNA。按纪要，指定 DNA 时不再进行系统自身的密码子优化；否则按蛋白输入的既有流程处理。结合原始文件和客户意愿确认；只有序列外观或不明确的字母组成时不能擅自判断，也不在此生成、转换或优化序列。
- `sp`：Signal Peptide（信号肽）。纪要说明当前不支持自定义；不要主动要求用户设计或提供自定义信号肽。字段本来就是可选，可省略或留空；现有适配器枚举保留兼容，不表示服务已经开放自定义。模板列是否删除或取消必填需后端确认。

## 设计、交付和人工确认

1. 收集信息、说明套餐、核实公司资格与可选项目，再在客户授权后提交原始设计文件。纪要提出设计等待上限 20 分钟；当前 `RUSHDATA_DESIGN_TIMEOUT` 默认 600 秒，MCP 还有整体调用时限。20 分钟是待确认的业务等待要求，不代表当前部署配置或实验周期。保存超时后核查已有订单，不能重新下单恢复。
2. 仅在本次设计 `result_saved` 已核实后、收集购物车资料和加入购物车前，实际调用原生单选卡片或 CLI 单项选择。中文问“设计已保存，是否查看本次设计结果？”，选项“需要，查看HTML设计结果”“不需要，继续下单”；英文问“The design has been saved. Would you like to view the design result?”，选项“Yes, view the HTML design result”“No, continue ordering”。只显示当前语言并等待真实答案。客户选择查看时，先只读取得本次已保存设计的真实结果，交付可打开的 HTML 文件或实际设计结果链接，再继续原已授权的购物车流程；不能仅宣称已生成。选择不查看时，不读取结果、不渲染 HTML，直接继续原流程。两者都不新增一般继续确认，也不代表最终提交同意。
3. 区分设计结果和实验数据报告。查看设计结果使用只读 `get_order_design_result`，传入完整原签名 `workflow_context`、当前 JWT 和会话语言；工具核验本次订单后读取 `/order/rushData/report?rushDataServiceId=<签名中的服务 ID>`；该接口直接返回后台结果 ZIP 中的 `report.html` 内容，客户端不接收或解压 ZIP。收到 `status=design_result_ready` 后，客户端将 `html` 按返回的 `filename` 保存为带 BOM 的 UTF-8（`utf-8-sig`），保持 HTML 内容原样以免原字符集声明导致乱码，并交付可点击文件或可用预览；仅展示代码、登录页或“已生成”不算交付。不得用订单号、保存回执、`/inspectionReportHtml` 或 `get_report_results` 实验报告充当设计结果。若读取、渲染或交付失败，解释已确认原因并保留订单，通过单项选择询问“重试读取设计结果”或“继续下单”（英文“Retry reading the design result”或“Continue ordering”）；只有客户选重试才重试失败步骤：实际读取失败才再次只读请求，本地保存或交付失败则复用已返回的 HTML，不自动重试或重跑设计。查看选择和交付状态保存在客户端外层，完整保留原签名 `workflow_context` 与当前 JWT。独立的实验数据报告仍需实际实验数据；其 JSON 查询及 `auto_html_report` HTML 生成流程不用于替代此处的设计结果。
4. 设计保存确认、上述查看选择及必要交付完成后，继续已授权的购物车流程，复用已有产品资料，只补问缺项。是否接收实物由客户明确选择；只需数据时可解释不收实物的选项，不默认 `shippingRequired=false`。已有地址绑定规则继续按接口执行。
5. 提交前核对具体订单、权威报价和折扣，确认客户的 PO 及真实公司信息是否已具备，并获得本次提交确认。`hasCompany=true`、`canSubmit=true`、表单填完、此前授权设计或查看/跳过设计 HTML，都不能替代这次确认。未知或缺少必要信息时，先请业务方人工核实，不自行推断已满足。
6. `submit/batch` 是提交订单等待人工确认，不是实际支付，也不是生产启动。MCP 当前没有 PO 参数或生产确认工具，不新增猜测字段，不声称已验证 PO 有效性。只有百英人工确认后才能推进生产。

交互式 CLI 在设计保存后询问查看选择；非交互 `run(args, business_token)` 必须在设计写入前显式指定 `--design-result view` 或 `--design-result skip`，缺少选择即停止，不能默认不查看。`--design-result-dir` 可指定本地 HTML 目录；`--report` 仍输出 JSON 执行结果，不是 HTML 设计结果。

## 订单阶段与进度说明

纪要的业务阶段为 **Pending Confirmation（待确认）→ In Production（生产中）→ Report（报告）→ Shipping（有实物才经过）→ Completed（完成）→ Invoice（账单）**。这是业务阶段说明，不是已经核实的 API 枚举映射，也不能据此推算当前订单进度。

当前 MCP 的 `get_order_cart` 只查询购物车，不是生产进度查询；`get_report_results` 也不能替代全部状态查询。向客户报告进度须依据实际返回的订单及时间，缺少字段说明时交由业务方确认，不捏造预计完成时间。

## 待核实清单

| 事项 | 需要补齐的依据 |
| --- | --- |
| Rush Data 知识库与仓库 | 周杰提供仓库；用于核对套餐、项目定义和预期结果。未接入前不声称三类 Skill 已全部打通。 |
| 抗原必填属性 | 完整字段、单位、URL 后端补全责任，以及业务完整性在何处拦截。 |
| 多个阳参 | 名称列表的请求编码、设计对象结构和后台关联条件。 |
| PO 与公司审核 | PO 在网页/后台如何采集、是否允许缺 PO 进入待确认，以及人工审核结果如何返回。 |
| 进度与报告 | 志伟补齐完整进度字段、六阶段对应枚举及时间含义；设计 HTML 已使用上述 `/order/rushData/report` 只读契约。 |
| 设计等待 / SP | 20 分钟的起止和超时语义；SP 模板列处理方式。 |

解释实验结果字段和制作实验报告 HTML 时继续使用报告 Skill 的 `references/result-schema.md`；本次设计 HTML 只使用已核实的设计结果来源。套餐知识只能说明预期数据，不能补造未返回的设计内容、检测结果或判定标准。
