"""Replay the healthcare-lakehouse Silver notebook logic on the raw CSVs (empty CSV field = null, as Spark reads it)."""
import csv, sys, json, collections
from decimal import Decimal
from pathlib import Path

root = Path(sys.argv[1]) / "datasets"
out = {}

def read(rel):
    with open(root / rel, newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f)
        head = next(r)
        return head, [tuple(x) for x in r]

def profile(rel_list, key):
    head, allrows = None, []
    per = {}
    for rel in rel_list:
        h, rr = read(rel)
        head = h
        per[rel] = len(rr)
        allrows += rr
    distinct = list(dict.fromkeys(allrows))
    ki = head.index(key)
    ids = collections.Counter(x[ki] for x in distinct)
    nulls = {c: sum(1 for x in distinct if x[i] == "") for i, c in enumerate(head)}
    ws = {c: sum(1 for x in distinct if x[i] != x[i].strip()) for i, c in enumerate(head)}
    return head, allrows, distinct, {
        "files": per, "rows": len(allrows), "after_dropDuplicates": len(distinct),
        "exact_dup_rows": len(allrows) - len(distinct),
        "dup_keys_after": sum(1 for v in ids.values() if v > 1),
        "nulls_after": {k: v for k, v in nulls.items() if v},
        "whitespace_after": {k: v for k, v in ws.items() if v},
    }

head, a, d, p = profile(["ehr/patients.csv"], "patient_id")
gi = head.index("gender")
p["gender"] = collections.Counter(x[gi] for x in d).most_common()
p["city_null_example"] = [x for x in d if x[head.index("city")] == ""][:3]
_c = collections.Counter(a); p["dup_example"] = [x for x in d if _c[x] > 1][:3]
out["patients"] = p

for name, rel, key in [("doctors", "ehr/doctors.csv", "doctor_id"),
                       ("hospitals", "master_data/hospitals.csv", "hospital_id"),
                       ("procedures", "master_data/procedures.csv", "procedure_id")]:
    head, a, d, p = profile([rel], key)
    if name == "procedures":
        ni, di = head.index("procedure_name"), head.index("department")
        trimmed = [tuple(v.strip() if i in (ni, di) else v for i, v in enumerate(x)) for x in a]
        p["after_trim_dropDuplicates"] = len(dict.fromkeys(trimmed))
        p["ws_examples"] = [x for x in a if x[ni] != x[ni].strip() or x[di] != x[di].strip()][:4]
        p["ws_rows_raw"] = sum(1 for x in a if x[ni] != x[ni].strip() or x[di] != x[di].strip())
    out[name] = p

years = range(2021, 2026)
head, a, d, p = profile([f"ehr/admissions_{y}.csv" for y in years], "admission_id")
di = head.index("admission_date")
p["missing_date_after"] = sum(1 for x in d if x[di] == "")
p["missing_date_example"] = [x for x in d if x[di] == ""][:2]
out["admissions"] = p

head, a, d, p = profile([f"billing/billing_{y}.csv" for y in years], "billing_id")
ti, ii, pi = head.index("total_cost"), head.index("insurance_paid"), head.index("patient_paid")
def q2(v): return Decimal(v).quantize(Decimal("0.01"))
mism = [x for x in a if x[ii] and x[pi] and x[ti] and q2(Decimal(x[ii]) + Decimal(x[pi])) != q2(Decimal(x[ti]))]
long_dec = [x for x in a if "." in x[pi] and len(x[pi].split(".")[1]) > 2]
long_dec_i = [x for x in a if "." in x[ii] and len(x[ii].split(".")[1]) > 2]
p["financial_mismatch"] = len(mism)
p["patient_paid_over_2dp"] = len(long_dec)
p["insurance_paid_over_2dp"] = len(long_dec_i)
p["over_2dp_examples"] = [x for x in long_dec[:4]]
p["max_dp_example"] = max(long_dec, key=lambda x: len(x[pi]))
out["billing"] = p
print(json.dumps(out, indent=1, default=str))
