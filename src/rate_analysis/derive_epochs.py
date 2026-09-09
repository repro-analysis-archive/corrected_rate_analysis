#!/usr/bin/env python3
"""Regenerate the relative-enrolment epoch assignment from the public MAMA-MIA clinical workbook.

Rule (recorded in config/epoch_canonical_mapping.json): epoch boundaries are placed at the first observed acquisition
date (arm-open start) and at the day after the last observed date (end + 1) of every EXPERIMENTAL arm, i.e. every
`nac_agent` value other than the two control arms `Paclitaxel` (HER2-negative cohort) and `Paclitaxel + Trastuzumab`
(HER2-positive cohort). Consecutive boundaries delimit raw intervals; adjacent intervals with an identical set of active
experimental arms are merged (none are, with these boundaries); the populated intervals are numbered chronologically
from 1. The rule is applied to the 980 I-SPY2 patients of both cohorts (dataset == "ISPY2", her2 in {0, 1}, non-missing
pcr) in workbook row order and yields 22 epochs.

Output: reproduction/splits/epoch_assignment.csv with the columns patient_id, date, epoch, the layout of the frozen
table. On the recorded workbook version (sha256 0d95c6af…, checksums/INPUT_PROVENANCE.txt) the regenerated file
reproduces the frozen table exactly (sha256 b893a669…). The loader (r4_stageA.py) and the prioritization scripts read
this file; run it first.

Added for the public release: the frozen record kept the assignment table but not the code that produced it. This
script implements the documented rule and was verified against the frozen table before release.
"""
import os, hashlib
import numpy as np, pandas as pd

RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
DATA = os.environ.get("JIIM_DATA_ROOT", os.path.join(RELEASE_ROOT, "external_data"))
CLINICAL_XLSX = os.path.join(DATA, "clinical_and_imaging_info.xlsx")
OUT = os.path.join(RELEASE_ROOT, "reproduction", "splits"); os.makedirs(OUT, exist_ok=True)
CONTROL_ARMS = {"Paclitaxel", "Paclitaxel + Trastuzumab"}
FROZEN_SHA256 = "b893a669f95ae1e92a346bbae23450fdb99fc6b899baad69b8679e0a42c99067"

df = pd.read_excel(CLINICAL_XLSX)
c = df[(df.dataset == "ISPY2") & (df.her2.isin([0.0, 1.0]))].dropna(subset=["pcr"]).copy()
c["d"] = pd.to_datetime(c["acquisition_date"])
arms = c[~c.nac_agent.isin(CONTROL_ARMS)].groupby("nac_agent")["d"].agg(["min", "max"])
bounds = sorted(set(list(arms["min"]) + list(arms["max"] + pd.Timedelta(days=1))))

raw = np.searchsorted(np.array(bounds, dtype="datetime64[ns]"), c["d"].values.astype("datetime64[ns]"), side="right")
edges = [pd.Timestamp.min] + bounds + [pd.Timestamp.max]

def active(i):
    lo, hi = edges[i], edges[i + 1]
    return frozenset(a for a, r in arms.iterrows() if r["min"] <= lo and r["max"] + pd.Timedelta(days=1) >= hi)

labels, cur, prev = [], 0, None
for i in range(len(edges) - 1):
    act = active(i)
    if prev is None or act != prev:
        cur += 1
    labels.append(cur); prev = act
merged = np.array([labels[i] for i in raw])
renum = {e: k + 1 for k, e in enumerate(sorted(set(merged)))}
c["epoch"] = [renum[e] for e in merged]

out = pd.DataFrame({"patient_id": c.patient_id.values, "date": c["d"].dt.strftime("%Y-%m-%d").values, "epoch": c["epoch"].values})
p = os.path.join(OUT, "epoch_assignment.csv"); out.to_csv(p, index=False)
h = hashlib.sha256(open(p, "rb").read()).hexdigest()
print(f"wrote {p}: {len(out)} patients, {out.epoch.nunique()} epochs from {len(bounds)} boundaries "
      f"({len(arms)} experimental arms); adjacent merges: {len(edges) - 1 - len(set(labels))}")
print(f"sha256 {h} -> {'MATCHES' if h == FROZEN_SHA256 else 'DIFFERS FROM'} the frozen table ({FROZEN_SHA256[:16]}...)")
