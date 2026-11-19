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

HOME_TITLE = "Abdullah Alhaddad | Data Engineer — Python, SQL, Spark, Databricks"
HOME_DESC = (
    "Abdullah Alhaddad, data engineer in Ankara, Türkiye. ETL pipelines, SQL Server "
    "data warehouses and Databricks lakehouses with Python, PySpark and Delta Lake."
)

# ---------------------------------------------------------------------------
# CONTENT
# ---------------------------------------------------------------------------
ABOUT = [
    "I'm a data engineer based in Ankara, Türkiye. My work sits between messy source "
    "systems and the people who need answers from them: I ingest raw files, clean and "
    "reconcile them, and model the result into tables an analyst can query without "
    "second-guessing the numbers.",
    "Most of what I build follows the <strong>Medallion Architecture</strong> — Bronze for "
    "data exactly as it arrived, Silver for cleaned and conformed records, Gold for "
    "business-ready star schemas and KPI tables. I've implemented that pattern end to end "
    "in <strong>Microsoft SQL Server</strong> with T-SQL stored procedures, and on "
    "<strong>Databricks</strong> with PySpark, Delta Lake and Unity Catalog — including a "
    "healthcare lakehouse covering five years of admissions and billing data.",
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

TOOLKIT = [
    ("Languages", ["Python", "SQL (T-SQL)", "Spark SQL"]),
    ("Processing", ["Apache Spark / PySpark", "Stored procedures", "BULK INSERT", "Databricks notebooks & jobs"]),
    ("Platforms", ["Databricks", "Delta Lake", "Unity Catalog", "Microsoft SQL Server", "SSMS"]),
    ("Modeling", ["Medallion architecture", "Dimensional modeling", "Star schema", "Surrogate keys", "SCD Type 1"]),
    ("Quality", ["Validation rules", "Deduplication", "Referential-integrity checks", "Idempotent loads"]),
    ("Practice", ["Git & GitHub", "Data catalogs", "Naming conventions", "Lineage documentation"]),
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
<tr><td><code>PX_CAT_G1V2.csv</code></td><td><code>dim_products</code></td><td>Trim whitespace; map categories and maintenance flags.</td></tr>
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
<tr><td><code>crm_products</code></td><td><code>crm_prd_info</code></td><td>Parse the product key; default null cost; normalize product line; cast dates.</td></tr>
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
data earns trust — every table passes through seven kinds of checks:</p>
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
]

NAV = [("About", "/#about"), ("Work", "/#work"), ("Toolkit", "/#toolkit"),
       ("Certificates", "/#certificates"), ("Contact", "/#contact")]

# ---------------------------------------------------------------------------
# RENDERING
# ---------------------------------------------------------------------------
TODAY = _dt.date.today().isoformat()


def asset_version(rel: str) -> str:
    data = (PUBLIC / rel).read_bytes()
    return hashlib.sha1(data).hexdigest()[:10]


CSS_V = asset_version("assets/css/style.css")
JS_V = asset_version("assets/js/main.js")
THEME_V = asset_version("assets/js/theme.js")

ICON_MOON = '<svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z"/></svg>'
ICON_SUN = '<svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
ICON_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'


def head(title: str, desc: str, path: str, jsonld: list[dict], og_type: str = "website") -> str:
    url = SITE_URL + path
    verify = (f'\n<meta name="google-site-verification" content="{escape(GOOGLE_SITE_VERIFICATION)}">'
              if GOOGLE_SITE_VERIFICATION else "")
    ld = "\n".join(
        f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>' for obj in jsonld
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<meta name="author" content="{NAME}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">{verify}
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
<meta name="theme-color" content="#f4f2ec" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#121210" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/instrument-serif-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/ibm-plex-sans-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css?v={CSS_V}">
<script src="/assets/js/theme.js?v={THEME_V}"></script>
{ld}
</head>"""


def header(current: str = "") -> str:
    cur = ' aria-current="page"'
    items = "".join(
        f'<li><a href="{href}"{cur if label == current else ""}>{label}</a></li>'
        for label, href in NAV
    )
    return f"""
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="{NAME} — home">
      <span class="brand-mark" aria-hidden="true">AA</span>
      <span class="brand-name">{NAME} <span>/ {ROLE}</span></span>
    </a>
    <nav class="nav" aria-label="Main">
      <ul>{items}</ul>
      <button class="icon-btn theme-toggle" type="button" aria-label="Switch light/dark theme">{ICON_MOON}{ICON_SUN}</button>
      <button class="icon-btn menu-toggle" type="button" aria-label="Menu" aria-expanded="false">{ICON_MENU}</button>
    </nav>
  </div>
</header>"""


def footer() -> str:
    year = _dt.date.today().year
    return f"""
<footer class="site-footer">
  <div class="wrap">
    <p class="m0">© {year} {NAME} · {ROLE} · {LOCATION}</p>
    <ul>
      <li><a href="{GITHUB}" rel="me noopener" target="_blank">GitHub</a></li>
      <li><a href="{LINKEDIN}" rel="me noopener" target="_blank">LinkedIn</a></li>
      <li><a href="mailto:{EMAIL}">Email</a></li>
    </ul>
  </div>
</footer>
<script src="/assets/js/main.js?v={JS_V}" defer></script>
</body>
</html>
"""


def layer_row(c: dict) -> str:
    """One row of the homepage card's pipeline list: layer name + the tables in it."""
    items = c["items"]
    shown = ", ".join(items[:3]) + (f" +{len(items) - 3}" if len(items) > 3 else "")
    return (f'<li class="ly ly-{c["tone"]}"><span class="ly-name">{escape(c["head"])}</span>'
            f'<span class="ly-items">{escape(shown)}</span></li>')


def diagram_svg(uid: str, cols: list[dict], label: str = "") -> str:
    """Draws a Bronze/Silver/Gold flow as inline SVG that follows the page theme."""
    colw, gap = 200, 40
    rows = max(len(c["items"]) for c in cols)
    H = 64 + rows * 36 + 10
    n = len(cols)
    W = n * colw + (n - 1) * gap
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="{uid}-t" xmlns="http://www.w3.org/2000/svg">',
           f'<title id="{uid}-t">{escape(label)}</title>']
    for i, c in enumerate(cols):
        x = i * (colw + gap)
        tone = c["tone"]
        out.append(f'<rect class="dg-col-bg" x="{x}.5" y="0.5" width="{colw - 1}" height="{H - 1}"/>')
        out.append(f'<rect class="dg-{tone}" x="{x}" y="0" width="{colw}" height="3"/>')
        out.append(f'<text class="dg-head dg-{tone}" x="{x + 12}" y="24">{escape(c["head"])}</text>')
        out.append(f'<text class="dg-sub" x="{x + 12}" y="42">{escape(c["sub"])}</text>')
        for j, item in enumerate(c["items"]):
            y = 60 + j * 36
            out.append(f'<g class="dg-item"><rect x="{x + 10}.5" y="{y}.5" width="{colw - 21}" height="27"/>'
                       f'<text x="{x + 20}" y="{y + 19}">{escape(item)}</text></g>')
        if i < n - 1:
            ay = H / 2
            x1, x2 = x + colw + 6, x + colw + gap - 6
            out.append(f'<path class="dg-arrow" d="M{x1} {ay}H{x2 - 6}"/>')
            out.append(f'<path class="dg-arrowhead" d="M{x2} {ay}l-7 -4v8z"/>')
    out.append("</svg>")
    return "".join(out)


PERSON_ID = SITE_URL + "/#person"
PERSON = {
    "@type": "Person",
    "@id": PERSON_ID,
    "name": NAME,
    "givenName": FIRST,
    "familyName": LAST,
    "jobTitle": ROLE,
    "url": SITE_URL + "/",
    "image": SITE_URL + "/assets/img/abdullah-alhaddad-800.jpg",
    "email": "mailto:" + EMAIL,
    "address": {"@type": "PostalAddress", "addressLocality": "Ankara", "addressCountry": "TR"},
    "sameAs": [LINKEDIN, GITHUB],
    "knowsAbout": ["Data Engineering", "ETL", "Data Warehousing", "Python", "SQL", "SQL Server",
                   "Apache Spark", "PySpark", "Databricks", "Delta Lake", "Dimensional Modeling",
                   "Medallion Architecture"],
    "hasCredential": [
        {"@type": "EducationalOccupationalCredential", "name": t, "credentialCategory": "certificate",
         "recognizedBy": {"@type": "Organization", "name": iss}, "url": link}
        for t, iss, _y, link in CERTIFICATES
    ],
}


def page_home() -> str:
    jsonld = [{
        "@context": "https://schema.org",
        "@graph": [
            PERSON,
            {"@type": "WebSite", "@id": SITE_URL + "/#website", "url": SITE_URL + "/", "name": NAME,
             "description": HOME_DESC, "inLanguage": "en", "publisher": {"@id": PERSON_ID}},
            {"@type": "ProfilePage", "@id": SITE_URL + "/#profile", "url": SITE_URL + "/", "name": HOME_TITLE,
             "isPartOf": {"@id": SITE_URL + "/#website"}, "mainEntity": {"@id": PERSON_ID},
             "dateModified": TODAY},
        ],
    }]

    about = "".join(f"<p>{p}</p>" for p in ABOUT)
    facts = "".join(f'<div><dt class="label">{escape(k)}</dt><dd>{escape(v)}</dd></div>' for k, v in FACTS)

    cases = []
    for i, p in enumerate(PROJECTS, 1):
        url = f"/projects/{p['slug']}/"
        metrics = "".join(f"<div><dt>{escape(l)}</dt><dd>{escape(v)}</dd></div>" for v, l in p["metrics"])
        layers = "".join(layer_row(c) for c in p["diagram"])
        cases.append(f"""
<article class="case">
  <div class="idx">{i:02d} / {len(PROJECTS):02d}</div>
  <div>
    <h3><a href="{url}">{escape(p['title'])}</a></h3>
    <p>{escape(p['summary'])}</p>
    <p class="stack">{' · '.join(escape(s) for s in p['stack'])}</p>
    <dl class="metrics">{metrics}</dl>
    <div class="links">
      <a href="{url}">Read the case study →</a>
      <a href="{p['repo']}" target="_blank" rel="noopener">Source on GitHub ↗</a>
    </div>
  </div>
  <ol class="layers" aria-label="Pipeline layers for {escape(p['title'])}">{layers}</ol>
</article>""")

    toolkit = "".join(
        f'<div><dt class="label">{escape(k)}</dt><dd>{"".join(f"<span>{escape(x)}</span>" for x in v)}</dd></div>'
        for k, v in TOOLKIT)
    principles = "".join(
        f'<li><span class="label">{i:02d}</span><h3>{escape(t)}</h3><p>{escape(d)}</p></li>'
        for i, (t, d) in enumerate(PRINCIPLES, 1))
    certs = "".join(
        f'<tr><td>{escape(t)}</td><td class="iss">{escape(iss)}</td><td class="yr">{y}</td>'
        f'<td><a href="{link}" target="_blank" rel="noopener">Verify ↗<span class="visually-hidden"> {escape(t)} certificate</span></a></td></tr>'
        for t, iss, y, link in CERTIFICATES)

    return head(HOME_TITLE, HOME_DESC, "/", jsonld) + header() + f"""
<main id="main">
<section class="hero" aria-labelledby="hero-title">
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <p class="status label"><span class="dot" aria-hidden="true"></span>Open to data engineering roles</p>
        <h1 id="hero-title">{FIRST}<br>{LAST}<span class="role">{ROLE} — pipelines, warehouses &amp; lakehouses</span></h1>
        <p class="lead">I turn raw, inconsistent source data into clean, modeled tables that analysts can trust — with Python, SQL Server, Apache Spark and Databricks.</p>
        <div class="actions">
          <a class="btn btn-solid" href="#work">See selected work <span class="arr">↓</span></a>
          <a class="btn btn-line" href="#contact">Get in touch</a>
        </div>
      </div>
      <figure class="portrait">
        <picture>
          <source type="image/webp" srcset="/assets/img/abdullah-alhaddad-480.webp 480w, /assets/img/abdullah-alhaddad-800.webp 800w" sizes="(max-width: 860px) 340px, 30vw">
          <img src="/assets/img/abdullah-alhaddad-800.jpg" srcset="/assets/img/abdullah-alhaddad-480.jpg 480w, /assets/img/abdullah-alhaddad-800.jpg 800w" sizes="(max-width: 860px) 340px, 30vw" width="800" height="1000" alt="Portrait of {NAME}, data engineer" fetchpriority="high">
        </picture>
        <figcaption class="label"><span>Fig. 01</span><span>{LOCATION}</span></figcaption>
      </figure>
    </div>
    <dl class="hero-meta">
      <div><dt class="label">Based in</dt><dd>{LOCATION}</dd></div>
      <div><dt class="label">Works with</dt><dd>Python · SQL · PySpark · Databricks</dd></div>
      <div><dt class="label">Builds</dt><dd>ETL pipelines · data warehouses · lakehouses</dd></div>
    </dl>
  </div>
</section>

<section class="flow" aria-label="How I structure a data pipeline">
  <div class="wrap">
    <ol>
      <li><span class="tag t-src">Source</span><h3>Raw systems</h3><p>CRM, ERP, EHR and billing exports — CSVs with all their quirks.</p></li>
      <li><span class="tag t-bronze">Bronze</span><h3>Land it</h3><p>Ingest as-is into raw tables, so every load can be replayed.</p></li>
      <li><span class="tag t-silver">Silver</span><h3>Clean it</h3><p>Deduplicate, cast, validate and standardize codes across systems.</p></li>
      <li><span class="tag t-gold">Gold</span><h3>Model it</h3><p>Star schemas and KPI tables shaped around business questions.</p></li>
      <li><span class="tag t-use">Use</span><h3>Answer it</h3><p>SQL and BI tools like Power BI query trusted, documented tables.</p></li>
    </ol>
  </div>
</section>

<section class="section" id="about" aria-labelledby="about-title">
  <div class="wrap">
    <div class="sec-head"><span class="num">01 — About</span><h2 id="about-title">Reliable data, built in layers.</h2></div>
    <div class="about-grid indent">
      <div class="prose">{about}</div>
      <dl class="facts">{facts}</dl>
    </div>
  </div>
</section>

<section class="section" id="work" aria-labelledby="work-title">
  <div class="wrap">
    <div class="sec-head"><span class="num">02 — Selected work</span><h2 id="work-title">Data engineering projects</h2>
      <p>Three end-to-end builds — from a SQL Server warehouse to Databricks lakehouses. Each has a full write-up and public source code.</p></div>
    <div class="cases">{''.join(cases)}</div>
  </div>
</section>

<section class="section" id="toolkit" aria-labelledby="toolkit-title">
  <div class="wrap">
    <div class="sec-head"><span class="num">03 — Toolkit</span><h2 id="toolkit-title">What I work with</h2>
      <p>The tools behind the projects above — every item here is used in at least one of them.</p></div>
    <dl class="toolkit indent">{toolkit}</dl>
  </div>
</section>

<section class="section" id="approach" aria-labelledby="approach-title">
  <div class="wrap">
    <div class="sec-head"><span class="num">04 — Approach</span><h2 id="approach-title">How I build pipelines</h2></div>
    <ol class="principles indent">{principles}</ol>
  </div>
</section>

<section class="section" id="certificates" aria-labelledby="certs-title">
  <div class="wrap">
    <div class="sec-head"><span class="num">05 — Certificates</span><h2 id="certs-title">Continuous learning</h2>
      <p>Verified courses in data engineering, Python, relational databases, Apache Spark, data warehousing and generative AI.</p></div>
    <div class="indent">
      <table class="certs">
        <thead><tr><th class="label">Course</th><th class="label">Issuer</th><th class="label">Year</th><th class="label"><span class="visually-hidden">Link</span></th></tr></thead>
        <tbody>{certs}</tbody>
      </table>
    </div>
  </div>
</section>

<section class="section" id="contact" aria-labelledby="contact-title">
  <div class="wrap">
    <div class="sec-head"><span class="num">06 — Contact</span><h2 id="contact-title">Let's talk data.</h2></div>
    <div class="contact-grid indent">
      <div>
        <p class="prose m0">Hiring for a data engineering role, or have a pipeline that needs building? Email is the fastest way to reach me.</p>
        <a class="big-mail" href="mailto:{EMAIL}">{EMAIL}</a>
      </div>
      <dl class="channels">
        <div><dt class="label">Phone</dt><dd><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></dd></div>
        <div><dt class="label">WhatsApp</dt><dd><a href="{WHATSAPP}" target="_blank" rel="noopener">Message on WhatsApp ↗</a></dd></div>
        <div><dt class="label">LinkedIn</dt><dd><a href="{LINKEDIN}" target="_blank" rel="me noopener">abdullah-alhaddad ↗</a></dd></div>
        <div><dt class="label">GitHub</dt><dd><a href="{GITHUB}" target="_blank" rel="me noopener">alhaddad-a ↗</a></dd></div>
        <div><dt class="label">Location</dt><dd>{LOCATION}</dd></div>
      </dl>
    </div>
  </div>
</section>
</main>""" + footer()


def page_project(idx: int) -> str:
    p = PROJECTS[idx]
    path = f"/projects/{p['slug']}/"
    url = SITE_URL + path
    jsonld = [{
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
                {"@type": "ListItem", "position": 2, "name": "Work", "item": SITE_URL + "/#work"},
                {"@type": "ListItem", "position": 3, "name": p["title"], "item": url},
            ]},
            {"@type": "SoftwareSourceCode", "@id": url + "#project", "name": p["title"],
             "description": p["description"], "url": url, "codeRepository": p["repo"],
             "programmingLanguage": ["Python", "SQL"] if idx else ["SQL"],
             "keywords": ", ".join(p["stack"]), "author": {"@type": "Person", "@id": PERSON_ID, "name": NAME, "url": SITE_URL + "/"},
             "image": SITE_URL + "/assets/img/og-image.jpg", "dateModified": TODAY},
        ],
    }]
    facts = "".join(f'<div><dt class="label">{escape(k)}</dt><dd>{escape(v)}</dd></div>' for k, v in p["facts"])
    toc = "".join(f'<li><a href="#{sid}">{escape(t)}</a></li>' for sid, t, _ in p["sections"])
    body = "".join(f'<section id="{sid}" aria-labelledby="{sid}-h"><h2 id="{sid}-h">{escape(t)}</h2>{html}</section>'
                   for sid, t, html in p["sections"])
    svg = diagram_svg("flow", p["diagram"], label=f"Data flow for {p['title']}: " + " → ".join(
        f"{c['head']} ({', '.join(c['items'])})" for c in p["diagram"]))
    prev_p = PROJECTS[idx - 1]
    next_p = PROJECTS[(idx + 1) % len(PROJECTS)]

    return head(p["seo_title"], p["description"], path, jsonld, og_type="article") + header("Work") + f"""
<main id="main">
<nav class="crumbs wrap" aria-label="Breadcrumb">
  <ol class="label"><li><a href="/">Home</a></li><li><a href="/#work">Work</a></li><li aria-current="page">Project {idx + 1:02d}</li></ol>
</nav>
<header class="cs-head wrap">
  <h1>{escape(p['title'])}</h1>
  <p class="lead">{escape(p['summary'])}</p>
  <div class="actions mt-28">
    <a class="btn btn-solid" href="{p['repo']}" target="_blank" rel="noopener">View source on GitHub <span class="arr">↗</span></a>
  </div>
  <dl class="cs-facts">{facts}</dl>
</header>
<div class="wrap">
  <figure class="wide-fig">
    <div class="diagram full">{svg}</div>
    <figcaption class="label mt-10">Fig. — Data flow, source to {escape(p['diagram'][-1]['head'].lower())}. Stack: {escape(' · '.join(p['stack']))}</figcaption>
  </figure>
  <div class="cs-body">
    <aside class="toc" aria-label="On this page"><span class="label">On this page</span><ol>{toc}</ol></aside>
    <article class="article">{body}</article>
  </div>
  <nav class="pager" aria-label="More projects">
    <a href="/projects/{prev_p['slug']}/"><span class="label">← Previous</span><span class="t">{escape(prev_p['title'])}</span></a>
    <a href="/projects/{next_p['slug']}/"><span class="label">Next →</span><span class="t">{escape(next_p['title'])}</span></a>
  </nav>
</div>
</main>""" + footer()


