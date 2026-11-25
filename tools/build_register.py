"""
Builds content/register.json for the portfolio from verified evidence.

Every count below was either copied from the author's own documentation or
recomputed from the public CSVs (see profile_p1.py / profile_p3.py / profile_p4.py).
Each citation is resolved to a line number in a local clone, and the build fails
if the quoted text can't be found — so nothing cites a line that doesn't exist.

usage: python -I build_register.py <dir-with-the-four-clones> <output.json>
"""
import json, sys
from pathlib import Path

CLONES = Path(sys.argv[1])
OUT = Path(sys.argv[2])

REPO = {
    "wh": "mssql-medallion-data-warehouse",
    "db": "databricks-medallion-pipeline",
    "hc": "healthcare-lakehouse-databricks",
    "hb": "harborview-bank-powerbi-analysis",
}
GH = "https://github.com/alhaddad-a/"


def cite(repo, path, find=None, label=None):
    """Resolve a citation to a GitHub URL (with a line anchor when `find` is given)."""
    f = CLONES / REPO[repo] / path
    if not f.exists():
        raise SystemExit(f"missing file: {repo}/{path}")
    url = f"{GH}{REPO[repo]}/blob/HEAD/{path}"
    line = None
    if find:
        if path.endswith(".ipynb"):
            text = f.read_text(encoding="utf-8")
            if find not in text and json.dumps(find)[1:-1] not in text:
                raise SystemExit(f"not found in {path}: {find!r}")
        else:
            for i, l in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                if find in l:
                    line = i
                    break
            if line is None:
                raise SystemExit(f"not found in {path}: {find!r}")
            url += ("?plain=1" if path.endswith(".md") else "") + f"#L{line}"
    return {"label": label or path.split("/")[-1] + (f", line {line}" if line else ""), "url": url}


def csv(repo, path):
    return cite(repo, path, None, f"{path.split('/')[-1]} (raw file)")


# ---------------------------------------------------------------------------
# Shared CRM + ERP source files — fixed in Case 01 (T-SQL) and, where the
# notebook really does it, in Case 02 (PySpark).
# ---------------------------------------------------------------------------
P1 = "scripts/silver/proc_load_silver.sql"
T1 = "tests/quality_checks_silver.sql"
NB = "scripts/silver_layer/"

