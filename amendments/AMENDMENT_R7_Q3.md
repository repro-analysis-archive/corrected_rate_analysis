# Amendment R7-Q3 — corrected evaluation-induced-optimism diagnostic under standard RATE/AUTOC

**Manuscript:** JDIM-D-26-02440
**Status:** protocol-locked post-audit. **Not prespecified.** Committed and hashed **before any
model was fitted.** Outputs to `R7_rate_q3/` only.
**`R7_rate_primary/` (including `FROZEN_R7/`) and every `FROZEN_*` set are INPUT ONLY.**
**Instruction of record:** `~/Downloads/JIIM_CC_R7_QA_and_Corrected_Q3_Instructions.md`.
**Predecessor:** `R7_rate_primary/AMENDMENT_R7_RATE.md`, commit `755aecb2`, results commit `2e87fa6f`.

---

## 1. What this measures, and what it does not

**Question.** How much does the corrected standard RATE/AUTOC **point estimate** change when the
prioritization rule is fitted and evaluated on the same patients instead of being evaluated on
independent patients?

This is an **evaluation-induced-optimism diagnostic**. It is **not** a test of treatment-effect
heterogeneity, and it produces **no p-value and no null distribution**.

It is not a recovery of the retired Q3. The retired Q3 compared regimes under the uncentred
`autoc()` statistic and calibrated them against 2,000 within-stratum treatment-label permutations,
whose null tested no-treatment-effect. Neither the statistic nor the null is carried forward. The
published +0.0992 to +0.2482 observed-optimism figures and the +0.1428 to +0.3173 null shifts are
retired and are not comparable to anything computed here.

## 2. Population and split — reused, not regenerated

HER2-negative n = 739, and the **exact fixed R7 50/50 split**:

- **H1** = the R7 *training* half, n = 370
- **H2** = the R7 *evaluation* half, n = 369

read from the frozen `R7_rate_primary/FROZEN_R7/split_739.csv`. No new split is drawn, and the
split is not re-seeded or adjusted.

## 3. Two-way symmetric design

The direction labels "train" and "evaluation" were an arbitrary product of one random draw, so the
diagnostic is run in both directions and reported separately as well as pooled.

| | prioritization rule fitted on | priorities predicted on | preprocessing fitted on |
|---|---|---|---|
| **A_H2** (honest) | H1 | H2 | H1 |
| **C_H2** (apparent) | H2 | H2 | H2 |
| **A_H1** (honest) | H2 | H1 | H2 |
| **C_H1** (apparent) | H1 | H1 | H1 |

`A_H2` already exists: it is the frozen R7 primary priority set and is **reused verbatim**, not
refitted. `C_H2`, `A_H1` and `C_H1` are new fits.

**Preprocessing rule, binding.** Every data-adaptive step — clinical `StandardScaler`, imaging
`StandardScaler`, `PCA` — is fitted on the half named in the last column and on no other rows. In
the honest regimes that is the opposite half; in the apparent regimes it is the same half on which
the rule is then evaluated. Model hyperparameters, seeds and feature definitions are the frozen
R4 ones, unchanged.

## 4. Evaluation scores

- **H2:** the **frozen R7 DR vector** is reused byte-for-byte from
  `FROZEN_R7/dr_scores_primary_heldout.csv`. `A_H2` and `C_H2` are scored against the identical
  vector, so the two differ only in the ranking.
- **H1:** one new common DR vector is built with the **same locked specification** —
  `causal_forest(X = Z_H1, Y, W = T, num.trees = 2000, seed = 42)`, `get_scores()`, where `Z_H1`
  is the R7 imaging-free covariate set (`build_Z.py`, reused unmodified) restricted to H1.
  `A_H1` and `C_H1` are scored against the identical vector.

Z excludes radiomics, BiomedCLIP, RAD-DINO, `tumor_subtype` (exactly collinear with `hr` in this
population) and `her2` (constant), and merges the two whitespace-variant `menopause` "pre" levels
in Z only. **Imaging never enters the evaluation score in either half.**

## 5. Estimands — point estimates only

```
optimism_H1     = RATE(C_H1) - RATE(A_H1)
optimism_H2     = RATE(C_H2) - RATE(A_H2)
pooled_optimism = (370 * optimism_H1 + 369 * optimism_H2) / 739
```

`pooled_optimism` is a **predeclared descriptive sample-size-weighted contrast**, defined here
before any of it is computed.

**No p-value, confidence interval or standard error is produced for C, for C - A, or for
`pooled_optimism`.** Standard RATE inference assumes a prioritization rule trained independently
of the evaluation data; C is deliberately trained on the same outcomes and treatment labels, so
grf's ordinary half-sample bootstrap SE does not describe its sampling behaviour, and an
A-versus-C bootstrap would require refitting C inside every resample, which this task does not do.

grf bootstrap SEs are retained **for the honest A rates only**, as ordinary held-out RATE
uncertainty, and are labelled as such. `RATE(A_H2)` must reproduce the frozen R7 Q1 values exactly;
that identity is asserted as a run check.

## 6. Permitted and prohibited wording — binding

**Permitted:** *same-sample evaluation increased the RATE point estimate* ·
*same-sample evaluation did not consistently increase the RATE point estimate*.

**Prohibited:** "significant optimism"; any `p < ...` attached to an optimism quantity; "null
distribution"; any claim that this reproduces, replaces or validates the retired Q3 numbers; any
statement that the diagnostic bears on whether treatment-effect heterogeneity exists.

## 7. Status of the R7 sequential cross-fold sensitivity — recorded here for the audit trail

The R7 sequential aggregation encountered a degenerate (constant) fold-2 rule in all six
configurations, and the handling — `t2 = 0` with the locked sqrt(K-1) denominator retained, plus a
secondary "restricted" aggregation — was decided **after** the degeneracy was observed. Both
variants are therefore **post hoc / exploratory**. The files are preserved for audit and are not
deleted. Neither p-value variant is used to support or refute Q1 in the manuscript. **The primary
independent held-out RATE analysis remains the inferential Q1 analysis.**

## 8. Stop conditions

Halt and report rather than continue if: the frozen R7 split or DR vector cannot be verified
against `FROZEN_R7/SHA256SUMS.txt`; `RATE(A_H2)` does not reproduce the frozen R7 Q1 values;
imaging enters either common evaluation score; anything under `R7_rate_primary/` or any
`FROZEN_*` set would be written; or any manuscript, figure or supplement file would be modified.
