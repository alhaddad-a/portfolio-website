"""Cross-check Harborview data-quality log counts against the raw CSVs and collect verbatim raw values."""
import csv, sys, json, collections, io, zipfile
from pathlib import Path

root = Path(sys.argv[1]) / "01_raw_data"
out = {}

def read(name):
    with open(root / name, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

c = read("customers.csv")
out["customers"] = {
    "rows": len(c),
    "distinct_rows": len(set(tuple(x.values()) for x in c)),
    "distinct_ids": len(set(x["customer_id"] for x in c)),
    "gender": collections.Counter(x["gender"] for x in c).most_common(),
    "income_band": collections.Counter(x["income_band"] for x in c).most_common(),
    "bdate_1900": sum(x["birth_date"] == "1900-01-01" for x in c),
    "email_upper_ex": [x["email"] for x in c if "@MAIL" in x["email"].upper() and x["email"] != x["email"].lower()][:2],
    "email_trailing": sum(x["email"].endswith(" ") for x in c),
    "region_blank": sum(x["region"] == "" for x in c),
    "signup_slash": sum("/" in x["signup_date"] for x in c),
    "signup_ex": [x["signup_date"] for x in c if "/" in x["signup_date"]][:5],
    "signup_17_12": [x["signup_date"] for x in c if x["signup_date"].startswith("17/12")][:2],
    "cols": list(c[0].keys()),
}
a = read("accounts.csv")
out["accounts"] = {
    "rows": len(a),
    "status": collections.Counter(x["status"] for x in a).most_common(),
    "close_before_open": sum(1 for x in a if x["close_date"] and x["close_date"] < x["open_date"]),
    "cbo_ex": [x for x in a if x["close_date"] and x["close_date"] < x["open_date"]][:2],
}
l = read("loans.csv")
out["loans"] = {
    "rows": len(l),
    "distinct": len(set(tuple(x.values()) for x in l)),
    "amount_empty": sum(x["loan_amount"] == "" for x in l),
    "rate_ge1": sum(1 for x in l if x["interest_rate"] and float(x["interest_rate"]) >= 1),
    "rate_ex": [x["interest_rate"] for x in l if x["interest_rate"] and float(x["interest_rate"]) >= 1][:5],
    "score_0": sum(x["credit_score_at_origination"] == "0" for x in l),
    "score_999": sum(x["credit_score_at_origination"] == "999" for x in l),
    "cols": list(l[0].keys()),
}
# transactions (zip, streamed)
z = zipfile.ZipFile(root / "transactions.zip")
name = [n for n in z.namelist() if n.endswith(".csv")][0]
n = 0; neg = 0; neg_ex = []; mc = collections.Counter(); blank_ch = 0; orphan = 0; orphan_ex = []; y2026 = 0; y2026_ex = []
seen = set(); dups = 0
with z.open(name) as f:
    r = csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig", newline=""))
    cols = r.fieldnames
    for x in r:
        n += 1
        t = tuple(x.values())
        if t in seen: dups += 1
        else: seen.add(t)
        mc[x["merchant_category"]] += 1
        if x["amount"].startswith("-"):
            neg += 1
            if len(neg_ex) < 2: neg_ex.append((x["txn_type"], x["amount"]))
        if x["channel"] == "": blank_ch += 1
        if not x["account_id"].startswith("A0"):
            orphan += 1
            if len(orphan_ex) < 2: orphan_ex.append(x["account_id"])
        if x["txn_datetime"][:4] >= "2026":
            y2026 += 1
            if len(y2026_ex) < 2: y2026_ex.append(x["txn_datetime"])
out["transactions"] = {"rows": n, "exact_dups": dups, "neg": neg, "neg_ex": neg_ex, "merchant_distinct": len(mc),
                       "merchant_ws_ex": [k for k in mc if k != k.strip()][:4], "blank_channel": blank_ch,
                       "orphan": orphan, "orphan_ex": orphan_ex, "y2026": y2026, "y2026_ex": y2026_ex, "cols": cols}
print(json.dumps(out, indent=1))
