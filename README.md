# Armenia's foreign policy after the 2020 war: three research records

Hand-collected records on Armenia's foreign policy after the 2020 Nagorno-Karabakh war: a chronology of turning points, a record of accusations exchanged by Armenian and Russian officials, and an inventory of foreign democracy assistance to Armenian organizations.

Compiled by Tigran Aghbalyan in August–October 2025 while working as a research assistant to Prof. Arman Grigoryan (Department of International Relations, Lehigh University). Converted to machine-readable tables and documented in November 2026.

## Contents

| File | Unit of observation | Size | Coverage |
|---|---|---|---|
| `data/chronology.csv` | Event | 31 | 10 Nov 2020 – 2 Sep 2025 |
| `data/statements.csv` | Dated statement or exchange | 27 | 17 Nov 2020 – 8 Sep 2025 |
| `data/democracy_assistance.csv` | Recipient organization × funder | 30 rows, 15 organizations | Funding periods between 1991 and 2027 |
| `data/funder_totals.csv` | Funder | 6 | As reported |

Variables are defined in [`CODEBOOK.md`](CODEBOOK.md).

- **Chronology.** Turning points in Armenia's relations with Russia, Azerbaijan, the EU and the United States, from the days after the 9 November 2020 ceasefire statement to the announced dissolution of the OSCE Minsk Group.
- **Statements.** Public accusations and replies between Armenian officials (Pashinyan, Mirzoyan, Simonyan) and Russian officials (Putin, Lavrov, Zakharova, Peskov) over CSTO obligations, the Russian peacekeeping mission and the Lachin corridor. 13 of the 27 entries contain direct quotations; the rest are paraphrases.
- **Democracy assistance.** Funding of Armenian media, civil-society and academic organizations by USAID, the National Endowment for Democracy, the Open Society Foundations, EU programs, Sida and others, with funding periods, amounts as reported, and the source for each line where one was recorded.

## Scope and limitations

Please read before using the data.

- **These are research notes in tabular form, not a systematic dataset.** Events and statements were selected by judgment as the important ones. Nothing was sampled and completeness is not claimed.
- **Wording is the compiler's.** Event names and descriptions are working notes and include characterizations. Entries have not been independently fact-checked since 2025.
- **Sources.** The chronology and the statements table do not yet carry source links. The assistance table has a source for 23 of 30 rows; 4 of 6 funder totals have none.
- **Amounts cannot be summed.** Many are partial ("part of a $15M program"), mix awards and disbursements, are in different currencies, or were not disclosed. They are kept as text.
- **Known inconsistencies in the assistance table.** Three funding periods begin before the recipient's founding year as recorded (rows 25, 29, 30), and one row has no amount (row 3). They are kept as recorded and flagged by the check script.
- **Dates.** Event 11 had no year in the original ("Sep 13-14"); 2022 is inferred from its position and flagged in `year_inferred`. Statement entries 5 and 13 are out of date order in the original; `entry_id` preserves the original order.

## Reproduce

Requires Python 3.8 or later. No packages are needed.

```
python3 scripts/build_data.py    # rebuilds chronology.csv and statements.csv from raw/
python3 scripts/check_data.py    # validates all four tables and lists entries to review
```

`build_data.py` copies the text as written, adds ISO dates, and lists the officials named in each statement. `democracy_assistance.csv` and `funder_totals.csv` were transcribed by hand from the original report, with each footnote resolved to its URL; the report itself is not included.

## Provenance

The original chronology, statements file and funding report were researched and written by Tigran Aghbalyan in 2025. The conversion to CSV, the scripts and this documentation were prepared in November 2026.

## Licence and citation

Code: MIT. Data and documentation: CC BY 4.0. See [`LICENSE`](LICENSE).

Aghbalyan, Tigran. 2026. *Armenia's foreign policy after the 2020 war: three research records.* https://github.com/aghbalyan/armenia-foreign-policy-records