def page_404() -> str:
    html = head(f"Page not found — {NAME}", "This page doesn't exist. Go back to Abdullah Alhaddad's data engineering portfolio.", "/404", [])
    html = html.replace('<meta name="robots" content="index, follow, max-image-preview:large">',
                        '<meta name="robots" content="noindex">')
    html = html.replace(f'<link rel="canonical" href="{SITE_URL}/404">\n', "")
    links = "".join(f'<li><a href="/projects/{p["slug"]}/">{escape(p["title"])}</a></li>' for p in PROJECTS)
    return html + header() + f"""
<main id="main" class="notfound">
  <div class="wrap">
    <p class="label">Error 404</p>
    <h1>This row didn't make it to Gold.</h1>
    <p class="prose">The page you're looking for doesn't exist or has moved.</p>
    <div class="actions nf-actions"><a class="btn btn-solid" href="/">Back to the homepage</a></div>
    <p class="label">Or read a case study</p>
    <ul class="prose">{links}</ul>
  </div>
</main>""" + footer()


def sitemap() -> str:
    urls = ["/"] + [f"/projects/{p['slug']}/" for p in PROJECTS]
    rows = "\n".join(
        f"  <url><loc>{SITE_URL}{u}</loc><lastmod>{TODAY}</lastmod>"
        f"<priority>{'1.0' if u == '/' else '0.8'}</priority></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}\n</urlset>\n'


def robots() -> str:
    return f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"


def security_txt() -> str:
    expires = (_dt.datetime.now(_dt.timezone.utc) + _dt.timedelta(days=365)).strftime("%Y-%m-%dT00:00:00Z")
    return (f"Contact: mailto:{EMAIL}\n"
            f"Expires: {expires}\n"
            "Preferred-Languages: en\n"
            f"Canonical: {SITE_URL}/.well-known/security.txt\n")


def write(rel: str, text: str) -> None:
    path = PUBLIC / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"  wrote public/{rel}")


def main() -> None:
    print("Building site...")
    write("index.html", page_home())
    for i, p in enumerate(PROJECTS):
        write(f"projects/{p['slug']}/index.html", page_project(i))
    write("404.html", page_404())
    write("sitemap.xml", sitemap())
    write("robots.txt", robots())
    write(".well-known/security.txt", security_txt())
    print("Done.")


if __name__ == "__main__":
    main()
