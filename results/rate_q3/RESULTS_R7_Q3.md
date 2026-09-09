# R7-Q3 — corrected evaluation-induced-optimism diagnostic under standard RATE/AUTOC

**Manuscript:** JDIM-D-26-02440 · **Amendment:** `AMENDMENT_R7_Q3.md`, committed **before
execution** at `709a9c39`, sha256 `769670d3…72edf`.
**Descriptive point-estimate diagnostic. No p-value, no confidence interval, no null distribution.
Not a test of treatment-effect heterogeneity. Not a recovery of the retired Q3.**

## Design executed

| | rule fitted on | priorities predicted on | preprocessing fitted on | evaluation score |
|---|---|---|---|---|
| A_H2 (honest) | H1 (n=370) | H2 (n=369) | H1 | frozen R7 H2 DR vector, reused byte-for-byte |
| C_H2 (apparent) | H2 | H2 | H2 | the same frozen H2 DR vector |
| A_H1 (honest) | H2 | H1 | H2 | new common H1 DR vector, same locked spec |
| C_H1 (apparent) | H1 | H1 | H1 | the same H1 DR vector |

H1 and H2 are the frozen R7 50/50 halves, reused verbatim; no new split was drawn. Within each
half the two rules are scored against an **identical** DR vector, so A and C differ **only** in the
ranking. `A_H2` is the frozen R7 priority set, not a refit.

**H1 evaluation forest overlap:** ê ∈ [0.5861, 0.8586], 0 % outside [0.05, 0.95] and [0.01, 0.99].
**Run check:** `RATE(A_H2)` reproduces the frozen R7 Q1 estimates to **3.4 × 10⁻¹⁴** (max over the
six configurations) — floating-point identical.

## Results

| Configuration | A_H1 | C_H1 | C−A H1 | A_H2 | C_H2 | C−A H2 | pooled C−A |
|---|---:|---:|---:|---:|---:|---:|---:|
| Clinical only | +0.0514 | +0.0965 | +0.0451 | −0.0668 | +0.2024 | +0.2692 | **+0.1570** |
| Clinical + radiomics | +0.1098 | +0.2270 | +0.1171 | −0.0454 | +0.2578 | +0.3032 | **+0.2101** |
| Clinical + BiomedCLIP | +0.0984 | +0.2702 | +0.1718 | +0.0975 | +0.2949 | +0.1974 | **+0.1846** |
| Clinical + RAD-DINO | +0.0569 | +0.2127 | +0.1558 | −0.1088 | +0.2941 | +0.4029 | **+0.2792** |
| Clinical + radiomics + BiomedCLIP *(historically designated reference configuration)* | +0.1023 | +0.3058 | +0.2034 | +0.0464 | +0.2971 | +0.2508 | **+0.2271** |
| Clinical + radiomics + RAD-DINO | +0.1062 | +0.2601 | +0.1539 | −0.0591 | +0.2774 | +0.3365 | **+0.2451** |
`optimism = RATE(C) − RATE(A)`; `pooled = (370·optimism_H1 + 369·optimism_H2)/739`, the weighting
predeclared in the amendment before any of it was computed.

### Held-out uncertainty for the honest rates only

The SEs below are ordinary grf half-sample bootstrap SEs (R = 2000, seed 20260906) for the
**honest A rates**, which are legitimate held-out RATE estimates. **No SE, CI or p-value is given
for C, for C − A, or for the pooled contrast**, because C is deliberately fitted on the same
outcomes and treatment labels it is evaluated against, and grf's SE assumes an independently
trained rule.

| Configuration | A_H1 | held-out SE | A_H2 | held-out SE |
|---|---:|---:|---:|---:|
| Clinical only | +0.0514 | 0.0529 | −0.0668 | 0.0542 |
| Clinical + radiomics | +0.1098 | 0.0455 | −0.0454 | 0.0560 |
| Clinical + BiomedCLIP | +0.0984 | 0.0447 | +0.0975 | 0.0407 |
| Clinical + RAD-DINO | +0.0569 | 0.0487 | −0.1088 | 0.0557 |
| Clinical + radiomics + BiomedCLIP | +0.1023 | 0.0447 | +0.0464 | 0.0412 |
| Clinical + radiomics + RAD-DINO | +0.1062 | 0.0438 | −0.0591 | 0.0610 |
## Readout

- **Range of pooled C − A across configurations:** +0.1570 to +0.2792.
- **Configurations with pooled C − A > 0:** **6 of 6**.
- **Both half-specific C − A values positive:** **6 of 6** (12 of 12 individual values positive).
- **Historically designated reference configuration:** pooled +0.2271, inside the range spanned by
  the other five (+0.1570 to +0.2792) and neither the largest nor the smallest. It behaves like the
  others.

**Same-sample evaluation increased the RATE point estimate** in every configuration and in both
directions of the split. The increase is of the same order as, and in several configurations
larger than, any of the honest RATE estimates themselves: the apparent values cluster at +0.10 to
+0.31 while the honest values span −0.11 to +0.11.

Two features of the table are worth recording without over-reading them:

1. **The apparent (C) estimates are far more alike across configurations than the honest (A)
   estimates.** C_H2 spans +0.2024 to +0.2971 and C_H1 spans +0.0965 to +0.3058, whereas the
   honest estimates span −0.1088 to +0.1098. Under same-sample evaluation the six configurations
   become hard to tell apart, which is what one would expect if the apparent value is dominated by
   the rule's ability to fit its own evaluation data rather than by any transportable ranking
   signal.
2. **The honest estimates are not stable across the two directions.** Every A_H1 value is positive
   (+0.0514 to +0.1098) while four of the six A_H2 values are negative. The two halves are
   independent draws of 370 and 369 patients from the same cohort, so this is sampling variability
   at this sample size, and it reinforces the R7 finding that configuration-level RATE estimates
   are unstable here (consistent with the previously recorded decision D45a). It is also the
   reason the diagnostic was run in both directions rather than only in the direction the R7 split
   happened to label "evaluation".

## Not claimed

No significance is attached to any optimism quantity. Nothing here bears on whether
treatment-effect heterogeneity exists, on Q1, or on Q2. The retired Q3 numbers (+0.0992 to +0.2482
observed optimism; +0.1428 to +0.3173 permutation-null shift) were computed with the uncentred
`autoc()` statistic against a treatment-label null that tested no-treatment-effect; they are not
comparable to anything in this table and are not restored by it.
