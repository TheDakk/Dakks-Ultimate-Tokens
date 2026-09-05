"""Append one row to the workbook's HISTORY sheet, in place, without a library round-trip.

The workbook has one writer for its ASSETS rows (``npm run art-upload``); HISTORY is
append-only and this is the reviewer's tool for growing it. It edits the xlsx the way
``write-workbook.mjs`` does: the ZIP is rewritten entry for entry, only the HISTORY sheet
XML and the HistoryTable definition change, and every other part is copied byte for byte.
It never opens the workbook through openpyxl or any spreadsheet library (which would drop
tables, validation and formatting on save).

    .venv\\Scripts\\python.exe append_history.py --action "..." --notes "..."
    .venv\\Scripts\\python.exe append_history.py --dry-run --action "..."   # show the row, write nothing

The new event_id is the last HIST- id plus one; the timestamp is today's date as an Excel
serial (matching the existing rows); the text cells reuse the style of the row above.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

SHEET_NAME = "HISTORY"
TABLE_NAME = "HistoryTable"
COLUMNS = {
    "event_id": "A",
    "event_type": "B",
    "timestamp": "C",
    "actor": "D",
    "qa_result": "O",
    "severity": "P",
    "action": "S",
    "notes": "T",
}


def excel_serial(day: dt.date) -> int:
    return (day - dt.date(1899, 12, 30)).days


def locate(z: zipfile.ZipFile) -> tuple[str, str]:
    """Return (sheet part, table part) for the HISTORY sheet and HistoryTable."""
    wb = z.read("xl/workbook.xml").decode("utf-8")
    m = re.search(r'<sheet\b[^>]*\bname="%s"[^>]*/>' % SHEET_NAME, wb)
    if not m:
        raise SystemExit(f"no sheet named {SHEET_NAME} in workbook.xml")
    rid = re.search(r'\br:id="([^"]+)"', m.group(0)).group(1)
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    rel = re.search(r'<Relationship\b[^>]*\bId="%s"[^>]*/>' % re.escape(rid), rels)
    target = re.search(r'\bTarget="([^"]+)"', rel.group(0)).group(1)
    sheet_part = target.lstrip("/")
    if not sheet_part.startswith("xl/"):
        sheet_part = "xl/" + sheet_part
    table_part = None
    for name in z.namelist():
        if name.startswith("xl/tables/") and name.endswith(".xml"):
            if re.search(r'\bname="%s"' % TABLE_NAME, z.read(name).decode("utf-8")):
                table_part = name
                break
    if table_part is None:
        raise SystemExit(f"no table named {TABLE_NAME} in the workbook")
    return sheet_part, table_part


def cell(ref: str, style: str, text: str) -> str:
    return (
        f'<c r="{ref}" s="{style}" t="inlineStr"><is><t xml:space="preserve">'
        f"{escape(text)}</t></is></c>"
    )


def build(args: argparse.Namespace) -> None:
    path: Path = args.root / "upload" / "Dakk-Ultimate-Tokens-Master.xlsx"
    if not path.exists():
        raise SystemExit(f"workbook not found: {path}")
    with zipfile.ZipFile(path) as z:
        sheet_part, table_part = locate(z)
        sheet = z.read(sheet_part).decode("utf-8")
        table = z.read(table_part).decode("utf-8")
        infos = z.infolist()
        raw = {i.filename: z.read(i.filename) for i in infos}

    ref = re.search(r'\bref="([A-Z]+)(\d+):([A-Z]+)(\d+)"', table)
    first_col, header_row, last_col, last_row = ref.group(1), int(ref.group(2)), ref.group(3), int(ref.group(4))
    if first_col != "A" or last_col != "T":
        raise SystemExit(f"unexpected HistoryTable ref {ref.group(0)}")
    last = re.search(r'<row r="%d"[^>]*>(.*?)</row>' % last_row, sheet, re.S)
    if not last:
        raise SystemExit(f"row {last_row} (last table row) not found in sheet XML")
    last_id = re.search(r'<c r="A%d"[^>]*>.*?<t[^>]*>(HIST-\d+)</t>' % last_row, last.group(0), re.S)
    if not last_id:
        raise SystemExit(f"row {last_row} carries no HIST- event_id; refusing to append after it")
    text_style = re.search(r'<c r="A%d" s="(\d+)"' % last_row, last.group(0)).group(1)
    date_style = re.search(r'<c r="C%d" s="(\d+)"' % last_row, last.group(0))
    date_style = date_style.group(1) if date_style else text_style

    new_row = last_row + 1
    new_id = "HIST-%04d" % (int(last_id.group(1).split("-")[1]) + 1)
    values = {
        "event_id": new_id,
        "event_type": args.event_type,
        "actor": args.actor,
        "qa_result": args.qa,
        "severity": args.severity,
        "action": args.action,
        "notes": args.notes,
    }
    cells = []
    for key, col in COLUMNS.items():
        if key == "timestamp":
            cells.append(f'<c r="C{new_row}" s="{date_style}"><v>{excel_serial(args.date)}</v></c>')
        elif values.get(key):
            cells.append(cell(f"{col}{new_row}", text_style, values[key]))
    row_xml = f'<row r="{new_row}">' + "".join(cells) + "</row>"

    print(f"{new_id}  row {new_row}  {args.date.isoformat()}  {args.event_type}/{args.actor}  {args.qa}/{args.severity}")
    print(f"  action: {args.action}")
    if args.notes:
        print(f"  notes:  {args.notes}")
    if args.dry_run:
        print("dry run: nothing written")
        return

    existing = re.search(r'<row r="%d"(?:[^>]*/>|[^>]*>.*?</row>)' % new_row, sheet, re.S)
    if existing:
        if re.search(r"<t[^>]*>[^<]", existing.group(0)):
            raise SystemExit(f"row {new_row} already holds text outside the table; refusing to overwrite")
        sheet = sheet[: existing.start()] + row_xml + sheet[existing.end():]
    else:
        sheet = sheet[: last.end()] + row_xml + sheet[last.end():]
    table = table.replace(ref.group(0), f'ref="A{header_row}:T{new_row}"', 1)
    raw[sheet_part] = sheet.encode("utf-8")
    raw[table_part] = table.encode("utf-8")

    fd, tmp = tempfile.mkstemp(prefix="hist-", suffix=".xlsx", dir=str(path.parent))
    os.close(fd)
    with zipfile.ZipFile(tmp, "w") as out:
        for info in infos:
            out.writestr(info, raw[info.filename], compress_type=info.compress_type, compresslevel=9)
    verify(Path(tmp), new_row, new_id)
    shutil.move(tmp, path)
    print(f"wrote {path}")


def verify(path: Path, new_row: int, new_id: str) -> None:
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        if bad:
            raise SystemExit(f"rewritten workbook fails zip test at {bad}")
        sheet_part, table_part = locate(z)
        table = z.read(table_part).decode("utf-8")
        sheet = z.read(sheet_part).decode("utf-8")
        names = re.findall(r'<table\b[^>]*\bname="([^"]+)"', b"".join(z.read(n) for n in z.namelist() if n.startswith("xl/tables/")).decode("utf-8"))
    if f'ref="A3:T{new_row}"' not in table:
        raise SystemExit("HistoryTable ref did not grow")
    if not re.search(r'<c r="A%d"[^>]*>.*?<t[^>]*>%s</t>' % (new_row, new_id), sheet, re.S):
        raise SystemExit("new row not found after rewrite")
    print(f"verified: {TABLE_NAME} ref A3:T{new_row}; tables present: {len(names)}")


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument("--action", required=True, help="the S column: what changed")
    ap.add_argument("--notes", default="", help="the T column: evidence, hashes, counts")
    ap.add_argument("--event-type", default="pipeline_change")
    ap.add_argument("--actor", default="spec_fix")
    ap.add_argument("--qa", default="pass")
    ap.add_argument("--severity", default="none")
    ap.add_argument("--date", type=dt.date.fromisoformat, default=dt.date.today())
    ap.add_argument("--dry-run", action="store_true")
    build(ap.parse_args(argv))


if __name__ == "__main__":
    main(sys.argv[1:])
