#!/usr/bin/env python3
"""LibreOffice will not run in this sandbox, so cached formula results are computed with the
`formulas` engine and injected into the workbook XML. fullCalcOnLoad is also set so Excel /
Sheets recalculate everything from the formulas themselves on open."""
import re, zipfile, io
import xml.etree.ElementTree as ET
import formulas

SRC = "/home/user/regcoffeenyc-tactical-shop-agents/greenhouse/Greenhouse_CashFlow_2000m2.xlsx"
NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
RNS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
ET.register_namespace("", NS)

xl = formulas.ExcelModel().loads(SRC).finish()
sol = xl.calculate()

values = {}
for k, v in sol.items():
    m = re.match(r"^'\[.*\](.+)'!([A-Z]+\d+)$", k)
    if not m:
        continue
    try:
        val = v.value[0, 0]
    except Exception:
        continue
    values[(m.group(1).upper(), m.group(2))] = val

zin = zipfile.ZipFile(SRC)
wbx = ET.fromstring(zin.read("xl/workbook.xml"))
rels = ET.fromstring(zin.read("xl/_rels/workbook.xml.rels"))
rid2t = {r.get("Id"): r.get("Target") for r in rels}
sheet_part = {}
for sh in wbx.find(f"{{{NS}}}sheets"):
    t = rid2t[sh.get(f"{{{RNS}}}id")]
    sheet_part[("xl/" + t.lstrip("/")).replace("xl/xl/", "xl/")] = sh.get("name").upper()

n_written = 0
parts = {}
for name in zin.namelist():
    data = zin.read(name)
    if name in sheet_part:
        sname = sheet_part[name]
        root = ET.fromstring(data)
        for c in root.iter(f"{{{NS}}}c"):
            f = c.find(f"{{{NS}}}f")
            if f is None:
                continue
            for old in c.findall(f"{{{NS}}}v"):
                c.remove(old)
            val = values.get((sname, c.get("r")))
            if val is None:
                continue
            if isinstance(val, bool):
                c.set("t", "b")
                text = "1" if val else "0"
            elif isinstance(val, str):
                c.set("t", "e" if val.startswith("#") else "str")
                text = val
            else:
                try:
                    fv = float(val)
                except (TypeError, ValueError):
                    continue
                if fv != fv or fv in (float("inf"), float("-inf")):
                    continue
                c.attrib.pop("t", None)
                text = repr(fv)
            v = ET.SubElement(c, f"{{{NS}}}v")
            v.text = text
            n_written += 1
        data = ET.tostring(root, encoding="UTF-8", xml_declaration=True)
    elif name == "xl/workbook.xml":
        root = ET.fromstring(data)
        calc = root.find(f"{{{NS}}}calcPr")
        if calc is None:
            calc = ET.SubElement(root, f"{{{NS}}}calcPr")
        calc.set("fullCalcOnLoad", "1")
        calc.set("calcId", "191029")
        data = ET.tostring(root, encoding="UTF-8", xml_declaration=True)
    parts[name] = data

buf = io.BytesIO()
with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zo:
    for name, data in parts.items():
        zo.writestr(name, data)
zin.close()
with open(SRC, "wb") as fh:
    fh.write(buf.getvalue())
print("cached values written:", n_written)
