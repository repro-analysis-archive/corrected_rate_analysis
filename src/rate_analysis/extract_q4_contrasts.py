#!/usr/bin/env python3
"""Re-serialise the Q4 pooled and half-specific contrasts of rate_q4_regimes.json into rate_q4_contrasts.json.

The contrasts file of the frozen record holds exactly the pooled_* and by_half contrast fields of the regimes file
plus a summary block. This script regenerates it and, when the released record is present, reports whether the
regenerated file agrees with results/rate_q4/rate_q4_contrasts.json. It performs no statistics.

    python src/rate_analysis/extract_q4_contrasts.py [path/to/rate_q4_regimes.json]

Default input: reproduction/rate_q4/rate_q4_regimes.json (the output of rate_q4.R). The output is always written to
reproduction/rate_q4/rate_q4_contrasts.json, so the released record is never overwritten.
"""
import os, sys, json
RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RELEASE_ROOT, "reproduction", "rate_q4", "rate_q4_regimes.json")
outdir = os.path.join(RELEASE_ROOT, "reproduction", "rate_q4"); dst = os.path.join(outdir, "rate_q4_contrasts.json")
r = json.load(open(src))
cfgs = list(r["results"].keys())
POOLED = ["pooled_P", "pooled_S", "pooled_PS", "pooled_B_minus_A", "q3_pooled_C_minus_A", "preprocessing_fraction_of_Q3"]
HALF = ["P_effect", "S_effect", "PS", "Total_B_minus_A"]
contrasts = {cg: {k: r["results"][cg][k] for k in POOLED} for cg in cfgs}
by_half = {cg: {h: {k: r["results"][cg]["by_half"][h][k] for k in HALF} for h in ("H1", "H2")} for cg in cfgs}
img = [cg for cg in cfgs if r["results"][cg]["has_imaging_block"]]
sign = lambda x: (x > 0) - (x < 0)
P = [contrasts[cg]["pooled_P"] for cg in img]; PS = [contrasts[cg]["pooled_PS"] for cg in img]
S = [contrasts[cg]["pooled_S"] for cg in cfgs]; BA = [contrasts[cg]["pooled_B_minus_A"] for cg in cfgs]
FR = [contrasts[cg]["preprocessing_fraction_of_Q3"] for cg in cfgs]
summary = {"pooled_P_range": [min(P), max(P)], "pooled_P_n_negative": sum(1 for x in P if x < 0),
           "pooled_S_range": [min(S), max(S)], "pooled_PS_range": [min(PS), max(PS)],
           "pooled_B_minus_A_range": [min(BA), max(BA)], "fraction_of_Q3_range": [min(FR), max(FR)],
           "n_configs_P_sign_agrees_across_halves": sum(1 for cg in img if sign(by_half[cg]["H1"]["P_effect"]) == sign(by_half[cg]["H2"]["P_effect"])),
           "n_configs_BminusA_sign_agrees_across_halves": sum(1 for cg in cfgs if sign(by_half[cg]["H1"]["Total_B_minus_A"]) == sign(by_half[cg]["H2"]["Total_B_minus_A"])),
           "n_imaging_configs": len(img)}
out = {"design": r["design"], "run_checks": r["run_checks"], "n_H1": r["n_H1"], "n_H2": r["n_H2"],
       "contrasts": contrasts, "by_half_contrasts": by_half, "summary": summary}
os.makedirs(outdir, exist_ok=True)
with open(dst, "w") as f: json.dump(out, f, indent=1)
print(f"wrote {dst}")
ref = os.path.join(RELEASE_ROOT, "results", "rate_q4", "rate_q4_contrasts.json")
if os.path.exists(ref):
    same_json = json.load(open(ref)) == out
    same_bytes = open(ref, "rb").read() == open(dst, "rb").read()
    print(f"agreement with the released record: json_equal={same_json}  byte_identical={same_bytes}")