ENTRIES = [
    dict(
        id="WH-01", source="wh", fixed_in=[1, 2], file="cust_info.csv", column="cst_firstname, cst_lastname",
        layer="Bronze → Silver", kind="whitespace",
        title="Spaces before and after customer names",
        raw=" Jon", expected="Jon",
        rows=29, of=18494, rows_note="17 first names and 22 last names carry a leading or trailing space; 29 rows in total.",
        spec={"type": "chars", "also": [["Yang ", "Yang"], ["  Zhu", "Zhu"]]},
        wrong="The CRM export stores names with stray spaces: row 1 is “ Jon”, “Yang ”. Nothing about the value looks wrong in a table view.",
        impact="“ Jon” and “Jon” are different strings. They split a GROUP BY, fail an equality join and sort apart from each other.",
        fixes=[(1, "TRIM() on both name columns in the Silver load.", "TRIM(cst_firstname) AS cst_firstname,\nTRIM(cst_lastname) AS cst_lastname,"),
               (2, "Trims every string column of the table in one loop, not just the ones known to be dirty.",
                "for field in df.schema.fields:\n    if isinstance(field.dataType, StringType):\n        df = df.withColumn(field.name, trim(col(field.name)))")],
        test={"note": "The repository’s whitespace check runs on cst_key; the name columns are trimmed on every load.",
              "sql": "-- Check for Unwanted Spaces\n-- Expectation: No Results\nSELECT \n    cst_key \nFROM silver.crm_cust_info\nWHERE cst_key != TRIM(cst_key);"},
        status="resolved",
        cites=[("wh", P1, "TRIM(cst_firstname) AS cst_firstname"), ("wh", T1, "WHERE cst_key != TRIM(cst_key)"),
               ("db", NB + "crm/silver_crm_cust_info.ipynb", "trim(col(field.name))")],
        raw_file=("wh", "datasets/source_crm/cust_info.csv"),
    ),
    dict(
        id="WH-02", source="wh", fixed_in=[1], file="cust_info.csv", column="cst_id",
        layer="Bronze → Silver", kind="duplicates",
        title="One customer, two records",
        raw="29433", expected="29433 — the latest record only",
        rows=6, of=18494, rows_note="5 customer IDs appear more than once: 6 extra rows.",
        spec={"type": "dupes", "rows": [["29433", "AW00029433", "", "", "M", "M", "2026-01-25"],
                                         ["29433", "AW00029433", "Thomas", "King", "M", "M", "2026-01-27"]],
              "cols": ["cst_id", "cst_key", "cst_firstname", "cst_lastname", "marital", "gndr", "cst_create_date"], "keep": 1},
        wrong="Some customers were exported twice. For ID 29433 the first copy has no name at all; the second, two days newer, is complete.",
        impact="A duplicate key in a dimension doubles every fact row that joins to it.",
        fixes=[(1, "Number each customer’s records by create date, newest first, and keep only the first.",
                "ROW_NUMBER() OVER (PARTITION BY cst_id ORDER BY cst_create_date DESC) AS flag_last\n...\nWHERE flag_last = 1; -- Select the most recent record per customer")],
        test={"sql": "-- Check for NULLs or Duplicates in Primary Key\n-- Expectation: No Results\nSELECT \n    cst_id,\n    COUNT(*) \nFROM silver.crm_cust_info\nGROUP BY cst_id\nHAVING COUNT(*) > 1 OR cst_id IS NULL;"},
        status="resolved",
        cites=[("wh", P1, "ROW_NUMBER() OVER (PARTITION BY cst_id ORDER BY cst_create_date DESC)"), ("wh", T1, "HAVING COUNT(*) > 1 OR cst_id IS NULL;")],
        raw_file=("wh", "datasets/source_crm/cust_info.csv"),
    ),
    dict(
        id="WH-03", source="wh", fixed_in=[1, 2], file="cust_info.csv", column="cst_id",
        layer="Bronze → Silver", kind="missing",
        title="Customer rows with no customer ID",
        raw="", expected="row excluded",
        rows=4, of=18494,
        spec={"type": "empty", "label": "cst_id"},
        wrong="Four rows arrive with an empty primary key.",
        impact="A row without a key can’t be joined to sales or to the ERP tables, and it can’t be deduplicated.",
        fixes=[(1, "Filtered out before deduplication.", "WHERE cst_id IS NOT NULL"),
               (2, "Same rule in PySpark.", 'df = df.filter(col("cst_id").isNotNull())')],
        test={"sql": "-- Check for NULLs or Duplicates in Primary Key\n-- Expectation: No Results\nSELECT \n    cst_id,\n    COUNT(*) \nFROM silver.crm_cust_info\nGROUP BY cst_id\nHAVING COUNT(*) > 1 OR cst_id IS NULL;"},
        status="resolved",
        cites=[("wh", P1, "WHERE cst_id IS NOT NULL"), ("db", NB + "crm/silver_crm_cust_info.ipynb", 'isNotNull()')],
        raw_file=("wh", "datasets/source_crm/cust_info.csv"),
    ),
    dict(
        id="WH-04", source="wh", fixed_in=[1, 2], file="cust_info.csv", column="cst_marital_status",
        layer="Bronze → Silver", kind="codes",
        title="Marital status stored as one-letter codes",
        raw="S", expected="Single",
        rows=18494, of=18494,
        spec={"type": "variants", "variants": [["M", 10013, "Married"], ["S", 8474, "Single"], ["", 7, "n/a"]]},
        wrong="The CRM stores marital status as M and S, and leaves seven rows empty.",
        impact="Codes are fine inside one system. In a warehouse that joins two systems, everybody reading the table has to know what they mean.",
        fixes=[(1, "Mapped to readable values; anything else becomes n/a.", "WHEN UPPER(TRIM(cst_marital_status)) = 'S' THEN 'Single'\nWHEN UPPER(TRIM(cst_marital_status)) = 'M' THEN 'Married'\nELSE 'n/a'"),
               (2, "Same mapping in PySpark.", 'F.when(F.upper(F.col("cst_marital_status")) == "S", "Single")\n .when(F.upper(F.col("cst_marital_status")) == "M", "Married")\n .otherwise("n/a")')],
        test={"note": "A consistency review rather than a pass/fail check:", "sql": "-- Data Standardization & Consistency\nSELECT DISTINCT \n    cst_marital_status \nFROM silver.crm_cust_info;"},
        status="resolved",
        cites=[("wh", P1, "WHEN UPPER(TRIM(cst_marital_status)) = 'S' THEN 'Single'"), ("db", NB + "crm/silver_crm_cust_info.ipynb", '"Single"')],
        raw_file=("wh", "datasets/source_crm/cust_info.csv"),
    ),
    dict(
        id="WH-05", source="wh", fixed_in=[1, 2], file="cust_info.csv", column="cst_gndr",
        layer="Silver → Gold", kind="missing",
        title="Gender missing in a quarter of CRM customers",
        raw="", expected="taken from the ERP",
        rows=4578, of=18494,
        spec={"type": "variants", "variants": [["M", 7068, "Male"], ["F", 6848, "Female"], ["", 4578, "n/a → ERP value"]]},
        wrong="4,578 CRM customers have no gender. The ERP file CUST_AZ12 has its own gender column for the same customers.",
        impact="Two systems disagree or have gaps; the model has to decide which one wins, and say so.",
        fixes=[(1, "Silver maps M/F to Male/Female. Gold treats the CRM as the primary source and falls back to the ERP when the CRM says n/a.",
                "WHEN ci.cst_gndr != 'n/a' THEN ci.cst_gndr -- CRM is the primary source for gender\nELSE COALESCE(ca.gen, 'n/a')  \t\t\t   -- Fallback to ERP data"),
               (2, "The same precedence rule in the Gold notebook.", "CASE\n    WHEN ci.gender <> 'n/a' THEN ci.gender\n    ELSE COALESCE(ca.gender, 'n/a')\nEND AS gender,")],
        status="resolved",
        cites=[("wh", "scripts/gold/ddl_gold.sql", "CRM is the primary source for gender"), ("db", "scripts/gold_layer/gold_dim_customers.ipynb", "COALESCE(ca.gender, 'n/a')")],
        raw_file=("wh", "datasets/source_crm/cust_info.csv"),
    ),
    dict(
        id="WH-06", source="wh", fixed_in=[1, 2], file="prd_info.csv", column="prd_key",
        layer="Bronze → Silver", kind="keys",
        title="Two keys packed into one product key",
        raw="CO-RF-FR-R92B-58", expected="cat_id CO_RF · prd_key FR-R92B-58",
        rows=397, of=397,
        spec={"type": "split", "parts": [["CO-RF", "CO_RF", "cat_id — joins the ERP category table"], ["-", "", ""], ["FR-R92B-58", "FR-R92B-58", "prd_key — joins sales"]]},
        wrong="The first five characters of every product key are a category code, written with a hyphen where the ERP category table uses an underscore.",
        impact="Without splitting the key, products can’t be joined to their category, and sales can’t be joined to products.",
        fixes=[(1, "Split into two columns and align the separator with the ERP.", "REPLACE(SUBSTRING(prd_key, 1, 5), '-', '_') AS cat_id, -- Extract category ID\nSUBSTRING(prd_key, 7, LEN(prd_key)) AS prd_key,        -- Extract product key"),
               (2, "Same split in PySpark.", 'df = df.withColumn("cat_id", F.regexp_replace(F.substring(col("prd_key"), 1, 5), "-", "_"))\ndf = df.withColumn("prd_key", F.substring(col("prd_key"), 7, F.length(col("prd_key"))))')],
        status="resolved",
        cites=[("wh", P1, "AS cat_id, -- Extract category ID"), ("db", NB + "crm/silver_crm_prd_info.ipynb", "regexp_replace")],
        raw_file=("wh", "datasets/source_crm/prd_info.csv"),
    ),
    dict(
        id="WH-07", source="wh", fixed_in=[1, 2], file="prd_info.csv", column="prd_line",
        layer="Bronze → Silver", kind="codes",
        title="Product line codes with a trailing space",
        raw="R ", expected="Road",
        rows=397, of=397,
        spec={"type": "variants", "variants": [["R ", 162, "Road"], ["M ", 112, "Mountain"], ["S ", 54, "Other Sales"], ["T ", 52, "Touring"], ["", 17, "n/a"]]},
        wrong="Every product line code is one letter followed by a space; 17 products have none.",
        impact="A comparison with 'R' fails on 'R '. The space is invisible in most tools.",
        fixes=[(1, "Trim, upper-case, then map each code to its name.", "WHEN UPPER(TRIM(prd_line)) = 'M' THEN 'Mountain'\nWHEN UPPER(TRIM(prd_line)) = 'R' THEN 'Road'\nWHEN UPPER(TRIM(prd_line)) = 'S' THEN 'Other Sales'\nWHEN UPPER(TRIM(prd_line)) = 'T' THEN 'Touring'\nELSE 'n/a'"),
               (2, "Trimmed by the all-columns loop, then mapped.", 'F.when(F.upper(col("prd_line")) == "M", "Mountain")\n .when(F.upper(col("prd_line")) == "R", "Road")')],
        test={"note": "A consistency review:", "sql": "-- Data Standardization & Consistency\nSELECT DISTINCT \n    prd_line \nFROM silver.crm_prd_info;"},
        status="resolved",
        cites=[("wh", P1, "WHEN UPPER(TRIM(prd_line)) = 'R' THEN 'Road'"), ("db", NB + "crm/silver_crm_prd_info.ipynb", '"Road"')],
        raw_file=("wh", "datasets/source_crm/prd_info.csv"),
    ),
    dict(
        id="WH-08", source="wh", fixed_in=[1, 2], file="prd_info.csv", column="prd_cost",
        layer="Bronze → Silver", kind="missing",
        title="Products with no cost",
        raw="", expected="0",
        rows=2, of=397,
        spec={"type": "empty", "label": "prd_cost"},
        wrong="Two products arrive with an empty cost.",
        impact="A NULL cost makes any margin or cost total silently NULL too.",
        fixes=[(1, "Defaulted to zero.", "ISNULL(prd_cost, 0) AS prd_cost,"),
               (2, "Same default in PySpark.", 'df = df.withColumn("prd_cost", F.coalesce(col("prd_cost"), F.lit(0)))')],
        test={"sql": "-- Check for NULLs or Negative Values in Cost\n-- Expectation: No Results\nSELECT \n    prd_cost \nFROM silver.crm_prd_info\nWHERE prd_cost < 0 OR prd_cost IS NULL;"},
        status="resolved",
        cites=[("wh", P1, "ISNULL(prd_cost, 0) AS prd_cost"), ("wh", T1, "WHERE prd_cost < 0 OR prd_cost IS NULL;"),
               ("db", NB + "crm/silver_crm_prd_info.ipynb", "F.coalesce")],
        raw_file=("wh", "datasets/source_crm/prd_info.csv"),
    ),
    dict(
        id="WH-09", source="wh", fixed_in=[1], file="prd_info.csv", column="prd_start_dt, prd_end_dt",
        layer="Bronze → Silver", kind="impossible",
        title="Products that end before they start",
        raw="2011-07-01 → 2007-12-28", expected="end = next start − 1 day",
        rows=200, of=397,
        spec={"type": "order", "a": ["prd_start_dt", "2011-07-01"], "b": ["prd_end_dt", "2007-12-28"], "key": "AC-HE-HL-U509-R · Sport-100 Helmet- Red"},
        wrong="Half of the product history rows have an end date earlier than their start date.",
        impact="Product history (which price applied when) can’t be trusted if a version ends before it begins.",
        fixes=[(1, "Ignore the stored end date. Rebuild it as the day before the next version of the same product starts.",
                "CAST(\n    LEAD(prd_start_dt) OVER (PARTITION BY prd_key ORDER BY prd_start_dt) - 1 \n    AS DATE\n) AS prd_end_dt -- Calculate end date as one day before the next start date")],
        test={"sql": "-- Check for Invalid Date Orders (Start Date > End Date)\n-- Expectation: No Results\nSELECT \n    * \nFROM silver.crm_prd_info\nWHERE prd_end_dt < prd_start_dt;"},
        status="resolved",
        cites=[("wh", P1, "LEAD(prd_start_dt) OVER (PARTITION BY prd_key ORDER BY prd_start_dt) - 1"), ("wh", T1, "WHERE prd_end_dt < prd_start_dt;")],
        raw_file=("wh", "datasets/source_crm/prd_info.csv"),
    ),
    dict(
        id="WH-10", source="wh", fixed_in=[1, 2], file="sales_details.csv", column="sls_order_dt",
        layer="Bronze → Silver", kind="format",
        title="Order dates stored as integers — some of them not dates",
        raw="20101229", expected="2010-12-29",
        rows=19, of=60398, rows_note="All 60,398 order dates are integers. 19 can’t be dates at all: 17 zeros, plus 32154 and 5489.",
        spec={"type": "pair", "pairs": [["20101229", "2010-12-29"], ["0", "NULL"], ["32154", "NULL"], ["5489", "NULL"]]},
        wrong="Order, ship and due dates arrive as eight-digit integers. Nineteen order dates are 0 or have the wrong number of digits.",
        impact="Integer dates can’t be filtered by month or compared with real dates; casting a bad one fails the whole load.",
        fixes=[(1, "Invalid values become NULL; the rest are cast through text to DATE.", "CASE \n    WHEN sls_order_dt = 0 OR LEN(sls_order_dt) != 8 THEN NULL\n    ELSE CAST(CAST(sls_order_dt AS VARCHAR) AS DATE)\nEND AS sls_order_dt,"),
               (2, "Same rule with an explicit yyyyMMdd pattern.", 'F.when(\n    (col("sls_order_dt") == 0) | (length(col("sls_order_dt")) != 8),\n    None\n).otherwise(F.to_date(col("sls_order_dt").cast("string"), "yyyyMMdd"))')],
        test={"note": "The same rule as a check on the raw table:", "sql": "-- Check for Invalid Dates\n-- Expectation: No Invalid Dates\nSELECT \n    NULLIF(sls_due_dt, 0) AS sls_due_dt \nFROM bronze.crm_sales_details\nWHERE sls_due_dt <= 0 \n    OR LEN(sls_due_dt) != 8 \n    OR sls_due_dt > 20500101 \n    OR sls_due_dt < 19000101;"},
        status="resolved",
        cites=[("wh", P1, "WHEN sls_order_dt = 0 OR LEN(sls_order_dt) != 8 THEN NULL"), ("wh", T1, "OR sls_due_dt > 20500101"),
               ("db", NB + "crm/silver_crm_sales_details.ipynb", "yyyyMMdd")],
        raw_file=("wh", "datasets/source_crm/sales_details.csv"),
    ),
    dict(
        id="WH-11", source="wh", fixed_in=[1], file="sales_details.csv", column="sls_sales",
        layer="Bronze → Silver", kind="arithmetic",
        title="Sales amounts that don’t equal quantity × price",
        raw="35 = 2 × 35", expected="70",
        rows=23, of=60398, rows_note="23 rows where the amount is missing, zero or negative, or doesn’t equal quantity × price.",
        spec={"type": "arith", "rows": [["SO58335", "35", "2", "35", "70"], ["SO61570", "-18", "1", "9", "9"], ["SO61548", "", "1", "9", "9"]]},
        wrong="The sales amount is sometimes missing, negative, or simply doesn’t match the quantity and price on the same line.",
        impact="Revenue is the number every report starts from. If the line total and its parts disagree, one of them is wrong.",
        fixes=[(1, "When the amount is missing, not positive or inconsistent, recompute it from quantity × |price|.",
                "WHEN sls_sales IS NULL OR sls_sales <= 0 OR sls_sales != sls_quantity * ABS(sls_price) \n\tTHEN sls_quantity * ABS(sls_price)\nELSE sls_sales")],
        test={"sql": "-- Check Data Consistency: Sales = Quantity * Price\n-- Expectation: No Results\nSELECT DISTINCT \n    sls_sales,\n    sls_quantity,\n    sls_price \nFROM silver.crm_sales_details\nWHERE sls_sales != sls_quantity * sls_price\n   OR sls_sales IS NULL \n   OR sls_quantity IS NULL \n   OR sls_price IS NULL\n   OR sls_sales <= 0 \n   OR sls_quantity <= 0 \n   OR sls_price <= 0\nORDER BY sls_sales, sls_quantity, sls_price;"},
        status="resolved",
        cites=[("wh", P1, "WHEN sls_sales IS NULL OR sls_sales <= 0 OR sls_sales != sls_quantity * ABS(sls_price)"), ("wh", T1, "-- Check Data Consistency: Sales = Quantity * Price")],
        raw_file=("wh", "datasets/source_crm/sales_details.csv"),
    ),
    dict(
        id="WH-12", source="wh", fixed_in=[1, 2], file="sales_details.csv", column="sls_price",
        layer="Bronze → Silver", kind="missing",
        title="Prices missing or negative",
        raw="-769", expected="769 (sales ÷ quantity)",
        rows=12, of=60398, rows_note="12 prices are empty, zero or negative (5 negative).",
        spec={"type": "empty", "label": "sls_price"},
        wrong="Twelve sale lines have no usable unit price.",
        impact="Price feeds every average-price and margin figure; a negative one flips the sign of whatever it touches.",
        fixes=[(1, "Derive the price from the line total.", "WHEN sls_price IS NULL OR sls_price <= 0 \n\tTHEN sls_sales / NULLIF(sls_quantity, 0)\nELSE sls_price  -- Derive price if original value is invalid"),
               (2, "Same derivation in PySpark, guarding against a zero quantity.", 'F.when(\n    (col("sls_price").isNull()) | (col("sls_price") <= 0),\n    F.when(\n        col("sls_quantity") != 0,\n        col("sls_sales") / col("sls_quantity")\n    ).otherwise(None)\n).otherwise(col("sls_price"))')],
        status="resolved",
        cites=[("wh", P1, "THEN sls_sales / NULLIF(sls_quantity, 0)"), ("db", NB + "crm/silver_crm_sales_details.ipynb", 'col("sls_sales") / col("sls_quantity")')],
        raw_file=("wh", "datasets/source_crm/sales_details.csv"),
    ),
    dict(
        id="WH-13", source="wh", fixed_in=[1, 2], file="CUST_AZ12.csv", column="CID",
        layer="Bronze → Silver", kind="keys",
        title="ERP customer keys with a three-letter prefix",
        raw="NASAW00011000", expected="AW00011000",
        rows=11042, of=18484,
        spec={"type": "chars", "cut": [0, 3]},
        wrong="The ERP writes the same customer number as the CRM, but 11,042 of them start with NAS.",
        impact="The ERP’s birth dates and genders can’t be joined to CRM customers until the keys match.",
        fixes=[(1, "Strip the prefix when present.", "WHEN cid LIKE 'NAS%' THEN SUBSTRING(cid, 4, LEN(cid)) -- Remove 'NAS' prefix if present\nELSE cid"),
               (2, "Same rule in PySpark.", 'F.when(col("cid").startswith("NAS"),\n       F.substring(col("cid"), 4, F.length(col("cid"))))\n .otherwise(col("cid"))')],
        status="resolved",
        cites=[("wh", P1, "WHEN cid LIKE 'NAS%' THEN SUBSTRING(cid, 4, LEN(cid))"), ("db", NB + "erp/silver_erp_cust_az12.ipynb", 'startswith(\\"NAS\\")')],
        raw_file=("wh", "datasets/source_erp/CUST_AZ12.csv"),
    ),
    dict(
        id="WH-14", source="wh", fixed_in=[1, 2], file="CUST_AZ12.csv", column="BDATE",
        layer="Bronze → Silver", kind="impossible",
        title="Customers born in the future",
        raw="11/20/9999", expected="NULL",
        rows=16, of=18484, rows_note="16 birth dates lie in the future, from 2038 to 9999.",
        spec={"type": "pair", "pairs": [["11/20/9999", "NULL"], ["7/6/2050", "NULL"], ["10/17/2038", "NULL"]]},
        wrong="Sixteen ERP birth dates are in the future; four of them are in the year 9999.",
        impact="A single impossible birth date wrecks an age distribution and any “average age” figure.",
        fixes=[(1, "Birth dates after today become NULL.", "WHEN bdate > GETDATE() THEN NULL\nELSE bdate"),
               (2, "Same rule in PySpark.", 'F.when(col("bdate") > F.current_date(), None)\n .otherwise(col("bdate"))')],
        test={"sql": "-- Identify Out-of-Range Dates\n-- Expectation: Birthdates between 1924-01-01 and Today\nSELECT DISTINCT \n    bdate \nFROM silver.erp_cust_az12\nWHERE bdate < '1924-01-01' \n   OR bdate > GETDATE();"},
        status="resolved",
        cites=[("wh", P1, "WHEN bdate > GETDATE() THEN NULL"), ("wh", T1, "Birthdates between 1924-01-01 and Today"),
               ("db", NB + "erp/silver_erp_cust_az12.ipynb", "current_date")],
        raw_file=("wh", "datasets/source_erp/CUST_AZ12.csv"),
    ),
    dict(
        id="WH-15", source="wh", fixed_in=[1, 2], file="CUST_AZ12.csv", column="GEN",
        layer="Bronze → Silver", kind="codes",
        title="Nine spellings of two genders",
        raw="M ", expected="Male",
        rows=18484, of=18484,
        spec={"type": "variants", "variants": [["Male", 8608, "Male"], ["Female", 8391, "Female"], ["", 1472, "n/a"], ["F", 4, "Female"], [" ", 3, "n/a"], ["M", 3, "Male"], ["  ", 1, "n/a"], ["M ", 1, "Male"], ["F ", 1, "Female"]]},
        wrong="The ERP gender column mixes full words, single letters, letters with a trailing space, and values that are only spaces.",
        impact="Counting by gender over this column gives nine groups instead of two (plus unknown).",
        fixes=[(1, "Trim, upper-case, accept both forms.", "WHEN UPPER(TRIM(gen)) IN ('F', 'FEMALE') THEN 'Female'\nWHEN UPPER(TRIM(gen)) IN ('M', 'MALE') THEN 'Male'\nELSE 'n/a'"),
               (2, "Same rule after the all-columns trim.", 'F.when(F.upper(col("gen")).isin("F", "FEMALE"), "Female")\n .when(F.upper(col("gen")).isin("M", "MALE"), "Male")\n .otherwise("n/a")')],
        test={"note": "A consistency review:", "sql": "-- Data Standardization & Consistency\nSELECT DISTINCT \n    gen \nFROM silver.erp_cust_az12;"},
        status="resolved",
        cites=[("wh", P1, "WHEN UPPER(TRIM(gen)) IN ('F', 'FEMALE') THEN 'Female'"), ("db", NB + "erp/silver_erp_cust_az12.ipynb", '\\"FEMALE\\"')],
        raw_file=("wh", "datasets/source_erp/CUST_AZ12.csv"),
    ),
    dict(
        id="WH-16", source="wh", fixed_in=[1, 2], file="LOC_A101.csv", column="CID",
        layer="Bronze → Silver", kind="keys",
        title="A hyphen in every location key",
        raw="AW-00011000", expected="AW00011000",
        rows=18484, of=18484,
        spec={"type": "chars", "cut": [2, 3]},
        wrong="The location file writes customer numbers with a hyphen the other two files don’t use.",
        impact="Without the fix, not one customer gets a country.",
        fixes=[(1, "Remove the hyphen.", "REPLACE(cid, '-', '') AS cid,"),
               (2, "Same rule in PySpark.", 'df = df.withColumn("cid", F.regexp_replace(col("cid"), "-", ""))')],
        status="resolved",
        cites=[("wh", P1, "REPLACE(cid, '-', '') AS cid"), ("db", NB + "erp/silver_erp_loc_a101.ipynb", "regexp_replace")],
        raw_file=("wh", "datasets/source_erp/LOC_A101.csv"),
    ),
    dict(
        id="WH-17", source="wh", fixed_in=[1, 2], file="LOC_A101.csv", column="CNTRY",
        layer="Bronze → Silver", kind="codes",
        title="One country, three spellings",
        raw="USA", expected="United States",
        rows=4994, of=18484, rows_note="2,591 USA, 1,500 US, 566 DE, 332 empty and 5 made only of spaces.",
        spec={"type": "variants", "variants": [["United States", 3391, "United States"], ["USA", 2591, "United States"], ["US", 1500, "United States"], ["Germany", 1214, "Germany"], ["DE", 566, "Germany"], ["", 332, "n/a"], ["  ", 2, "n/a"], [" ", 2, "n/a"], ["   ", 1, "n/a"]]},
        wrong="Country names are mixed with ISO-style codes, and some values are empty or only spaces.",
        impact="Sales by country would show the United States three times.",
        fixes=[(1, "Map codes to names; empty or blank becomes n/a.", "WHEN TRIM(cntry) = 'DE' THEN 'Germany'\nWHEN TRIM(cntry) IN ('US', 'USA') THEN 'United States'\nWHEN TRIM(cntry) = '' OR cntry IS NULL THEN 'n/a'\nELSE TRIM(cntry)"),
               (2, "Same mapping in PySpark.", 'F.when(col("cntry") == "DE", "Germany")\n .when(col("cntry").isin("US", "USA"), "United States")\n .when((col("cntry") == "") | col("cntry").isNull(), "n/a")\n .otherwise(col("cntry"))')],
        test={"note": "A consistency review:", "sql": "-- Data Standardization & Consistency\nSELECT DISTINCT \n    cntry \nFROM silver.erp_loc_a101\nORDER BY cntry;"},
        status="resolved",
        cites=[("wh", P1, "WHEN TRIM(cntry) IN ('US', 'USA') THEN 'United States'"), ("db", NB + "erp/silver_erp_loc_a101.ipynb", '\\"United States\\"')],
        raw_file=("wh", "datasets/source_erp/LOC_A101.csv"),
    ),
    dict(
        id="WH-18", source="wh", fixed_in=[1], file="PX_CAT_G1V2.csv", column="CAT, SUBCAT, MAINTENANCE",
        layer="Silver", kind="whitespace",
        title="Category table: checked, nothing to fix",
        raw="Accessories", expected="Accessories",
        rows=0, of=37,
        spec={"type": "clean", "query": "WHERE cat != TRIM(cat) OR subcat != TRIM(subcat) OR maintenance != TRIM(maintenance)"},
        wrong="Nothing. The category table is the one source file with no whitespace, code or key problems; it is loaded as it arrives.",
        impact="A clean result is a result too: it is the reason this table can be loaded without transformation.",
        fixes=[],
        test={"sql": "-- Check for Unwanted Spaces\n-- Expectation: No Results\nSELECT \n    * \nFROM silver.erp_px_cat_g1v2\nWHERE cat != TRIM(cat) \n   OR subcat != TRIM(subcat) \n   OR maintenance != TRIM(maintenance);"},
        status="clean",
        cites=[("wh", T1, "WHERE cat != TRIM(cat)")],
        raw_file=("wh", "datasets/source_erp/PX_CAT_G1V2.csv"),
    ),

    # -----------------------------------------------------------------------
    # Healthcare lakehouse — Silver notebooks. Counts replayed from the CSVs.
    # -----------------------------------------------------------------------
    dict(
        id="HC-01", source="hc", fixed_in=[3], file="patients.csv", column="all columns",
        layer="Bronze → Silver", kind="duplicates",
        title="A hundred patients listed twice",
        raw="1,M,", expected="one row per patient",
        rows=100, of=100100, rows_note="100,100 rows in; 100,000 after removing exact copies.",
        spec={"type": "count", "in": 100100, "out": 100000, "unit": "patient rows"},
        wrong="The patient file contains 100 rows that are exact copies of other rows.",
        impact="Every admission for a duplicated patient would join twice.",
        detected="The notebook compares the row count with the count after dropDuplicates(), and separately checks that patient_id is unique.",
        fixes=[(3, "Exact copies removed.", "patients_clean = patients.dropDuplicates()")],
        status="resolved",
        cites=[("hc", "scripts/silver/ehr/patients.ipynb", "dropDuplicates()")],
        raw_file=("hc", "datasets/ehr/patients.csv"),
    ),
    dict(
        id="HC-02", source="hc", fixed_in=[3], file="patients.csv", column="city",
        layer="Bronze → Silver", kind="missing",
        title="Patients with no city — kept, but set aside",
        raw="", expected="moved to patients_missing_city",
        rows=51, of=100000,
        spec={"type": "quarantine", "in": 100000, "out": 99949, "aside": 51, "table": "health.silver.patients_missing_city"},
        wrong="51 patients have no city.",
        impact="Dropping them would lose real patients; keeping them in the main table would put blanks into every geographic breakdown.",
        detected="Null-count profile of every column.",
        fixes=[(3, "Valid rows go to health.silver.patients; the 51 go to their own table instead of being deleted.",
                'valid_patients = patients_clean.filter(\n    F.col("city").isNotNull()\n)\npatients_missing_city = patients_clean.filter(\n    F.col("city").isNull()\n)')],
        status="resolved",
        cites=[("hc", "scripts/silver/ehr/patients.ipynb", "patients_missing_city")],
        raw_file=("hc", "datasets/ehr/patients.csv"),
    ),
    dict(
        id="HC-03", source="hc", fixed_in=[3], file="admissions_2021–2025.csv", column="admission_date",
        layer="Bronze → Silver", kind="missing",
        title="Admissions with no admission date",
        raw="1,57399,246,4724,216,", expected="moved to admissions_missing_date",
        rows=105, of=500000, rows_note="105 of 500,000 admissions across the five yearly files.",
        spec={"type": "quarantine", "in": 500000, "out": 499895, "aside": 105, "table": "health.silver.admissions_missing_date",
              "row": ["admission_id", "patient_id", "hospital_id", "doctor_id", "procedure_id", "admission_date"],
              "vals": ["1", "57399", "246", "4724", "216", ""]},
        wrong="The very first admission in the 2021 file has every ID but no date. 105 admissions are like that.",
        impact="An admission without a date can’t be counted in admissions_by_year, but its billing still exists.",
        detected="Null-count profile after consolidating the five yearly files.",
        fixes=[(3, "The five yearly files are unioned first; rows without a date are written to a separate table.",
                'valid_admissions = admissions.filter(\n    F.col("admission_date").isNotNull()\n)\nadmissions_missing_date = admissions.filter(\n    F.col("admission_date").isNull()\n)')],
        status="resolved",
        cites=[("hc", "scripts/silver/ehr/admissions.ipynb", "admissions_missing_date")],
        raw_file=("hc", "datasets/ehr/admissions_2021.csv"),
    ),
    dict(
        id="HC-04", source="hc", fixed_in=[3], file="billing_2021–2025.csv", column="patient_paid",
        layer="Bronze → Silver", kind="format",
        title="Money with fifteen decimal places",
        raw="6585.389999999999", expected="6585.39",
        rows=245846, of=500000,
        spec={"type": "pair", "pairs": [["6585.389999999999", "6585.39"], ["14690.099999999999", "14690.10"]]},
        wrong="Nearly half of the patient payments carry floating-point noise: 6585.389999999999 instead of 6585.39.",
        impact="Sums drift by fractions of a cent and equality checks between totals fail for no business reason.",
        detected="Min/max profile and a financial integrity check on the consolidated billing table.",
        fixes=[(3, "Both payment columns rounded to two decimals.", 'billing_clean = (\n    billing\n    .withColumn(\n        "insurance_paid",\n        F.round(F.col("insurance_paid"), 2)\n    )\n    .withColumn(\n        "patient_paid",\n        F.round(F.col("patient_paid"), 2)\n    )\n)')],
        status="resolved",
        cites=[("hc", "scripts/silver/billing/billing.ipynb", "Round Financial Values to 2 Decimal Places")],
        raw_file=("hc", "datasets/billing/billing_2021.csv"),
    ),
    dict(
        id="HC-05", source="hc", fixed_in=[3], file="billing_2021–2025.csv", column="total_cost = insurance_paid + patient_paid",
        layer="Silver", kind="arithmetic",
        title="Do the payments add up? Checked: yes",
        raw="15029 = 8443.61 + 6585.39", expected="0 mismatches",
        rows=0, of=500000,
        spec={"type": "clean", "query": "round(insurance_paid + patient_paid, 2) != round(total_cost, 2)"},
        wrong="Nothing — every bill’s two payments add up to its total, once rounded to the cent.",
        impact="This is the check that makes the revenue Gold tables safe to sum.",
        fixes=[],
        test={"lang": "python", "sql": 'billing_mismatch = billing.filter(\n    F.round(\n        F.col("insurance_paid") + F.col("patient_paid"),\n        2\n    ) != F.round(F.col("total_cost"), 2)\n)\nprint(\n    f"Mismatched Records: {billing_mismatch.count()}"\n)'},
        status="clean",
        cites=[("hc", "scripts/silver/billing/billing.ipynb", "Financial Integrity Validation")],
        raw_file=("hc", "datasets/billing/billing_2021.csv"),
    ),
    dict(
        id="HC-06", source="hc", fixed_in=[3], file="admissions + billing, 2021–2025", column="admission_id, billing_id",
        layer="Silver", kind="duplicates",
        title="Business keys across ten yearly files: unique",
        raw="admission_id", expected="0 duplicates",
        rows=0, of=1000000,
        spec={"type": "clean", "query": "count(*) vs count(distinct id) — 500,000 = 500,000, twice"},
        wrong="Nothing. Splitting a table into yearly files is a common way to get duplicate IDs; these files don’t have any.",
        impact="Unique keys are what allow billing to be joined back to admissions one-to-one.",
        fixes=[],
        test={"lang": "python", "sql": 'total_rows = billing.count()\ndistinct_billing_ids = (\n    billing\n    .select("billing_id")\n    .distinct()\n    .count()\n)'},
        status="clean",
        cites=[("hc", "scripts/silver/billing/billing.ipynb", "Business Key Validation"), ("hc", "scripts/silver/ehr/admissions.ipynb", "distinct_admission_ids")],
        raw_file=("hc", "datasets/billing/billing_2021.csv"),
    ),
]

