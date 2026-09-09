# R7 — standard centred, doubly robust RATE/AUTOC: Q1 and Q2

**Manuscript:** JDIM-D-26-02440 · **Scope:** Q1 and Q2 only. Corrected Q3 and Q4 deferred.
**Amendment:** `AMENDMENT_R7_RATE.md`, committed **before execution** at
`755aecb2525365e18c7224d509dd03e12a944ac6`, sha256 `2c4fafd0…b0d13a`.
**Metric:** `grf::rank_average_treatment_effect`, `target = "AUTOC"`, grf 2.6.1.
**No result below is comparable to the retired uncentred `autoc()` statistic.**

---

## 0. Design actually executed

| item | value |
|---|---|
| population | HER2-negative **n = 739** (Q1 re-based from 693; the 693 overlap restriction existed only to enable label permutation) |
| split | plain random 50/50, `numpy.random.default_rng(42).permutation`, **Y not used, T not used, no stratification**; **train 370 / evaluation 369**; not re-drawn or adjusted after inspection |
| priorities | six configurations fitted on the **training half only**; clinical scaler, imaging scaler and PCA all fitted on the training half only; one CATE priority predicted per evaluation patient |
| evaluation score | **one common** AIPW score from `causal_forest(X = Z, Y, W = T, num.trees = 2000, seed = 42)` fitted on the **evaluation half only**, `get_scores()`; identical vector for all six rules, so comparisons differ **only** in the ranking |
| Z (imaging-free) | age (+ missingness indicator), hr, mammaprint, ethnicity, bmi_group, menopause (two whitespace-variant "pre" levels merged **in Z only**), enrolment-epoch dummies from a fixed 22-level basis → **40 columns** on the primary evaluation half (levels absent from that half are dropped and listed in `Z_provenance.json`; 39 columns on the empty-arm subset, 34–40 across the sequential folds). **Excluded:** `tumor_subtype` (exactly collinear with `hr`: luminal_a↔hr=1 n=381, triple_negative↔hr=0 n=358, zero off-diagonal), `her2` (constant), radiomics, BiomedCLIP, RAD-DINO |
| uncertainty | grf **half-sample bootstrap** (`boot_grf(half.sample = TRUE)`: ⌊n/2⌋ patients drawn without replacement), **R = 2000**, seed 20260906; SE = sd across replicates; CI = est ± 1.96·SE; p = 2Φ(−\|est/SE\|) |
| multiplicity | Holm across the six Q1 tests. **None** for the single Q2 primary contrast |

**Overlap on the evaluation half:** estimated ê ∈ **[0.5498, 0.8634]**, quantiles (5/25/50/75/95) =
0.688 / 0.758 / 0.785 / 0.815 / 0.846; **0 %** outside [0.05, 0.95] and outside [0.01, 0.99].
This is an **estimated observed treatment-assignment mechanism conditional on the available design
and baseline covariates**, not a reconstruction of the unavailable I-SPY2 randomization probabilities.

**Stop-rule verification (re-run after all results):** the split is reproducible from the seed alone and its constructor references neither Y nor T; train and evaluation patient sets are disjoint; Z contains no radiomics, BiomedCLIP, RAD-DINO or `tumor_subtype` column; one DR-score vector is shared by all six rules; the retired `autoc()` is not computed anywhere in R7; all frozen sets re-verified intact after the run (FROZEN_R4 34/34, FROZEN_EVALBIAS 15/15, FROZEN_DECOMP 19/19, Linux 2×2 freeze 31/31, 0 FAILED); no file outside `R7_rate_primary/` was created or modified.

**Interface check:** `rank_average_treatment_effect(forest, …)` vs
`rank_average_treatment_effect.fit(get_scores(forest), …)` agree to **3.5 × 10⁻¹⁶**.

---

## Q1 PRIMARY — independent held-out evaluation (n = 369)

| Configuration | RATE/AUTOC | SE | 95 % CI | raw p | Holm p |
|---|---:|---:|---|---:|---:|
| Clinical only | −0.0668 | 0.0542 | −0.1731 to +0.0395 | .218 | .873 |
| Clinical + radiomics | −0.0454 | 0.0560 | −0.1551 to +0.0644 | .418 | .873 |
| Clinical + BiomedCLIP | **+0.0975** | 0.0407 | +0.0178 to +0.1773 | **.0165** | .099 |
| Clinical + RAD-DINO | −0.1088 | 0.0557 | −0.2179 to +0.0003 | .0506 | .253 |
| Clinical + radiomics + BiomedCLIP *(historically designated reference configuration)* | +0.0464 | 0.0412 | −0.0345 to +0.1272 | .261 | .873 |
| Clinical + radiomics + RAD-DINO | −0.0591 | 0.0610 | −0.1787 to +0.0605 | .333 | .873 |

