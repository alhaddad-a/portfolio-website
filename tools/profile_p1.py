"""Profile the CRM/ERP source CSVs (projects 01 and 02) against the rules in proc_load_silver.sql."""
import csv, sys, json, collections, datetime
from pathlib import Path

root = Path(sys.argv[1])
out = {}

def rows(rel):
    with open(root / rel, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def ws(v):
    return v != v.strip()

# --- cust_info
r = rows("datasets/source_crm/cust_info.csv")
ids = [x["cst_id"] for x in r]
nonnull = [i for i in ids if i.strip() != ""]
c = collections.Counter(nonnull)
out["cust_info"] = {
    "rows": len(r),
    "null_id": sum(1 for i in ids if i.strip() == ""),
    "dup_ids": sum(1 for k, v in c.items() if v > 1),
    "dup_extra_rows": sum(v - 1 for v in c.values() if v > 1),
    "dup_example": [x for x in r if c.get(x["cst_id"], 0) > 1][:4],
    "first_ws": sum(ws(x["cst_firstname"]) for x in r),
    "first_ws_lead": sum(x["cst_firstname"] != x["cst_firstname"].lstrip() for x in r),
    "last_ws": sum(ws(x["cst_lastname"]) for x in r),
    "name_ws_any": sum(ws(x["cst_firstname"]) or ws(x["cst_lastname"]) for x in r),
    "key_ws": sum(ws(x["cst_key"]) for x in r),
    "marital": collections.Counter(x["cst_marital_status"] for x in r).most_common(),
    "gndr": collections.Counter(x["cst_gndr"] for x in r).most_common(),
    "first3": r[:5],
}
# rows surviving: non-null id, one per id
out["cust_info"]["silver_rows"] = len(c)

# --- prd_info
r = rows("datasets/source_crm/prd_info.csv")
out["prd_info"] = {
    "rows": len(r),
    "cost_null": sum(1 for x in r if x["prd_cost"].strip() == ""),
    "line": collections.Counter(x["prd_line"] for x in r).most_common(),
    "end_before_start": sum(1 for x in r if x["prd_end_dt"] and x["prd_start_dt"] and x["prd_end_dt"] < x["prd_start_dt"]),
    "end_before_start_ex": [x for x in r if x["prd_end_dt"] and x["prd_end_dt"] < x["prd_start_dt"]][:3],
    "nm_ws": sum(ws(x["prd_nm"]) for x in r),
    "sample": r[:3],
}

# --- sales_details
r = rows("datasets/source_crm/sales_details.csv")
def bad_date(v):
    v = v.strip()
    return v == "" or v == "0" or len(v) != 8
def num(v):
    v = v.strip()
    return None if v == "" else float(v)
bad_sales, bad_price, ex_sales, ex_price = 0, 0, [], []
for x in r:
    s, q, p = num(x["sls_sales"]), num(x["sls_quantity"]), num(x["sls_price"])
    if s is None or s <= 0 or (q is not None and p is not None and s != q * abs(p)) or p is None:
        bad_sales += 1
        if len(ex_sales) < 6: ex_sales.append(x)
    if p is None or p <= 0:
        bad_price += 1
        if len(ex_price) < 4: ex_price.append(x)
out["sales_details"] = {
    "rows": len(r),
    "order_bad": sum(bad_date(x["sls_order_dt"]) for x in r),
    "order_bad_ex": [x["sls_order_dt"] for x in r if bad_date(x["sls_order_dt"])][:8],
    "order_bad_values": collections.Counter(x["sls_order_dt"] for x in r if bad_date(x["sls_order_dt"])).most_common(8),
    "ship_bad": sum(bad_date(x["sls_ship_dt"]) for x in r),
    "due_bad": sum(bad_date(x["sls_due_dt"]) for x in r),
    "sales_inconsistent": bad_sales,
    "sales_ex": ex_sales,
    "price_bad": bad_price,
    "price_ex": ex_price,
}

# --- CUST_AZ12
r = rows("datasets/source_erp/CUST_AZ12.csv")
today = datetime.date(2026, 11, 25)
def pdate(v):
    m, d, y = v.split("/") if "/" in v else (None, None, None)
    if m is None:
        return datetime.date.fromisoformat(v)
    return datetime.date(int(y), int(m), int(d))
dates = [(x, pdate(x["BDATE"])) for x in r if x["BDATE"].strip()]
out["cust_az12"] = {
    "rows": len(r),
    "nas": sum(x["CID"].startswith("NAS") for x in r),
    "future": sum(1 for _, d in dates if d > today),
    "future_ex": [(x["CID"], x["BDATE"]) for x, d in dates if d > today][:5],
    "before_1924": sum(1 for _, d in dates if d < datetime.date(1924, 1, 1)),
    "before_1924_ex": [(x["CID"], x["BDATE"]) for x, d in dates if d < datetime.date(1924, 1, 1)][:5],
    "gen": collections.Counter(x["GEN"] for x in r).most_common(),
    "bdate_formats": collections.Counter("slash" if "/" in x["BDATE"] else "iso" for x in r).most_common(),
}

# --- LOC_A101
r = rows("datasets/source_erp/LOC_A101.csv")
out["loc_a101"] = {
    "rows": len(r),
    "hyphen": sum("-" in x["CID"] for x in r),
    "sample": r[:2],
    "cntry": collections.Counter(x["CNTRY"] for x in r).most_common(),
}

# --- PX_CAT
r = rows("datasets/source_erp/PX_CAT_G1V2.csv")
out["px_cat"] = {
    "rows": len(r),
    "ws": sum(ws(x["CAT"]) or ws(x["SUBCAT"]) or ws(x["MAINTENANCE"]) for x in r),
    "maint": collections.Counter(x["MAINTENANCE"] for x in r).most_common(),
}
print(json.dumps(out, indent=1, default=str))
