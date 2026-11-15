# Codebook


## data/chronology.csv (one row per event)

| Column | Meaning |
|---|---|
| `event_id` | Row number in the original table (1–31) |
| `date_start` | First day of the event, YYYY-MM-DD |
| `date_end` | Last day of the event; same as `date_start` for one-day events |
| `year_inferred` | `yes` if the original gave no year and the year of the row above was used (event 11 only) |
| `date_as_written` | The date exactly as typed in the original |
| `event` | Short name of the event, as written |
| `details` | Description, as written |

## data/statements.csv (one row per dated entry)

| Column | Meaning |
|---|---|
| `entry_id` | Position in the original file (1–27). The original is not in strict date order (entries 5 and 13) |
| `date` | Date of the statement, YYYY-MM-DD |
| `heading` | The text that follows the date on the entry's first line: usually the speaker and the occasion |
| `body` | The rest of the entry: summary and quotations, as written. Paragraphs are separated by line breaks |
| `officials_named` | Which of seven officials are named in the entry (Pashinyan, Mirzoyan, Simonyan, Putin, Lavrov, Zakharova, Peskov), found by name search and separated by "; ". Empty if none is named |
| `n_direct_quotes` | Number of opening quotation marks in the entry. 0 means the entry is a paraphrase |

`officials_named` records who is mentioned, not who is speaking: several entries involve two speakers (an accusation and the reply).

## data/democracy_assistance.csv (one row per organization and funder)

| Column | Meaning |
|---|---|
| `row_id` | Row number (1–30) |
| `org_id` | Organization number in the original report (1–15) |
| `organization` | Recipient organization |
| `established` | Founding year as given in the report. Two years separated by " / " where the report names two linked bodies |
| `funder` | USAID; NED (National Endowment for Democracy); OSF (Open Society Foundations); EU; Sida (Sweden); or other, named in full |
| `period_start`, `period_end` | First and last year of funding as given in the report |
| `amount_as_written` | The amount exactly as written, including qualifiers. Empty if the report gives none |
| `source_url` | The footnoted source for that line of the report. Empty if the line has no footnote |

## data/funder_totals.csv (one row per funder)

| Column | Meaning |
|---|---|
| `funder` | Funder name as written |
| `period_as_written` | Years covered, as written |
| `total_as_written` | Aggregate figure, as written. Estimates and ranges are kept as text |
| `source_url` | Footnoted source, if any |