**No configuration reaches significance after Holm adjustment.** The old treatment-label
permutation p-values are not used and are not carried forward.

## Q2 PRIMARY — paired incremental comparison (same 369 patients, same DR scores)

| Comparison | ΔRATE | paired SE | 95 % CI | p |
|---|---:|---:|---|---:|
| historically designated reference configuration − clinical only | **+0.1132** | 0.0737 | **−0.0314 to +0.2577** | **.125** |

Component estimates from the same paired call: reference +0.0464 (SE 0.0412), clinical only
−0.0668 (SE 0.0542). Paired SE via grf's two-priority interface, which shares the bootstrap draws
across the two rules (`"In case of two priorities do a paired bootstrap estimating both prios on
same sample"`).

**The sign is opposite to the retired uncentred contrast (−0.0289).** That was anticipated: near
invariance of the old Δ to ATE centering said nothing about invariance to replacing raw prefix arm
means with doubly robust scores. **Neither result demonstrates an incremental effect.**

## Q2 SENSITIVITIES — same fixed split; p values secondary and unadjusted

| Sensitivity | n eval | Comparison (direction as written) | ΔRATE | SE | 95 % CI | p |
|---|---:|---|---:|---:|---|---:|
| MammaPrint-expanded baseline | 369 | (reference + MammaPrint) − (clinical + MammaPrint) | +0.1332 | 0.0940 | −0.0511 to +0.3174 | .157 |
| no-epoch CATE | 369 | reference − clinical only | +0.1067 | 0.0741 | −0.0385 to +0.2520 | .150 |
| alternative treatment-nuisance CATE | 369 | reference − clinical only | +0.1216 | 0.0820 | −0.0391 to +0.2824 | .138 |
| empty-arm exclusion (n = 728) | 366 | reference − clinical only | +0.0424 | 0.0817 | −0.1177 to +0.2026 | .603 |

Component estimates: MammaPrint +0.0669 / −0.0663; no-epoch +0.0453 / −0.0615; alt-nuisance
+0.0673 / −0.0543; empty-arm +0.0226 / −0.0199. All four point in the same (positive) direction as
the primary contrast; all four intervals cover zero. The empty-arm row is markedly attenuated.

**HER2-positive (n = 241): `NOT ESTIMATED FOR INFERENCE`.** The population contains 31 controls in
total; the independent split leaves 15 in the training half and 16 in the evaluation half, too few
for a stable evaluation forest or a stable RATE. No model was fitted and no p-value was produced.
Exploratory/descriptive status unchanged (D53). Recorded in `rate_her2pos_not_estimated.json`.

## Q1 SEQUENTIAL SENSITIVITY — new Y-independent random 5-fold partition, seed 42

For k = 2…5 the rule is fitted on folds 1…k−1 and evaluated on fold k; DR scores come from a
causal forest on fold k alone. Aggregation `z = Σ t_k / √(K−1)`, K = 5, then Holm across six.

| Configuration | fold t-statistics (k = 2,3,4,5) | z | raw p | Holm p | restricted z (k=3 folds) | restricted Holm |
|---|---|---:|---:|---:|---:|---:|
| Clinical only | 0.00\*, +1.04, +1.50, +0.97 | +1.752 | .080 | .319 | +2.024 | .172 |
| Clinical + radiomics | 0.00\*, −1.21, +0.25, +1.65 | +0.344 | .731 | 1.00 | +0.397 | 1.00 |
| Clinical + BiomedCLIP | 0.00\*, +0.20, +2.04, +2.48 | **+2.359** | **.0183** | .110 | +2.724 | **.039** |
| Clinical + RAD-DINO | 0.00\*, −0.29, +1.36, −0.60 | +0.239 | .811 | 1.00 | +0.277 | 1.00 |
| Clinical + radiomics + BiomedCLIP | 0.00\*, +0.47, +0.70, +2.79 | +1.977 | .048 | .240 | +2.283 | .112 |
| Clinical + radiomics + RAD-DINO | 0.00\*, −1.24, +2.37, +1.10 | +1.118 | .264 | .791 | +1.291 | .590 |

