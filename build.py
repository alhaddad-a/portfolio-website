#!/usr/bin/env python3
"""
Static site generator for Abdullah Alhaddad's portfolio.

    python build.py

Edit the CONTENT section below, run the script, and every page in /public is
rewritten as plain, fully-rendered HTML (no JavaScript needed to read it —
which is what lets Google index the content reliably). Also writes
sitemap.xml with today's date.

Only the Python standard library is used.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
PUBLIC = ROOT / "public"

# ---------------------------------------------------------------------------
# SITE SETTINGS — change SITE_URL if you move to a custom domain.
# ---------------------------------------------------------------------------
SITE_URL = "https://alhaddad-a.vercel.app"
# Paste the content value from Google Search Console's "HTML tag" method here
# (e.g. "AbC123..."). Leave empty if you verify via DNS or file upload.
GOOGLE_SITE_VERIFICATION = "2ttHLWMo1YR8NXcPjT3yxVdfPMFLkX1mqTFv_3ep96M"

NAME = "Abdullah Alhaddad"
FIRST, LAST = "Abdullah", "Alhaddad"
ROLE = "Data Engineer"
LOCATION = "Ankara, Türkiye"
EMAIL = "alhaddad.a.hani@gmail.com"
PHONE_DISPLAY = "+90 535 231 66 86"
PHONE_TEL = "+905352316686"
WHATSAPP = "https://wa.me/905352316686?text=" + "Hello%20Abdullah%2C%20I%20saw%20your%20portfolio%20and%20would%20like%20to%20get%20in%20touch."
LINKEDIN = "https://www.linkedin.com/in/abdullah-alhaddad-76a101344/"
GITHUB = "https://github.com/alhaddad-a"

HOME_TITLE = "Abdullah Alhaddad | Data Engineer"
HOME_DESC = (
    "Abdullah Alhaddad, Data Engineer in Ankara. SQL Server data warehouses, Databricks "
    "lakehouses, PySpark pipelines and Power BI analytics: four projects from raw files to tested models."
)

# ---------------------------------------------------------------------------
# CONTENT
# ---------------------------------------------------------------------------
ABOUT_LEAD = ("My work sits between messy source systems and the people who need answers "
              "from them.")
ABOUT = [
    "I'm a data engineer based in Ankara, Türkiye. I ingest raw files, clean and "
    "reconcile them, and model the result into tables an analyst can query without "
    "second-guessing the numbers.",
    "Most of what I build follows the <strong>Medallion Architecture</strong> — Bronze for "
    "data exactly as it arrived, Silver for cleaned and conformed records, Gold for "
    "business-ready star schemas and KPI tables. I've implemented that pattern end to end "
    "in <strong>Microsoft SQL Server</strong> with T-SQL stored procedures, and on "
    "<strong>Databricks</strong> with PySpark, Delta Lake and Unity Catalog — including a "
    "healthcare lakehouse covering five years of admissions and billing data. I also take "
    "data through to the decision: a Power BI analysis of a retail bank's 2025 results, "
    "ending in a memo to the CFO.",
    "I care about the unglamorous parts: data-quality checks that run as code, scripts "
    "that can be re-run safely, and documentation the next engineer can actually use. "
    "I'm open to data engineering roles and collaborations.",
]

FACTS = [
    ("Based in", LOCATION),
    ("Focus", "Data warehousing, ETL/ELT, lakehouse pipelines"),
    ("Core stack", "Python · SQL · PySpark · Databricks"),
    ("Modeling", "Dimensional / star schema, Medallion"),
    ("Status", "Open to opportunities"),
]

# The toolkit is drawn as a matrix: each tool is marked against the case files
# (1–4, in PROJECTS order) whose write-ups show it in use.
TOOLKIT = [
    ("Languages", [("Python", [2, 3]), ("SQL / T-SQL", [1]), ("Spark SQL", [2, 3])]),
    ("Processing", [("Apache Spark / PySpark", [2, 3]), ("Stored procedures", [1]), ("BULK INSERT", [1]),
                    ("Databricks notebooks & jobs", [2, 3]), ("Power Query (M)", [4])]),
    ("Storage & platforms", [("Microsoft SQL Server", [1]), ("SSMS", [1]), ("Databricks", [2, 3]),
                             ("Delta Lake", [2, 3]), ("Unity Catalog", [2, 3])]),
    ("Modeling", [("Medallion architecture", [1, 2, 3]), ("Dimensional modeling / star schema", [1, 2, 4]),
                  ("Surrogate keys", [2]), ("SCD Type 1", [1])]),
    ("Quality & validation", [("Validation rules", [1, 3]), ("Deduplication", [1, 3, 4]),
                              ("Referential-integrity checks", [1, 4]), ("Idempotent, re-runnable loads", [1, 2, 3]),
                              ("Reconciliation checks", [4])]),
    ("Analytics", [("Power BI", [4]), ("DAX", [4])]),
    ("Practice", [("Git & GitHub", [1, 2, 3, 4]), ("Data catalog", [1]), ("Naming conventions", [1]),
                  ("Lineage documentation", [1])]),
]

PRINCIPLES = [
    ("Keep raw data raw",
     "Bronze stores source data exactly as it arrived. When a cleaning rule turns out to be "
     "wrong, I can fix it and replay from Bronze instead of going back to the source."),
    ("Quality checks are tests",
     "Nulls, duplicates, business keys, domain values and financial totals are validated by "
     "scripts that live in the repo next to the pipeline — not by eyeballing a table."),
    ("Re-runnable by design",
     "Scripts check whether objects exist before creating them, and loads are full refreshes, "
     "so running a pipeline twice gives the same result as running it once."),
    ("Documented for the next person",
     "Each project ships with a data catalog, naming conventions and a source-to-target "
     "lineage table, so someone new can find where every column comes from."),
]

CERTIFICATES = [
    ("Python Project for Data Engineering", "Coursera", "2025",
     "https://www.coursera.org/account/accomplishments/verify/60ZS3IUWIADG"),
    ("Introduction to Data Engineering", "Coursera", "2025",
     "https://www.coursera.org/account/accomplishments/verify/ISM8KESVTK0T"),
    ("Introduction to Relational Databases", "Coursera", "2025",
     "https://www.coursera.org/account/accomplishments/verify/07IJTT5M0YTK"),
    ("Python for Data Science, AI & Development", "Coursera", "2025",
     "https://www.coursera.org/account/accomplishments/verify/DHVEAMC5054Q"),
    ("Generative AI: Prompt Engineering Basics", "Coursera", "2025",
     "https://www.coursera.org/account/accomplishments/verify/10Y6ITKVRB60"),
    ("Big Data with Apache Spark on Python", "Udemy", "2025",
     "https://www.udemy.com/certificate/UC-28a1517c-fdd3-4f7e-8059-a2295e7efa4d/"),
    ("Data Warehouse Fundamentals for Beginners", "Udemy", "2024",
     "https://www.udemy.com/certificate/UC-fec6d173-8a9e-466a-a877-3788f7db48db/"),
]

PROJECTS = [
    {
        "slug": "sql-data-warehouse",
        "title": "SQL Server Medallion Data Warehouse",
        "seo_title": "SQL Server Data Warehouse Project | Abdullah Alhaddad",
        "summary": (
            "An end-to-end data warehouse in Microsoft SQL Server that merges CRM and ERP "
            "exports into a star schema ready for analytics."
        ),
        "description": (
            "A SQL Server data warehouse using the Medallion Architecture: CRM and ERP data "
            "loaded with T-SQL stored procedures and modeled into a star schema."
        ),
        "stack": ["SQL Server", "T-SQL", "Stored procedures", "BULK INSERT", "Star schema"],
        "repo": "https://github.com/alhaddad-a/mssql-medallion-data-warehouse",
        "metrics": [("6", "source CSV files"), ("2", "source systems"), ("3", "Gold models")],
        "diagram": [
            {"tone": "src", "head": "Sources", "sub": "CSV · CRM + ERP",
             "items": ["cust_info", "prd_info", "sales_details", "LOC_A101", "CUST_AZ12", "PX_CAT_G1V2"],
             "count": "6", "unit": "CSV files"},
            {"tone": "bronze", "head": "Bronze", "sub": "schema bronze",
             "items": ["crm_cust_info", "crm_prd_info", "crm_sales_details", "erp_loc_a101", "erp_cust_az12", "erp_px_cat_g1v2"],
             "count": "6", "unit": "raw tables"},
            {"tone": "silver", "head": "Silver", "sub": "schema silver",
             "items": ["crm_cust_info", "crm_prd_info", "crm_sales_details", "erp_loc_a101", "erp_cust_az12", "erp_px_cat_g1v2"],
             "count": "6", "unit": "clean tables"},
            {"tone": "gold", "head": "Gold", "sub": "schema gold · views",
             "items": ["dim_customers", "dim_products", "fact_sales"],
             "count": "3", "unit": "star-schema views"},
        ],
        "facts": [("Platform", "Microsoft SQL Server 2019+"), ("Sources", "CRM + ERP CSV exports (~116K records)"), ("Output", "Star schema: 2 dimensions, 1 fact")],
        "sections": [
            ("problem", "The problem", """
<p>Sales questions — who buys what, where, and how often — need customers, products and
transactions in one place. Here they lived in two systems: a <strong>CRM</strong>
(customer info, product info, sales details) and an <strong>ERP</strong> (customer
demographics, locations, product categories). The two used different key formats, different
codes for the same values, and had the usual quality issues: duplicates, stray whitespace,
dates stored as integers and impossible birth dates.</p>
<p>The goal was a single warehouse where an analyst can join a clean fact table to clean
dimensions and trust the result.</p>"""),
            ("architecture", "Architecture", """
<p>One <code>DataWarehouse</code> database with three schemas, one per Medallion layer:</p>
<ul>
<li><strong>Bronze — raw ingestion.</strong> Each source CSV is loaded as-is into its own table
with <code>BULK INSERT</code>, wrapped in the stored procedure <code>bronze.load_bronze</code>.</li>
<li><strong>Silver — cleaning and standardization.</strong> <code>silver.load_silver</code>
deduplicates, trims, casts types, validates values and standardizes codes across both systems.</li>
<li><strong>Gold — analytical model.</strong> Views expose a star schema:
<code>gold.dim_customers</code>, <code>gold.dim_products</code> (SCD Type 1 catalog) and
<code>gold.fact_sales</code>, ready for any BI tool.</li>
</ul>"""),
            ("lineage", "Transformations & lineage", """
<p>Every source file is traceable to the Gold object it feeds:</p>
<div class="table-scroll"><table>
<thead><tr><th>Source file</th><th>Gold object</th><th>Key transformations</th></tr></thead>
<tbody>
<tr><td><code>cust_info.csv</code></td><td><code>dim_customers</code></td><td>Keep the latest record per customer by create date; trim names; map marital status (S/M → Single/Married) and gender (M/F → Male/Female).</td></tr>
<tr><td><code>LOC_A101.csv</code></td><td><code>dim_customers</code></td><td>Remove hyphens from keys; normalize country codes (DE → Germany, US → United States).</td></tr>
<tr><td><code>CUST_AZ12.csv</code></td><td><code>dim_customers</code></td><td>Strip the <code>NAS</code> prefix from IDs; invalidate future birth dates; standardize gender.</td></tr>
<tr><td><code>prd_info.csv</code></td><td><code>dim_products</code></td><td>Split the compound product key to extract the category ID; map product lines; derive end dates with <code>LEAD()</code>.</td></tr>
<tr><td><code>PX_CAT_G1V2.csv</code></td><td><code>dim_products</code></td><td>Loaded as it arrives; the quality check finds no unwanted spaces.</td></tr>
<tr><td><code>sales_details.csv</code></td><td><code>fact_sales</code></td><td>Cast integer dates to <code>DATE</code>; check and repair pricing so that Sales = Quantity × Price.</td></tr>
</tbody></table></div>"""),
            ("quality", "Data quality", """
