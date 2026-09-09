"""Canonical cohort definition from the public MAMA-MIA clinical workbook.

Identical to the rule of the frozen loader (src/rate_analysis/r4_stageA.py, function load): rows with
dataset == "ISPY2", her2 == 0 (HER2-negative) or her2 == 1 (HER2-positive) and a non-missing pcr value, in workbook
row order. Returns the 739 (HER2-negative) or 241 (HER2-positive) patient identifiers. On the recorded workbook
version this order equals the row order of the frozen feature matrices.

Added for the public release so that no patient-identifier list needs to be distributed.
"""
import pandas as pd

HER2 = {"her2neg": 0.0, "her2pos": 1.0}


def cohort_ids(cohort, xlsx):
    df = pd.read_excel(xlsx)
    c = df[(df.dataset == "ISPY2") & (df.her2 == HER2[cohort])].dropna(subset=["pcr"])
    return list(c["patient_id"])