**\* Fold 2 is degenerate and this was not anticipated.** Its rule is trained on fold 1 alone
(n = 148, 41 controls), and under the frozen hyperparameters
(`CausalForestDML(n_estimators=500, min_samples_leaf=20, cv=5)`) the fitted effect function is
**exactly constant** — one unique predicted value for all 148 evaluation patients, in all six
configurations. A constant rule has RATE identically 0 with no ranking variability; grf returns
estimate 0 and std.err 0, so the t-statistic is 0/0. **It is encoded as t₂ = 0 (zero evidence)
while the locked √(K−1) = 2 denominator is retained**, which dilutes the aggregate and is
therefore conservative. The `restricted` columns instead divide by √3, the number of
non-degenerate folds; they are reported alongside and are **secondary**. This handling rule was
fixed after observing the degeneracy and is recorded here for that reason.

## Implementation cross-check

| Configuration | grf 2.6.1 | direct re-implementation | \|diff\| | econml `calc_uplift(metric="toc")` |
|---|---:|---:|---:|---:|
| Clinical only | −0.06679 | −0.06679 | 4.5e−15 | −0.04040 |
| Clinical + radiomics | −0.04539 | −0.04539 | 1.8e−15 | −0.04668 |
| Clinical + BiomedCLIP | +0.09753 | +0.09753 | 2.3e−15 | +0.10243 |
| Clinical + RAD-DINO | −0.10879 | −0.10879 | 3.4e−14 | −0.09313 |
| Clinical + radiomics + BiomedCLIP | +0.04637 | +0.04637 | 1.9e−15 | +0.03364 |
| Clinical + radiomics + RAD-DINO | −0.05912 | −0.05912 | 5.4e−15 | −0.05129 |

An independent Python re-implementation of grf's exact definition (rank descending, average DR
scores within tied groups, `TOC = cummean(Γ) − ATE`, `RATE = mean(TOC)` over all n increments)
reproduces grf to ≤ 3.4 × 10⁻¹⁴ on all six. econml agrees in **sign on 6/6** and reproduces the
top-two and bottom-one ordering; ranks 3–5 permute among three configurations whose grf values lie
within 0.02 of one another. That is expected: econml integrates a 50-point left-Riemann sum
truncated to q ∈ [0.05, 0.95], grf integrates all n increments over q ∈ (0, 1]. **Different
estimands; sign / ordering / gross-error check only, as pre-declared.**

---

# Interpretation

### Q1 — evidence of treatment-effect prioritization / heterogeneity
**Supported in NONE of the six configurations.** No configuration survives Holm adjustment in the
primary held-out analysis (smallest Holm p = .099, clinical + BiomedCLIP) or in the locked
sequential sensitivity (smallest Holm p = .110, the same configuration). Clinical + BiomedCLIP is
the only configuration with a raw p < .05 in either analysis, and it reaches Holm significance
only in the secondary restricted sequential aggregation (Holm p = .039), which is not the locked
primary rule. **This is a failure to demonstrate, not a demonstration of absence:** no equivalence
margin was defined, the evaluation half contains 81 controls, and the design is underpowered.

### Q2 — incremental value of the historically designated reference configuration beyond clinical variables
**NOT DEMONSTRATED.** ΔRATE = +0.1132 (95 % CI −0.0314 to +0.2577; p = .125). All four
sensitivities agree in direction and all cover zero. The interval spans zero, so this is failure to
demonstrate an incremental difference — **not** equivalence, and **not** evidence that imaging
carries no treatment-effect information. Note that the point estimate is now **positive**, whereas
the retired uncentred statistic gave −0.0289; the manuscript's previous negative point estimate
cannot be carried into the corrected framework in either magnitude or sign.

### Stability — primary held-out vs sequential sensitivity
**PARTIALLY CONCORDANT.** Concordant on what matters: both rank clinical + BiomedCLIP first, and
under both, nothing survives multiplicity adjustment. Discordant on individual configurations —
most visibly clinical only, which is **−0.0668 (p = .218)** in the held-out analysis but has
positive t-statistics in all three non-degenerate sequential folds (z = +1.75). The two analyses
use different partitions and different amounts of training data, and the degenerate first
sequential fold removes a quarter of that design's intended evidence. Configuration-level RATE
estimates should therefore be treated as unstable at this sample size, consistent with the
already-recorded decision D45a.

### Carried forward unchanged
No claim of configuration superiority. No relative-improvement figure. No equivalence claim. The
old permutation p-values are retired as ranking evidence. Configuration 5 is named only as the
*historically designated reference configuration*.