<p>Quality checks live in the repository as SQL scripts, run after each load:</p>
<ul>
<li><code>tests/quality_checks_silver.sql</code> — formatting, trimming and date-normalization rules.</li>
<li><code>tests/quality_checks_gold.sql</code> — key uniqueness, foreign-key mappings between the fact and dimensions, and overall model integrity.</li>
</ul>
<p>Scripts are idempotent (they check <code>OBJECT_ID</code> before creating objects), and the
repo includes a <code>data_catalog.md</code> and <code>naming_conventions.md</code> so the model is
documented, not just built.</p>"""),
            ("run", "Running it", """
<p>After creating the database, schemas and tables, the whole pipeline is two calls:</p>
<pre><code>-- Load raw CSVs into Bronze
EXEC bronze.load_bronze;

-- Clean, standardize and load Silver
EXEC silver.load_silver;</code></pre>
<p>The Gold layer is made of views, so it is always current with Silver.</p>"""),
        ],
    },
    {
        "slug": "databricks-medallion-pipeline",
        "title": "Databricks Medallion Pipeline",
        "seo_title": "Databricks Medallion Pipeline (PySpark) | Abdullah Alhaddad",
        "summary": (
            "The CRM + ERP integration rebuilt as a lakehouse on Databricks — PySpark "
            "transforms, Delta Lake tables and Unity Catalog governance."
        ),
        "description": (
            "A Bronze → Silver → Gold pipeline on Databricks with PySpark, Delta Lake and "
            "Unity Catalog, modeling CRM and ERP data into a star schema."
        ),
        "stack": ["Databricks", "PySpark", "Delta Lake", "Unity Catalog", "Spark SQL"],
        "repo": "https://github.com/alhaddad-a/databricks-medallion-pipeline",
        "metrics": [("6", "Bronze Delta tables"), ("4", "orchestrated stages"), ("3", "Gold tables")],
        "diagram": [
            {"tone": "src", "head": "Volume", "sub": "source_systems",
             "items": ["source_crm/*.csv", "source_erp/*.csv"], "count": "6", "unit": "CSV files"},
            {"tone": "bronze", "head": "Bronze", "sub": "datalakehouse.bronze",
             "items": ["crm_cust_info", "crm_prd_info", "crm_sales_details", "erp_cust_az12", "erp_loc_a101", "erp_px_cat_g1v2"],
             "count": "6", "unit": "Delta tables"},
            {"tone": "silver", "head": "Silver", "sub": "datalakehouse.silver",
             "items": ["crm_customers", "crm_products", "crm_sales", "erp_customers", "erp_cust_location", "erp_product_category"],
             "count": "6", "unit": "conformed tables"},
            {"tone": "gold", "head": "Gold", "sub": "datalakehouse.gold",
             "items": ["dim_customers", "dim_products", "fact_sales"], "count": "3", "unit": "star schema"},
        ],
        "facts": [("Platform", "Databricks + Unity Catalog"), ("Storage", "Delta Lake (managed tables)"), ("Orchestration", "Notebooks via dbutils / Jobs")],
        "sections": [
            ("why", "Why rebuild it", """
<p>The <a href="/projects/sql-data-warehouse/">SQL Server warehouse</a> proved the data model.
This project moves the same CRM and ERP integration onto a <strong>lakehouse</strong>: files in
cloud storage, transformations in PySpark, tables in Delta Lake and access governed by Unity
Catalog — the setup most teams now run at scale.</p>"""),
            ("architecture", "Architecture", """
<p>Everything lives in a Unity Catalog called <code>datalakehouse</code>, with one schema per layer
and a volume for the raw files:</p>
<ul>
<li><code>init_lakehouse</code> creates the <code>bronze</code>, <code>silver</code> and
<code>gold</code> schemas and the <code>datalakehouse.bronze.source_systems</code> volume.</li>
<li><strong>Bronze</strong> reads each CSV with headers and schema inference and overwrites a managed Delta table.</li>
<li><strong>Silver</strong> is driven by <code>silver_orchestration</code>, which runs six child notebooks with <code>dbutils.notebook.run</code>.</li>
<li><strong>Gold</strong> is driven by <code>gold_orchestration</code>, which builds the dimensions first and the fact table last, in dependency order.</li>
</ul>"""),
            ("silver", "Silver transformations", """
<div class="table-scroll"><table>
<thead><tr><th>Silver table</th><th>From Bronze</th><th>Key transformations</th></tr></thead>
<tbody>
<tr><td><code>crm_customers</code></td><td><code>crm_cust_info</code></td><td>Trim strings; normalize marital status and gender; drop null IDs; rename columns.</td></tr>
<tr><td><code>crm_products</code></td><td><code>crm_prd_info</code></td><td>Parse the product key; default null cost; normalize product line; cast the start date.</td></tr>
<tr><td><code>crm_sales</code></td><td><code>crm_sales_details</code></td><td>Parse <code>yyyyMMdd</code> dates; derive price from sales ÷ quantity when invalid.</td></tr>
<tr><td><code>erp_customers</code></td><td><code>erp_cust_az12</code></td><td>Strip the <code>NAS</code> prefix; validate birth dates; normalize gender.</td></tr>
<tr><td><code>erp_customer_location</code></td><td><code>erp_loc_a101</code></td><td>Clean customer IDs; map country codes (DE, US, …).</td></tr>
<tr><td><code>erp_product_category</code></td><td><code>erp_px_cat_g1v2</code></td><td>Convert the maintenance flag to boolean.</td></tr>
</tbody></table></div>"""),
            ("gold", "Gold model", """
<ul>
<li><code>dim_customers</code> — CRM customers enriched with ERP demographics and location, with a
<code>ROW_NUMBER</code> surrogate key. Gender comes from the CRM, falling back to the ERP when missing.</li>
<li><code>dim_products</code> — CRM products joined to ERP categories, with a surrogate <code>product_key</code>.</li>
<li><code>fact_sales</code> — sales lines joined to both dimensions, carrying order, ship and due dates plus sales amount, quantity and price.</li>
</ul>
<p>A typical question it answers — revenue by country and product line:</p>
<pre><code>SELECT c.country,
       p.product_line,
       SUM(f.sales_amount) AS total_sales
FROM   datalakehouse.gold.fact_sales    f
JOIN   datalakehouse.gold.dim_customers c ON f.customer_key = c.customer_key
JOIN   datalakehouse.gold.dim_products  p ON f.product_key  = p.product_key
GROUP  BY c.country, p.product_line
ORDER  BY total_sales DESC;</code></pre>"""),
            ("ops", "Running as a job", """
<p>The four notebooks map directly onto a Databricks Job with four dependent tasks:
<strong>init</strong> (once) → <strong>ingest</strong> (Bronze) → <strong>transform</strong>
(Silver) → <strong>model</strong> (Gold). Each layer only starts when the previous one succeeds.</p>"""),
        ],
    },
    {
        "slug": "healthcare-lakehouse",
        "title": "Healthcare Lakehouse on Databricks",
        "seo_title": "Healthcare Lakehouse on Databricks | Abdullah Alhaddad",
        "summary": (
            "Five years of hospital admissions and billing files turned into validated, "
            "Power BI-ready revenue and activity KPIs."
        ),
        "description": (
            "Healthcare data pipeline on Databricks with PySpark and Delta Lake: 14 source "
            "files, 7 quality checks and Gold KPI tables for hospital revenue."
        ),
        "stack": ["Databricks", "PySpark", "Spark SQL", "Delta Lake", "Power BI"],
        "repo": "https://github.com/alhaddad-a/healthcare-lakehouse-databricks",
        "metrics": [("14", "source CSV files"), ("7", "quality-check types"), ("5", "Gold KPI tables")],
        "diagram": [
            {"tone": "src", "head": "Sources", "sub": "EHR · billing · master",
             "items": ["patients", "doctors", "admissions_2021–25", "billing_2021–25", "hospitals", "procedures"],
             "count": "14", "unit": "CSV files"},
            {"tone": "bronze", "head": "Bronze", "sub": "raw · full refresh",
             "items": ["patients", "doctors", "admissions", "billing", "hospitals", "procedures"],
             "count": "6", "unit": "Delta tables"},
            {"tone": "silver", "head": "Silver", "sub": "validated",
             "items": ["patients", "doctors", "admissions", "billing", "hospitals", "procedures"],
             "count": "7", "unit": "check types"},
            {"tone": "gold", "head": "Gold", "sub": "business KPIs",
             "items": ["revenue_by_hospital", "revenue_by_state", "revenue_by_specialty", "admissions_by_year", "procedure_perf."],
             "count": "5", "unit": "KPI tables"},
            {"tone": "use", "head": "Consume", "sub": "reporting",
             "items": ["Power BI"], "count": "BI", "unit": "dashboards"},
        ],
        "facts": [("Platform", "Databricks · catalog health"), ("Sources", "EHR, billing, master data (~1.1M records)"), ("Output", "5 KPI tables for Power BI")],
        "sections": [
            ("problem", "The problem", """
<p>Hospitals produce clinical and financial data in separate places — admissions in the EHR,
charges in billing, reference data for hospitals and procedures elsewhere — and usually as
yearly extracts. Answering a simple question like <em>“which specialty brings in the most
revenue?”</em> means stitching all of it together and trusting the joins.</p>
<p>This project builds a lakehouse that does that stitching once, validates it, and publishes
answers as tables a BI tool can read directly.</p>"""),
            ("sources", "Data sources", """
<ul>
<li><strong>Clinical (EHR):</strong> patients, doctors, and admissions split into yearly files for 2021–2025.</li>
<li><strong>Financial:</strong> billing, also yearly for 2021–2025.</li>
<li><strong>Master data:</strong> hospitals and procedures.</li>
</ul>
<p>A one-time <code>lakehouse_setup</code> notebook selects the <code>health</code> catalog,
creates the <code>bronze</code>, <code>silver</code> and <code>gold</code> schemas and the volume
the raw CSVs are uploaded to.</p>"""),
            ("quality", "Silver: validation", """
<p>Bronze keeps the files exactly as received (full-refresh Delta tables). Silver is where the
data earns trust. Across the Silver notebooks there are seven kinds of check:</p>
<ol>
<li>Null validation</li>
<li>Duplicate validation</li>
<li>Business-key validation</li>
<li>Whitespace validation</li>
<li>Domain validation (allowed values)</li>
<li>Financial validation (amounts that make sense)</li>
<li>Standardization of formats and codes</li>
</ol>
<p>Entities are integrated through business keys: admissions link to patients, doctors,
hospitals and procedures, and billing links back to admissions.</p>"""),
            ("gold", "Gold: business questions", """
<p>Each Gold table answers one question a hospital manager would actually ask:</p>
<div class="table-scroll"><table>
<thead><tr><th>Gold table</th><th>Question it answers</th></tr></thead>
<tbody>
<tr><td><code>revenue_by_hospital</code></td><td>Which hospitals generate the most revenue?</td></tr>
<tr><td><code>revenue_by_state</code></td><td>Which states generate the most revenue?</td></tr>
<tr><td><code>revenue_by_specialty</code></td><td>Which medical specialties generate the most revenue?</td></tr>
<tr><td><code>admissions_by_year</code></td><td>How are admissions changing over time?</td></tr>
<tr><td><code>procedure_performance</code></td><td>Which procedures are performed most often?</td></tr>
</tbody></table></div>"""),
            ("next", "What I'd add next", """
