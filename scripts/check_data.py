"""Check the four data tables.

FAIL  = the file is broken (wrong columns, unreadable date, missing text).
        The script exits with an error if there is any FAIL.
NOTE  = the file is valid, but a human should look at the entry
        (for example, a row with no source). Notes do not stop the script.

Run from the repository root:
    python3 scripts/check_data.py
"""
import csv
import sys
from datetime import date
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
fails, notes = [], []


def load(name, columns):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != columns:
            fails.append("%s: columns are %s, expected %s" % (name, reader.fieldnames, columns))
        return list(reader)


def parse(d):
    return date.fromisoformat(d)


# ---- chronology -----------------------------------------------------------
chron = load("chronology.csv", ["event_id", "date_start", "date_end", "year_inferred",
                                "date_as_written", "event", "details"])
if len(chron) != 31:
    fails.append("chronology: %d rows, expected 31" % len(chron))
previous = None
for r in chron:
    tag = "chronology event %s" % r["event_id"]
    try:
        start, end = parse(r["date_start"]), parse(r["date_end"])
    except ValueError:
        fails.append(tag + ": unreadable date")
        continue
    if end < start:
        fails.append(tag + ": ends before it starts")
    if not (date(2020, 11, 9) <= start <= date(2025, 12, 31)):
        fails.append(tag + ": date outside Nov 2020 - 2025")
    if not r["event"].strip() or not r["details"].strip():
        fails.append(tag + ": empty event or details")
    if previous and start < previous:
        notes.append(tag + ": dated earlier than the row above it")
    if r["year_inferred"] == "yes":
        notes.append(tag + ": year not in the original (%r); %s assumed"
                     % (r["date_as_written"], r["date_start"][:4]))
    previous = start

# ---- statements -----------------------------------------------------------
stmts = load("statements.csv", ["entry_id", "date", "heading", "body",
                                "officials_named", "n_direct_quotes"])
if len(stmts) != 27:
    fails.append("statements: %d rows, expected 27" % len(stmts))
previous = None
for r in stmts:
    tag = "statements entry %s" % r["entry_id"]
    try:
        d = parse(r["date"])
    except ValueError:
        fails.append(tag + ": unreadable date")
        continue
    if not r["heading"].strip() and not r["body"].strip():
        fails.append(tag + ": no text")
    if previous and d < previous:
        notes.append(tag + " (%s): dated earlier than the entry above it" % r["date"])
    if int(r["n_direct_quotes"]) == 0:
        notes.append(tag + " (%s): paraphrase only, no direct quotation" % r["date"])
    previous = d

# ---- democracy assistance -------------------------------------------------
aid = load("democracy_assistance.csv", ["row_id", "org_id", "organization", "established",
                                        "funder", "period_start", "period_end",
                                        "amount_as_written", "source_url"])
if len(aid) != 30:
    fails.append("democracy_assistance: %d rows, expected 30" % len(aid))
if len({r["org_id"] for r in aid}) != 15:
    fails.append("democracy_assistance: expected 15 organizations")
for r in aid:
    tag = "assistance row %s (%s, %s)" % (r["row_id"], r["organization"], r["funder"])
    if int(r["period_end"]) < int(r["period_start"]):
        fails.append(tag + ": period ends before it starts")
    founded = min(int(y) for y in r["established"].split(" / "))
    if int(r["period_start"]) < founded:
        notes.append(tag + ": funding starts %s, before the organization was founded (%d)"
                     % (r["period_start"], founded))
    if not r["source_url"].strip():
        notes.append(tag + ": no source")
    if not r["amount_as_written"].strip():
        notes.append(tag + ": no amount")

totals = load("funder_totals.csv", ["funder", "period_as_written", "total_as_written", "source_url"])
for r in totals:
    if not r["source_url"].strip():
        notes.append("funder total (%s): no source" % r["funder"])

# ---- report ---------------------------------------------------------------
print("Rows: chronology %d, statements %d, assistance %d (%d organizations), funder totals %d"
      % (len(chron), len(stmts), len(aid), len({r["org_id"] for r in aid}), len(totals)))
print("\nNOTES for a human to review: %d" % len(notes))
for n in notes:
    print("  -", n)
print("\nFAILS: %d" % len(fails))
for f in fails:
    print("  -", f)
sys.exit(1 if fails else 0)
