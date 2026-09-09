#!/usr/bin/env python3
"""R7 step 6 - implementation cross-check on the SAME grf DR scores and the SAME priorities.
(1) direct re-implementation of grf's exact RATE definition (all n patient increments);
(2) econml.validate.utils.calc_uplift(metric='toc') - a DIFFERENT estimand by construction
    (50-point left-Riemann sum truncated to q in [0.05,0.95]); sign / ordering / gross-error only."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r7_common import *
from econml.validate.utils import calc_uplift

dr = pd.read_csv(f"{OUT}/dr_scores_primary_heldout.csv")
pri = pd.read_csv(f"{OUT}/priorities_primary_heldout.csv")
G = dr.dr_score.values.astype(float)

def rate_grf_exact(gamma, s):
    """grf estimate_rate, unweighted: rank descending, average tied groups, TOC = cummean - ATE,
    RATE = mean(TOC) over all n increments."""
    r = pd.Series(s).rank(method="dense").values          # ties share a rank, as as.factor() does
    order = np.argsort(-r, kind="stable")
    g = pd.DataFrame({"r": r[order], "g": gamma[order]})
    g["g"] = g.groupby("r")["g"].transform("mean")        # average DR scores within tied groups
    gs = g.g.values
    ate = gs.mean()
    toc = np.cumsum(gs) / np.arange(1, len(gs) + 1) - ate
    return float(toc.mean())

out, cfgs = {}, list(CONFIGS.keys())
for cg in cfgs:
    d = pri[pri.configuration == cg]
    assert (d.patient_id.values == dr.patient_id.values).all()
    s = d.priority.values.astype(float)
    direct = rate_grf_exact(G, s)
    coeff, cerr, _ = calc_uplift(s.reshape(-1, 1), s.reshape(-1, 1), G.reshape(-1, 1),
                                 np.linspace(5, 95, 50), "toc", n_bootstrap=200)
    out[cg] = {"direct_grf_definition": direct,
               "econml_calc_uplift_toc": float(coeff), "econml_influence_se": float(cerr)}
grf_json = json.load(open(f"{OUT}/rate_q1_primary.json"))["q1"]
print(f"{'configuration':28s} {'grf':>9s} {'direct':>9s} {'|diff|':>9s} {'econml':>9s}")
for cg in cfgs:
    g = grf_json[cg]["estimate"]; d = out[cg]["direct_grf_definition"]; e = out[cg]["econml_calc_uplift_toc"]
    out[cg]["grf_estimate"] = g; out[cg]["abs_diff_direct_vs_grf"] = abs(g - d)
    out[cg]["sign_agrees_econml"] = bool(np.sign(g) == np.sign(e))
    print(f"{cg:28s} {g:+9.5f} {d:+9.5f} {abs(g-d):9.2e} {e:+9.5f}")
rk = lambda v: list(pd.Series(v, index=cfgs).rank(ascending=False).astype(int))
order = {"grf": rk([grf_json[c]["estimate"] for c in cfgs]),
         "direct": rk([out[c]["direct_grf_definition"] for c in cfgs]),
         "econml": rk([out[c]["econml_calc_uplift_toc"] for c in cfgs])}
print("\nrank order (1 = highest):", json.dumps(order))
json.dump({"note": "grf is primary; the direct implementation reproduces grf's definition exactly; "
                   "econml uses a truncated 50-point grid on q in [0.05,0.95] and is a "
                   "sign/ordering/gross-error check only, not a replication",
           "per_configuration": out, "rank_order": order,
           "max_abs_diff_direct_vs_grf": max(out[c]["abs_diff_direct_vs_grf"] for c in cfgs),
           "sign_agreement_grf_vs_econml": all(out[c]["sign_agrees_econml"] for c in cfgs),
           "rank_order_identical_grf_vs_econml": order["grf"] == order["econml"]},
          open(f"{OUT}/crosscheck_implementations.json", "w"), indent=1)
print("\nwrote crosscheck_implementations.json")