<ul>
<li>Incremental loading instead of full refreshes</li>
<li>Delta Live Tables and Databricks Workflows for scheduling</li>
<li>Automated data-quality monitoring and unit tests for transformations</li>
<li>A published Power BI dashboard on top of the Gold layer</li>
</ul>"""),
        ],
    },
    {
        "slug": "harborview-bank-analysis",
        "title": "Harborview Bank Power BI Analysis",
        "seo_title": "Harborview Bank Power BI Analysis | Abdullah Alhaddad",
        "summary": (
            "A Power BI analysis that settles a CFO-vs-Retail argument: fee income hit a "
            "record, but East-region credit losses turned the bank's 2025 result negative."
        ),
        "description": (
            "Power BI case study: 2.3M bank transactions cleaned in Power Query, modeled as a "
            "star schema and checked with DAX to explain a negative 2025 result."
        ),
        "stack": ["Power BI", "Power Query (M)", "DAX", "Star schema", "Reconciliation checks"],
        "langs": ["DAX", "Power Query M"],
        "repo": "https://github.com/alhaddad-a/harborview-bank-powerbi-analysis",
        "docs": [
            ("Full report (PDF)", "https://github.com/alhaddad-a/harborview-bank-powerbi-analysis/blob/HEAD/04_outputs/Dashboard.pdf"),
            ("CFO memo (PDF)", "https://github.com/alhaddad-a/harborview-bank-powerbi-analysis/blob/HEAD/04_outputs/CFO_Memo.pdf"),
        ],
        "metrics": [("2.3M", "transactions analysed"), ("19", "data issues fixed"), ("6", "report pages")],
        "diagram": [
            {"tone": "src", "head": "Raw data", "sub": "9 CSV files · 2023–2025",
             "items": ["transactions (2.3M)", "accounts", "customers", "loans", "products", "branches", "3 lookup tables"],
             "count": "9", "unit": "CSV files"},
            {"tone": "silver", "head": "Clean", "sub": "Power Query (M)",
             "items": ["19 issues fixed", "duplicates removed", "mixed dates parsed", "rates % → decimals", "placeholder scores", "orphan keys dropped"],
             "count": "19", "unit": "fixes"},
            {"tone": "gold", "head": "Model", "sub": "star schema · Import",
             "items": ["Transactions (fact)", "Loans (fact)", "Customers", "Accounts", "Products", "Branches", "Date (marked)"],
             "count": "7", "unit": "tables"},
            {"tone": "use", "head": "DAX", "sub": "measures + checks",
             "items": ["churn & reactivation", "12-mo default rate", "price-change effect", "reconciliation"],
             "count": "", "unit": ""},
            {"tone": "use", "head": "Report", "sub": "6 pages + CFO memo",
             "items": ["Overview", "Fee Income", "Credit Risk", "Customers", "Price Change", "Data Checks"],
             "count": "6", "unit": "pages"},
        ],
        "facts": [("Tool", "Power BI Desktop (Import mode)"), ("Data", "Simulated retail bank, 2023–2025"), ("Output", "6-page report + CFO memo")],
        "sections": [
            ("question", "The business question", """
<p>Leadership disagreed about 2025. The <strong>Head of Retail</strong> called it the best year
for fee income, thanks to the July 2024 rise in the monthly checking fee from $5 to $12. The
<strong>CFO</strong> said overall results got worse, with customers leaving and credit losses rising.</p>
<p>The analysis tests both claims and recommends whether to keep the fee, and what to do about
customers and credit risk in 2026. Before looking at any values, each claim was turned into
neutral questions (an issue tree), with 14 KPIs and written hypotheses.</p>"""),
            ("findings", "What the data showed", """
{SHOT:overview:Overview page: fee income, credit losses and measurable result by year, 2023–2025}
<ol>
<li><strong>Fee income rose 2.6×</strong>, from $0.45M (2023) to $1.16M (2025), because of the price,
not more customers: accounts paying the fee fell from 8,803 to 7,994.</li>
<li><strong>The price rise very likely cost customers.</strong> Mass checking closures went from 0.39%
to 3.05% a month in the first nine months at $12, while fee-free customers stayed flat. The jump
started the week of the change, hit only checking, and appeared in every region: about 2,640
extra closures by December 2025.</li>
<li><strong>The fee is still a net gain, but a shrinking one:</strong> about +$743K after an estimated
$0.29M of lost revenue, with the monthly gain falling from $59K to $32K.</li>
<li><strong>The measurable result fell from +$2.56M to −$0.41M</strong> because gross credit losses rose
ninefold, from $0.52M to $4.65M, not because of the fee.</li>
<li><strong>Three quarters of 2025 credit losses came from the East region.</strong> East branches
roughly tripled lending from early 2024, about half of it to borrowers scoring under 650; their
2024 loans defaulted 10.5% of the time within a year, against 2.1% elsewhere.</li>
</ol>
{SHOT:credit-risk:Credit Risk page: where the 2025 credit losses came from}
<p><strong>Verdict:</strong> both leaders were partly right. Fee income did reach a record, but credit
losses in East turned the result negative.</p>"""),
            ("cleaning", "Data cleaning in Power Query", """
<p>Every column was profiled on the full data set, and 19 problems across four tables were fixed
and logged, each with how it was found and how many rows it affected. For example:</p>
<ul>
<li>120 duplicate customers, 20 duplicate loans and 9,279 duplicate transactions.</li>
<li>Two date formats in one column: a plain type change would have silently swapped day and month on 549 rows.</li>
<li>Interest rates stored as percentages instead of decimals, and placeholder credit scores of 0 and 999.</li>
<li>Transactions dated after the extract date, and 150 transactions on accounts that don't exist.</li>
</ul>"""),
            ("model", "Data model", """
<p>A star schema in Import mode, with auto date/time and automatic relationship detection turned
off. Every relationship is defined by hand, one-to-many and single-direction.</p>
<div class="table-scroll"><table>
<thead><tr><th>Table</th><th>Rows</th><th>Role</th></tr></thead>
<tbody>
<tr><td>Transactions</td><td>2,319,645</td><td>Fact: payments, fees and transfers</td></tr>
<tr><td>Loans</td><td>5,300</td><td>Fact: amount, rate, balance, status</td></tr>
<tr><td>Accounts</td><td>36,605</td><td>Dimension between Customers and Transactions</td></tr>
<tr><td>Customers</td><td>20,000</td><td>Dimension: segment, region, income band</td></tr>
<tr><td>Branches</td><td>25</td><td>Dimension: branch, city, region</td></tr>
<tr><td>Products</td><td>6</td><td>Dimension: checking, savings, card, three loan types</td></tr>
<tr><td>Date</td><td>2,557</td><td>Marked date table, 2019–2025</td></tr>
</tbody></table></div>
<p>Two design decisions worth calling out:</p>
<ul>
<li><strong>Two dates on Loans, one active.</strong> The issue date drives volume and default rate by vintage;
the default date is an inactive relationship switched on with <code>USERELATIONSHIP</code> inside the loss measures.</li>
<li><strong>No Branches → Customers relationship.</strong> It would create two filter paths to Loans
(issuing branch vs. home branch), so customer geography uses Customers[Region] instead.</li>
</ul>"""),
            ("validation", "DAX measures & validation", """
<p>Measures are grouped into folders with descriptions, and include month-end customer snapshots,
churn and reactivation flows, a 12-month default rate by loan vintage, and a control-group
estimate of the closures caused by the price change.</p>
{SHOT:price-change:Price Change page: did the $12 fee pay off after lost customers?}
<p>Every KPI was reconciled against totals calculated outside Power BI, and against identities that
must hold every month: <em>fee income = paying accounts × average fee</em>, and <em>customers at end =
start + new + returning − leavers</em>. All checks return zero and are shown on a dedicated
Data Checks page in the report.</p>"""),
            ("recommendations", "Recommendations & limits", """
<ol>
<li><strong>Tighten credit approval in East now:</strong> bring the share of sub-650 loans back to the
12–16% seen elsewhere and review late East loans one by one.</li>
<li><strong>Keep the $12 fee, but protect the Mass base:</strong> record why customers leave and test a
fee waiver for active customers on a random group first.</li>
<li><strong>Investigate the July 2025 chargebacks</strong> ($373K, not confirmed as fraud) and fix the data gaps.</li>
</ol>
<p>The report never calls the result “profit”: the data has no operating costs, deposit interest or
loan-loss provisions, and losses are gross because there is no recovery data. Harborview is a
fictional bank on a simulated dataset; no real customer information is used.</p>"""),
        ],
    },
]


def shot(name: str, alt: str) -> str:
    """Responsive screenshot figure for a case study (files in assets/img/harborview-*)."""
    base = f"/assets/img/harborview-{name}"
    return (f'<figure class="shot"><img src="{base}-960.webp" '
            f'srcset="{base}-960.webp 960w, {base}-1600.webp 1600w" sizes="(max-width: 800px) 100vw, 760px" '
            f'width="1600" height="900" loading="lazy" decoding="async" alt="{escape(alt)}">'
            f'<figcaption class="label">{escape(alt)}</figcaption></figure>')


def expand_shots(html: str) -> str:
    return re.sub(r"\{SHOT:([\w-]+):([^}]+)\}", lambda m: shot(m.group(1), m.group(2)), html)



# ---------------------------------------------------------------------------
# CONTENT — the register. Generated from verified evidence (see tools/README.md);
# every count is from the author's documentation or recomputed from the raw CSVs.
# ---------------------------------------------------------------------------
REGISTER = json.loads((ROOT / "content" / "register.json").read_text(encoding="utf-8"))
ENTRIES: list[dict] = REGISTER["entries"]
BY_ID = {e["id"]: e for e in ENTRIES}

# Personal background, in the author's own words. Left empty on purpose until
# supplied — the site renders nothing rather than an invented biography.
PERSONAL = ""

SHORT = ["SQL Server warehouse", "Databricks pipeline", "Healthcare lakehouse", "Harborview Bank"]
SOURCE_OF = {"wh": [1, 2], "hc": [3], "hb": [4]}
KIND = {
    "whitespace": "Whitespace", "codes": "Inconsistent codes", "keys": "Keys & identifiers",
    "duplicates": "Duplicates", "missing": "Missing values", "impossible": "Impossible values",
    "format": "Format", "scale": "Scale & sign", "arithmetic": "Arithmetic", "placeholder": "Placeholders",
}
STATUS = {
    "resolved": ("Resolved", "Fixed in the pipeline, every time it runs."),
    "clean": ("Checked · clean", "A check that ran and found nothing."),
    "reopened": ("Reopened", "A fix that was later shown to be wrong."),
    "open": ("Open", "Unresolved, flagged, and measured."),
    "limitation": ("Known limitation", "Kept in the data and disclosed wherever it matters."),
}
LANG = {1: "T-SQL", 2: "PySpark", 3: "PySpark", 4: "Power Query"}
# Harborview: the log's per-table "Result" line is the verification after cleaning (verbatim).
_LOG = "https://github.com/alhaddad-a/harborview-bank-powerbi-analysis/blob/HEAD/02_documentation/02_Data_Quality_Log.md?plain=1"
HB_RESULT = {
    "customers.csv": ("20,000 rows. gender has 2 values, income_band 4, region 5 with none blank, email 20,000 unique, birth_date 104 null, signup_date 0 errors. Every home_branch_id matches a branch.", 41),
    "accounts.csv": ("36,605 rows. Open 25,971 and Closed 10,634; every open account has an empty close_date; 40 corrected dates flagged.", 57),
    "loans.csv": ("5,300 loans. Interest rate 0.038 to 0.145, credit score 520 to 850 with 39 unknown, no empty loan amounts (15 calculated and flagged).", 81),
    "transactions": ("2,319,645 rows. 17 merchant categories, 7 channels plus Unknown, all amounts positive, latest date 2025-12-31, no orphans.", 100),
}
TODAY = _dt.date.today().isoformat()


def eurl(e: dict) -> str:
    return f"/register/{e['id'].lower()}/"


def purl(n: int) -> str:
    return f"/projects/{PROJECTS[n - 1]['slug']}/"


def num(n) -> str:
    return "—" if n is None else f"{n:,}"


def asset_version(rel: str) -> str:
    return hashlib.sha1((PUBLIC / rel).read_bytes()).hexdigest()[:10]


CSS_V = asset_version("assets/css/style.css")
JS_V = asset_version("assets/js/main.js")
THEME_V = asset_version("assets/js/theme.js")


def head(title: str, desc: str, path: str, jsonld: list[dict], og_type: str = "website", noindex: bool = False) -> str:
    url = SITE_URL + path
    verify = (f'\n<meta name="google-site-verification" content="{escape(GOOGLE_SITE_VERIFICATION)}">'
              if GOOGLE_SITE_VERIFICATION and path == "/" else "")
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>' for o in jsonld)
    robots = "noindex" if noindex else "index, follow, max-image-preview:large"
    canon = "" if noindex else f'\n<link rel="canonical" href="{url}">'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<meta name="author" content="{NAME}">
<meta name="robots" content="{robots}">{canon}{verify}
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{NAME}, {ROLE}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(title)}">
<meta name="twitter:description" content="{escape(desc)}">
<meta name="twitter:image" content="{SITE_URL}/assets/img/og-image.jpg">
<meta name="theme-color" content="#f4f3ee">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/source-serif-4-vf-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/ibm-plex-mono-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css?v={CSS_V}">
<script src="/assets/js/theme.js?v={THEME_V}"></script>
{ld}
</head>"""


