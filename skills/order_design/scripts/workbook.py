"""Read sample counts from the original XLSX without editing or returning sequences."""

from io import BytesIO
import posixpath
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZipFile


_NS = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
_HELPER_SHEETS = {"ai_spec", "_mapping", "_options"}
_CHAIN_HEADERS = {"vh", "vl", "vhh", "vh/protein"}


def count_antibody_records(content: bytes) -> int:
    """Count named rows under sample/chain headers; leave known helper sheets untouched."""
    try:
        with ZipFile(BytesIO(content)) as book:
            # Limit expanded XML as well as the compressed upload; never extract ZIP paths.
            if sum(item.file_size for item in book.infolist()) > 64 * 1024 * 1024:
                raise ValueError("设计表展开后过大，请使用本次下单的样本表重新上传。")
            shared = []
            if "xl/sharedStrings.xml" in book.namelist():
                shared = ["".join(node.itertext()) for node in
                          ET.fromstring(book.read("xl/sharedStrings.xml")).findall("x:si", _NS)]

            def cell_text(cell):
                if cell.get("t") == "inlineStr":
                    return "".join(node.text or "" for node in cell.findall(".//x:t", _NS)).strip()
                value = cell.findtext("x:v", default="", namespaces=_NS)
                if cell.get("t") == "s" and value and (not value.isascii() or len(value) > 12):
                    raise KeyError("invalid shared-string index")
                if cell.get("t") == "s" and value and not value.isdigit():
                    raise KeyError("invalid shared-string index")
                return (shared[int(value)] if cell.get("t") == "s" and value else value).strip()

            links = {node.get("Id"): node.get("Target") for node in
                     ET.fromstring(book.read("xl/_rels/workbook.xml.rels"))
                     if node.get("TargetMode") != "External"}
            counts = []
            for sheet in ET.fromstring(book.read("xl/workbook.xml")).findall("x:sheets/x:sheet", _NS):
                if sheet.get("name", "").strip().lower().replace(" ", "_") in _HELPER_SHEETS:
                    continue
                target = links.get(sheet.get("{" + _REL + "}id"))
                if not target:
                    continue
                path = posixpath.normpath(target.lstrip("/") if target.startswith("/") else "xl/" + target)
                if not path.startswith("xl/worksheets/"):
                    continue
                name_column, data_columns, count = None, set(), 0
                for row in ET.fromstring(book.read(path)).findall("x:sheetData/x:row", _NS):
                    cells = {"".join(c for c in cell.get("r", "") if c.isalpha()): cell_text(cell)
                             for cell in row.findall("x:c", _NS)}
                    if name_column is None:
                        headers = {column: text.lower().replace(" ", "_") for column, text in cells.items()}
                        names = [column for column, text in headers.items() if text == "protein_name"]
                        chains = {column for column, text in headers.items() if text in _CHAIN_HEADERS}
                        # Mapping tables can mention protein_name as a value; a sample header also needs a chain column.
                        if names and chains:
                            name_column = names[0]
                            data_columns = chains
                        continue
                    if cells.get(name_column):
                        count += 1
                    elif any(cells.get(column) for column in data_columns):
                        raise ValueError("设计表中有未填写抗体名称的样本行，请补齐表格后重新上传；无需手填抗体数量。")
                if name_column is not None:
                    counts.append(count)
            if len(counts) != 1:
                raise ValueError("请上传包含一个抗体样本数据表的设计模板（含抗体名称及链信息）；多个样本表需先明确本单范围。")
            if not counts[0]:
                raise ValueError("设计表中没有抗体样本，请补齐表格后重新上传。")
            return counts[0]
    except (BadZipFile, KeyError, IndexError, ET.ParseError, OSError, RuntimeError, UnicodeError, OverflowError):
        raise ValueError("无法读取抗体设计表，请上传有效的原始 XLSX 文件；无需手填抗体数量。") from None