# ---------------------------------------------------------------------------
# Harborview Bank — copied from the author's data-quality log (numbers verified
# against the raw CSVs; see profile_p4.py).
# ---------------------------------------------------------------------------
LOG = "02_documentation/02_Data_Quality_Log.md"
MEMO_MISSING = "Ask the data owner for the missing November and December 2025 customers and correct the 40 account close dates."


def hb(n, file, column, kind, title, raw, expected, rows, of, found, fix, spec, wrong, impact, find, status="resolved", **kw):
    e = dict(id=f"HB-{n}", source="hb", fixed_in=[4], file=file, column=column, layer="Power Query", kind=kind,
             title=title, raw=raw, expected=expected, rows=rows, of=of, detected=found,
             fixes=[(4, fix, None)], spec=spec, wrong=wrong, impact=impact, status=status,
             cites=[("hb", LOG, find)], raw_file=("hb", "01_raw_data/" + (file if file.endswith(".csv") else "customers.csv")))
    e.update(kw)
    return e


ENTRIES += [
    hb("02", "customers.csv", "customer_id", "duplicates", "120 customers copied whole", "C10200 ×2", "one row each",
       120, 20120, "Count 20,120, distinct 20,000, unique 19,880", "Removed duplicates across all columns.",
       {"type": "count", "in": 20120, "out": 20000, "unit": "customer rows"},
       "Whole customer rows appear twice.", "Every account and loan of a duplicated customer would be counted twice in customer-level KPIs.",
       "| 2 | customer_id |"),
    hb("03", "customers.csv", "gender", "codes", "Eight versions of two values", "FEMALE", "Female",
       1968, 20120, "Distinct count 8, expected 2", "Capitalised each word, then replaced M with Male and F with Female (whole cell).",
       {"type": "variants", "variants": [["Female", 9107, "Female"], ["Male", 9032, "Male"], ["male", 355, "Male"], ["f", 340, "Female"], ["M", 340, "Male"], ["m", 322, "Male"], ["FEMALE", 316, "Female"], ["F", 308, "Female"]]},
       "Case and abbreviations: male, FEMALE, M, m, F, f next to Male and Female.", "A slicer on gender would show eight options.",
       "| 3 | gender |"),
    hb("04", "customers.csv", "birth_date", "placeholder", "Customers aged 126", "1900-01-01", "null",
       104, 20120, "Minimum value and a temporary filter", "Replaced with null; customers kept, age analysis skips them.",
       {"type": "pair", "pairs": [["1900-01-01", "null"]], "note": "age 126"},
       "A placeholder date standing in for “unknown”.", "Placeholder values are missing data that looks real — they pass every type check.",
       "| 4 | birth_date |", lesson="Placeholder values (0, 999, 1900-01-01) are missing data that looks real."),
    hb("07", "customers.csv", "email", "whitespace", "Shouting emails with a trailing space", "NOAH.ROSSI5541@MAIL.EXAMPLE ", "noah.rossi5541@mail.example",
       1030, 20120, "Contains \"@MAIL\" 1,030; ends with a space 1,030", "Trimmed and lower-cased.",
       {"type": "chars"},
       "Upper case and a trailing space, always on the same rows.", "The same address in two forms breaks uniqueness and any join on email.",
       "| 7 | email |"),
    hb("08", "customers.csv", "region", "missing", "Missing region stored as an empty string", "", "the home branch’s region",
       299, 20120, "2% empty; 6 distinct values (5 regions and blank)", "Filled from the home branch’s region (20,000 of 20,000 matched).",
       {"type": "empty", "label": "region"},
       "Region is blank — an empty string, not a null.", "A null check alone wouldn’t find it.",
       "| 8 | region |", lesson="Missing values can be empty strings, not null. Check both.", rows_note="299 rows; 298 after removing duplicates."),
    hb("11", "customers.csv", "income_band", "codes", "Hgh", "Hgh", "High",
       189, 20120, "Distinct count 8; minimum \" Medium\" shows the space", "Trimmed, capitalised each word, replaced Hgh with High.",
       {"type": "variants", "variants": [["Medium", 8036, "Medium"], ["Low", 7155, "Low"], ["High", 3648, "High"], ["Very High", 1091, "Very High"], ["Very high", 56, "Very High"], ["Hgh", 46, "High"], ["low", 44, "Low"], [" Medium", 44, "Medium"]]},
       "Eight values instead of four: case, a typo and a leading space.", "Income-band breakdowns would split real groups and hide 46 high earners.",
       "| 11 | income_band |"),
    hb("12", "customers.csv", "signup_date", "format", "Two date formats in one column", "17/12/2022", "2022-12-17",
       1423, 20120, "Value list; filter on \"/\"", "Custom column parsing each format separately, 0 errors.",
       {"type": "pair", "pairs": [["17/12/2022", "2022-12-17"], ["2022-12-17", "2022-12-17"]], "note": "17 can only be a day"},
       "YYYY-MM-DD and DD/MM/YYYY mixed together. 17/12/2022 proves the second format is day first.",
       "A US-locale type change would have failed on 874 rows and silently swapped day and month on 549.",
       "| 12 | signup_date |"),
    hb("01", "accounts.csv", "status", "codes", "Four spellings of open and closed", "CLOSED", "Closed",
       1831, 36605, "Distinct count 4; the four counts add to 36,605", "Capitalised each word: Open 25,971, Closed 10,634.",
       {"type": "variants", "variants": [["Open", 24669, "Open"], ["Closed", 10105, "Closed"], ["open", 1302, "Open"], ["CLOSED", 529, "Closed"]]},
       "open and CLOSED next to Open and Closed.", "Counting open accounts by an exact match would miss 1,302 of them.",
       "| 1 | status |"),
    hb("18", "accounts.csv", "close_date, open_date", "impossible", "Accounts closed before they were opened", "2019-02-09 → 2019-01-10", "open_date + 30 days",
       40, 36605, "True/false check column, 40 true", "Set close_date to open_date + 30 and flagged the rows in close_date_corrected.",
       {"type": "order", "a": ["open_date", "2019-02-09"], "b": ["close_date", "2019-01-10"], "key": "A000295 · checking"},
       "40 accounts closed exactly 30 days before they opened. open_date is right: account IDs follow open-date order.",
       "An account can’t churn before it exists; these rows would distort closure rates.",
       "| 18 | close_date and open_date |", status="reopened", see="HB-L2", memo=MEMO_MISSING),
    hb("19", "loans.csv", "loan_id", "duplicates", "Twenty loans listed twice", "L00079 ×2", "5,300 unique loans",
       20, 5320, "Count 5,320, distinct 5,300, unique 5,280; Keep Duplicates on all columns returned 40 rows", "Removed duplicates; 5,300 unique loans.",
       {"type": "count", "in": 5320, "out": 5300, "unit": "loan rows"},
       "Exact copies of 20 loans.", "Duplicated loans double their balance and, if they default, their loss.",
       "| 19 | loan_id |"),
    hb("24", "loans.csv", "loan_amount", "missing", "Loan amounts left blank", "", "calculated, flagged",
       15, 5320, "15 empty strings", "Flagged in loan_amount_calculated, then calculated from payment, rate and term with the standard loan formula, rounded to 100. Tested first on loans with a known amount.",
       {"type": "empty", "label": "loan_amount"},
       "Fifteen loans have no amount — stored as an empty string.", "Lending volume by year would be understated, silently.",
       "| 24 | loan_amount |", lesson="Before filling a missing value with a formula, test the formula on rows where the answer is known."),
    hb("25", "loans.csv", "interest_rate", "scale", "Rates stored as percentages", "9.96", "0.0996",
       341, 5320, "Sorted descending; filtered values not starting with \"0.\"", "Divided by 100 when 1 or higher. Average fell from 71.5% to about 9%.",
       {"type": "scale", "from": "9.96", "to": "0.0996", "note": "average 71.5% → about 9%"},
       "341 rates are written as percentages (9.96) among decimals (0.0996).", "One column, two scales: the average rate came out at 71.5%.",
       "| 25 | interest_rate |", rows_note="341 rows; 339 after removing duplicates."),
    hb("28", "loans.csv", "credit_score_at_origination", "placeholder", "Credit scores of 0 and 999", "999", "null → “Unknown” band",
       39, 5320, "Minimum 0, maximum 999", "Replaced with null; loans kept and shown as \"Unknown\" in score bands.",
       {"type": "pair", "pairs": [["0", "null"], ["999", "null"]], "note": "valid range 300–850"},
       "Scores outside the 300–850 scale: 0 on 22 loans, 999 on 17.", "Credit score was the strongest predictor of default in this analysis; placeholder scores would land in the wrong bands.",
       "| 28 | credit_score_at_origination |"),
    hb("34", "transactions", "txn_id", "duplicates", "9,279 transactions listed twice", "T00000320 ×2", "one row each",
       9279, 2329114, "Count 2,329,114, distinct 2,319,835; Keep Duplicates on all columns returned 18,558 rows", "Removed duplicates.",
       {"type": "count", "in": 2329114, "out": 2319835, "unit": "transaction rows"},
       "Exact copies of 9,279 transactions.", "Fee income is a sum of transactions; copies inflate it.",
       "| 34 | txn_id |", raw_file=("hb", "01_raw_data/transactions.zip")),
    hb("35", "transactions", "account_id", "keys", "Transactions on accounts that don’t exist", "A945569", "excluded",
       150, 2329114, "Filter on IDs not starting with \"A0\"", "Inner merge with accounts excluded them (35 credits $95,720.53, 101 debits $24,646.13, 14 fees $112.00).",
       {"type": "chars", "note": "real accounts end at A036605"},
       "Orphans: account IDs in the A9xxxxx range, while real accounts end at A036605.", "Money with no account can’t be assigned to a customer, segment or region.",
       "| 35 | account_id |", raw_file=("hb", "01_raw_data/transactions.zip"), rows_note="150 rows (counted after duplicates were removed)."),
    hb("36", "transactions", "txn_datetime", "impossible", "Transactions from the future", "2026-03-02 00:00:00", "removed",
       40, 2329114, "Maximum 2026-04-29; filter on 2026", "Removed rows dated 2026 or later.",
       {"type": "pair", "pairs": [["2026-03-02 00:00:00", "removed"]], "note": "extract ends 2025-12-31"},
       "Dates after the extract date: March and April 2026, all at midnight.", "Future rows would appear in a period that hasn’t happened.",
       "| 36 | txn_datetime |", raw_file=("hb", "01_raw_data/transactions.zip")),
    hb("38", "transactions", "merchant_category", "codes", "34 categories that are really 17", "retail  ", "Retail",
       46503, 2329114, "34 distinct, exactly 17 doubled", "Trimmed and capitalised each word; 17 values.",
       {"type": "chars"},
       "Lower case and two trailing spaces, on the same rows.", "Spending by category would show every category twice.",
       "| 38 | merchant_category |", raw_file=("hb", "01_raw_data/transactions.zip"), rows_note="46,503 rows; 46,320 after removing duplicates."),
    hb("39", "transactions", "amount", "scale", "Direction stored twice", "-22.75", "22.75 (Debit)",
       17403, 2329114, "Filter on values starting with \"-\": all Debit", "Absolute value; direction stays in txn_type.",
       {"type": "pair", "pairs": [["-22.75", "22.75"]], "note": "txn_type already says Debit"},
       "Some Debit rows carry a negative amount — the direction is in the sign and in txn_type.", "Summing debits would partly cancel itself out.",
       "| 39 | amount | Negative amounts", raw_file=("hb", "01_raw_data/transactions.zip"), rows_note="17,403 rows; 17,327 after removing duplicates."),
    hb("41", "transactions", "channel", "missing", "Missing channel stored as an empty string", "", "Unknown",
       12231, 2329114, "7 channels plus blank; 12,231 blanks", "Replaced the blank with \"Unknown\".",
       {"type": "empty", "label": "channel"},
       "Normal debits and credits with an empty channel.", "Channel shares would quietly exclude 12,231 transactions.",
       "| 41 | channel |", raw_file=("hb", "01_raw_data/transactions.zip"), rows_note="12,231 rows; 12,183 after removing duplicates."),
    hb("32", "loans.csv", "default_date, origination_date", "impossible", "Loans that default before they’re issued? None", "0", "0",
       0, 5300, "True/false check column, 0 true", "None needed.",
       {"type": "clean", "query": "default_date < origination_date"},
       "Nothing — a cross-column rule checked and passed.", "Same check that caught the 40 accounts (#18), run on loans.",
       "| 32 | default_date and origination_date |", status="clean", fixes=[], lesson="A clean column is a result too: record \"no issues\"."),
]