NAV = [("Home", "/", "home"), ("Projects", "/projects/", "projects"), ("About", "/about/", "about"),
       ("Investigations", "/investigations/", "investigations"), ("Certificates", "/certificates/", "certificates"),
       ("Contact", "/contact/", "contact")]


def chrome(current: str = "") -> str:
    items = []
    for label, href, key in NAV:
        cur = ' aria-current="page"' if key == current else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return f"""
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap head-row">
    <a class="brand" href="/"><span class="brand-mark" aria-hidden="true">AA</span><span class="brand-name">{NAME}</span></a>
    <nav aria-label="Main"><ul class="nav">{"".join(items)}</ul></nav>
  </div>
</header>"""


def footer() -> str:
    year = _dt.date.today().year
    return f"""
<footer class="site-foot">
  <div class="wrap foot-row">
    <p class="foot-id"><strong>{NAME}</strong><span>{ROLE} · {LOCATION}</span></p>
    <ul class="foot-links">
      <li><a href="mailto:{EMAIL}">Email</a></li>
      <li><a href="{LINKEDIN}" target="_blank" rel="me noopener">LinkedIn</a></li>
      <li><a href="{GITHUB}" target="_blank" rel="me noopener">GitHub</a></li>
      <li><a href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp</a></li>
    </ul>
  </div>
  <div class="wrap"><p class="foot-small">© {year} {NAME}</p></div>
</footer>
<script src="/assets/js/main.js?v={JS_V}" defer></script>
</body>
</html>
"""


# ---- raw values -----------------------------------------------------------
def raw_html(v: str, cut: list | None = None) -> str:
    """A raw value exactly as it arrived: spaces made visible, an empty value shown as empty."""
    if v == "":
        return '<code class="raw nil"><span class="nil-t">empty</span></code>'
    out = []
    n = len(v)
    for i, ch in enumerate(v):
        c = escape(ch)
        # a space is only a defect when it leads, trails, doubles up, or is the whole value
        if ch == " " and (i == 0 or i == n - 1 or v[i - 1] == " " or (i + 1 < n and v[i + 1] == " ")):
            c = '<span class="sp"> </span>'
        if cut and cut[0] <= i < cut[1]:
            c = f'<del>{c}</del>'
        out.append(c)
    return '<code class="raw">' + "".join(out).replace("</del><del>", "") + "</code>"


def status_html(s: str) -> str:
    return f'<span class="st st-{s}"><i aria-hidden="true"></i>{STATUS[s][0]}</span>'


def projects_of(e: dict) -> str:
    return " · ".join(SHORT[c - 1] for c in e["fixed_in"])


# Shown first on the Investigations page: one clear example from each kind of source.
FEATURED_INV = ["WH-01", "WH-15", "HC-04", "HB-04", "HB-12", "HC-05"]


def register_rows(entries: list[dict]) -> str:
    out = []
    for e in entries:
        cut = e["spec"].get("cut") if e["spec"]["type"] == "chars" else None
        raw = '<span class="zero-cell">0 rows returned</span>' if e["status"] == "clean" else raw_html(e["raw"], cut)
        out.append(f"""<li class="iv" data-src="{' '.join(str(c) for c in e['fixed_in'])}" data-status="{e['status']}">
  <a href="{eurl(e)}">
    <span class="iv-id">{e['id']}</span>
    <span class="iv-raw">{raw}</span>
    <span class="iv-title">{escape(e['title'])}</span>
    <span class="iv-proj">{escape(projects_of(e))}</span>
    <span class="iv-st">{status_html(e['status'])}</span>
  </a>
</li>""")
    return "".join(out)


# ---- specimens: each entry page is composed around its raw value -----------
def bar(n: int, mx: int) -> str:
    return f'<span class="vbar" aria-hidden="true"><b class="w{max(1, round(100 * n / mx))}"></b></span>'


def specimen(e: dict) -> str:
    s = e["spec"]
    t = s["type"]
    where = f'{escape(e["file"])} · {escape(e["column"])}'
    if t == "chars":
        v = e["raw"]
        cut = s.get("cut")
        long_ = len(v) > 14
        ruler = "".join(f"<span><i>{i if (not long_ or i == 1 or i % 5 == 0 or i == len(v)) else ''}</i></span>" for i in range(1, len(v) + 1))
        also = ""
        if s.get("also"):
            also = '<ul class="sp-also">' + "".join(
                f'<li>{raw_html(a)} <span class="arr" aria-hidden="true">→</span> <code class="clean">{escape(b)}</code></li>' for a, b in s["also"]) + "</ul>"
        note = f'<p class="sp-note">{escape(s["note"])}</p>' if s.get("note") else ""
        return f"""<div class="sp sp-chars">
  <p class="sp-cap">As it arrived <span>{where}</span></p>
  <div class="sp-big{' sp-long' if long_ else ''}">{raw_html(v, cut)}<span class="ruler" aria-hidden="true">{ruler}</span></div>
  <p class="sp-cap">As it leaves</p>
  <div class="sp-out"><code class="clean">{escape(e['expected'])}</code></div>
  {also}{note}
</div>"""
    if t == "variants":
        mx = max(n for _, n, _ in s["variants"])
        rows = "".join(
            f'<tr><td>{raw_html(v)}</td><td class="num">{n:,}</td><td>{bar(n, mx)}</td><td class="arr" aria-hidden="true">→</td><td><code class="clean">{escape(c)}</code></td></tr>'
            for v, n, c in s["variants"])
        canon = len({c.split(" ")[0] for _, _, c in s["variants"]})
        return f"""<div class="sp sp-variants">
  <p class="sp-cap">Every value in the column, as it arrived <span>{where}</span></p>
  <table class="vt"><caption class="visually-hidden">Distinct raw values, their row counts and the value each becomes</caption>
  <thead><tr><th scope="col">Raw value</th><th scope="col" class="num">Rows</th><th scope="col"><span class="visually-hidden">Share</span></th><th></th><th scope="col">Becomes</th></tr></thead>
  <tbody>{rows}</tbody></table>
  <p class="sp-note">{len(s['variants'])} distinct values in, {canon} out.</p>
</div>"""
    if t == "pair":
        rows = "".join(f'<li>{raw_html(a)}<span class="arr" aria-hidden="true">→</span><code class="clean">{escape(b)}</code></li>' for a, b in s["pairs"])
        note = f'<p class="sp-note">{escape(s["note"])}</p>' if s.get("note") else ""
        return f"""<div class="sp sp-pair">
  <p class="sp-cap">As it arrived <span>{where}</span> <span class="sp-cap-r">As it leaves</span></p>
  <ul class="pairs">{rows}</ul>{note}
</div>"""
    if t == "scale":
        return f"""<div class="sp sp-scale">
  <p class="sp-cap">As it arrived <span>{where}</span></p>
  <div class="scale"><span class="sc-a">{raw_html(s['from'])}</span><span class="sc-op">÷ 100</span><span class="sc-b"><code class="clean">{escape(s['to'])}</code></span></div>
  <p class="sp-note">{escape(s['note'])}</p>
</div>"""
    if t == "order":
        (la, va), (lb, vb) = s["a"], s["b"]
        return f"""<div class="sp sp-order">
  <p class="sp-cap">One row, as it arrived <span>{escape(s['key'])}</span></p>
  <div class="tl" role="img" aria-label="{escape(lb)} {escape(vb)} is earlier than {escape(la)} {escape(va)}">
    <span class="tl-axis"></span>
    <span class="tl-pt tl-b"><b>{escape(vb)}</b><span>{escape(lb)}</span></span>
    <span class="tl-pt tl-a"><b>{escape(va)}</b><span>{escape(la)}</span></span>
    <span class="tl-gap">ends before it begins</span>
  </div>
</div>"""
    if t == "dupes":
        th = "".join(f'<th scope="col">{escape(c)}</th>' for c in s["cols"])
        tr = "".join(
            f'<tr class="{"keep" if i == s["keep"] else "drop"}">' + "".join(f"<td>{raw_html(v)}</td>" for v in r)
            + f'<td class="dv">{"kept — newest" if i == s["keep"] else "dropped"}</td></tr>' for i, r in enumerate(s["rows"]))
        return f"""<div class="sp sp-dupes">
  <p class="sp-cap">Both rows, as they arrived <span>{escape(e['file'])}</span></p>
  <div class="t-scroll"><table class="dt"><thead><tr>{th}<th><span class="visually-hidden">Outcome</span></th></tr></thead><tbody>{tr}</tbody></table></div>
</div>"""
    if t == "count":
        diff = s["in"] - s["out"]
        return f"""<div class="sp sp-count">
  <p class="sp-cap">Rows in → rows out <span>{where}</span></p>
  <div class="ct"><span class="ct-n">{s['in']:,}</span><span class="arr" aria-hidden="true">→</span><span class="ct-n">{s['out']:,}</span></div>
  <p class="sp-note">{diff:,} exact copies removed from {escape(s['unit'])}. Nothing else is removed at this step.</p>
</div>"""
    if t == "quarantine":
        row = ""
        if s.get("row"):
            cells = "".join(f'<td>{raw_html(v)}</td>' for v in s["vals"])
            heads = "".join(f'<th scope="col">{c}</th>' for c in s["row"])
            row = f'<div class="t-scroll"><table class="dt"><thead><tr>{heads}</tr></thead><tbody><tr>{cells}</tr></tbody></table></div>'
        return f"""<div class="sp sp-quarantine">
  <p class="sp-cap">As it arrived <span>{where}</span></p>
  {row}
  <div class="qz">
    <div><span class="qz-n">{s['in']:,}</span><span class="qz-l">rows in</span></div>
    <div><span class="qz-n">{s['out']:,}</span><span class="qz-l">to the Silver table</span></div>
    <div class="qz-aside"><span class="qz-n">{s['aside']:,}</span><span class="qz-l">set aside in <code>{escape(s['table'])}</code></span></div>
  </div>
</div>"""
    if t == "arith":
        tr = "".join(f'<tr><td><code>{a}</code></td><td>{raw_html(b)}</td><td class="num"><code>{c}</code></td><td class="num"><code>{d}</code></td><td class="num"><code class="clean">{f}</code></td></tr>' for a, b, c, d, f in s["rows"])
        return f"""<div class="sp sp-arith">
  <p class="sp-cap">Three lines, as they arrived <span>{where}</span></p>
  <div class="t-scroll"><table class="dt"><thead><tr><th scope="col">order</th><th scope="col">sls_sales</th><th scope="col" class="num">qty</th><th scope="col" class="num">price</th><th scope="col" class="num">sales, recomputed</th></tr></thead><tbody>{tr}</tbody></table></div>
</div>"""
    if t == "split":
        parts = "".join(f'<span class="kp{" kp-sep" if not lab else ""}"><code>{escape(a)}</code>{f"<span>{escape(lab)}</span>" if lab else ""}</span>' for a, b, lab in s["parts"])
        return f"""<div class="sp sp-split">
  <p class="sp-cap">As it arrived <span>{where}</span></p>
  <div class="keyparts">{parts}</div>
  <p class="sp-cap">As it leaves</p>
  <div class="sp-out"><code class="clean">{escape(e['expected'])}</code></div>
</div>"""
    if t == "empty":
        return f"""<div class="sp sp-empty">
  <p class="sp-cap">As it arrived <span>{where}</span></p>
  <div class="field"><span class="field-l">{escape(s['label'])}</span>{raw_html('')}</div>
  <p class="sp-cap">As it leaves</p>
  <div class="sp-out"><code class="clean">{escape(e['expected'])}</code></div>
</div>"""
    if t == "clean":
        return f"""<div class="sp sp-clean">
  <p class="sp-cap">The check <span>{where}</span></p>
  <pre class="q"><code>{escape(s['query'])}</code></pre>
  <p class="zero-rows"><span>0</span> rows returned</p>
</div>"""
    if t == "limitation":
        cells = "".join(f'<div><span class="lim-n">{escape(n)}</span><span class="lim-l">{escape(m)} 2025</span></div>' for m, n in s["series"])
        return f"""<div class="sp sp-limit">
  <p class="sp-cap">New customers per month <span>{where}</span></p>
  <div class="lim">{cells}</div>
</div>"""
    if t == "sensitivity":
        tr = "".join(f'<tr><th scope="row">{escape(a)}</th><td class="num">{escape(b)}</td><td class="num">{escape(c)}</td><td class="num">{escape(d)}</td></tr>' for a, b, c, d in s["rows"])
        return f"""<div class="sp sp-sens">
  <p class="sp-cap">Sensitivity test — every key result recalculated without the 40 customers</p>
  <div class="t-scroll"><table class="dt st-table"><thead><tr><th scope="col">Result</th><th scope="col" class="num">All customers</th><th scope="col" class="num">Without the 40</th><th scope="col" class="num">Change</th></tr></thead><tbody>{tr}</tbody></table></div>
  <p class="sp-note">No conclusion changes. The dates stay flagged until the source is corrected.</p>
</div>"""
    raise ValueError(t)


