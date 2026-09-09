# Amendment R7-Q4 — corrected preprocessing-placement diagnostic under standard RATE/AUTOC

**Manuscript:** JDIM-D-26-02440
**Status:** protocol-locked post-audit. **Not prespecified.** Committed and hashed **before any
model was fitted.** Outputs to `R7_rate_q4/` only.
**`R7_rate_primary/`, `R7_rate_q3/` and every `FROZEN_*` set are INPUT ONLY.**
**Instruction of record:** `~/Downloads/JIIM_CC_R7_Corrected_Q4_Observed_Preprocessing_Diagnostic.md`
**Predecessors:** R7 amendment `755aecb2` / results `2e87fa6f`; Q3 amendment `709a9c39` / results `54881e3a`.

---

## 1. The question, narrowed

> How much does allowing evaluation-patient information into **unsupervised preprocessing alone**
> change the standard RATE/AUTOC point estimate, while the treatment-prioritization model itself
> stays trained on the opposite half?

This is a **descriptive preprocessing-leakage diagnostic on observed data**. It is not a test of
anything, and it produces no confirmatory p-value.

## 2. What is retired and not reproduced

The old Q4 2×2 analysis measured the **variance of an uncentred bespoke statistic across 2,000
within-stratum treatment-label permutations**, and reported log-variance main effects exponentiated
into ratios (P 1.047–1.083 etc., Fig. 5B). That statistic, that null and those ratios are retired.
Nothing here reproduces, relabels or approximates them, and the 2,000-draw permutation architecture
is not rerun.

Three quantities must not be conflated, and only the third is computed here:

| quantity | what it is | status |
|---|---|---|
| null-distribution variance | spread of a statistic across permuted-label draws | retired with the old Q4 |
| sampling standard error | uncertainty of an observed estimate under resampling | not the object of this task |
| **change in the observed RATE point estimate under a preprocessing-placement change** | an additive contrast between two observed point estimates | **this task** |

## 3. Population, split and directions

HER2-negative n = 739, and the **frozen R7 50/50 split reused verbatim**:
**H1** = R7 training half (n = 370), **H2** = R7 evaluation half (n = 369). No new split is drawn.

The diagnostic is run **symmetrically in both directions**. For each evaluation half, the causal
forest is trained on the **opposite half only**. Model fitting is honest in every regime; only
preprocessing placement is manipulated.

## 4. The four regimes

| regime | imaging block (scaler + PCA) | clinical scaler | causal forest | evaluated on |
|---|---|---|---|---|
| **A** | training half | training half | training half | held-out half |
| **D1** | **full n = 739** | training half | training half | held-out half |
| **D2** | training half | **full n = 739** | training half | held-out half |
| **B** | **full n = 739** | **full n = 739** | training half | held-out half |

**Binding:** held-out outcomes `Y` and treatment labels `T` never enter causal-forest fitting in any
regime. Only unsupervised preprocessing is allowed to see evaluation-half covariates. Model
hyperparameters, seeds and feature definitions are the frozen R4 ones, unchanged.

**Factor P is the entire imaging-block preprocessing placement — scaling *and* PCA together.** They
are implementationally inseparable (the PCA is fitted on the imaging scaler's output), and P must
never be described as "PCA placement".

**Clinical only:** factor P is structurally absent, so D1 must equal A and B must equal D2
identically. Both identities are computed and reported **as control checks**; pooled P and pooled
P×S are reported as structural **N/A** and are never manufactured.

**Run checks:** `A` evaluated on H2 must reproduce the frozen R7 primary priorities and RATEs
exactly, and `A` evaluated on H1 must reproduce the frozen Q3 `A_H1` RATEs exactly. Both identities
are asserted.

## 5. Evaluation scores — reused, not rebuilt

- **H2:** the frozen R7 DR vector, `R7_rate_primary/FROZEN_R7/dr_scores_primary_heldout.csv`,
  reused byte-for-byte.
- **H1:** the frozen corrected-Q3 DR vector, `R7_rate_q3/FROZEN_R7Q3/dr_scores_H1.csv`, reused
  byte-for-byte.

Both are **configuration-independent and imaging-free** by construction. Hashes are verified before
use. No configuration-specific evaluation score is permitted anywhere in Q4.

## 6. Estimands — additive point-estimate contrasts

Per configuration and per evaluation half:

```
P_effect_half = 0.5 * [ (D1 - A) + (B - D2) ]
S_effect_half = 0.5 * [ (D2 - A) + (B - D1) ]
PS_half       = (B - D2) - (D1 - A)
Total_half    = B - A
```

pooled descriptively by evaluation-half size:

```
pooled_effect = ( 370 * effect_H1 + 369 * effect_H2 ) / 739
```

These are **additive contrasts between RATE point estimates**. They are **not** variance ratios,
are **not** exponentiated, and are **not** causal effects.

## 7. Uncertainty

Ordinary grf half-sample bootstrap SEs are **stored for reference only** and must not be used to
claim that any A-versus-D1/D2/B difference is statistically supported. The leakage regimes
deliberately use evaluation-half covariates during preprocessing, so grf's SE does not describe
the sampling behaviour of those regimes, and no confirmatory p-value is attached to any Q4
quantity.

## 8. Relation to corrected Q3 — descriptive only

Q3 measured same-sample **model development and evaluation** reuse. Q4 measures evaluation-patient
leakage through **unsupervised preprocessing** while model fitting stays honest. Different
quantities on different paths. The ratio

```
preprocessing_fraction_of_Q3 = |Q4 pooled (B - A)| / |Q3 pooled (C - A)|
```

is reported only to say whether preprocessing leakage is small, similar or large relative to the
total same-sample reuse effect. **It is not a decomposition**, and no percentage-of-optimism claim
may be built on it.

## 9. Permitted and prohibited wording — binding

**Permitted:** *full-sample imaging preprocessing changed the RATE point estimate by …* ·
*clinical-scaler placement had little apparent effect* · *the preprocessing-only change was small
relative to the total same-sample evaluation increase* · *the direction was inconsistent across
split halves*.

**Prohibited:** "significant" · any `p < …` attached to a Q4 quantity · "caused" · "accounted for
X % of optimism" · "conservative" · "null variance" · "variance ratio" · "PCA caused the optimism"
· "preprocessing was harmless".

## 10. Stop conditions

Halt and report rather than continue if: the frozen split or either DR vector fails its hash check;
regime A fails to reproduce the frozen R7 / Q3 values; held-out `Y` or `T` reaches a causal-forest
fit; a configuration-specific or imaging-containing evaluation score is used; anything under
`R7_rate_primary/`, `R7_rate_q3/` or any `FROZEN_*` set would be written; or any manuscript, figure
or supplement file would be modified.
