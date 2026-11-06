"""Local input guidance; no credentials, network, configuration reads, or writes."""

from __future__ import annotations

import base64
import binascii
from copy import deepcopy
import json
import math
from typing import Any
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, validators

from .client import (
    BASIC_DESCRIPTION, BINDING, CATEGORIES, CUSTOM_ITEMS, DEVELOPABILITY, FIXED_ITEMS, ITEM_LABELS, MAX_FILE_BYTES, PACKAGE_DISPLAY_TEXT,
    RushDataClient, RushDataError, _positive_id, _selection, custom_selection_errors,
)
from .workbook import count_antibody_records
from .localization import localize_catalog_summary, localize_text, normalize_language


MAX_BASE64_CHARS = 4 * ((MAX_FILE_BYTES + 2) // 3)
MAX_ISSUES = 64
_OPERATIONS = {"design": "start_order_design", "cart": "add_order_to_cart"}


def _text(description, limit=None, *, nullable=False, trim=False):
    result = {"type": ["string", "null"] if nullable else "string", "description": description}
    if limit is not None:
        result["maxLength"] = limit
    if trim:
        result["x-trim"] = True
    return result


def _object(properties, required=(), **extra):
    return {"type": "object", "properties": properties, "required": list(required),
            "additionalProperties": False, **extra}


# The old design extension only validates presence/nonblank JSON values. Do not invent
# stronger field types, units, or positive-control layouts before backend confirmation.
_LEGACY_VALUE = {
    "type": ["string", "number", "boolean", "array", "object"],
    "description": "旧设计扩展的非空 JSON 值；准确类型、单位须后端确认，不是购物车 DTO 字段。",
}
_DESIGN_SOURCE_FIELDS = {
    "CUSTOMER_URL": ("referenceUrl",),
    "SUPPLIER_CATALOG": ("supplier", "catalogNumber", "specification"),
    "MANUAL": ("sampleName", "proteinTag", "proteinConcentration", "proteinMolecularWeight", "proteinBuffer"),
}
_DESIGN_SOURCE_OPTIONS = [
    {"label": "使用我们的产品库（无需提供链接）", "value": "SUPPLIER_CATALOG"},
    {"label": "提供外部产品链接", "value": "CUSTOMER_URL"},
    {"label": "手动填写已有抗原资料", "value": "MANUAL"},
]
_LABELS = {
    "data": "设计资料", "projectName": "项目名称", "catalogNumber": "套餐或供应商货号",
    "antigenCount": "抗原数量", "usingdna": "是否指定使用原始 DNA",
    "id": "原服务 ID", "sp": "信号肽（预留）", "testItems": "检测项目", "antigens": "抗原列表",
    "positiveControls": "设计阳参资料", "sourceType": "抗原来源", "referenceUrl": "产品链接",
    "supplier": "供应商名称", "specification": "产品规格", "sampleName": "样品名称",
    "proteinTag": "蛋白标签", "proteinConcentration": "蛋白浓度", "proteinMolecularWeight": "蛋白分子量",
    "proteinBuffer": "样品缓冲液", "cart_data": "购物车资料", "projectNo": "实际项目编号",
    "shippingRequired": "是否需要发货", "positiveControl": "所选阳参名称", "productUrl": "产品链接",
    "antigenName": "抗原名称", "catalogNo": "供应商货号", "supplierName": "供应商名称",
    "sampleLabel": "样品标签", "sampleMolecularWeight": "样品分子量", "sampleStorageBuffer": "样品保存液",
    "sampleConcentration": "样品浓度", "price": "产品价格", "usdPrice": "美元价格",
    "filename": "原始 Excel 文件名", "file_base64": "原始 Excel 文件内容",
}
_DESIGN_FIELD_EXAMPLES = {
    "referenceUrl": "https://example.com/antigen",
    "supplier": "<客户端选中产品自动回传的供应商>", "catalogNumber": "<客户端选中产品自动回传的货号>", "specification": "<客户端选中产品自动回传的规格>",
    "sampleName": "<客户提供的样品名称>", "proteinTag": "<客户提供的蛋白标签>",
    "proteinConcentration": "<客户提供的真实浓度，类型和单位须按接口确认>",
    "proteinMolecularWeight": "<客户提供的真实分子量，类型和单位须按接口确认>",
    "proteinBuffer": "<客户提供的样品缓冲液资料>",
}
_DESIGN_ANTIGEN_EXAMPLES = [
    {"sourceType": source, **{name: _DESIGN_FIELD_EXAMPLES[name] for name in fields}}
    for source, fields in _DESIGN_SOURCE_FIELDS.items()
]
_CART_ANTIGEN_EXAMPLES = [
    {"productUrl": "https://example.com/antigen"},
    {"antigenName": "<实际抗原名称>", "catalogNo": "<实际供应商货号>", "supplierName": "<实际供应商名称>"},
]
_DESIGN_ANTIGEN = _object({
    "sourceType": {"type": "string", "enum": list(_DESIGN_SOURCE_FIELDS),
                   "x-options": _DESIGN_SOURCE_OPTIONS,
                   "description": "按 x-options 原文展示三种方式，不改写为提供供应商名称和货号。使用我们的产品库无需客户提供链接或货号；仅提供外部产品链接方式询问链接。用户改选来源后按新方式继续，不重复询问已选来源或保留旧方式的待填问题。"},
    "referenceUrl": {**_text("已有 HTTPS 地址，不含账号密码；仅外部产品链接方式向客户询问。", 2048), "format": "https-url"},
    **{name: deepcopy(_LEGACY_VALUE) for name in (
        "supplier", "catalogNumber", "specification", "sampleName", "proteinTag",
        "proteinConcentration", "proteinMolecularWeight", "proteinBuffer",
    )},
}, ("sourceType",), **{
    # Existing design validation preserves backend-confirmed supplier extension fields.
    "additionalProperties": True,
    "x-required-by-source": {key: list(value) for key, value in _DESIGN_SOURCE_FIELDS.items()},
    "examples": _DESIGN_ANTIGEN_EXAMPLES,
})
for _name, _example in _DESIGN_FIELD_EXAMPLES.items():
    _DESIGN_ANTIGEN["properties"][_name]["examples"] = [_example]
_DESIGN_ANTIGEN["properties"]["catalogNumber"]["label"] = "供应商货号"
_DESIGN_ANTIGEN["properties"]["supplier"].update(
    label="供应商（产品库自动带入）",
    description="关键词查询后，由客户选中的真实产品自动带入，不是客户单独填写或选择的字段。")
for _field in ("catalogNumber", "specification", "referenceUrl"):
    _DESIGN_ANTIGEN["properties"][_field]["description"] += " 供应商目录模式下由客户选中的实际产品自动带入，不要求客户手填。"
_CATALOG_OPTION = _object({
    "label": {"type": "string", "minLength": 1, "maxLength": 2048},
    **{name: {"type": "string", "minLength": 1, "maxLength": 2048}
       for name in ("supplier", "catalogNumber", "specification", "referenceUrl")},
    **{name: {"type": "string", "maxLength": 2048}
       for name in ("sampleName", "proteinTag", "proteinConcentration", "proteinMolecularWeight", "proteinBuffer")},
}, ("label", "supplier", "catalogNumber", "specification"))
_CATALOG_SEARCH = _object({
    "keyword": {"type": "string", "minLength": 1, "maxLength": 255},
    "page_size": {"type": "integer", "minimum": 1, "maximum": 50},
    "total": {"type": "integer", "minimum": 0},
    "has_more": {"type": "boolean"},
    "next_page": {"type": ["integer", "null"], "minimum": 1},
    "catalog_summary": {"type": "string", "maxLength": 2000},
}, ("keyword", "page_size", "total", "has_more", "next_page", "catalog_summary"), allOf=[
    {"if": {"properties": {"has_more": {"const": True}}},
     "then": {"properties": {"next_page": {"type": "integer"}}},
     "else": {"properties": {"next_page": {"type": "null"}}}},
])
_CATEGORY_LABELS = {"SAMPLE_TYPE": "样本形式", "PROTEIN_PROPERTY": "蛋白性质检测",
                    "BINDING": "结合检测", "DEVELOPABILITY": "开发性检测"}
_TEST_ITEMS = _object({name: {
    "type": "array", "items": {"type": "string"}, "uniqueItems": True,
    "label": _CATEGORY_LABELS[name],
    "description": "用户选择的业务键；真实 ID 由预检目录唯一解析，不能填写 testItemIds。",
} for name in CATEGORIES})
_TEST_ITEMS["type"] = ["object", "null"]
_TEST_ITEMS["description"] = "固定套餐可省略；Customized 必须紧接套餐选择，先确认样本形式，再一起收集蛋白性质、结合和开发性检测，不能跳过或代选。"
_TEST_ITEMS["x-fixed-packages"] = {
    key: {category: list(items) for category, items in zip(CATEGORIES, values)}
    for key, values in FIXED_ITEMS.items()
}
_TEST_ITEMS["x-custom-package"] = {
    "supernatant": {"PROTEIN_PROPERTY": ["Titer"], "BINDING": ["FACS_iQue_1_point", "ELISA_1_point"],
                    "DEVELOPABILITY": [], "description": "至少选择一项 BINDING。"},
    "purified antibody": {"PROTEIN_PROPERTY": ["cGE", "SEC_HPLC", "SEC_UPLC"],
                          "BINDING": sorted(BINDING), "DEVELOPABILITY": sorted(DEVELOPABILITY),
                          "description": "至少一项蛋白性质，且 BINDING/DEVELOPABILITY 合计至少一项。"},
}
_DESIGN_DATA = _object({
    "id": {"type": ["integer", "string"], "description": "仅重设计时提供原服务 ID；新建省略。正整数，上限 9223372036854775807。",
           "x-existing-identity": True},
    "catalogNumber": {"type": "string", "enum": [*FIXED_ITEMS, "BRD401"], "label": "套餐",
                      "description": f"先介绍四种套餐再请用户选择。Basic：{BASIC_DESCRIPTION}"
                                     "Standard 使用纯化抗体，提供纯度和结合特性数据；Premium 在此基础上增加热稳定性、多反应性和自身相互作用信息；"
                                     "Customized 按需求组合检测。具体价格和折扣以后台报价为准。界面显示套餐名称，不展示内部编码，不默认或代选。",
                      "x-options": [{"label": text, "value": code} for code, text in PACKAGE_DISPLAY_TEXT.items()]},
    "testItems": _TEST_ITEMS,
    "projectName": {**_text("用户提供的项目昵称，去除首尾空白后 1–100 字符；保留内部空格、下划线和横杠，不是系统项目编号。", 100, trim=True), "minLength": 1,
                    "examples": ["客户项目名称（示例，请填写实际名称）"]},
    "antigenCount": {"type": "integer", "minimum": 1, "maximum": 3, "description": "实际抗原数量，须与提交的 antigens JSON 条目数一致；Basic 必须为 1。"},
    "usingdna": {"type": "boolean", "description": "确认是否指定使用客户提供的原始 DNA；按纪要，true 时不再进行系统自身的密码子优化。结合原始文件和客户意愿确认，不凭序列外观猜测；false 有效但不得默认。", "examples": [True, False]},
    "sp": {"type": "string", "enum": ["", "MGWSCIILFLVATATGVHS", "MHSSALLCCLVLLTGVRA"],
           "description": "Signal Peptide（信号肽），可省略或留空；当前不支持自定义，不主动要求填写。保留原适配器枚举以兼容已有资料，不生成替代内容。"},
    "antigens": {"type": "array", "minItems": 1, "maxItems": 3, "items": _DESIGN_ANTIGEN,
                 "description": "旧设计扩展结构，数量与 antigenCount 相同；需业务后端确认支持。",
                 "examples": [[example] for example in _DESIGN_ANTIGEN_EXAMPLES]},
    "positiveControls": {"type": "array", "items": {"type": "object"},
                         "description": "旧设计扩展对象数组；内部字段和必要条件须后端确认，不能套用购物车 positiveControl 字符串。"},
}, ("catalogNumber", "projectName", "antigenCount", "usingdna", "antigens"))
_CART_TEXT_LIMITS = {"antigenName": 255, "catalogNo": 128, "specification": 255, "productUrl": 1000,
                     "sampleLabel": 255, "sampleMolecularWeight": 200,
                     "sampleStorageBuffer": 1000, "supplierName": 255}
_CART_ANTIGEN = _object({
    **{name: _text("真实业务字段；未使用时可省略或为 null，不猜测缺失数据。", limit, nullable=True, trim=True)
       for name, limit in _CART_TEXT_LIMITS.items()},
    **{name: {"type": ["number", "null"], "description": "有限 JSON 数值或 null；实际 0 保留，未知不得补 0。"}
       for name in ("price", "usdPrice", "sampleConcentration")},
}, description="URL 模式仅 productUrl 有值；产品模式需 antigenName、catalogNo、supplierName。")
_CART_ANTIGEN["properties"]["productUrl"]["format"] = "https-url"
_CART_ANTIGEN["properties"]["productUrl"]["description"] = "定位到具体抗原产品的 HTTPS 链接；URL 模式其他字段须省略或为 null，完整属性由后端或人工核实。"
_CART_ANTIGEN["properties"]["sampleLabel"]["description"] = "产品已确认的标签信息；不能根据名称猜测或自行更换标签。"
_CART_ANTIGEN["properties"]["sampleMolecularWeight"]["description"] = "实际产品分子量，保留供应商给出的单位或范围；未知不推算。"
_CART_ANTIGEN["properties"]["sampleStorageBuffer"]["description"] = "实际产品的缓冲液配方/溶液信息（Formulation），不是储存温度等 Storage instructions；未知待核实。"
_CART_ANTIGEN["properties"]["sampleConcentration"]["description"] = "实际产品浓度的有限数值；单位映射须后端确认，未知为 null，不将未知写成 0。"
_CART_ANTIGEN["x-product-required"] = ["antigenName", "catalogNo", "supplierName"]
_CART_ANTIGEN["examples"] = _CART_ANTIGEN_EXAMPLES
_CATALOG_OPTION["properties"]["cart_data"] = deepcopy(_CART_ANTIGEN)
_CART_ANTIGEN["x-input-modes"] = [
    {"label": "产品链接", "value": "product_url", "fields": ["productUrl"]},
    {"label": "产品信息", "value": "product_fields", "fields": ["antigenName", "catalogNo", "supplierName"]},
]
for _example in _CART_ANTIGEN_EXAMPLES:
    for _name, _value in _example.items():
        _CART_ANTIGEN["properties"][_name]["examples"] = [_value]
_CART_DATA = _object({
    "projectNo": {**_text("实际设计详情中的项目编号；不得从项目名或订单号推断。", 100, trim=True),
                  "minLength": 1, "x-existing-identity": True, "examples": ["<从已有设计详情取得>"]},
    "shippingRequired": {"type": "boolean", "description": "用户必须明确选择；false 会解除已有收件地址绑定，true 需要网站已绑定地址。不得默认。",
                         "examples": [True, False]},
    "antigens": {"type": "array", "minItems": 1, "maxItems": 3, "items": _CART_ANTIGEN,
                 "description": "1–3 个用户选择的购物车抗原对象，不能复制旧设计 sourceType 结构。",
                 "examples": [[example] for example in _CART_ANTIGEN_EXAMPLES]},
    "positiveControl": {"type": "string", "description": "推荐但可选；从本次抗体列表中由用户确认的阳性参考名称，可为空字符串，不重复填写序列等属性。当前仅支持单字符串，多个名称的编码须后端确认，不能自行拼接或改为数组。"},
}, ("projectNo", "shippingRequired", "antigens"))
_SCHEMAS = {
    "design": _object({
        "data": _DESIGN_DATA,
        "catalog_options": {"type": "array", "items": _CATALOG_OPTION,
                            "description": "系统/后端返回的已加载真实抗原候选，跨批按供应商、货号和规格去重合并；不是向客户索要的资料，不发送给设计 API。"},
        "catalog_search": {**_CATALOG_SEARCH,
                           "description": "查询工具返回的分页和统计元数据，连同 catalog_options 保留以生成继续加载入口；不是业务字段，不发送给设计 API。"},
        "filename": {"type": "string", "description": "原始 .xlsx 文件名，不含目录、换行或空字符。", "examples": ["customer.xlsx"]},
        "file_base64": {"type": "string", "minLength": 1, "maxLength": MAX_BASE64_CHARS,
                        "contentEncoding": "base64", "description": "用户原始非空 XLSX 的标准 Base64，解码后最多 10 MiB；不接收路径或下载地址。",
                        "examples": ["<原始 XLSX 的标准 Base64，仅为格式占位>"]},
    }, ("data", "filename", "file_base64")),
    "cart": _object({"cart_data": _CART_DATA}, ("cart_data",)),
}
# 同名字段在设计套餐与抗原供应商目录中含义不同，面向用户分别显示。
_DESIGN_DATA["properties"]["catalogNumber"]["label"] = "服务套餐"
_DESIGN_ANTIGEN["properties"]["catalogNumber"]["label"] = "供应商货号"

def _label_fields(node):
    for name, child in node.get("properties", {}).items():
        child.setdefault("label", _LABELS.get(name, name))
        _label_fields(child)
    if "items" in node:
        _label_fields(node["items"])


for _schema in _SCHEMAS.values():
    _schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    _schema["examples_are_placeholders"] = True
    _label_fields(_schema)

# JSON Schema normally considers 48.0 an integer. Match the execution client's exact
# Python integer checks and reject booleans/non-finite numbers without echoing values.
_TYPES = Draft202012Validator.TYPE_CHECKER.redefine_many({
    "integer": lambda checker, value: type(value) is int,
    "number": lambda checker, value: type(value) in (int, float) and (type(value) is int or math.isfinite(value)),
})
_Validator = validators.extend(Draft202012Validator, type_checker=_TYPES)


def _localize_examples(value, language):
    """Only call for application-owned schema placeholders, never submitted values."""
    if isinstance(value, str):
        return localize_text(value, language)
    if isinstance(value, list):
        return [_localize_examples(item, language) for item in value]
    if isinstance(value, dict):
        return {key: _localize_examples(item, language) for key, item in value.items()}
    return value


def _localize_metadata(node, language):
    for name in ("label", "description"):
        if name in node:
            node[name] = localize_text(node[name], language)
    for name in ("x-options", "x-input-modes"):
        for option in node.get(name, []):
            option["label"] = localize_text(option["label"], language)
    if "examples" in node:
        node["examples"] = _localize_examples(node["examples"], language)
    for child in node.get("properties", {}).values():
        _localize_metadata(child, language)
    for child in node.get("x-custom-package", {}).values():
        _localize_metadata(child, language)
    for name in ("items", "if", "then", "else"):
        if isinstance(node.get(name), dict):
            _localize_metadata(node[name], language)
    for child in node.get("allOf", []):
        _localize_metadata(child, language)
    return node


def schema_for_stage(stage: str, *, language: str = "zh") -> dict:
    """Return an independent schema copy; callers cannot mutate later requests."""
    if not isinstance(stage, str) or stage not in _SCHEMAS:
        raise ValueError("stage must be design or cart.")
    schema = _localize_metadata(deepcopy(_SCHEMAS[stage]), language)
    if stage == "design" and normalize_language(language) == "en":
        schema["properties"]["data"]["properties"]["catalogNumber"]["description"] = (
            "Introduce all four packages using their exact option labels, then ask the customer to choose. "
            "Show package names, not internal codes; do not choose a default. Pricing and discounts depend on the backend quote.")
    return schema


def _normalize(value, schema):
    if isinstance(value, str) and schema.get("x-trim"):
        value = value.strip()
        # 与购物车执行器一致：可空文本的空串等同未填写；不把 false 或数字 0 当成缺项。
        return None if not value and "null" in schema.get("type", []) else value
    if isinstance(value, dict):
        props = schema.get("properties", {})
        return {key: _normalize(item, props[key]) if key in props else item for key, item in value.items()}
    if isinstance(value, list) and "items" in schema:
        return [_normalize(item, schema["items"]) for item in value]
    return value


def _node_and_path(parts, schema):
    safe = []
    for part in parts:
        if isinstance(part, str) and part in schema.get("properties", {}):
            safe.append(part)
            schema = schema["properties"][part]
        elif type(part) is int and part >= 0 and "items" in schema:
            safe.append(str(part))
            schema = schema["items"]
        else:
            break  # Arbitrary extension keys may themselves contain secrets.
    return schema, "/" + "/".join(safe) if safe else ""


def _https(value, *, no_whitespace=False):
    if not isinstance(value, str):
        return False
    try:
        url = urlsplit(value)
        return bool(url.scheme == "https" and url.hostname and url.username is None and url.password is None
                    and (not no_whitespace or not any(char.isspace() for char in value)))
    except ValueError:
        return False


def _question(path, node, *, title=None, language="zh"):
    node = _localize_metadata(deepcopy(node), language)
    english = normalize_language(language) == "en"
    if title is None and path == "/data/catalogNumber":
        title = localize_text("请选择本次套餐", language)
    options = deepcopy(node.get("x-options", []))
    if not options and "enum" in node:
        options = [{"label": str(value), "value": value} for value in node["enum"]]
    if not options and node.get("type") == "boolean":
        options = [{"label": localize_text("是", language), "value": True},
                   {"label": localize_text("否", language), "value": False}]
    types = node.get("type", [])
    types = [types] if isinstance(types, str) else types
    kind = "single_select" if options else "fields" if any(item in types for item in ("object", "array")) else "text"
    label = node.get("label", localize_text("资料", language))
    parts = path.strip("/").split("/")
    if len(parts) > 3 and parts[1] == "antigens" and parts[2].isdigit():
        label = f"{label} for antigen {int(parts[2]) + 1}" if english else f"第 {int(parts[2]) + 1} 个抗原的{label}"
    result = {
        "id": path.strip("/").replace("/", "_") or "input",
        "field_paths": [path], "title": title or (
            f"Please {'select' if options else 'enter'} {label}" if english else f"请{'选择' if options else '填写'}{label}"),
        "input_type": kind, "examples": deepcopy(node.get("examples", [])),
    }
    if options:
        result["options"] = options
    elif kind == "text":
        result["allow_free_text"] = True
    if node.get("description"):
        result["description"] = node["description"]
    return result


def _custom_question(data, language="zh"):
    selected = data.get("testItems")
    errors = custom_selection_errors(selected, language=language)
    if not errors:
        return None
    category = next(iter(errors))
    return _custom_category_question(selected, category, errors[category], language)


def _custom_category_question(selected, category, description="", language="zh"):
    path = "/data/testItems/" + category
    question = _question(path, _TEST_ITEMS["properties"][category], language=language,
                         title=("Please select " + localize_text(_CATEGORY_LABELS[category], language) + " for Customized"
                                if normalize_language(language) == "en" else "请选择自定义套餐的" + _CATEGORY_LABELS[category]))
    question["description"] = description
    if category == "SAMPLE_TYPE":
        question.update(input_type="single_select", options=[
            {"label": localize_text(ITEM_LABELS[sample], language), "value": [sample]} for sample in CUSTOM_ITEMS])
        return question
    sample = selected["SAMPLE_TYPE"][0]
    choices = CUSTOM_ITEMS[sample][category]
    if not choices or (category == "PROTEIN_PROPERTY" and sample == "supernatant"):
        question.update(input_type="single_select", options=[{
            "label": (", " if normalize_language(language) == "en" else "、").join(
                localize_text(ITEM_LABELS[item], language) for item in choices
            ) if choices else localize_text("不添加开发性检测（表达上清不支持）", language),
            "value": list(choices),
        }])
    else:
        minimum = int(category == "PROTEIN_PROPERTY" or (category == "BINDING" and sample == "supernatant")
                      or (category == "DEVELOPABILITY" and selected.get("BINDING") == []))
        question.update(input_type="multi_select", allow_free_text=True, min_selections=minimum,
                        allow_empty=not minimum,
                        options=[{"label": localize_text(ITEM_LABELS[item], language), "value": item} for item in choices])
        question["description"] += localize_text(" 可多选；", language) + localize_text(
            "至少选择一项。" if minimum else "不需要时请明确选择不检测。", language)
        if category == "BINDING":
            question["description"] += localize_text("BLI 2/4 点、FACS 单/8 点、ELISA 单/8 点以及两个 SPR 平台均允许同时选择。", language)
    return question


def _missing_custom_questions(data, language):
    selected = data.get("testItems")
    selected = selected if isinstance(selected, dict) else {}
    sample = selected.get("SAMPLE_TYPE")
    if not (isinstance(sample, list) and len(sample) == 1
            and isinstance(sample[0], str) and sample[0] in CUSTOM_ITEMS):
        return [_custom_category_question(selected, "SAMPLE_TYPE", language=language)]
    questions = []
    for category in CATEGORIES:
        if category != "SAMPLE_TYPE" and category not in selected:
            question = _custom_category_question(selected, category, language=language)
            # Cross-category constraints are checked only after collecting the whole selection.
            if question["input_type"] == "multi_select":
                question.update(min_selections=0, allow_empty=True)
            questions.append(question)
    return questions


def _catalog_label(candidate, language):
    """Rebuild only recognized UI labels, preserving all real product attributes."""
    label = candidate["label"]
    cart = candidate.get("cart_data", {})
    cart = cart if isinstance(cart, dict) else {}
    name = candidate.get("sampleName") or cart.get("antigenName")
    if not isinstance(name, str) or not name:
        return label
    tag = candidate.get("proteinTag") or cart.get("sampleLabel")
    if tag is not None and not isinstance(tag, str):
        return label

    def render(english):
        parts = [name, ("Catalog number " if english else "货号 ") + candidate["catalogNumber"],
                 candidate["supplier"], candidate["specification"]]
        if tag:
            parts.append(("Tag " if english else "标签 ") + tag)
        return " · ".join(" ".join(part.split()) for part in parts)

    translated = {"zh": render(False), "en": render(True)}
    return translated[normalize_language(language)] if label in translated.values() else label


def _catalog_question(prefix, catalog_options, catalog_search=None, *, language="zh"):
    """Ask a search keyword, then offer real products returned by the authenticated catalog tool."""
    english = normalize_language(language) == "en"
    options = []
    seen = set()
    for candidate in catalog_options:
        if candidate.get("referenceUrl") and not _https(candidate["referenceUrl"]):
            continue
        key = (candidate["supplier"], candidate["catalogNumber"], candidate["specification"])
        if key in seen:
            continue
        seen.add(key)
        product = {key: value for key, value in candidate.items() if key not in ("label", "cart_data")}
        product["sourceType"] = "SUPPLIER_CATALOG"
        label = _catalog_label(candidate, language)
        for detail in (candidate["supplier"], candidate["catalogNumber"], candidate["specification"]):
            if detail not in label:
                label += " · " + detail
        option = {"label": label, "value": product}
        if "cart_data" in candidate:
            option["cart_data"] = deepcopy(candidate["cart_data"])
        options.append(option)
    question = {"id": prefix.strip("/").replace("/", "_") + "_product",
                "field_paths": [prefix], "title": localize_text("请选择查询到的抗原货号及规格", language),
                "allow_free_text": False,
                "description": "展示关键词查询返回的真实名称、货号、标签和规格，客户选择后自动带入供应商等资料。"
                               "完整列出后台返回的可选候选，不擅自按关键词精确匹配、供应商或物种再次筛选；可说明模糊匹配，未经客户确认不隐藏结果。"
                               "cart_data 单独保留供加购复用，不放入设计抗原对象；不编造货号或要求客户补链接。"}
    if english:
        question["description"] = (
            "Show the actual names, catalog numbers, tags, and specifications returned by the search. "
            "After selection, fill supplier information automatically. Preserve all returned candidates, including fuzzy "
            "matches and different suppliers or species; ask the customer before applying additional filters. "
            "Keep cart_data separately for cart reuse. Do not invent catalog numbers or ask for a missing link. ")
    if options or catalog_search:
        product_count = len({(option["value"]["supplier"], option["value"]["catalogNumber"]) for option in options})
        summary = (f"Loaded {product_count} selectable products with {len(options)} specifications. " if english
                   else f"已加载可选产品 {product_count} 款、规格 {len(options)} 个。")
        if catalog_search:
            summary = (f"The current source has {catalog_search['total']} matching products. " if english
                       else f"当前来源共匹配 {catalog_search['total']} 款产品；") + summary
            batch_summary = localize_catalog_summary(catalog_search["catalog_summary"], language)
            if english:
                if catalog_search["has_more"]:
                    summary += "More results remain to be loaded. "
                elif batch_summary is not None:
                    summary += "The last search page has been reached; products or specifications with incomplete information are excluded from selectable counts. "
                if batch_summary is not None:
                    summary += "Search batch details: " + batch_summary
                else:
                    summary += ("The saved batch explanation is not recognized. Check the original backend result for any "
                                "incomplete loads or other issues; completeness is unconfirmed. ")
            else:
                if catalog_search["has_more"]:
                    summary += "仍有结果未加载。"
                elif batch_summary is not None:
                    summary += "当前查询已到末页；资料不完整的产品或规格不计入可选数量。"
                if batch_summary is not None:
                    summary += "本批查询说明：" + batch_summary
                else:
                    summary += "无法识别保存的批次说明；请核对原始后台查询结果中的部分加载原因或其他问题，当前不能确认结果已完整加载。"
            question["catalog_search"] = deepcopy(catalog_search)
            question["catalog_search"]["catalog_summary"] = batch_summary if batch_summary is not None else summary
            if catalog_search["has_more"]:
                options.append({"label": localize_text("继续加载更多产品", language), "value": {"catalog_action": "load_more"},
                                "client_action": "search_order_antigens",
                                "arguments": {"keyword": catalog_search["keyword"], "page_no": catalog_search["next_page"],
                                              "page_size": catalog_search["page_size"], "language": normalize_language(language)}})
        else:
            summary += ("Total and pagination information were not provided; these are not necessarily all matching results. " if english
                        else "未提供查询总数和分页信息，不代表全部匹配结果。")
        options.append({"label": localize_text("更换关键词", language), "value": {"catalog_action": "change_keyword"},
                        "client_action": "ask_catalog_keyword"})
        question.update(input_type="single_select", ui_only=True, client_action="select_catalog_product", options=options)
        question["description"] = summary + question["description"] + (
            "Navigation actions are not product information. Use next_page and page_size unchanged when loading more, "
            "merging candidates by supplier, catalog number, and specification. Clear old candidates and pagination when "
            "changing keywords. Only put the selected real product in the antigen; never put catalog_action or catalog_search in the design."
            if english else
            "导航动作不是产品资料：继续加载时原样使用 next_page 和 page_size，按供应商、货号、规格合并去重候选；"
            "更换关键词时清除旧候选和分页后重新提问。只将客户选中的真实产品写入抗原，不将 catalog_action、catalog_search 写入设计对象。")
    else:
        question.update(input_type="text", ui_only=True, client_action="search_order_antigens",
                        credential_check_required=True, allow_free_text=True,
                        title=localize_text("请输入要查询的抗原名称或关键词（例如 CD2）", language), examples=["CD2"])
        question["description"] = ("先检查当前客户有效 JWT，或已有 Biointron Account 和 App Key；仅补问缺少的凭据并兑换，再询问关键词。"
                                   "通过原生文本弹窗或 CLI input 收集关键词，调用 search_order_antigens 查询百英自有产品库；"
                                   "关键词只作为查询参数，不写入设计对象。展示真实货号供选择；无匹配时换关键词，有更多结果时允许翻页。"
                                   "没有专用产品选择界面也能使用普通弹窗或 CLI 编号菜单完成，不等待额外选择器。")
        if english:
            question["description"] = (
                "Check for the current customer's valid JWT or existing Biointron Account and App Key. Ask only for missing "
                "credentials and exchange them before asking for a keyword. Use a native text dialog or CLI input, then call "
                "search_order_antigens to search our catalog. Keywords are search parameters, not design data. Show actual "
                "catalog numbers for selection; allow changing keywords when no results match and loading more when available. "
                "A normal dialog or numbered CLI menu is sufficient; do not wait for a dedicated product selector.")
    return question


QUESTION_DELIVERY_INSTRUCTIONS = (
    "For collecting, needs_input or needs_credentials, call the actual question tool with the current "
    "interaction.native_question batch and wait for all its answers. Independent questions share one call; "
    "resolve branch choices and credential prerequisites before dependent questions. "
    "In Codex, when request_user_input_async is available, call it with interaction.native_question; "
    "a text question omits options and still opens a card. Never limit cards to multiple-choice fields. "
    "Use only a question tool available in the current mode; do not switch to Plan mode to ask. "
    "Map selected labels to their original values, merge all answers and continue collecting without "
    "validating each ordinary answer. Do not repeat a pending question or replace it with a checklist. "
    "A CLI with no native question tool collects the whole batch through interactive terminal prompts. "
    "Only if neither native questions nor an interactive terminal is available, explain that limitation and ask "
    "the current batch in text. The full schema, issues and missing_fields are internal diagnostics, "
    "not a questionnaire to paste to the customer. Keep API addresses out of customer questions; "
    "use the MCP response's server connection metadata, not the client's local config search. "
    "Honor a current question's credential prerequisite, reusing known credentials and asking only for a missing field."
)


def native_question_arguments(question: dict, *, language: str = "zh") -> dict:
    """Arguments for an available Codex text/choice question tool, not a claim that it ran."""
    prompt = {"title": question["title"]}
    options = question.get("options", [])
    if options and question.get("input_type") == "multi_select":
        instruction = ("Enter one or more assay names separated by commas." if language == "en" else
                       "请输入一个或多个检测名称，多个名称用逗号分隔。")
        if question.get("allow_empty"):
            instruction += " Enter None if no assay is needed." if language == "en" else "不需要检测时请输入“不检测”。"
        prompt["title"] += "\n" + instruction + "\n" + "\n".join("- " + item["label"] for item in options)
    elif options:
        prompt["options"] = [item["label"] for item in options]
    return {"questions": [prompt]}


def _question_batch(questions):
    """Keep branch and authenticated-catalog prerequisites ahead of dependent fields."""
    for path in ("/data/catalogNumber", "/data/testItems/SAMPLE_TYPE"):
        gated = [question for question in questions if path in question["field_paths"]]
        if gated:
            return gated
    custom = [question for question in questions if question["field_paths"][0].startswith("/data/testItems/")]
    if custom:
        return custom
    if any("/data/antigenCount" in question["field_paths"] for question in questions):
        return [question for question in questions if not question["field_paths"][0].startswith("/data/antigens")]
    sources = [question for question in questions
               if question["field_paths"][0].endswith("/sourceType") or question.get("fields_by_option")]
    if sources:
        return [question for question in questions
                if question in sources or "/antigens" not in question["field_paths"][0]]
    catalog = [question for question in questions
               if question.get("client_action") in ("search_order_antigens", "select_catalog_product")]
    return catalog[:1] if catalog else questions


def _interaction(stage, issues, supplied, *, language="zh", batch_questions=False, validation_deferred=False):
    """Recommend questions to the host AI; never open a UI or fill example values itself."""
    questions, deferred = [], []
    english = normalize_language(language) == "en"
    root_name = "data" if stage == "design" else "cart_data"
    root = supplied.get(root_name, {}) if isinstance(supplied, dict) else {}
    root = root if isinstance(root, dict) else {}
    catalog_options = supplied.get("catalog_options", []) if isinstance(supplied, dict) else []
    if not isinstance(catalog_options, list):
        catalog_options = []
    if validation_deferred:
        # Only guard the display helper's structure here; business validation belongs to the write boundary.
        catalog_options = [item for item in catalog_options if isinstance(item, dict) and all(
            isinstance(item.get(name), str) and item[name]
            for name in ("label", "supplier", "catalogNumber", "specification"))]
    else:
        catalog_options = [item for item in catalog_options if not list(_Validator(_CATALOG_OPTION).iter_errors(item))]
    catalog_search = supplied.get("catalog_search") if isinstance(supplied, dict) else None
    if catalog_search is not None:
        if validation_deferred:
            if not isinstance(catalog_search, dict) or not all(
                name in catalog_search for name in _CATALOG_SEARCH["required"]
            ) or not isinstance(catalog_search.get("catalog_summary"), str):
                catalog_search = None
        elif list(_Validator(_CATALOG_SEARCH).iter_errors(catalog_search)):
            catalog_search = None
    if stage == "design":
        deferred.extend(["/catalog_options", "/catalog_search"])
    if stage == "design" and root.get("catalogNumber") == "BRD401":
        if validation_deferred:
            custom_questions = _missing_custom_questions(root, language)
        elif batch_questions:
            selected = root.get("testItems")
            conflicts = custom_selection_errors(selected, language=language)
            categories = ["SAMPLE_TYPE"] if "SAMPLE_TYPE" in conflicts else list(conflicts)
            custom_questions = [_custom_category_question(selected, category, conflicts[category], language)
                                for category in categories]
        else:
            custom_questions = [question for question in [_custom_question(root, language)] if question]
        if custom_questions:
            questions.extend(custom_questions)
            deferred.append("/data/testItems")
    if stage == "design" and any(item["path"] in ("/filename", "/file_base64") for item in issues):
        file_issue = next(item for item in issues if item["path"] in ("/filename", "/file_base64"))
        explanation = file_issue.get("description", "") if file_issue["code"] != "missing" else ""
        questions.append({"id": "design_workbook", "field_paths": ["/file_base64"],
                          "input_type": "text", "ui_only": True, "client_action": "read_local_design_workbook",
                          "allow_free_text": True, "title": localize_text("请输入本次抗体设计表（.xlsx）的本地文件路径", language),
                          "description": explanation + (
                              " Open a native text dialog or CLI path prompt and wait for the answer; upload instructions alone are insufficient. "
                              "Use an available file picker or reuse this order's readable original attachment. The path is only for local client "
                              "reading: read the original file and supply filename and file_base64, never the path itself, to the backend. "
                              "Explain file-read failures and ask for the path again. Count antibodies on a best-effort basis; never ask the "
                              "customer for a count or Base64."
                              if english else " 实际调用原生文本提问或 CLI 路径输入并等待回答，不能只发送上传说明；无选项也要提问。"
                                         "有可用文件选择工具时可直接打开；已提供可读取的本次附件则复用，不重复索要路径。"
                                         "路径仅供客户端读取原始文件并生成 filename 和 file_base64，不能把路径直接填入 file_base64 或传给后台。"
                                         "文件读取失败时说明原因并重新询问路径；抗体数量由表格自动统计，不向客户索要数量或 Base64。"),
                          "accepted_extensions": [".xlsx"], "related_fields": ["/filename"]})
        deferred.extend(["/filename", "/file_base64"])
    array_path = f"/{root_name}/antigens"
    antigen_issues = [item for item in issues if item["path"] == array_path or item["path"].startswith(array_path + "/")]
    if antigen_issues:
        antigens = root.get("antigens")
        antigens = antigens if isinstance(antigens, list) else []
        count = root.get("antigenCount")
        slots = count if stage == "design" and type(count) is int and 1 <= count <= 3 else max(1, len(antigens))
        for index in range(min(slots, 3)):
            item = antigens[index] if index < len(antigens) else None
            prefix = f"{array_path}/{index}"
            if stage == "design":
                source = item.get("sourceType") if isinstance(item, dict) else None
                if isinstance(source, str) and source in _DESIGN_SOURCE_FIELDS:
                    if source == "SUPPLIER_CATALOG" and any(
                        issue["path"] == prefix or issue["path"].startswith(prefix + "/") for issue in antigen_issues
                    ):
                        questions.append(_catalog_question(prefix, catalog_options, catalog_search, language=language))
                        deferred.append(prefix)
                    continue
                path = prefix + "/sourceType"
                question = _question(path, _DESIGN_ANTIGEN["properties"]["sourceType"], language=language,
                                     title=(f"How would you like to provide information for antigen {index + 1}?" if english
                                            else f"第 {index + 1} 个抗原，你希望如何提供资料？"))
                question["examples"] = []
            else:
                # An existing URL or any supplied product field (including 0) already identifies the mode.
                if isinstance(item, dict) and any(
                    name in item if validation_deferred else item.get(name) is not None and item[name] != ""
                    for name in _CART_ANTIGEN["properties"]
                ):
                    continue
                question = _question(prefix, _CART_ANTIGEN, language=language,
                                     title=(f"Please select how to provide information for antigen {index + 1}" if english
                                            else f"请选择第 {index + 1} 个抗原的资料方式"))
                question.update(input_type="single_select", ui_only=True,
                                options=[{"label": localize_text(mode["label"], language), "value": mode["value"]} for mode in _CART_ANTIGEN["x-input-modes"]],
                                fields_by_option={mode["value"]: [prefix + "/" + name for name in mode["fields"]]
                                                  for mode in _CART_ANTIGEN["x-input-modes"]},
                                description=("This choice is only for step-by-step input. Ask for the actual fields of the selected mode; "
                                             "do not put this option value or sourceType in the cart DTO." if english else
                                             "此选择仅用于弹窗分步收集；继续询问所选方式的真实字段，不能把选项值或 sourceType 放入购物车 DTO。"))
            questions.append(question)
            deferred.append(prefix)
    asked = set()
    for item in issues:
        path = item["path"]
        if path == "/data/antibodyProjectCount":
            continue
        if path in asked or any(path == prefix or path.startswith(prefix + "/") for prefix in deferred):
            continue
        if path == array_path and deferred:
            continue
        # Missing parent objects are explained by their individual fields; do not ask for both.
        if any(other["path"] != path and other["path"].startswith(path + "/") for other in issues):
            continue
        asked.add(path)
        questions.append(_question(path, item, language=language))
    # 按业务字段顺序提问；抗原的来源分支不能插到套餐、项目和数量之前。
    if stage in _SCHEMAS:
        field_order = {f"/{root_name}/{name}": index for index, name in enumerate(
            _SCHEMAS[stage]["properties"][root_name]["properties"])}
        questions.sort(key=lambda question: field_order.get(
            "/".join(question["field_paths"][0].split("/")[:3]), len(field_order)))
    questions = _question_batch(questions) if batch_questions else questions[:1]
    interaction = {
        "preferred_ui": "native_question_dialog", "fallback_ui": "terminal_prompt",
        "sequential": not batch_questions, "batch": batch_questions,
        "max_questions_per_turn": max(1, len(questions)),
        "await_response": True, "resume_after_response": True,
        "examples_are_placeholders": True, "questions": questions,
        "required_action": "ask_current_question",
        "instructions": QUESTION_DELIVERY_INSTRUCTIONS + " " + (
            "Introduce packages first; Customized asks sample type before the assay categories. "
            "Collect independent questions together. Preserve supplied answers, including false, 0 and empty assay "
            "selections. Defer ordinary field validation until immediately before design or cart writes, then ask "
            "only for corrections that are needed. Collection completion is not validation or write authorization. "
            "Reuse credentials, original attachments and catalog selections. Never ask for antibody count or Base64. "
            "Keep catalog navigation out of business data, use returned next_page, and retain every returned product "
            "candidate unless the customer requests filtering. Check company permissions before submitting a design."
            if english else
            "先介绍套餐；Customized 先选样本形式，再一起收集检测类别。互不依赖的问题一批提问，"
            "保留已经填写的答案，包括 false、0 和明确不检测的空列表。普通字段在真正设计或加购前统一校验，"
            "届时只补问需要修正的项；收集齐备不等于校验通过，也不代表获得写入授权。"
            "复用凭据、本次原始附件与选中的产品，不询问抗体数量或 Base64。产品库导航不写入业务资料，"
            "按返回的 next_page 继续加载，未经客户选择不筛掉任何候选；提交设计前仍检查公司权限。"
        ),
    }
    if questions:
        interaction["native_question"] = {"questions": [
            native_question_arguments(question, language=language)["questions"][0] for question in questions
        ]}
    return {key: interaction[key] for key in ("required_action", "native_question", "questions") if key in interaction} | interaction


def compact_input_report(report: dict) -> dict:
    """Keep the current MCP action and its diagnostics without repeating the full form."""
    result = {key: value for key, value in report.items() if key not in ("schema", "missing_fields")}
    interaction = report.get("interaction")
    paths = []
    preserve_validation_issues = isinstance(interaction, dict) and interaction.get("batch") and not report.get("validation_deferred")
    if isinstance(interaction, dict):
        interaction = dict(interaction)
        batched = report.get("validation_deferred") or interaction.get("batch")
        questions = interaction.get("questions", [])
        if not batched:
            questions = questions[:1]
        interaction["questions"] = questions
        for question in questions:
            paths.extend(question.get("field_paths", []))
            paths.extend(question.get("related_fields", []))
        interaction["instructions"] = (
            "Follow required_action and credential prerequisites first, reusing the current valid JWT. "
            "Call the available native question tool with all questions in native_question, including text input; "
            "otherwise collect the batch through terminal prompts. Wait for the real answers, map labels to the original values, "
            "and merge with known answers, preserving false, 0 and empty assay selections. Keep the current language. "
            "Collect ordinary answers without per-answer validation; validate together before design or cart writes. "
            "Do not reread rules, reconnect, ask for antibody count, or treat input readiness as write authorization."
            if report.get("language") == "en" else
            "先执行 required_action 和凭据前置条件，复用当前有效 JWT。实际调用可用的原生提问工具，"
            "用 native_question 一次提问当前整批，文本输入也要弹卡；无原生能力时用终端收集这批答案。"
            "等待真实答案，将选项标签映射回原值并合并已有资料，保留 false、0 和明确不检测的空列表，沿用当前语言。"
            "普通字段先收集，设计或加购前统一校验，不逐项回调校验。"
            "不重读规则、不重连、不询问抗体数量；资料齐备不代表获得写入授权。"
        )
        result["interaction"] = interaction
    if "issues" in result:
        result["issues"] = [
            {key: value for key, value in issue.items() if key not in ("examples", "x-options")}
            for issue in report["issues"]
            if preserve_validation_issues or issue.get("code") != "missing" or any(
                issue["path"] == path or issue["path"].startswith(path + "/")
                or path.startswith(issue["path"] + "/") for path in paths
            )
        ]
    if "/data/catalogNumber" not in paths:
        result.pop("package_display_text", None)
        result.pop("display_instructions", None)
    return result


def collect_order_input(stage: str, supplied: dict | None = None, *, language: str = "zh") -> dict:
    """Collect unanswered fields in compatible batches without validating ordinary answers."""
    language = normalize_language(language)
    valid_stage = isinstance(stage, str) and stage in _SCHEMAS
    schema = schema_for_stage(stage, language=language) if valid_stage else {}
    value = _normalize({} if supplied is None else supplied, schema)
    root_name = "data" if stage == "design" else "cart_data"
    root = value.get(root_name, {}) if isinstance(value, dict) else {}
    root = root if isinstance(root, dict) else {}
    issues = []

    def add(parts, *, unresolved=False):
        node, path = _node_and_path(parts, schema)
        metadata = {key: deepcopy(node[key]) for key in (
            "label", "description", "type", "enum", "examples", "x-options", "format",
            "contentEncoding", "minimum", "maximum", "minLength", "maxLength", "x-existing-identity",
        ) if key in node}
        issues.append({"path": path, "code": "unresolved_choice" if unresolved else "missing", **metadata})

    if not valid_stage:
        issues.append(_localize_metadata({
            "path": "/stage", "code": "unresolved_choice", "type": "string", "enum": ["design", "cart"],
            "label": "资料阶段", "description": "请选择 design 或 cart。",
        }, language))
    elif stage == "design":
        package = root.get("catalogNumber")
        if not isinstance(package, str) or package not in (*FIXED_ITEMS, "BRD401"):
            add(["data", "catalogNumber"], unresolved="catalogNumber" in root)
        elif package == "BRD401" and (custom_questions := _missing_custom_questions(root, language)):
            for question in custom_questions:
                add(question["field_paths"][0].strip("/").split("/"))
        else:
            for name in ("projectName", "antigenCount", "usingdna"):
                if name not in root:
                    add(["data", name])
            count = root.get("antigenCount")
            if type(count) is int and 1 <= count <= 3:
                antigens = root.get("antigens")
                antigens = antigens if isinstance(antigens, list) else []
                for index in range(count):
                    antigen = antigens[index] if index < len(antigens) else {}
                    antigen = antigen if isinstance(antigen, dict) else {}
                    prefix = ["data", "antigens", index]
                    source = antigen.get("sourceType")
                    if not isinstance(source, str) or source not in _DESIGN_SOURCE_FIELDS:
                        add([*prefix, "sourceType"], unresolved="sourceType" in antigen)
                    elif source == "SUPPLIER_CATALOG":
                        if any(name not in antigen for name in _DESIGN_SOURCE_FIELDS[source]):
                            add(prefix)
                    else:
                        for name in _DESIGN_SOURCE_FIELDS[source]:
                            if name not in antigen:
                                add([*prefix, name])
            elif "antigenCount" in root:
                # The count controls which antigen questions exist; it must resolve before branching.
                add(["data", "antigenCount"], unresolved=True)
            for name in ("filename", "file_base64"):
                if not isinstance(value, dict) or name not in value:
                    add([name])
    else:
        for name in ("projectNo", "shippingRequired", "antigens"):
            if name not in root:
                add(["cart_data", name])
        antigens = root.get("antigens")
        if isinstance(antigens, list):
            for index, antigen in enumerate(antigens[:3]):
                if not isinstance(antigen, dict):
                    continue
                prefix = ["cart_data", "antigens", index]
                supplied_fields = set(antigen).intersection(_CART_ANTIGEN["properties"])
                if not supplied_fields:
                    add(prefix)
                elif "productUrl" not in antigen or (
                    antigen["productUrl"] is None and supplied_fields != {"productUrl"}
                ):
                    for name in _CART_ANTIGEN["x-product-required"]:
                        if name not in antigen:
                            add([*prefix, name])

    result = {
        "status": "collecting" if issues else "collected", "language": language,
        "mode": "collect", "next_input_mode": "collect" if issues else "validate",
        "stage": stage if valid_stage else None, "operation": _OPERATIONS.get(stage) if valid_stage else None,
        "write_performed": False, "validation_deferred": True, "issues": issues, "derived_fields": {},
        "missing_fields": [item["path"] for item in issues if item["code"] == "missing"],
        "schema": schema, "next_action": "ask_current_question" if issues else f"validate_before_{stage}",
        "examples_are_placeholders": True,
        "scope": "collection_only; validate all inputs and existing authorization checks before any write",
    }
    if valid_stage and stage == "design":
        result["package_display_text"] = {option["value"]: localize_text(option["label"], language) for option in
                                          _DESIGN_DATA["properties"]["catalogNumber"]["x-options"]}
    if issues:
        result["interaction"] = _interaction(
            stage if valid_stage else None, issues, value, language=language,
            batch_questions=True, validation_deferred=True,
        )
        result = {key: result[key] for key in ("status", "language", "next_action", "interaction")} | result
    return result


def inspect_order_input(
    stage: str, supplied: dict | None = None, *, language: str = "zh", count_workbook: bool = True,
    batch_questions: bool = False,
) -> dict:
    """Explain local missing/invalid fields without echoing any submitted values.

    ready means only local input checks passed. It does not verify identity, permission,
    spreadsheet contents, the live item catalog, or the server's draft-contract gate.
    Disable count_workbook for question routing; transfer validation still runs.
    """
    language = normalize_language(language)
    if not isinstance(stage, str) or stage not in _SCHEMAS:
        issues = [{"path": "/stage", "code": "invalid_format", "type": "string", "enum": ["design", "cart"],
                   "label": "资料阶段", "description": "请选择 design 或 cart。"}]
        issues = [_localize_metadata(item, language) for item in issues]
        return {"status": "needs_input", "language": language, "mode": "validate", "next_input_mode": "validate",
                "stage": None, "operation": None, "write_performed": False,
                "issues": issues, "missing_fields": [], "schema": {}, "examples_are_placeholders": True,
                "interaction": _interaction(None, issues, {}, language=language, batch_questions=batch_questions),
                "next_action": "ask_current_question"}
    schema = schema_for_stage(stage, language=language)
    value = _normalize({} if supplied is None else supplied, schema)
    if stage == "design" and isinstance(value, dict) and isinstance(value.get("data"), dict):
        # 客户手填或旧上下文中的数量不参与决策，只使用当前上传表格的实际统计值。
        value["data"].pop("antibodyProjectCount", None)
    derived_fields = {}
    issues = []
    seen = set()

    def add(parts, code, description=None):
        node, path = _node_and_path(parts, schema)
        key = (path, code)
        if key in seen or len(issues) >= MAX_ISSUES:
            return
        seen.add(key)
        metadata = {key: deepcopy(node[key]) for key in (
            "label", "description", "type", "enum", "examples", "x-options", "format", "contentEncoding", "minimum", "maximum",
            "minLength", "maxLength", "minItems", "maxItems", "x-existing-identity",
        ) if key in node}
        if description:
            metadata["description"] = localize_text(description, language)
        issues.append({"path": path, "code": code, **metadata})

    def missing(parts, node):
        add(parts, "missing")
        for name in node.get("required", []):
            missing([*parts, name], node["properties"][name])

    for error in _Validator(schema).iter_errors(value):
        parts = list(error.absolute_path)
        if error.validator == "required":
            for name in error.validator_value:
                if name not in error.instance:
                    missing([*parts, name], error.schema["properties"][name])
        else:
            code = "invalid_type" if error.validator == "type" else (
                "conflict" if error.validator in ("additionalProperties", "uniqueItems") else "invalid_format")
            add(parts, code, "存在不支持的字段；请只提供 schema 中声明的字段。" if error.validator == "additionalProperties" else None)
        if len(issues) >= MAX_ISSUES:
            break

    if isinstance(value, dict) and stage == "design":
        data = value.get("data")
        if isinstance(data, dict):
            if "id" in data and _positive_id(data["id"]) is None:
                add(["data", "id"], "invalid_format")
            catalog = data.get("catalogNumber")
            if isinstance(catalog, str) and catalog in (*FIXED_ITEMS, "BRD401"):
                if catalog == "BRD401":
                    selected = data.get("testItems")
                    for category, message in custom_selection_errors(selected, language=language).items():
                        missing_selection = not isinstance(selected, dict) or category not in selected
                        add(["data", "testItems", category], "missing" if missing_selection else "conflict", message)
                else:
                    try:
                        _selection(data, language=language)
                    except RushDataError:
                        add(["data", "testItems"], "conflict", "检测项组合不符合所选套餐；按 schema 中的套餐规则修正，不更换套餐或猜测 ID。")
            antigens = data.get("antigens")
            count = data.get("antigenCount")
            if catalog == "BRD101" and type(count) is int and count != 1:
                add(["data", "antigenCount"], "conflict", "BRD101 必须且仅有一个抗原。")
            if isinstance(antigens, list):
                if type(count) is int and len(antigens) != count:
                    add(["data", "antigens"], "conflict", "数组长度必须等于 antigenCount。")
                for index, antigen in enumerate(antigens[:3]):
                    if not isinstance(antigen, dict):
                        continue
                    prefix = ["data", "antigens", index]
                    source = antigen.get("sourceType")
                    required = _DESIGN_SOURCE_FIELDS.get(source, ()) if isinstance(source, str) else ()
                    catalog_message = "请先输入抗原关键词查询产品库，再选择返回的货号和规格；供应商等字段自动带入，无需提供链接。" if source == "SUPPLIER_CATALOG" else None
                    for name in required:
                        field_path = prefix if source == "SUPPLIER_CATALOG" else [*prefix, name]
                        if name not in antigen:
                            add(field_path, "missing", catalog_message)
                        elif antigen[name] is None or not str(antigen[name]).strip():
                            add(field_path, "invalid_format", catalog_message or "所选来源要求该字段为非空值；准确类型须业务后端确认。")
                    if "referenceUrl" in antigen and isinstance(antigen["referenceUrl"], str) and not _https(antigen["referenceUrl"]):
                        add(prefix if source == "SUPPLIER_CATALOG" else [*prefix, "referenceUrl"], "invalid_format", catalog_message)
            for name in ("antigens", "positiveControls"):
                if name in data:
                    try:
                        json.dumps(data[name], allow_nan=False)
                    except (ValueError, TypeError, OverflowError):
                        add(["data", name], "invalid_format", "扩展内容必须是有限数值组成的有效 JSON；不回显提交内容。")
        filename = value.get("filename")
        if isinstance(filename, str) and (not filename.lower().endswith(".xlsx") or any(char in filename for char in ("/", "\\", "\r", "\n", "\0"))):
            add(["filename"], "invalid_format")
        encoded = value.get("file_base64")
        if isinstance(encoded, str) and len(encoded) <= MAX_BASE64_CHARS:
            try:
                content = base64.b64decode(encoded, validate=True)
                if not content or len(content) > MAX_FILE_BYTES:
                    add(["file_base64"], "invalid_format")
                elif count_workbook:
                    try:
                        count = count_antibody_records(content)
                        derived_fields["antibodyProjectCount"] = count
                    except ValueError:
                        # Counting is advisory; only the business API decides whether the workbook is acceptable.
                        pass
            except (ValueError, binascii.Error):
                add(["file_base64"], "invalid_format")
    elif isinstance(value, dict) and stage == "cart":
        cart = value.get("cart_data")
        if isinstance(cart, dict):
            raw_cart = supplied.get("cart_data", {}) if isinstance(supplied, dict) else cart
            project = raw_cart.get("projectNo")
            if isinstance(project, str) and (project.strip() == "—" or any(ord(char) < 32 for char in project)):
                add(["cart_data", "projectNo"], "invalid_format")
            antigens = cart.get("antigens")
            if isinstance(antigens, list):
                for index, antigen in enumerate(antigens[:3]):
                    if not isinstance(antigen, dict):
                        continue
                    prefix = ["cart_data", "antigens", index]
                    url = antigen.get("productUrl")
                    if isinstance(url, str) and url:
                        if not _https(url, no_whitespace=True):
                            add([*prefix, "productUrl"], "invalid_format")
                        if any(item is not None for key, item in antigen.items() if key != "productUrl"):
                            add(prefix, "conflict", "URL 模式只能 productUrl 有值，其他字段须省略或为 null。")
                    elif url is None or url == "":
                        for name in ("antigenName", "catalogNo", "supplierName"):
                            if name not in antigen:
                                add([*prefix, name], "missing")
                            elif antigen[name] is None or antigen[name] == "":
                                add([*prefix, name], "invalid_format", "产品模式要求该字段为非空文本。")
            # Keep the final readiness decision in agreement with the actual cart writer.
            if not issues:
                try:
                    RushDataClient._validate_cart_data(raw_cart)
                except RushDataError:
                    add(["cart_data"], "conflict", "购物车资料未通过执行器的当前字段规则，请按 schema 核实。")
    result = {"status": "needs_input" if issues else "ready", "language": language, "mode": "validate",
            "next_input_mode": "validate" if issues else None, "stage": stage, "operation": _OPERATIONS[stage],
            "write_performed": False, "issues": issues,
            "derived_fields": derived_fields,
            "missing_fields": [item["path"] for item in issues if item["code"] == "missing"],
            "schema": schema, "next_action": "ask_current_question" if issues else "continue_existing_workflow",
            "examples_are_placeholders": True,
            "scope": "local_input_only; server authorization, catalog, save proof and contract checks still apply"}
    if stage == "design":
        result["package_display_text"] = {option["value"]: localize_text(option["label"], language) for option in
                                          _DESIGN_DATA["properties"]["catalogNumber"]["x-options"]}
        result["display_instructions"] = ("套餐介绍直接使用 package_display_text 中对应套餐的原文，不从 Titer 等内部检测键重新翻译或生成简介。"
                                          "抗原来源使用当前选项原文；产品库先检查当前客户凭据，再询问关键词并查询真实货号，选择后自动带入资料。")
        if language == "en":
            result["display_instructions"] = (
                "Use package_display_text verbatim for package introductions, without regenerating descriptions from internal assay keys. "
                "Use the source option labels exactly. Before catalog search, reuse/check current customer credentials, then ask for a "
                "keyword and query real catalog numbers; fill product information automatically after selection.")
    if issues:
        result["interaction"] = _interaction(stage, issues, value, language=language, batch_questions=batch_questions)
        # Put the current action before the full diagnostic schema in serialized tool output.
        result = {key: result[key] for key in ("status", "language", "next_action", "interaction")} | result
    return result