def page_entry(i: int) -> str:
    e = ENTRIES[i]
    sec = []

    def q(title, body, cls=""):
        sec.append(f'<section class="qa{cls}"><h2>{title}</h2>{body}</section>')

    q("What was wrong", f'<p>{escape(e["wrong"])}</p>' + (f'<p class="muted">{escape(e["rows_note"])}</p>' if e.get("rows_note") else ""))
    q("Evidence", f'<figure class="e-spec">{specimen(e)}</figure>', " qa-ev")
    if e.get("detected"):
        q("How it was detected", f'<p>{escape(e["detected"])}</p>')
    else:
        q("How it was detected", '<p>Recomputed from the raw file, which is public in the project repository.</p>')
    q("Why it matters", f'<p>{escape(e["impact"])}</p>')
    if e["fixes"]:
        fx = []
        for f in e["fixes"]:
            code = (f'<details class="code"><summary>Show the {LANG[f["case"]]}</summary><pre><code>{escape(f["code"])}</code></pre></details>'
                    if f.get("code") else "")
            label = f'<p class="fix-h">{escape(PROJECTS[f["case"] - 1]["title"])}</p>' if len(e["fixes"]) > 1 else ""
            fx.append(f'<div class="fix">{label}<p>{escape(f["text"])}</p>{code}</div>')
        title = "What remains, and what I’d do" if e["status"] in ("open", "limitation") else "What was done"
        q(title, "".join(fx))
    if e.get("test"):
        t = e["test"]
        note = f'<p>{escape(t["note"])}</p>' if t.get("note") else "<p>A query that should return no rows after the fix.</p>"
        q("How it was verified", note + f'<details class="code"><summary>Show the check</summary><pre><code>{escape(t["sql"])}</code></pre></details>')
    elif e["source"] == "hb" and e["status"] == "resolved" and e["file"] in HB_RESULT:
        txt, line = HB_RESULT[e["file"]]
        q("How it was verified", f'<p>The quality log records the table’s state after its cleaning steps:</p><blockquote class="result"><p>{escape(txt)}</p><footer><a href="{_LOG}#L{line}" target="_blank" rel="noopener">02_Data_Quality_Log.md, line {line} ↗</a></footer></blockquote><p>Every KPI built on it was then reconciled against totals calculated outside Power BI.</p>')
    elif e["status"] == "reopened":
        q("Why it was reopened", f'<p>A later check against the transactions table showed the correction was wrong for most of these accounts. <a href="{eurl(BY_ID[e["see"]])}">See {e["see"]}</a>.</p>')
    extra = ""
    if e.get("memo"):
        extra += f'<blockquote class="memo"><p>{escape(e["memo"])}</p><footer>CFO memo, recommendation 3 · <a href="https://github.com/alhaddad-a/harborview-bank-powerbi-analysis/blob/HEAD/04_outputs/CFO_Memo.pdf" target="_blank" rel="noopener">CFO_Memo.pdf ↗</a></footer></blockquote>'
    if e.get("lesson"):
        extra += f'<p class="lesson"><span>Lesson recorded in the project</span>“{escape(e["lesson"])}”</p>'
    if e.get("see") and e["status"] != "reopened":
        extra += f'<p class="see">Related: <a href="{eurl(BY_ID[e["see"]])}">{e["see"]} · {escape(BY_ID[e["see"]]["title"])}</a></p>'
    if e["id"] == "HB-L2":
        extra += f'<p class="see">The original fix: <a href="{eurl(BY_ID["HB-18"])}">HB-18 · {escape(BY_ID["HB-18"]["title"])}</a></p>'
    cites = "".join(f'<li><a href="{c["url"]}" target="_blank" rel="noopener">{escape(c["label"])} ↗</a></li>' for c in e["cites"])
    projs = "".join(f'<li><a href="{purl(c)}">{escape(PROJECTS[c - 1]["title"])}</a></li>' for c in e["fixed_in"])
    rows = (num(e['rows']) + (' of ' + num(e['of'])) if e['of'] else num(e['rows'])) if e['rows'] is not None else "—"
    prev_e, next_e = ENTRIES[i - 1], ENTRIES[(i + 1) % len(ENTRIES)]
    desc = f'{e["id"]}: {e["title"]}. {e["wrong"]}'[:158]
    jsonld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Investigations", "item": SITE_URL + "/investigations/"},
        {"@type": "ListItem", "position": 2, "name": e["id"], "item": SITE_URL + eurl(e)}]}]
    return head(f'{e["id"]} · {e["title"]} — {NAME}', desc, eurl(e), jsonld, og_type="article") + chrome("investigations") + f"""
<main id="main" class="entry">
  <div class="wrap narrow">
    <nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="/investigations/">Investigations</a></li><li aria-current="page">{e['id']}</li></ol></nav>
    <header class="e-head">
      <p class="e-meta"><span class="e-id">{e['id']}</span>{status_html(e['status'])}</p>
      <h1>{escape(e['title'])}</h1>
      <p class="e-src">{escape(projects_of(e))}</p>
    </header>
    {"".join(sec)}{extra}
    <section class="qa refs">
      <h2>References</h2>
      <dl class="ref-list">
        <div><dt>File</dt><dd><code>{escape(e['file'])}</code></dd></div>
        <div><dt>Column</dt><dd><code>{escape(e['column'])}</code></dd></div>
        <div><dt>Layer</dt><dd>{escape(e['layer'])}</dd></div>
        <div><dt>Rows affected</dt><dd>{rows}</dd></div>
        <div><dt>Status</dt><dd>{STATUS[e['status']][1]}</dd></div>
        <div><dt>Project</dt><dd><ul>{projs}</ul></dd></div>
      </dl>
      <p class="cites-h">Sources in the repositories</p>
      <ul class="cites">{cites}</ul>
    </section>
    <nav class="pager" aria-label="More investigations">
      <a href="{eurl(prev_e)}"><span>← {prev_e['id']}</span>{escape(prev_e['title'])}</a>
      <a href="{eurl(next_e)}"><span>{next_e['id']} →</span>{escape(next_e['title'])}</a>
    </nav>
  </div>
</main>""" + footer()


# ---- shared: person ---------------------------------------------------------
PERSON_ID = SITE_URL + "/#person"
PERSON = {
    "@type": "Person", "@id": PERSON_ID, "name": NAME, "givenName": FIRST, "familyName": LAST,
    "jobTitle": ROLE, "url": SITE_URL + "/", "image": SITE_URL + "/assets/img/abdullah-alhaddad-800.jpg",
    "email": "mailto:" + EMAIL,
    "address": {"@type": "PostalAddress", "addressLocality": "Ankara", "addressCountry": "TR"},
    "sameAs": [LINKEDIN, GITHUB],
    "knowsAbout": ["Data Engineering", "ETL", "Data Warehousing", "Data Quality", "Python", "SQL", "SQL Server",
                   "Apache Spark", "PySpark", "Databricks", "Delta Lake", "Dimensional Modeling",
                   "Medallion Architecture", "Power BI", "DAX"],
    "hasCredential": [
        {"@type": "EducationalOccupationalCredential", "name": t, "credentialCategory": "certificate",
         "recognizedBy": {"@type": "Organization", "name": iss}, "url": link}
        for t, iss, _y, link in CERTIFICATES],
}

# ---- project cards: one short line each, 3 tags, a real preview -------------
CARDS = [
    ("SQL Server Data Warehouse",
     "A Medallion data warehouse in Microsoft SQL Server that merges CRM and ERP exports into a tested star schema.",
     ["SQL Server", "T-SQL", "Star schema"]),
    ("Databricks Medallion Pipeline",
     "The same CRM and ERP integration rebuilt as a lakehouse, with PySpark notebooks, Delta Lake tables and Unity Catalog.",
     ["Databricks", "PySpark", "Delta Lake"]),
    ("Healthcare Lakehouse",
     "Five years of hospital admission and billing files, validated and turned into revenue and activity KPI tables.",
     ["Databricks", "PySpark", "Data quality"]),
    ("Harborview Bank Analytics",
     "A Power BI analysis of a bank’s 2025 results: fee income hit a record, but credit losses in one region turned the year negative.",
     ["Power BI", "Power Query", "DAX"]),
]


def pv_img(base: str, alt: str, w: int, h: int, sizes: str) -> str:
    return (f'<img src="/assets/img/{base}-960.webp" srcset="/assets/img/{base}-960.webp 960w, /assets/img/{base}-1600.webp 1600w" '
            f'sizes="{sizes}" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{escape(alt)}">')