# Known limitations — recorded in the log and the memo, not hidden.
ENTRIES += [
    dict(id="HB-L1", source="hb", fixed_in=[4], file="customers.csv, accounts.csv", column="signup_date, open_date",
         layer="Analysis", kind="missing", title="The customers who stop arriving in November",
         raw="7 · 3", expected="about 250 a month",
         rows=None, of=None, rows_note="7 new customers in November 2025 and 3 in December, against about 250 a month.",
         spec={"type": "limitation", "series": [["Oct", "~250"], ["Nov", "7"], ["Dec", "3"]]},
         wrong="New customers almost stop after 31 October 2025; account openings stop on 15 December.",
         impact="Active and new customers are understated for November and December 2025. Churn, closures, fees and losses are not affected.",
         detected="A sudden break in a flow that was steady for years — treated as a data question before a business finding.",
         fixes=[(4, "Kept the data. Customer counts are reported to October 2025, and this is stated on the dashboard, in the memo and in the README.", None)],
         status="limitation", memo=MEMO_MISSING,
         lesson="A sudden break in a flow that was steady for years is a data question before it is a business finding.",
         cites=[("hb", LOG, "| L1 | customers, accounts |"), ("hb", "02_documentation/05_Findings_Log.md", "| D1 |")],
         raw_file=("hb", "01_raw_data/customers.csv")),
    dict(id="HB-L2", source="hb", fixed_in=[4], file="accounts.csv, transactions", column="close_date",
         layer="Analysis", kind="impossible", title="My fix for #18 was wrong for most of the 40",
         raw="close_date = open_date + 30", expected="still flagged",
         rows=40, of=36605, rows_note="27 of the 40 corrected accounts have transactions after the new close date (1,436 rows); 12 checking accounts kept paying the fee (239 fees, $1,692).",
         spec={"type": "sensitivity", "rows": [["Customers who left, 2023 to 2025", "3,775", "3,762", "-0.3%"],
                                               ["Customers who left, Jul 2024 to Dec 2025", "3,044", "3,037", "-0.2%"],
                                               ["Mass checking closure rate before the change", "0.391% a month", "0.389% a month", "-0.002 points"],
                                               ["Extra Mass closures, Jul 2024 to Dec 2025", "2,640.7", "2,639.8", "under 0.1%"],
                                               ["Net effect of the price change", "$742,519", "$741,381", "-0.2%"]]},
         wrong="The correction applied in #18 — close date = open date + 30 — doesn’t survive a check against another table: most of these accounts kept transacting after their new close date.",
         impact="Very small: 0.1% of accounts. It explains why fee-paying accounts exceed open Mass checking accounts by 0 to 10 a month.",
         detected="Testing the cleaning assumption against the transactions table.",
         fixes=[(4, "Unresolved and still flagged. Recommended fix: set the close date to the end of the month of the last transaction, or treat the account as open if activity continues to December 2025. Every key result was recalculated without the 40 customers: no conclusion changes.", None)],
         status="open", memo=MEMO_MISSING,
         lesson="Test a cleaning assumption against other tables before trusting it (L2).",
         cites=[("hb", LOG, "| L2 | accounts, transactions |"), ("hb", LOG, "### Sensitivity test for L2")],
         raw_file=("hb", "01_raw_data/accounts.csv")),
]

