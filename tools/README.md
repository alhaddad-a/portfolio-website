# Verifying the register

`content/register.json` is the site's source of truth: every entry on the homepage and every
page under `/register/` is rendered from it by `build.py`.

Each entry's counts come from one of two places:

- **The author's own documentation**, copied as written. For example, the Harborview data-quality log
  (`02_Data_Quality_Log.md`).
- **The public raw CSVs, recomputed.** That covers the SQL Server / Databricks CRM + ERP files and the healthcare files.

Every citation on an entry page links to the exact line it came from.

## Re-deriving the numbers

Clone the four project repositories into one folder, then run:

```
python -I tools/profile_p1.py   <clones>/mssql-medallion-data-warehouse      # CRM + ERP files (cases 01, 02)
python -I tools/profile_p3.py   <clones>/healthcare-lakehouse-databricks     # replays the Silver notebook rules
python -I tools/profile_p4.py   <clones>/harborview-bank-powerbi-analysis    # cross-checks the quality log
python -I tools/build_register.py <clones> content/register.json             # regenerates the dataset
```

`build_register.py` resolves every citation to a line number. The build stops if any quoted line
can't be found, so a citation can't point at text that doesn't exist.

## Rules the dataset follows

- Only defects documented by the author, or reproducible from the raw files with the project's own rules.
- Harborview business findings (the chargebacks, for example) are **not** entries. As the quality log puts it:
  "The quality log is for data that is wrong. Patterns in correct data go on a separate list."
- A check that found nothing is recorded as `clean`, following the log's lesson "A clean column is a result too".
- A fix is credited to case 02 (Databricks) only where its notebook really applies it.
- `PERSONAL` in `build.py` is intentionally empty. Personal background is only added in the author's own words.

## Known counting notes

- HB-35 (orphan transactions): the raw file has 151 such rows; the log reports 150, counted after duplicates
  were removed. The site uses the log's figure and says so.
- WH-14 (future birth dates): "future" is relative to the load date (`GETDATE()` / `current_date()`). All 16
  dates are 2038 or later.