def star_preview() -> str:
    def t(name, cols, cls=""):
        return f'<div class="st-t{cls}"><b>{name}</b>' + "".join(f"<span>{c}</span>" for c in cols) + "</div>"
    return ('<div class="pv-star">' + t("dim_customers", ["customer_key", "country", "gender"])
            + t("fact_sales", ["customer_key", "product_key", "sales_amount"], " st-fact")
            + t("dim_products", ["product_key", "category", "product_line"]) + "</div>")


DAG = [("init_lakehouse", "Schemas and source volume"),
       ("bronze", "Six CSVs into Delta tables"),
       ("silver_orchestration", "Six PySpark cleaning notebooks"),
       ("gold_orchestration", "Dimensions first, then fact_sales")]


def dag_preview(with_desc: bool = True) -> str:
    li = "".join(f'<li><i>{n}</i><code>{t}</code>' + (f'<span>{escape(d)}</span>' if with_desc else "") + "</li>"
                 for n, (t, d) in enumerate(DAG, 1))
    return f'<ol class="pv-dag">{li}</ol>'


def preview(n: int, sizes: str = "(max-width: 760px) 100vw, 600px") -> str:
    if n == 1:
        return f'<div class="pv pv-1" role="img" aria-label="Star schema: fact_sales joined to dim_customers and dim_products">{star_preview()}</div>'
    if n == 2:
        return f'<div class="pv pv-2" role="img" aria-label="Four notebook stages: init_lakehouse, bronze, silver_orchestration, gold_orchestration">{dag_preview()}</div>'
    if n == 3:
        return '<div class="pv pv-3">' + pv_img("healthcare-data-flow", "Data flow diagram from the project repository: 14 CSV files through Bronze and Silver into five Gold KPI tables", 1600, 1067, sizes) + "</div>"
    return '<div class="pv pv-4">' + pv_img("harborview-overview", "Harborview Bank Power BI overview page", 1600, 900, sizes) + "</div>"


def tags_html(tags: list[str]) -> str:
    return '<ul class="tags">' + "".join(f"<li>{escape(t)}</li>" for t in tags) + "</ul>"


HERO_ILLUSTRATION = """<svg class="hero-ill" viewBox="0 0 420 280" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <circle cx="245" cy="128" r="88" fill="#efe2a2" opacity="0.6"/>
  <ellipse cx="76" cy="146" rx="34" ry="12" fill="#f6f3ea" stroke="#1d1c1a" stroke-width="1.6"/>
  <path d="M42 146v62c0 6.6 15.2 12 34 12s34-5.4 34-12v-62" fill="#f6f3ea" stroke="#1d1c1a" stroke-width="1.6"/>
  <path d="M42 167c0 6.6 15.2 12 34 12s34-5.4 34-12" stroke="#1d1c1a" stroke-width="1.4"/>
  <path d="M42 188c0 6.6 15.2 12 34 12s34-5.4 34-12" stroke="#1d1c1a" stroke-width="1.4"/>
  <path d="M76 134V94c0-10 8-18 18-18h54" stroke="#1d1c1a" stroke-width="1.5"/>
  <g stroke="#1d1c1a" stroke-width="1.6">
    <path d="M150 182l64-26 64 26-64 26-64-26z" fill="#e9e3d4"/>
    <path d="M150 182v18l64 26 64-26v-18" fill="#efeadd"/>
    <path d="M150 138l64-26 64 26-64 26-64-26z" fill="#f1ede2"/>
    <path d="M150 138v18l64 26 64-26v-18" fill="#e9e3d4"/>
    <path d="M150 94l64-26 64 26-64 26-64-26z" fill="#f6f3ea"/>
    <path d="M150 94v18l64 26 64-26v-18" fill="#f1ede2"/>
  </g>
  <path d="M244 214v18c0 10 8 18 18 18h26" stroke="#1d1c1a" stroke-width="1.5"/>
  <path d="M276 106l108-26c4-1 8 2 8 6v98c0 4-3 8-7 9l-108 26c-4 1-8-2-8-6V115c0-4 3-8 7-9z" fill="#f6f3ea" stroke="#1d1c1a" stroke-width="1.6"/>
  <rect x="286" y="176" width="10" height="22" fill="#ddd6c6" stroke="#1d1c1a" stroke-width="1.2"/>
  <rect x="304" y="160" width="10" height="34" fill="#ddd6c6" stroke="#1d1c1a" stroke-width="1.2"/>
  <rect x="322" y="148" width="10" height="42" fill="#e6d27a" stroke="#1d1c1a" stroke-width="1.2"/>
  <rect x="340" y="128" width="10" height="58" fill="#ddd6c6" stroke="#1d1c1a" stroke-width="1.2"/>
  <rect x="358" y="114" width="10" height="68" fill="#1d1c1a"/>
</svg>"""


# ---- home -------------------------------------------------------------------
def page_home() -> str:
    jsonld = [{"@context": "https://schema.org", "@graph": [
        PERSON,
        {"@type": "WebSite", "@id": SITE_URL + "/#website", "url": SITE_URL + "/", "name": NAME,
         "description": HOME_DESC, "inLanguage": "en", "publisher": {"@id": PERSON_ID}},
        {"@type": "ProfilePage", "@id": SITE_URL + "/#profile", "url": SITE_URL + "/", "name": HOME_TITLE,
         "isPartOf": {"@id": SITE_URL + "/#website"}, "mainEntity": {"@id": PERSON_ID}, "dateModified": TODAY}]}]
    tiles = []
    for i, (title, blurb, tags) in enumerate(CARDS, 1):
        tiles.append(f"""<li class="tile">
  <a href="{purl(i)}">
    {preview(i, "(max-width: 760px) 100vw, 560px")}
    <span class="tile-body">
      <span class="tile-n">{i:02d}</span>
      <span class="tile-h">{escape(title)}</span>
      <span class="tile-p">{escape(blurb)}</span>
      <span class="tile-tags">{"".join(f"<span>{escape(t)}</span>" for t in tags)}</span>
      <span class="tile-go">View project <span aria-hidden="true">→</span></span>
    </span>
  </a>
</li>""")
    return head(HOME_TITLE, HOME_DESC, "/", jsonld) + chrome("home") + f"""
<main id="main" class="home">
  <section class="hero" aria-labelledby="hero-h">
    <div class="wrap hero-grid">
      <div class="hero-text">
        <p class="hello">Hi, I’m <strong>{NAME}</strong> — a {ROLE.lower()} in {LOCATION.split(",")[0]}.</p>
        <h1 id="hero-h">I turn raw data into <mark>reliable</mark> data systems.</h1>
        <p class="lede">I take messy source files, clean and reconcile them, and model the result into tables an analyst can query without second-guessing the numbers.</p>
        <p class="cta"><a class="btn" href="/projects/">View projects <span aria-hidden="true">→</span></a><a class="text-link" href="/investigations/">Explore my data investigations</a></p>
      </div>
      <div class="hero-art">{HERO_ILLUSTRATION}</div>
    </div>
  </section>

  <section class="work" aria-labelledby="work-h">
    <div class="wrap">
      <header class="sec-head">
        <h2 id="work-h">Projects</h2>
        <p>Four end-to-end builds, from raw files to tested models and reports.</p>
      </header>
      <ol class="tiles">{"".join(tiles)}</ol>
    </div>
  </section>

  <section class="hello-band" aria-label="Contact">
    <div class="wrap band-row">
      <p>Open to data engineering roles and collaborations.</p>
      <p><a class="btn btn-line" href="/contact/">Get in touch</a></p>
    </div>
  </section>
</main>""" + footer()


# ---- projects index ---------------------------------------------------------
def page_projects() -> str:
    rows = []
    for i, (title, blurb, tags) in enumerate(CARDS, 1):
        p = PROJECTS[i - 1]
        rows.append(f"""<article class="pj" aria-labelledby="pj-{i}">
  <a class="pj-pv" href="{purl(i)}" tabindex="-1" aria-hidden="true">{preview(i)}</a>
  <div class="pj-text">
    <p class="eyebrow">Project {i:02d}</p>
    <h2 id="pj-{i}"><a href="{purl(i)}">{escape(title)}</a></h2>
    <p>{escape(blurb)}</p>
    {tags_html(tags)}
    <p class="pj-links"><a class="btn" href="{purl(i)}">Read the case study <span aria-hidden="true">→</span></a><a class="text-link" href="{p['repo']}" target="_blank" rel="noopener">GitHub ↗</a></p>
  </div>
</article>""")
    jsonld = [{"@context": "https://schema.org", "@type": "CollectionPage", "url": SITE_URL + "/projects/",
               "name": f"Projects — {NAME}", "mainEntity": {"@id": PERSON_ID}}]
    return head(f"Projects — {NAME}, {ROLE}",
                "Four data engineering and analytics projects: SQL Server Data Warehouse, Databricks Medallion Pipeline, Healthcare Lakehouse, and Harborview Bank Power BI Analysis.",
                "/projects/", jsonld) + chrome("projects") + f"""
<main id="main" class="projects-page">
  <div class="wrap">
    <header class="page-head">
      <h1>Projects</h1>
      <p>Four projects, each taking real-world-shaped data from raw files to something people can use.</p>
    </header>
    <div class="pj-list">{"".join(rows)}</div>
  </div>
</main>""" + footer()


# ---- investigations ---------------------------------------------------------
def filters() -> str:
    cases = '<option value="">All projects</option>' + "".join(
        f'<option value="{i}">{escape(CARDS[i - 1][0])}</option>' for i in range(1, 5))
    st = '<option value="">Any status</option>' + "".join(
        f'<option value="{k}">{v[0]}</option>' for k, v in STATUS.items())
    return f"""<div class="filters" role="search" aria-label="Filter investigations">
  <label><span>Project</span><select id="f-case">{cases}</select></label>
  <label><span>Status</span><select id="f-status">{st}</select></label>
  <p class="f-count" aria-live="polite">Showing <span data-count>{len(ENTRIES)}</span> of {len(ENTRIES)}</p>
  <button type="button" class="f-reset" hidden>Clear filters</button>
</div>"""


def page_investigations() -> str:
    featured = [BY_ID[x] for x in FEATURED_INV]
    ordered = featured + [e for e in ENTRIES if e["id"] not in FEATURED_INV]
    jsonld = [{"@context": "https://schema.org", "@type": "CollectionPage", "url": SITE_URL + "/investigations/",
               "name": f"Data Quality Investigations — {NAME}", "mainEntity": {"@id": PERSON_ID}}]
    return head(f"Investigations — {NAME}, {ROLE}",
                f"{len(ENTRIES)} real data quality problems found in my four projects, each with the evidence, the fix and how it was verified.",
                "/investigations/", jsonld) + chrome("investigations") + f"""
<main id="main" class="inv-page">
  <div class="wrap">
    <header class="page-head">
      <h1>Investigations</h1>
      <p>Real data problems I found in my projects. Open any one to see the evidence, the fix and how it was checked.</p>
    </header>
    <section id="register" aria-label="Investigations">
      {filters()}
      <ol class="iv-list" id="r-list" data-preview="6">{register_rows(ordered)}</ol>
      <p class="r-empty" hidden>Nothing matches these filters.</p>
      <p class="r-more-wrap" hidden><button type="button" class="btn btn-line" data-show-all>View all {len(ENTRIES)} investigations</button></p>
    </section>
  </div>
</main>""" + footer()


# ---- project pages ----------------------------------------------------------
def entries_for(case: int) -> list[dict]:
    return [e for e in ENTRIES if case in e["fixed_in"]]