PROFILE_SOURCES = {  # raw-file row counts, recomputed from the CSVs
    "wh": [["cust_info.csv", "CRM", 18494], ["prd_info.csv", "CRM", 397], ["sales_details.csv", "CRM", 60398],
           ["CUST_AZ12.csv", "ERP", 18484], ["LOC_A101.csv", "ERP", 18484], ["PX_CAT_G1V2.csv", "ERP", 37]],
    "hc": [["patients.csv", "EHR", 100100], ["doctors.csv", "EHR", 5000]]
          + [[f"admissions_{y}.csv", "EHR", 100000] for y in range(2021, 2026)]
          + [[f"billing_{y}.csv", "Billing", 100000] for y in range(2021, 2026)]
          + [["hospitals.csv", "Master", 500], ["procedures.csv", "Master", 1000]],
}

out = []
for e in ENTRIES:
    e = dict(e)
    e["cites"] = [cite(*c) for c in e["cites"]]
    rf = e.pop("raw_file", None)
    if rf:
        e["cites"].insert(0, csv(*rf))
    e["fixes"] = [{"case": c, "text": t, "code": code} for c, t, code in e["fixes"]]
    out.append(e)

ids = [e["id"] for e in out]
assert len(ids) == len(set(ids)), "duplicate ids"
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({"_note": "Generated from verified evidence; see tools/README.md. Counts are rows in the raw source files.",
                           "entries": out, "sources": PROFILE_SOURCES}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out), "entries ->", OUT)
