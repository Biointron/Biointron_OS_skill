"""Translate application display copy only; never pass customer or catalog data here."""

from __future__ import annotations

import re


def normalize_language(language: str = "zh") -> str:
    """The caller chooses language from conversational prose, not order field values."""
    return "en" if isinstance(language, str) and language.lower().replace("_", "-").split("-")[0] == "en" else "zh"


_EN = {
    "RUSHDATA_CONTINUATION_SECRET 必须为至少 32 位的随机签名密钥。": "RUSHDATA_CONTINUATION_SECRET must be a random signing secret of at least 32 characters.",
    "RUSHDATA_BASE_URL 必须为 HTTPS API 基础地址，本机测试可用 HTTP。": "RUSHDATA_BASE_URL must be an HTTPS API base URL. HTTP is allowed for local testing.",
    "business_token 含无效字符。": "business_token contains invalid characters.",
    "RushData 超时必须是有限正数。": "The RushData timeout must be a finite positive number.",
    "RUSHDATA_TIME_ZONE 应填写 IANA 时区，例如 Asia/Shanghai 或 UTC。": "RUSHDATA_TIME_ZONE must be an IANA time zone, such as Asia/Shanghai or UTC.",
    "RUSHDATA_DRAFT_CONTRACT_CONFIRMED 只能为 true/false。": "RUSHDATA_DRAFT_CONTRACT_CONFIRMED must be true or false.",
    "本次调用必须提供 business_token，不使用服务器共享业务令牌。": "Provide business_token for this call; a shared server-side business token is not used.",
    "请在服务端配置 RUSHDATA_BASE_URL。": "Configure RUSHDATA_BASE_URL on the server.",
    "Basic：上清表达、抗体表达量（上清抗体浓度）检测和 BLI 两点结合检测。": "Basic: Supernatant expression, antibody expression level (supernatant antibody concentration) measurement, and two-point BLI binding analysis.",
    "Standard：使用纯化抗体，检测纯度和 SPR 结合特性。": "Standard: Purified antibodies with purity and SPR binding characterization.",
    "Premium：在 Standard 基础上增加热稳定性、多反应性和自身相互作用检测。": "Premium: Standard plus thermal stability, polyreactivity, and self-interaction assays.",
    "Customized：先选择样本形式，再由你逐项选择蛋白性质、结合和开发性检测。": "Customized: Choose the sample type, then select protein property, binding, and developability assays.",
    "使用我们的产品库（无需提供链接）": "Use our product catalog (no link required)",
    "提供外部产品链接": "Provide an external product link",
    "手动填写已有抗原资料": "Enter existing antigen information manually",
    "设计资料": "design information", "项目名称": "project name", "套餐或供应商货号": "package or supplier catalog number",
    "抗原数量": "number of antigens", "是否指定使用原始 DNA": "whether to use the original DNA",
    "原服务 ID": "existing service ID", "信号肽（预留）": "signal peptide (reserved)", "检测项目": "assays",
    "抗原列表": "antigen list", "设计阳参资料": "design positive control information", "抗原来源": "antigen source",
    "产品链接": "product link", "供应商名称": "supplier name", "产品规格": "product specification",
    "样品名称": "sample name", "蛋白标签": "protein tag", "蛋白浓度": "protein concentration",
    "蛋白分子量": "protein molecular weight", "样品缓冲液": "sample buffer", "购物车资料": "cart information",
    "实际项目编号": "actual project number", "是否需要发货": "whether shipping is required",
    "所选阳参名称": "selected positive control name", "抗原名称": "antigen name", "供应商货号": "supplier catalog number",
    "样品标签": "sample tag", "样品分子量": "sample molecular weight", "样品保存液": "sample storage buffer",
    "样品浓度": "sample concentration", "产品价格": "product price", "美元价格": "price in USD",
    "原始 Excel 文件名": "original Excel filename", "原始 Excel 文件内容": "original Excel file contents",
    "供应商（产品库自动带入）": "supplier (filled from the catalog)", "样本形式": "sample type",
    "蛋白性质检测": "protein property assays", "结合检测": "binding assays", "开发性检测": "developability assays",
    "服务套餐": "service package", "套餐": "package", "产品信息": "product information", "资料": "information",
    "资料阶段": "input stage", "是": "Yes", "否": "No",
    "表达上清": "Expression supernatant", "纯化后的抗体": "Purified antibody",
    "抗体表达量（上清抗体浓度）": "Antibody expression level (supernatant antibody concentration)",
    "cGE 纯度检测": "cGE purity analysis", "BLI-Octet 2 点": "BLI-Octet 2 points", "BLI-Octet 4 点": "BLI-Octet 4 points",
    "FACS-iQue 单点": "FACS-iQue 1 point", "FACS-iQue 8 点": "FACS-iQue 8 points",
    "ELISA 单点": "ELISA 1 point", "ELISA 8 点": "ELISA 8 points", "未支持的检测项目": "Unsupported assay",
    "不添加开发性检测（表达上清不支持）": "No developability assays (not supported for supernatant)",
    "继续加载更多产品": "Load more products", "更换关键词": "Change keyword",
    "请选择查询到的抗原货号及规格": "Please select an antigen catalog number and specification",
    "请输入要查询的抗原名称或关键词（例如 CD2）": "Please enter the antigen name or keyword (for example, CD2)",
    "请输入本次抗体设计表（.xlsx）的本地文件路径": "Please enter the local path to the antibody design workbook (.xlsx) for this order",
    "请选择本次套餐": "Please select a package for this order",
    "请选择 design 或 cart。": "Please select design or cart.",
    "<客户端选中产品自动回传的供应商>": "<supplier returned from the selected catalog product>",
    "<客户端选中产品自动回传的货号>": "<catalog number returned from the selected catalog product>",
    "<客户端选中产品自动回传的规格>": "<specification returned from the selected catalog product>",
    "<客户提供的样品名称>": "<sample name supplied by the customer>",
    "<客户提供的蛋白标签>": "<protein tag supplied by the customer>",
    "<客户提供的真实浓度，类型和单位须按接口确认>": "<actual concentration supplied by the customer; confirm type and units against the API>",
    "<客户提供的真实分子量，类型和单位须按接口确认>": "<actual molecular weight supplied by the customer; confirm type and units against the API>",
    "<客户提供的样品缓冲液资料>": "<sample buffer information supplied by the customer>",
    "<实际抗原名称>": "<actual antigen name>", "<实际供应商货号>": "<actual supplier catalog number>",
    "<实际供应商名称>": "<actual supplier name>", "<从已有设计详情取得>": "<from the existing design details>",
    "<原始 XLSX 的标准 Base64，仅为格式占位>": "<standard Base64 of the original XLSX; format placeholder only>",
    "客户项目名称（示例，请填写实际名称）": "Customer project name (example; enter the actual name)",
    "旧设计扩展的非空 JSON 值；准确类型、单位须后端确认，不是购物车 DTO 字段。": "Nonempty JSON value for the legacy design extension. Confirm its exact type and units with the backend; this is not a cart DTO field.",
    "按 x-options 原文展示三种方式，不改写为提供供应商名称和货号。使用我们的产品库无需客户提供链接或货号；仅提供外部产品链接方式询问链接。用户改选来源后按新方式继续，不重复询问已选来源或保留旧方式的待填问题。": "Display the three source options exactly as provided in x-options. Our catalog does not require the customer to supply a link or catalog number. Ask for a link only for the external product link option. If the customer changes source, continue with the new source and discard pending questions from the previous source.",
    "已有 HTTPS 地址，不含账号密码；仅外部产品链接方式向客户询问。": "Existing HTTPS address without embedded credentials. Ask only when the customer chooses an external product link.",
    "关键词查询后，由客户选中的真实产品自动带入，不是客户单独填写或选择的字段。": "Filled automatically from the real product selected after keyword search; do not ask the customer to enter or select this field separately.",
    " 供应商目录模式下由客户选中的实际产品自动带入，不要求客户手填。": " In catalog mode, fill this from the actual selected product; do not ask the customer to enter it manually.",
    "用户选择的业务键；真实 ID 由预检目录唯一解析，不能填写 testItemIds。": "Business keys selected by the customer. Resolve actual IDs uniquely from the preflight catalog; do not enter testItemIds.",
    "固定套餐可省略；Customized 必须紧接套餐选择，由客户依次确认样本形式、蛋白性质、结合和开发性检测，不能跳过或代选。": "Optional for fixed packages. Immediately after choosing Customized, the customer must confirm the sample type, protein property, binding, and developability assays in sequence; do not skip or choose on their behalf.",
    "至少选择一项 BINDING。": "Select at least one binding assay.",
    "至少一项蛋白性质，且 BINDING/DEVELOPABILITY 合计至少一项。": "Select at least one protein property assay and at least one binding or developability assay.",
    "仅重设计时提供原服务 ID；新建省略。正整数，上限 9223372036854775807。": "Provide the existing service ID only for redesign; omit it for new designs. A positive integer, at most 9223372036854775807.",
    "用户提供的项目昵称，去除首尾空白后 1–100 字符；保留内部空格、下划线和横杠，不是系统项目编号。": "Customer-provided project name: 1–100 characters after trimming surrounding whitespace. Preserve internal spaces, underscores, and hyphens. This is not a system project number.",
    "实际抗原数量，须与提交的 antigens JSON 条目数一致；Basic 必须为 1。": "Actual number of antigens, matching the number of entries in antigens; Basic requires exactly one.",
    "确认是否指定使用客户提供的原始 DNA；按纪要，true 时不再进行系统自身的密码子优化。结合原始文件和客户意愿确认，不凭序列外观猜测；false 有效但不得默认。": "Confirm whether to use the original customer-provided DNA. When true, the system does not perform its own codon optimization. Confirm using the original file and the customer's preference; do not infer this from the sequence. False is valid but must not be selected by default.",
    "Signal Peptide（信号肽），可省略或留空；当前不支持自定义，不主动要求填写。保留原适配器枚举以兼容已有资料，不生成替代内容。": "Signal peptide: optional or blank. Custom values are not currently supported; do not proactively request it. Retain the adapter's existing enum for compatibility and do not generate replacements.",
    "旧设计扩展结构，数量与 antigenCount 相同；需业务后端确认支持。": "Legacy design extension structure, with as many entries as antigenCount; backend support must be confirmed.",
    "旧设计扩展对象数组；内部字段和必要条件须后端确认，不能套用购物车 positiveControl 字符串。": "Array of legacy design extension objects. Confirm internal fields and requirements with the backend; do not substitute the cart's positiveControl string.",
    "真实业务字段；未使用时可省略或为 null，不猜测缺失数据。": "Actual product field; omit it or use null when unused. Do not guess missing data.",
    "有限 JSON 数值或 null；实际 0 保留，未知不得补 0。": "A finite JSON number or null. Preserve actual zero values; do not use zero for unknown values.",
    "URL 模式仅 productUrl 有值；产品模式需 antigenName、catalogNo、supplierName。": "In URL mode, only productUrl has a value. Product information mode requires antigenName, catalogNo, and supplierName.",
    "定位到具体抗原产品的 HTTPS 链接；URL 模式其他字段须省略或为 null，完整属性由后端或人工核实。": "HTTPS link to the specific antigen product. In URL mode, omit other fields or use null; complete attributes must be verified by the backend or a person.",
    "产品已确认的标签信息；不能根据名称猜测或自行更换标签。": "Confirmed product tag information; do not infer it from the name or substitute a different tag.",
    "实际产品分子量，保留供应商给出的单位或范围；未知不推算。": "Actual product molecular weight, preserving the supplier's units or range; do not estimate unknown values.",
    "实际产品的缓冲液配方/溶液信息（Formulation），不是储存温度等 Storage instructions；未知待核实。": "Actual product buffer formulation or solution information, not storage instructions such as temperature. Unknown information requires verification.",
    "实际产品浓度的有限数值；单位映射须后端确认，未知为 null，不将未知写成 0。": "Finite numeric value for the actual product concentration. Confirm unit mapping with the backend; use null, not zero, when unknown.",
    "实际设计详情中的项目编号；不得从项目名或订单号推断。": "Project number from the actual design details; do not infer it from a project name or order number.",
    "用户必须明确选择；false 会解除已有收件地址绑定，true 需要网站已绑定地址。不得默认。": "The customer must explicitly choose. False removes any existing shipping address association; true requires an address already linked on the website. Do not choose a default.",
    "1–3 个用户选择的购物车抗原对象，不能复制旧设计 sourceType 结构。": "One to three customer-selected cart antigen objects; do not copy the legacy design sourceType structure.",
    "推荐但可选；从本次抗体列表中由用户确认的阳性参考名称，可为空字符串，不重复填写序列等属性。当前仅支持单字符串，多个名称的编码须后端确认，不能自行拼接或改为数组。": "Recommended but optional: a positive reference name confirmed by the customer from this order's antibody list. An empty string is allowed; do not repeat sequence or other attributes. Only a single string is supported. Confirm encoding of multiple names with the backend; do not concatenate names or convert to an array.",
    "系统/后端返回的已加载真实抗原候选，跨批按供应商、货号和规格去重合并；不是向客户索要的资料，不发送给设计 API。": "Loaded real antigen candidates returned by the system/backend, merged across batches by supplier, catalog number, and specification. Do not request these from the customer or send them to the design API.",
    "查询工具返回的分页和统计元数据，连同 catalog_options 保留以生成继续加载入口；不是业务字段，不发送给设计 API。": "Search pagination and summary metadata. Retain with catalog_options to provide the load-more action; this is not business data and must not be sent to the design API.",
    "原始 .xlsx 文件名，不含目录、换行或空字符。": "Original .xlsx filename without directories, line breaks, or null characters.",
    "用户原始非空 XLSX 的标准 Base64，解码后最多 10 MiB；不接收路径或下载地址。": "Standard Base64 of the customer's original nonempty XLSX, at most 10 MiB after decoding. File paths and download URLs are not accepted here.",
    "存在不支持的字段；请只提供 schema 中声明的字段。": "Unsupported fields are present. Provide only fields declared in the schema.",
    "检测项组合不符合所选套餐；按 schema 中的套餐规则修正，不更换套餐或猜测 ID。": "The assay combination does not match the selected package. Correct it using the schema's package rules; do not change the package or guess IDs.",
    "BRD101 必须且仅有一个抗原。": "Basic requires exactly one antigen.",
    "数组长度必须等于 antigenCount。": "The number of entries must equal antigenCount.",
    "请先输入抗原关键词查询产品库，再选择返回的货号和规格；供应商等字段自动带入，无需提供链接。": "First search the product catalog with an antigen keyword, then select a returned catalog number and specification. Supplier information is filled automatically; no link is required.",
    "所选来源要求该字段为非空值；准确类型须业务后端确认。": "The selected source requires a nonempty value for this field. Confirm its exact type with the business backend.",
    "扩展内容必须是有限数值组成的有效 JSON；不回显提交内容。": "Extension content must be valid JSON with finite numbers; submitted values are not echoed.",
    "URL 模式只能 productUrl 有值，其他字段须省略或为 null。": "In URL mode, only productUrl may have a value; omit other fields or use null.",
    "产品模式要求该字段为非空文本。": "Product information mode requires nonempty text for this field.",
    "购物车资料未通过执行器的当前字段规则，请按 schema 核实。": "Cart information does not meet the executor's current field rules. Check it against the schema.",
    "自定义套餐需要先确定样本形式，请选择表达上清或纯化后的抗体。": "Choose a sample type for Customized first: expression supernatant or purified antibody.",
    "表达上清与纯化后的抗体互斥，请只选择一种样本形式。": "Expression supernatant and purified antibody are mutually exclusive. Select one sample type.",
    "请由客户选择并确认这一类检测项目；不检测时也须明确选择，不得跳过或代填。": "The customer must select and confirm this assay category, including an explicit choice when no assay is needed. Do not skip or choose on their behalf.",
    "请从可选检测项目中选择，不要填写其他类型的数据。": "Choose from the available assays; do not enter other types of data.",
    "同一个检测项目不能重复选择，请去掉重复项。": "An assay cannot be selected twice. Remove the duplicates.",
    "本组至少需要选择一个检测项目。": "Select at least one assay in this category.",
    "结合检测与开发性检测不能同时不选，请在其中至少选择一项。": "Binding and developability cannot both be empty. Select at least one assay from either category.",
    " 可多选；": " Multiple selections are allowed. ", "至少选择一项。": "Select at least one.",
    "不需要时请明确选择不检测。": "Explicitly choose no assay if none is needed.",
    "BLI 2/4 点、FACS 单/8 点、ELISA 单/8 点以及两个 SPR 平台均允许同时选择。": "You may select both BLI 2/4-point variants, both FACS 1/8-point variants, both ELISA 1/8-point variants, and both SPR platforms together.",
    "百英产品库未找到匹配产品。": "No matching products were found in the Biointron catalog.",
    " 已读取全部页面。": " All pages have been read.",
    " 已读至末页；本批不包含此前页面。": " The last page has been reached; earlier pages are not included in this batch.",
    " 部分页面或产品资料存在问题，请查看具体说明；可选规格数不等于匹配产品总数。": " Some pages or product details have issues; see the details. The number of selectable specifications is not the total number of matching products.",
    "产品库分页统计在查询期间发生变化，已停止合并；不能将已有结果视为完整目录。": "Catalog pagination counts changed during the search. Loading has stopped; the results already loaded cannot be treated as the complete catalog.",
    "后续页面只返回了已加载的产品规格，已停止合并；请核对分页，不能确认目录已完整加载。": "A later page returned only previously loaded specifications. Loading has stopped; check pagination before treating the catalog as complete.",
    "本次产品资料较大，已停止合并；请缩小关键词或使用更小的每页数量重新查询。": "The product information is too large for this batch. Loading has stopped; narrow the keyword or use a smaller page size for a new search.",
    "请输入 1–255 个字符的抗原关键词，例如 CD2。": "Enter an antigen keyword of 1–255 characters, such as CD2.",
    "产品库页码必须为正整数。": "The catalog page number must be a positive integer.",
    "产品库每页数量必须为 1–50。": "The catalog page size must be between 1 and 50.",
    "产品库返回的分页结构不完整，请由服务维护方核对；不能把接口错误当作没有产品。": "The catalog returned incomplete pagination information. Ask the service maintainer to check it; an API error does not mean there are no products.",
    "产品记录不是对象": "The product record is not an object",
    "缺少可选择的产品规格": "No selectable product specifications were provided",
    "产品链接格式无效，已省略；仍可按货号选择产品": "The invalid product link was omitted; the product can still be selected by catalog number",
    "产品链接不可用，已省略；仍可按货号选择产品。": "The unavailable product link was omitted; the product can still be selected by catalog number.",
    "产品规格不是对象": "The product specification is not an object",
    "货号 ": "Catalog number ",
    "标签 ": "Tag ",
    "当前不是安全交互终端，已停止且未发起业务写入；请在终端运行，自动化请显式调用 run(args, business_token)。": "A secure interactive terminal is unavailable. The operation stopped without business writes. Run this in a terminal; for automation, explicitly call run(args, business_token).",
    "输入已结束或终端无法安全读取凭据，已停止；未继续发起业务写入。": "Input ended or the terminal could not read credentials securely. The operation stopped without further business writes.",
    "仅供格式参考，不能默认使用：": "Format examples only; do not use these as defaults: ",
    "请选择编号（多选用逗号分隔，不检测填 0）：": "Select option numbers (comma-separated for multiple choices; enter 0 for no assay): ",
    "请选择编号：": "Select an option number: ",
    "请输入实际值（复杂对象/数组请用 JSON）：": "Enter the actual value (use JSON for complex objects or arrays): ",
    "请填写有效且不重复的项目编号；需要检测时至少选择规定的项目数。": "Enter valid, unique option numbers and select at least the required number of assays.",
    "输入格式或选项无效，请重新填写；不会使用示例代填。": "The input format or selection is invalid. Please enter it again; examples will not be used as defaults.",
    "当前调用方未提供产品库查询能力；仍可选择已有候选，查询更多需使用已接入查询的 CLI 入口。": "Catalog search is unavailable from this caller. You may select an existing choice; use the CLI with catalog access to search for more products.",
    "请输入要查询的抗原名称或关键词（例如 CD2）：": "Enter an antigen name or keyword to search for (for example, CD2): ",
    "请输入 1–255 个字符的抗原关键词。": "Enter an antigen keyword of 1–255 characters.",
    "产品库返回的候选格式不完整，请联系服务维护方；未继续下单。": "The catalog returned incomplete choices. Contact the service maintainer; ordering has stopped.",
    "产品库没有返回可继续的页码，已停止加载；不能猜测下一页。": "The catalog did not return a valid continuation page. Loading has stopped; the next page cannot be guessed.",
    "部分查询或产品资料存在问题，已保留成功加载的候选；不能将当前可选数量当作全部匹配结果。": "Some searches or product details have issues. Successfully loaded choices have been retained; their count is not the total number of matches.",
    "未完成原因：": "Reason loading did not complete: ",
    "仍有结果未加载，可继续加载更多产品。": "More results remain. You may load more products.",
    "当前查询已到末页；资料不完整的产品或规格不计入可选数量。": "The last page has been reached. Products or specifications with incomplete details are excluded from the selectable count.",
    "当前没有可选产品，可更换关键词。": "No products are currently selectable. You may change the keyword.",
    "选择产品编号，0 更换关键词": "Select a product number, 0 to change the keyword",
    "，N 继续加载更多产品": ", N to load more products",
    "，Q 结束输入：": ", Q to finish: ",
    "当前调用方未提供关键词查询能力；可选择已有产品或结束输入。": "Keyword search is unavailable from this caller. Select an existing product or finish.",
    "用户结束了产品选择；未继续发起业务写入。": "Product selection was ended by the user. No further business writes were made.",
    "请选择已加载产品编号或所列操作。": "Select a loaded product number or one of the listed actions.",
    "当前资料无法形成可回答的问题，已停止且未发起业务写入。": "The current information cannot produce an answerable question. The operation stopped without business writes.",
    "当前调用方未提供产品库查询能力；请通过已接入查询的 CLI 入口继续，不能手填或编造货号。": "Catalog search is unavailable from this caller. Continue through the CLI with catalog access; catalog numbers must not be manually invented.",
    "所选产品资料未通过校验，请重新查询并选择。": "The selected product details did not pass validation. Please search and select again.",
    "请输入本次抗体设计表（.xlsx）的本地文件路径：": "Enter the local path to the antibody design workbook (.xlsx) for this order: ",
    "请提供非空且不超过 10 MiB 的原始 XLSX 文件。": "Provide the original, nonempty XLSX file, no larger than 10 MiB.",
    "文件无法读取，请重新输入本次设计表的本地文件路径。": "The file could not be read. Enter the local path to this order's design workbook again.",
    "本项资料未通过校验，请重新填写；通过后再进入下一项。": "This information did not pass validation. Enter it again before moving to the next item.",
    "请求 JSON 路径（可留空，改用问答填写；原文件不会修改）：": "Request JSON path (leave blank to answer questions; the original file will not be changed): ",
    "请求文件无法读取、解析或不是 JSON 对象，请重新选择路径或留空填写。": "The request file could not be read or parsed as a JSON object. Enter another path or leave it blank to answer questions.",
    "原始文件无法读取，或不是非空且不超过 10 MiB 的 .xlsx，请重新输入本地文件路径。": "The original file could not be read or is not a nonempty .xlsx file no larger than 10 MiB. Enter the local file path again.",
    "请输入本次明确选中的订单号，多个以空格或逗号分隔：": "Enter the order numbers explicitly selected for this operation, separated by spaces or commas: ",
    "Biointron Account 与 App Key 可在 https://os.biointron.com/ 核实；仅用于本次执行，不写入请求文件或报告。": "Verify your Biointron Account and App Key at https://os.biointron.com/. They are used only for this invocation and are not written to request files or reports.",
    "本次已有 JWT（必填，不回显、不保存）：": "Existing JWT for this invocation (required; hidden and not saved): ",
    "Biointron Account（必填）：": "Biointron Account (required): ",
    "App Key（必填）：": "App Key (required): ",
    "非交互 CLI 未注入本次凭据，已停止且未读取输入；自动化请调用 run(args, business_token)，不使用固定环境令牌。": "No credentials were injected into this noninteractive CLI invocation. It stopped without reading input. For automation, call run(args, business_token); a fixed environment token is not used.",
    "用户结束了输入或执行；业务若已开始则结果可能未确认，请先查询，不要自动重试。": "The user ended input or execution. If business processing had begun, its outcome may be unconfirmed. Query the status first; do not retry automatically.",
    "请先配置 RUSHDATA_BASE_URL；尚未请求登录或业务接口。": "Configure RUSHDATA_BASE_URL first. No login or business API request has been sent.",
    "Biointron Account 或 App Key 格式无效，请重新填写。": "The Biointron Account or App Key format is invalid. Enter it again.",
    "Biointron Account / App Key 换取业务令牌失败；未继续请求业务接口。": "The Biointron Account / App Key exchange for a business token failed. No business API request followed.",
    "登录响应超过大小限制；未继续请求业务接口。": "The login response exceeded the size limit. No business API request followed.",
    "登录响应未确认成功；请核对 Biointron Account 和 App Key，未继续请求业务接口。": "The login response did not confirm success. Check the Biointron Account and App Key. No business API request followed.",
    "登录响应缺少有效业务令牌；未继续请求业务接口。": "The login response did not include a valid business token. No business API request followed.",
    "登录请求失败、超时或响应格式无效；未重试，也未继续请求业务接口。": "The login request failed, timed out, or returned an invalid response. It was not retried, and no business API request followed.",
    "正在进行订单设计，预计需要较长时间，请耐心等待。\n\nBiointron provides high-throughput antibody expression and profiling.\n\n- **10,000 / day** — Antibodies expressed\n- As fast as **3 days** — CHO cell expression\n- **30+** — Developability assay readouts\n\n设计完成后，我会继续反馈结果。": "Your order design is in progress and may take some time. Please wait.\n\nBiointron provides high-throughput antibody expression and profiling.\n\n- **10,000 / day** — Antibodies expressed\n- As fast as **3 days** — CHO cell expression\n- **30+** — Developability assay readouts\n\nI will share the results when the design is complete.",
}