def files_table(key: str) -> str:
    rows = REGISTER["sources"][key]
    total = sum(r[2] for r in rows)
    tr = "".join(f'<tr><td><code>{escape(f)}</code></td><td>{escape(s)}</td><td class="num">{n:,}</td></tr>' for f, s, n in rows)
    return f"""<div class="table-scroll"><table><caption class="visually-hidden">Source files and their row counts</caption>
<thead><tr><th scope="col">File</th><th scope="col">System</th><th scope="col" class="num">Rows</th></tr></thead>
<tbody>{tr}</tbody><tfoot><tr><th scope="row" colspan="2">{len(rows)} files</th><td class="num">{total:,}</td></tr></tfoot></table></div>"""


LINEAGE = [
    ("cust_info.csv", "crm_cust_info", "dim_customers"),
    ("LOC_A101.csv", "erp_loc_a101", "dim_customers"),
    ("CUST_AZ12.csv", "erp_cust_az12", "dim_customers"),
    ("sales_details.csv", "crm_sales_details", "fact_sales"),
    ("prd_info.csv", "crm_prd_info", "dim_products"),
    ("PX_CAT_G1V2.csv", "erp_px_cat_g1v2", "dim_products"),
]


def lineage_svg() -> str:
    cw = 7.8
    xs, xb, xv, xg = 168, 300, 584, 858
    ys = [86 + i * 46 for i in range(len(LINEAGE))]
    groups: dict[str, list[int]] = {}
    for (_s, _b, g), y in zip(LINEAGE, ys):
        groups.setdefault(g, []).append(y)
    gy = {g: sum(v) / len(v) for g, v in groups.items()}
    title = "Lineage: " + "; ".join(f"{s} to bronze and silver {b}, then gold {g}" for s, b, g in LINEAGE)
    o = ['<svg class="lineage" viewBox="0 0 1050 350" role="img" aria-labelledby="lg-t" xmlns="http://www.w3.org/2000/svg">',
         f'<title id="lg-t">{escape(title)}</title>']
    for x, anchor, h, sub in [(xs - 12, "end", "Source files", "6 CSV · CRM + ERP"), (xb - 4, "start", "Bronze", "loaded as-is"),
                              (xv - 4, "start", "Silver", "cleaned · standardized"), (xg - 4, "start", "Gold", "star schema · views")]:
        o.append(f'<text class="lg-head" x="{x}" y="26" text-anchor="{anchor}">{h}</text>')
        o.append(f'<text class="lg-sub" x="{x}" y="45" text-anchor="{anchor}">{sub}</text>')
    o.append(f'<path class="lg-star" d="M{xg} {gy["dim_customers"]:.0f}V{gy["dim_products"]:.0f}"/>')
    for (s, b, g), y in zip(LINEAGE, ys):
        yg = gy[g]
        bx = xb + 14 + len(b) * cw + 10
        vx = xv + 14 + len(b) * cw + 10
        mid = (vx + xg) / 2
        o.append(f'<path class="ln" d="M{xs + 6} {y}H{xb - 6}"/>')
        o.append(f'<path class="ln" d="M{bx:.0f} {y}H{xv - 6}"/>')
        o.append(f'<path class="ln" d="M{vx:.0f} {y}C{mid:.0f} {y} {mid:.0f} {yg:.0f} {xg - 6} {yg:.0f}"/>')
        o.append(f'<text class="lg-t" x="{xs - 12}" y="{y + 4.5}" text-anchor="end">{s}</text>')
        o.append(f'<rect class="nd" x="{xs - 4}.5" y="{y - 4}.5" width="8" height="8"/>')
        o.append(f'<rect class="nd" x="{xb - 4}.5" y="{y - 4}.5" width="8" height="8"/><text class="lg-t" x="{xb + 14}" y="{y + 4.5}">{b}</text>')
        o.append(f'<rect class="nd" x="{xv - 4}.5" y="{y - 4}.5" width="8" height="8"/><text class="lg-t" x="{xv + 14}" y="{y + 4.5}">{b}</text>')
    for g, y in gy.items():
        o.append(f'<rect class="nd-gold" x="{xg - 4}.5" y="{y - 4:.0f}.5" width="8" height="8"/>')
        o.append(f'<text class="lg-t lg-gold" x="{xg + 14}" y="{y + 4.5:.1f}">{g}</text>')
    o.append(f'<text class="lg-sub" x="{xg - 4}" y="340">1 fact · 2 dimensions</text>')
    o.append("</svg>")
    lst = {}
    for s, _b, g in LINEAGE:
        lst.setdefault(g, []).append(s)
    ul = '<ul class="lineage-list" aria-hidden="true">' + "".join(
        f'<li><b>{g}</b><span>from {", ".join(lst[g])}</span></li>' for g in lst) + "</ul>"
    return "".join(o) + ul


def steps_html(steps: list[tuple[str, str]]) -> str:
    return '<ol class="steps">' + "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in steps) + "</ol>"


def details_html(idx: int, keys: list[str]) -> str:
    secs = {k: (t, h) for k, t, h in PROJECTS[idx - 1]["sections"]}
    out = []
    for k in keys:
        if k == "files":
            out.append(f'<details class="more"><summary>Source files and row counts</summary><div class="prose">{files_table("wh")}</div></details>')
            continue
        t, h = secs[k]
        if k == "findings":
            h = re.sub(r"\{SHOT:overview:[^}]+\}", "", h)
        out.append(f'<details class="more"><summary>{escape(t)}</summary><div class="prose">{expand_shots(h)}</div></details>')
    n = len(entries_for(idx))
    inv = f'<p class="inv-link"><a href="/investigations/?case={idx}#register">See the {n} data problems logged for this project <span aria-hidden="true">→</span></a></p>'
    return f'<section class="pf-sec pf-more" aria-labelledby="more-{idx}"><h2 id="more-{idx}">Evidence and technical details</h2><div class="more-list">{"".join(out)}</div>{inv}</section>'


def sec(title: str, body: str, key: str, cls: str = "") -> str:
    return f'<section class="pf-sec{cls}" aria-labelledby="{key}"><h2 id="{key}">{title}</h2>{body}</section>'


def tech(tools: list[str], key: str) -> str:
    return sec("Technologies", tags_html(tools), key)


def profile_1() -> str:
    return (
        sec("Architecture", f'<figure class="fig">{lineage_svg()}<figcaption>Each source file lands in Bronze as it arrives, is cleaned in Silver, and feeds one of three Gold views.</figcaption></figure>', "a1")
        + sec("What I built", steps_html([
            ("Load", "<code>bronze.load_bronze</code> bulk-loads all six CRM and ERP CSV files exactly as they arrive."),
            ("Clean", "<code>silver.load_silver</code> removes duplicate customers, trims names, maps codes to readable values, fixes keys and casts integer dates."),
            ("Model", "Gold views expose a star schema: <code>dim_customers</code>, <code>dim_products</code> and <code>fact_sales</code>."),
            ("Test", "SQL scripts in <code>tests/</code> check formatting, key uniqueness, and that every sale maps to both dimensions."),
        ]), "b1")
        + sec("Results", f"""<div class="r-split">
  <div>
    <p class="inout"><span>18,494</span><span class="arr" aria-hidden="true">→</span><span>18,484</span></p>
    <p class="inout-l">CRM customer rows in, customers out</p>
    <p>Four rows had no customer ID and six were older copies of a customer. Without them, CRM customers line up one-to-one with both ERP customer files.</p>
  </div>
  <div>{preview(1)}<p class="cap">The Gold layer: one fact table, two dimensions.</p></div>
</div>""", "r1")
        + tech(["Microsoft SQL Server", "T-SQL", "Stored procedures", "BULK INSERT", "SSMS", "Dimensional modeling", "Git & GitHub"], "t1")
        + details_html(1, ["lineage", "quality", "run", "files"])
    )


def profile_2() -> str:
    return (
        sec("Architecture", f'<p class="lead-s">Everything lives in one Unity Catalog, <code>datalakehouse</code>, and runs as four dependent stages.</p>{dag_preview()}', "a2")
        + sec("What I built", steps_html([
            ("Set up the catalog", "Created <code>bronze</code>, <code>silver</code> and <code>gold</code> schemas and a volume for the raw files."),
            ("Clean in PySpark", "Six Silver notebooks trim every string column automatically, parse dates, and conform keys and codes."),
            ("Model in order", "Gold builds both dimensions with surrogate keys first, then loads <code>fact_sales</code>."),
        ]), "b2")
        + sec("Results", """<p class="layers"><span><b>6</b> Bronze tables</span><span class="arr" aria-hidden="true">→</span><span><b>6</b> Silver tables</span><span class="arr" aria-hidden="true">→</span><span><b>3</b> Gold tables</span></p>
<p>A star schema in Delta Lake that answers questions like revenue by country and product line:</p>
<pre><code>SELECT c.country, p.product_line, SUM(f.sales_amount) AS total_sales
FROM   datalakehouse.gold.fact_sales f
JOIN   datalakehouse.gold.dim_customers c ON f.customer_key = c.customer_key
JOIN   datalakehouse.gold.dim_products  p ON f.product_key  = p.product_key
GROUP  BY c.country, p.product_line
ORDER  BY total_sales DESC;</code></pre>""", "r2")
        + tech(["Databricks", "PySpark", "Spark SQL", "Delta Lake", "Unity Catalog", "Python", "Git & GitHub"], "t2")
        + details_html(2, ["architecture", "silver", "gold", "ops"])
    )


def profile_3() -> str:
    flow = [("patients", "100,100", "99,949", "100 exact duplicates removed; 51 patients without a city set aside in <code>patients_missing_city</code>."),
            ("admissions, 5 yearly files", "500,000", "499,895", "105 admissions without a date set aside in <code>admissions_missing_date</code>."),
            ("billing, 5 yearly files", "500,000", "500,000", "Amounts rounded to two decimals."),
            ("doctors, hospitals, procedures", "6,500", "6,500", "Same row count in Silver.")]
    li = "".join(f'<li><p class="fl-h"><code>{a}</code></p><p class="fl-n"><span>{b}</span><span class="arr" aria-hidden="true">→</span><span>{c}</span></p><p class="fl-d">{d}</p></li>' for a, b, c, d in flow)
    return (
        sec("Architecture", f'<figure class="fig fig-img">{preview(3, "(max-width: 1100px) 100vw, 1040px")}<figcaption>The data-flow diagram from the project repository. <a href="/assets/img/healthcare-data-flow-1600.webp">Open full size</a></figcaption></figure>', "a3")
        + sec("What I built", steps_html([
            ("Consolidate", "Combined five years of admission and billing extracts with the patient, doctor, hospital and procedure files."),
            ("Validate", "Silver notebooks check nulls, duplicates, business keys, whitespace, allowed values, money and formats. Incomplete records go to quarantine tables instead of being deleted."),
            ("Publish", "Five Gold tables answer one manager question each, such as revenue by hospital or admissions by year."),
        ]), "b3")
        + sec("Results", f'<p class="lead-s">Rows in each source, and rows in Silver after validation:</p><ol class="flow-list">{li}</ol>', "r3")
        + tech(["Databricks", "PySpark", "Spark SQL", "Delta Lake", "Unity Catalog", "Python", "Git & GitHub"], "t3")
        + details_html(3, ["sources", "quality", "gold", "next"])
    )


