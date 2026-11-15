"""Build the two machine-readable tables from the original Word files.

Reads   raw/Chronology.docx                     (a three-column table)
        raw/ARM-RUS mutual accusations.docx     (dated paragraphs)
Writes  data/chronology.csv
        data/statements.csv

The text of every entry is copied as written in the Word files. The script
adds a machine-readable date next to the date as originally typed, lists the
officials named in each statement, and fixes the three spelling slips listed
in SPELLING below. Nothing else is corrected or re-worded.

Uses only the Python standard library. Run from the repository root:
    python3 scripts/build_data.py
"""
import csv
import html
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
DATA = ROOT / "data"

MONTHS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
          "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}


# Spelling slips in the originals, fixed in the output (original -> corrected).
SPELLING = {
    "Lachin corridoe": "Lachin corridor",
    "1991 Ama-Ata": "1991 Alma-Ata",
    "this timesetting": "this time setting",
}

# Officials whose names are searched for in each statement entry.
OFFICIALS = ["Pashinyan", "Mirzoyan", "Simonyan", "Putin", "Lavrov", "Zakharova", "Peskov"]


def fix_spelling(text):
    for wrong, right in SPELLING.items():
        text = text.replace(wrong, right)
    return text


def docx_xml(path):
    """A .docx file is a zip archive; the text lives in word/document.xml."""
    return zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")


def paragraphs(xml):
    """Return the plain text of each paragraph, skipping empty ones."""
    out = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S):
        text = html.unescape(re.sub(r"<[^>]+>", "", p)).strip()
        if text:
            out.append(text)
    return out


def iso(year, month_name, day):
    return "%04d-%02d-%02d" % (int(year), MONTHS[month_name[:3].lower()], int(day))


# ---------------------------------------------------------------- chronology
def build_chronology():
    xml = docx_xml(RAW / "Chronology.docx")
    rows = re.findall(r"<w:tr[ >].*?</w:tr>", xml, flags=re.S)
    records = []
    last_year = None
    for row in rows[1:]:                      # rows[0] is the header row
        cells = re.findall(r"<w:tc[ >].*?</w:tc>", row, flags=re.S)
        written, event, details = [fix_spelling(" ".join(paragraphs(c))) for c in cells]

        full = re.match(r"^([A-Za-z]+)\.? (\d{1,2}), (\d{4})$", written)
        span = re.match(r"^([A-Za-z]+)\.? (\d{1,2})-(\d{1,2})$", written)
        if full:
            start = end = iso(full.group(3), full.group(1), full.group(2))
            last_year = full.group(3)
            year_inferred = "no"
        elif span:
            # The original gives no year ("Sep 13-14"). The table is in date
            # order, so the year of the row above is used and flagged.
            start = iso(last_year, span.group(1), span.group(2))
            end = iso(last_year, span.group(1), span.group(3))
            year_inferred = "yes"
        else:
            raise ValueError("Unrecognised date in chronology: %r" % written)

        records.append({
            "event_id": len(records) + 1,
            "date_start": start,
            "date_end": end,
            "year_inferred": year_inferred,
            "date_as_written": written,
            "event": event,
            "details": details,
        })
    write_csv(DATA / "chronology.csv", records)
    return len(records)


# ---------------------------------------------------------------- statements
DATED = re.compile(r"^([A-Z][a-z]{2,8})\.? (\d{1,2}), (\d{4})\s*[.:,]?\s*(.*)$", re.S)


def build_statements():
    xml = docx_xml(RAW / "ARM-RUS mutual accusations.docx")
    records = []
    for text in paragraphs(xml):
        m = DATED.match(text)
        if m and m.group(1)[:3].lower() in MONTHS:
            # A paragraph that opens with a date starts a new entry.
            records.append({
                "entry_id": len(records) + 1,
                "date": iso(m.group(3), m.group(1), m.group(2)),
                "heading": m.group(4).strip(),
                "body": "",
            })
        elif records:
            # Any other paragraph belongs to the entry above it.
            sep = "\n" if records[-1]["body"] else ""
            records[-1]["body"] += sep + text
        else:
            raise ValueError("Text before the first dated entry: %r" % text[:60])

    for r in records:
        whole = r["heading"] + " " + r["body"]
        r["officials_named"] = "; ".join(name for name in OFFICIALS if name in whole)
        r["n_direct_quotes"] = whole.count("“")      # opening curly quote
    write_csv(DATA / "statements.csv", records)
    return len(records)


def write_csv(path, records):
    DATA.mkdir(exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(records[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(records)


if __name__ == "__main__":
    print("chronology.csv:", build_chronology(), "events")
    print("statements.csv:", build_statements(), "entries")