def localize_text(text: str, language: str = "zh") -> str:
    """Translate exact application-owned copy; unknown strings remain intact."""
    if normalize_language(language) == "zh":
        return text
    if text in _EN:
        return _EN[text]
    # These schema descriptions append one fixed catalog-mode note.
    suffix = " 供应商目录模式下由客户选中的实际产品自动带入，不要求客户手填。"
    if text.endswith(suffix):
        return localize_text(text[:-len(suffix)], language) + _EN[suffix]
    return text


def localize_catalog_summary(text: str, language: str = "zh") -> str | None:
    """Render known saved summaries in either language; flag unknown copy for review."""
    language = normalize_language(language)
    empty = "百英产品库未找到匹配产品。"
    if text in (empty, _EN[empty]):
        return localize_text(empty, language)
    complete = " 已读取全部页面。"
    last_page = " 已读至末页；本批不包含此前页面。"
    issues = " 部分页面或产品资料存在问题，请查看具体说明；可选规格数不等于匹配产品总数。"
    patterns = {
        "zh": (
            r"百英产品库共 (?P<total>\d+) 个匹配产品；本次读取第 (?P<first>\d+)–(?P<last>\d+) 页的 "
            r"(?P<records>\d+) 条产品记录，整理出 (?P<products>\d+) 款可选产品、(?P<options>\d+) 个规格选项。"
            r"(?P<paging> 尚未加载完，可从第 \d+ 页继续。| 已读取全部页面。| 已读至末页；本批不包含此前页面。)"
            r"(?P<issues> 部分页面或产品资料存在问题，请查看具体说明；可选规格数不等于匹配产品总数。)?"),
        "en": (
            r"The Biointron catalog contains (?P<total>\d+) matching products\. This batch read (?P<records>\d+) product records "
            r"from pages (?P<first>\d+)–(?P<last>\d+), with (?P<products>\d+) selectable products and (?P<options>\d+) specification options\."
            r"(?P<paging> More results remain; continue from page \d+\.| All pages have been read\.|"
            r" The last page has been reached; earlier pages are not included in this batch\.)"
            r"(?P<issues> Some pages or product details have issues; see the details\. "
            r"The number of selectable specifications is not the total number of matching products\.)?"),
    }
    for source_language, pattern in patterns.items():
        match = re.fullmatch(pattern, text)
        if not match:
            continue
        if source_language == language:
            return text
        fields = match.groupdict()
        if language == "en":
            result = ("The Biointron catalog contains {total} matching products. This batch read {records} product records "
                      "from pages {first}–{last}, with {products} selectable products and {options} specification options.").format(**fields)
        else:
            result = ("百英产品库共 {total} 个匹配产品；本次读取第 {first}–{last} 页的 "
                      "{records} 条产品记录，整理出 {products} 款可选产品、{options} 个规格选项。").format(**fields)
        more = re.fullmatch(
            r" 尚未加载完，可从第 (\d+) 页继续。" if source_language == "zh" else
            r" More results remain; continue from page (\d+)\.", fields["paging"])
        if more:
            result += (f" More results remain; continue from page {more.group(1)}." if language == "en" else
                       f" 尚未加载完，可从第 {more.group(1)} 页继续。")
        else:
            paging = complete if fields["paging"] in (complete, _EN[complete]) else last_page
            result += localize_text(paging, language)
        return result + (localize_text(issues, language) if fields["issues"] else "")
    return None