def profile_4() -> str:
    return (
        sec("What the data showed", f"""{shot("overview", "Overview page: fee income, credit losses and measurable result by year, 2023–2025")}
<ol class="findings">
  <li><strong>Fee income rose 2.6×</strong>, from $0.45M in 2023 to $1.16M in 2025, because of the higher fee, not more customers.</li>
  <li><strong>The measurable result fell from +$2.56M to −$0.41M</strong>, because gross credit losses rose ninefold.</li>
  <li><strong>Three quarters of 2025 credit losses came from the East region</strong>, where lending to borrowers scoring under 650 had grown.</li>
</ol>
<p class="verdict">Both leaders were partly right: fee income did reach a record, but credit losses in East turned the result negative.</p>""", "f4")
        + sec("How it’s built", """<ol class="chain">
  <li><b>9 source files</b><span>CSV, 2023–2025</span></li>
  <li><b>Power Query</b><span>19 data problems fixed and logged</span></li>
  <li><b>Star schema</b><span>2 fact tables, 5 dimensions</span></li>
  <li><b>DAX + report</b><span>6 pages and a memo to the CFO</span></li>
</ol>""", "a4")
        + sec("What I built", steps_html([
            ("Scope first", "Turned each leader’s claim into neutral questions, with 14 KPIs and written hypotheses, before looking at the values."),
            ("Clean", "Profiled every column on the full data and fixed duplicates, mixed date formats, rates stored as percentages and placeholder credit scores."),
            ("Model and measure", "Built the star schema by hand, then DAX measures for churn, default rate by loan vintage and the effect of the price change."),
            ("Reconcile", "Checked every KPI against totals calculated outside Power BI. The checks are on their own report page and all return zero."),
        ]), "b4")
        + tech(["Power BI", "Power Query (M)", "DAX", "Star schema", "Git & GitHub"], "t4")
        + details_html(4, ["question", "findings", "cleaning", "model", "validation", "recommendations"])
    )


PROFILES = [profile_1, profile_2, profile_3, profile_4]
INTROS = [
    "Customer, product and sales data lived in two systems, a CRM and an ERP, with different key formats, different codes for the same values, duplicates and dates stored as integers. This warehouse brings them into one SQL Server database an analyst can trust.",
    "The SQL Server warehouse proved the data model. Here the same CRM and ERP integration runs on Databricks: raw files in a Unity Catalog volume, transformations in PySpark and tables in Delta Lake.",
    "Hospitals keep admissions, billing and reference data in separate places, often as yearly extracts. This lakehouse stitches fourteen files together once, validates them, and publishes answers as tables a BI tool can read.",
    "Leadership at a fictional bank disagreed about 2025. The Head of Retail called it a record year for fee income after the monthly checking fee rose from $5 to $12; the CFO said results got worse. This analysis tests both claims.",
]


def page_profile(idx: int) -> str:
    p = PROJECTS[idx]
    n = idx + 1
    path = purl(n)
    url = SITE_URL + path
    jsonld = [{"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Projects", "item": SITE_URL + "/projects/"},
            {"@type": "ListItem", "position": 2, "name": p["title"], "item": url}]},
        {"@type": "SoftwareSourceCode", "@id": url + "#project", "name": p["title"], "description": p["description"],
         "url": url, "codeRepository": p["repo"],
         "programmingLanguage": p.get("langs") or (["Python", "SQL"] if idx else ["SQL"]),
         "keywords": ", ".join(p["stack"]),
         "author": {"@type": "Person", "@id": PERSON_ID, "name": NAME, "url": SITE_URL + "/"}, "dateModified": TODAY}]}]
    prev_n, next_n = (idx - 1) % 4 + 1, (idx + 1) % 4 + 1
    return head(p["seo_title"], p["description"], path, jsonld, og_type="article") + chrome("projects") + f"""
<main id="main" class="profile p{n}">
  <div class="wrap">
    <header class="pf-head">
      <nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="/projects/">Projects</a></li><li aria-current="page">Project {n:02d}</li></ol></nav>
      <h1>{escape(CARDS[idx][0])}</h1>
      <p class="pf-intro">{INTROS[idx]}</p>
      <p class="pf-links"><a class="btn btn-line" href="{p['repo']}" target="_blank" rel="noopener">Source code on GitHub ↗</a>{"".join(f' <a class="btn btn-line" href="{u}" target="_blank" rel="noopener">{escape(t)} ↗</a>' for t, u in p.get("docs", []))}</p>
    </header>
    {PROFILES[idx]()}
    <nav class="pager" aria-label="Other projects">
      <a href="{purl(prev_n)}"><span>← Project {prev_n:02d}</span>{escape(CARDS[prev_n - 1][0])}</a>
      <a href="{purl(next_n)}"><span>Project {next_n:02d} →</span>{escape(CARDS[next_n - 1][0])}</a>
    </nav>
  </div>
</main>""" + footer()


# ---- about ------------------------------------------------------------------
def page_about() -> str:
    principles = "".join(f'<li><h3>{escape(t)}</h3><p>{escape(d)}</p></li>' for t, d in PRINCIPLES)
    personal = f"<p>{PERSONAL}</p>" if PERSONAL else ""
    jsonld = [{"@context": "https://schema.org", "@type": "AboutPage", "url": SITE_URL + "/about/", "name": f"About — {NAME}",
               "mainEntity": {"@id": PERSON_ID}}]
    return head(f"About — {NAME}, {ROLE}",
                "Data engineer based in Ankara, Türkiye. How I design pipelines, model data, and test data quality.",
                "/about/", jsonld) + chrome("about") + f"""
<main id="main" class="about-page">
  <div class="wrap">
    <div class="ab-grid">
      <figure class="ab-fig"><picture>
        <source type="image/webp" srcset="/assets/img/abdullah-alhaddad-480.webp 480w, /assets/img/abdullah-alhaddad-800.webp 800w" sizes="(max-width: 700px) 160px, 280px">
        <img src="/assets/img/abdullah-alhaddad-480.jpg" srcset="/assets/img/abdullah-alhaddad-480.jpg 480w, /assets/img/abdullah-alhaddad-800.jpg 800w" sizes="(max-width: 700px) 160px, 280px" width="800" height="1000" decoding="async" alt="Portrait of {NAME}">
      </picture></figure>
      <div class="ab-text">
        <h1>About</h1>
        <p class="ab-lead">{ABOUT_LEAD}</p>
        {personal}
        <p>{ABOUT[0]}</p>
        <p>{ABOUT[1]}</p>
        <p>{ABOUT[2]}</p>
        <p class="ab-links"><a class="btn" href="/projects/">See my projects <span aria-hidden="true">→</span></a><a class="text-link" href="/contact/">Get in touch</a></p>
      </div>
    </div>
    <section class="approach" aria-labelledby="ap-h">
      <h2 id="ap-h">How I work</h2>
      <ol class="principles">{principles}</ol>
    </section>
  </div>
</main>""" + footer()


# ---- certificates -----------------------------------------------------------
def page_certificates() -> str:
    certs = "".join(
        f'<li><span class="c-t">{escape(t)}</span><span class="c-i">{escape(iss)} · {y}</span><a class="c-v" href="{link}" target="_blank" rel="noopener" aria-label="View certificate: {escape(t)} (opens {escape(iss)})">View ↗</a></li>'
        for t, iss, y, link in CERTIFICATES)
    jsonld = [{"@context": "https://schema.org", "@type": "CollectionPage", "url": SITE_URL + "/certificates/",
               "name": f"Certificates — {NAME}", "mainEntity": {"@id": PERSON_ID}}]
    return head(f"Certificates — {NAME}, {ROLE}",
                "Seven verified certificates in Python, SQL, Relational Databases, Data Warehousing, and Apache Spark.",
                "/certificates/", jsonld) + chrome("certificates") + f"""
<main id="main" class="certs-page">
  <div class="wrap narrow">
    <header class="page-head">
      <h1>Certificates</h1>
      <p>Courses I’ve completed. Each link opens the issuer’s verification page.</p>
    </header>
    <ol class="certs">{certs}</ol>
  </div>
</main>""" + footer()


# ---- contact ----------------------------------------------------------------
def page_contact() -> str:
    jsonld = [{"@context": "https://schema.org", "@type": "ContactPage", "url": SITE_URL + "/contact/",
               "name": f"Contact — {NAME}", "mainEntity": {"@id": PERSON_ID}}]
    return head(f"Contact — {NAME}, {ROLE}",
                f"Get in touch with {NAME}, {ROLE} in {LOCATION}.",
                "/contact/", jsonld) + chrome("contact") + f"""
<main id="main" class="contact-page">
  <div class="wrap narrow">
    <header class="page-head">
      <h1>Contact</h1>
      <p>I’m open to data engineering roles and collaborations. Email is the fastest way to reach me.</p>
    </header>
    <a class="mail" href="mailto:{EMAIL}">{EMAIL}</a>
    <ul class="channels">
      <li><span>LinkedIn</span><a href="{LINKEDIN}" target="_blank" rel="me noopener">abdullah-alhaddad ↗</a></li>
      <li><span>GitHub</span><a href="{GITHUB}" target="_blank" rel="me noopener">alhaddad-a ↗</a></li>
      <li><span>WhatsApp</span><a href="{WHATSAPP}" target="_blank" rel="noopener">Send a message ↗</a></li>
      <li><span>Phone</span><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
      <li><span>Based in</span><span class="ch-v">{LOCATION}</span></li>
    </ul>
  </div>
</main>""" + footer()


def page_404() -> str:
    links = "".join(f'<li><a href="{purl(i)}">{escape(c[0])}</a></li>' for i, c in enumerate(CARDS, 1))
    return head(f"Page not found — {NAME}", "This page doesn't exist.", "/404", [], noindex=True) + chrome() + f"""
<main id="main" class="notfound">
  <div class="wrap narrow">
    <header class="page-head">
      <p class="eyebrow">Error 404</p>
      <h1>Page not found</h1>
      <p>This page doesn’t exist or has moved. Try the <a href="/">home page</a>, or one of my projects:</p>
    </header>
    <ul class="nf-list">{links}</ul>
  </div>
</main>""" + footer()


def sitemap() -> str:
    urls = ["/", "/projects/", "/investigations/", "/about/", "/certificates/", "/contact/"] + [purl(i) for i in range(1, 5)] + [eurl(e) for e in ENTRIES]
    rows = "\n".join(
        f"  <url><loc>{SITE_URL}{u}</loc><lastmod>{TODAY}</lastmod><priority>{'1.0' if u == '/' else ('0.9' if u == '/projects/' else ('0.8' if u.startswith('/projects') else '0.6'))}</priority></url>"
        for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}\n</urlset>\n'


def robots() -> str:
    return f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"


def security_txt() -> str:
    expires = (_dt.datetime.now(_dt.timezone.utc) + _dt.timedelta(days=365)).strftime("%Y-%m-%dT00:00:00Z")
    return (f"Contact: mailto:{EMAIL}\nExpires: {expires}\nPreferred-Languages: en\n"
            f"Canonical: {SITE_URL}/.well-known/security.txt\n")


def write(rel: str, text: str) -> None:
    path = PUBLIC / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    print("Building site...")
    write("index.html", page_home())
    write("projects/index.html", page_projects())
    write("investigations/index.html", page_investigations())
    for i in range(len(PROJECTS)):
        write(f"projects/{PROJECTS[i]['slug']}/index.html", page_profile(i))
    for i, e in enumerate(ENTRIES):
        write(eurl(e).strip("/") + "/index.html", page_entry(i))
    write("about/index.html", page_about())
    write("certificates/index.html", page_certificates())
    write("contact/index.html", page_contact())
    write("404.html", page_404())
    write("sitemap.xml", sitemap())
    write("robots.txt", robots())
    write(".well-known/security.txt", security_txt())
    print(f"  home, projects, investigations ({len(ENTRIES)} entries), 4 case studies, about, certificates, contact, 404")
    print("Done.")


if __name__ == "__main__":
    main()
