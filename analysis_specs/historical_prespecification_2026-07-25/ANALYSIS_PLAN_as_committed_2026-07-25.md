# ANALYSIS_PLAN.md

**Manuscript:** JDIM-D-26-02440 (JIIM major revision) · **Deadline:** 2026-09-07
**Status:** ⚠️ **AMENDED DRAFT — NOT COMMITTED.** Awaiting final sign-off.
**Version:** v3, 2026-07-25 — incorporates *R1 Consolidated Sign-off* in full.

```
COMMIT HASH : __________________
COMMIT TIME : __________________  (UTC)
SIGNED OFF  : __________________
```

THIRD-PARTY TIMESTAMP : see `COMMIT_RECORD.md`

**Nothing is re-analysed until that commit exists.**

**Paths relocated 2026-07-25 [R1 §B1, §D]** — both project trees are now outside every cloud-sync
root, because folder synchronisation reverted the archive freeze three times:

| was | now |
|---|---|
| `~/<former-workspace>/` | **`~/JIIM_Revision/`** |
| `~/<former-archive>/` | **`~/研究保存用/RIC_Breast/`** |

Freeze verified by attempted write in the new location: create and delete both `Operation not
permitted`; 238/238 files verify against the manifest. Earlier documents in this workspace cite the
former paths; they are historical records and are not rewritten.

Authority: the *R1 Consolidated Sign-off* governs. Where it amends or overrides the Stage 0
document or the R0–R6 addendum, the R1 ruling stands. Changes in this version are marked **[R1 §n]**.

---

## 1. Estimand, cohorts, outcome

| item | value | verified |
|---|---|---|
| Estimand | CATE τ(x) = E[Y(1) − Y(0) \| X = x]; assignment to the **pooled** experimental arm |
| Outcome Y | pCR (ypT0/is ypN0), binary |
| Treatment T | `nac_agent != control`; control = `Paclitaxel` (HER2−, n=178) / `Paclitaxel + Trastuzumab` (HER2+, n=31) | ✅ |
| HER2− | n 739, control 178 / experimental 561, pCR 205 | ✅ Part 2b |
| HER2+ | n 241, control 31 / experimental 210, pCR 111 | ✅ Part 2b |
| Clinical covariates (p=5) | `age`, `tumor_subtype_enc`, `ethnicity_enc`, `bmi_group_enc`, `menopause_enc` | ✅ code |

**R6 correction:** the submitted Methods list "tumor subtype, HER2 status, age, ethnicity, menopausal
status". The code uses **BMI group**, not HER2 status; HER2 cannot be a covariate because the cohorts
are defined by it.

---

## 2. Results file and deposit **[R1 §2]**

R4 writes a **new canonical results file under a new, unambiguous name** — never `figure_data.json`.
**Neither** existing `figure_data.json` is deposited; both become historical artifacts. The deposit is
assembled **by explicit path, never by basename match**.

Recorded in the discrepancy ledger:

1. The canonical working tree holds the **superseded** (pre-Option-B) generation under the exact
   basename the manuscript promises to deposit. Assembling the deposit as the manuscript describes
   would have shipped a file contradicting every headline number.
2. The Methods sentence — all values "generated programmatically from the canonical analysis-results
   file (figure_data.json, deposited as Supplementary Material)" — is **false in the canonical tree**
   and must be rewritten in R6 to name the new file and describe what actually happened.

---

## 3. Evaluation regime — strict out-of-fold is primary

Per outer fold (K = 5), fit on training folds only, apply to the held-out fold only:
`StandardScaler` → `PCA` (transform-only on test) → both nuisance models → `CausalForestDML` →
`cf.effect(X_test)`. No patient's τ̂ is informed by their own outcome. AUTOC and Gap are computed once
on the assembled OOF vector. In-sample evaluation appears **only** as a labelled sensitivity analysis.

Reference implementation: `optionA/run_pca_in_fold_optionA.py::run_outer_cv` (lines 138–170), read and
confirmed leak-free. Its `OUTDIR` hazard was patched 2026-07-25.

Expected: HER2− principal AUTOC ≈ **0.1243**, not 0.4015.

---

## 4. Nuisance models and treatment handling **[R1 §5 — OVERRIDE]**

| | |
|---|---|
| **Primary** | `discrete_treatment=True` — classifier for ê(x) = P(T=1\|X), calibrated probabilities |
| **Prespecified sensitivity** | the **primary specification with `discrete_treatment=False` only** |

One additional main run per cohort. **No additional permutation cost** — permutation runs on the
primary only. This converts a documented defect into a robustness result.

**Exactly one factor changes between primary and sensitivity** [R1 §A2], so the comparison is
interpretable. The sensitivity is **not** "the archived configuration": the archive additionally used
`GradientBoostingRegressor(n_estimators=200, max_depth=3)` for both nuisances and in-sample
evaluation. **The archived configuration is not re-run** — R0 already reproduced it bit-for-bit
(AUTOC 0.401494354487434, |diff| = 0).

> The archive differs from the new primary in **three** respects — evaluation regime (in-sample vs
> strict OOF), nuisance model (gradient boosting vs random forest), and treatment handling
> (`discrete_treatment` False vs True). **No decomposition of those three is attempted.** The
> archived number is being **retracted, not explained.** Recorded in the ledger.

**(a) Nuisance specification — fixed, not tuned [R1 §A1]:**

| | m̂(x) = E[Y\|X] | ê(x) = P(T=1\|X) |
|---|---|---|
| estimator | `RandomForestRegressor` | `RandomForestClassifier` |
| `n_estimators` | 500 | 500 |
| `min_samples_leaf` | 5 | 5 |
| **`max_features`** | **`'sqrt'`** | **`'sqrt'`** |
| `random_state` | 42 | 42 |
| all other arguments | scikit-learn defaults | scikit-learn defaults |

**`max_features` is stated explicitly because the defaults differ between the two estimators.**
`RandomForestRegressor` defaults to `max_features=1.0` (all features) while `RandomForestClassifier`
defaults to `'sqrt'`; falling through to defaults would therefore give m̂ and ê *different*
hyperparameters — the opposite of "identical for both". With p up to 55 after PCA, √55 ≈ 7 gives
useful decorrelation in the nuisance stage, and it is already the conventional choice for one of the
two. This value appears in Methods, not merely in code.

**(b) I-SPY2 randomisation probabilities — NOT RECOVERABLE. The claim is deleted.**
All 50 columns of `clinical_and_imaging_info.xlsx` were checked: there is **no** arm-assignment
probability, propensity, or randomisation-weight field (zero matches for `prob|random|assign|arm|ps`),
and no CSV/JSON in the tree carries one. The dataset records only the assigned `nac_agent`. I-SPY2's
adaptive randomisation probabilities are time-varying and Bayesian-updated, published in aggregate
rather than per patient. → The Methods sentence *"the known propensity score from adaptive
randomization provided an additional advantage"* is **removed** in R6. ê(x) is estimated, not known.

**(c) Ê[T\|X] is NOT clipped to [0,1] under `discrete_treatment=False`.** Established by static
inspection of econml 0.16.0 (no model was fitted):
- `dml/causal_forest.py:78` — `VarT = np.clip(propensities*(1-propensities), 1e-2, inf)` sits inside
  `if self._discrete_treatment and self._drate:`, i.e. the **discrete path only**, and applies to the
  doubly-robust ATE, not to the CATE.
- `dml/dml.py:205` — `clipped_T_res = sign_T_res * np.clip(np.abs(T_res), 1e-5, inf)` floors the
  residual **magnitude** away from zero to avoid division by zero. It is not a [0,1] bound.

So a regressor on binary T can and does produce ê(x) outside [0,1], and econml applies no correction.
Under the primary (`discrete_treatment=True`) `predict_proba` is inherently in [0,1].

**Propensity / positivity diagnostics — reported for BOTH configurations [R1 §A3]:**

| diagnostic | purpose |
|---|---|
| min, max, and quantiles of ê(x) | distributional summary |
| proportion outside **[0, 1]** | structurally zero under `predict_proba` — so for the primary this is a **check that it behaves as expected**, and for the sensitivity it quantifies a real defect |
| **proportion outside [0.05, 0.95]** | **positivity / overlap** |

The last is not a formality. In HER2+, 31 controls out of 241 with `min_samples_leaf=5` can produce
leaves that are entirely treated, so `predict_proba` can return values at or near 1. That is a
**positivity failure, not a numerical nuisance**, and it is reported rather than clipped — a reviewer
will ask about overlap, and this answers the question before it is put.

Forest: `CausalForestDML(n_estimators=500, min_samples_leaf=20, random_state=42, cv=5)`.
PCA: 30 components for FM blocks, 20 for radiomics.
**R6 correction:** the Methods say **300 trees**; the code says 500, and 300 yields 0.3994.

---

## 5. Configurations

Six per cohort, on **identical fixed folds**: clinical only (p=5) · clinical + corrected radiomics ·
clinical + BiomedCLIP · clinical + RAD-DINO † · clinical + corrected radiomics + BiomedCLIP ·
clinical + corrected radiomics + RAD-DINO †  († only if RAD-DINO survives §8.)

---

## 6. Analysis hierarchy

| tier | content |
|---|---|
| **PRIMARY** | HER2− · clinical + corrected radiomics + BiomedCLIP · **AUTOC under strict OOF** · ΔAUTOC vs clinical-only |
| Secondary | remaining HER2− configurations; Gap; BLP |
| Exploratory | HER2+ cohort; encoder comparisons; agent-specific analyses |

"Prespecified" applies to this plan's contents once committed, and **never** retrospectively to the
submitted study.

---

## 7. Radiomics extraction **[R1 §3 — AMENDED]**

### 7.1 Why the original is discarded

`normalize=True, normalizeScale=1` then `binWidth=25` collapses the signal: **738/739** tumours fall
below one bin width; **0 of 739** land in the 30–130 reference band; 296/739 (40.05 %) are
single-grey-level.

### 7.2 Parameters — binCount **determined by the pre-fixed rule, not by preference**

The rule was fixed by R1 **before** the distribution was measured:

> Choose the largest binCount in {32, 64} for which at least 95 % of tumours have at least 10 voxels
> per bin. If 64 qualifies → primary 64, sensitivity 32. If only 32 → primary 32, sensitivity 64.
> If neither → stop and report.

**Measured** (`R2_features/roi_voxel_distribution.{py,json}`; 980 ROIs resampled to 1 mm isotropic,
nearest-neighbour, label 1; 0 errors; pure geometry, no outcome touched):

| cohort | n | median | IQR | min | max | ≥ 640 vox | ≥ 320 vox |
|---|---|---|---|---|---|---|---|
| HER2− | 739 | 11,559 | [6,076 – 22,836] | 819 | 587,422 | **100.00 %** | 100.00 % |
| HER2+ | 241 | 7,745 | [4,341 – 17,761] | 378 | 377,379 | **99.59 %** | 100.00 % |
| union | 980 | 10,649 | [5,561 – 21,824] | 378 | 587,422 | **99.90 %** | 100.00 % |

Proportion below each threshold (union): <320 = 0.00 %, <640 = 0.10 %, <1280 = 1.02 %, <2560 = 5.82 %.

**Rule outcome: binCount 64 qualifies** (99.90 % ≥ 640 voxels, against the 95 % requirement), and it
qualifies identically in HER2− alone (100 %), HER2+ alone (99.59 %) and the union. The median tumour
carries ≈ 166 voxels per bin at 64 bins — an order of magnitude above the requirement.

| parameter | **primary** | sensitivity |
|---|---|---|
| `binCount` | **64** *(by rule)* | **32** |
| `binWidth` | not used | not used |
| `normalize` | **False** | False |
| `resampledPixelSpacing` | **[1, 1, 1] mm**, B-spline (image); masks nearest-neighbour | same |
| scope | 3D (`force2D=False`) | same |

Extractor: pyradiomics **`3.1.1.dev111+g8ed579383`** — the exact git commit that produced the
archived features, so original-vs-corrected differences are attributable to parameters, not the tool.

### 7.3 QC acceptance criteria — outcome-blinded, fixed in advance

| # | metric | acceptance | original extraction |
|---|---|---|---|
| Q1 | median **effective (non-empty)** bins per tumour within [30, 130] | required | median 2 ❌ |
| Q2 | ≥ 90 % of tumours with **effective** bins in [16, 256] | required | 0 % ❌ |
| Q3 | proportion with **`abs(Entropy) < 1e-12`** ≤ 1 % | required | 40.05 % ❌ |
| Q4 | proportion with `GLCM JointEnergy == 1.0` ≤ 1 % | required | 40.05 % ❌ |
| Q5 | proportion with `firstorder Uniformity > 0.99` ≤ 5 % | required | 89.0 % ❌ |
| Q6 | zero/near-zero-variance texture features ≤ 5 % of 75 | required | 0 % whole-cohort |
| Q7 | extraction failures / NaN / Inf == 0 | required | 0 ✅ |
| Q8 | features with \|ρ\| > 0.9 vs `MeshVolume` reported, not excluded | disclosure | 4 at ≥ 0.80 |
| **Q9** | proportion of tumours with **< 10 voxels per bin** ≤ 5 % | required | **0.10 %** at 64 bins ✅ |

**Q1/Q2 count *effective non-empty* bins, not nominal `binCount`** [R1 §3]. Under FBN the nominal
count is `binCount` by construction, which would make both criteria vacuous; effective bins measure
something real — tumours with fewer distinct intensity values than `binCount` leave bins empty.

**Q3 must be coded `abs(Entropy) < 1e-12`, never `== 0`.** The equality test returns **zero** rows:
all 296 degenerate cases carry −3.203426503814917e-16. The same artefact affects
`glcm_JointEntropy`, `SumEntropy`, `DifferenceEntropy`.

**Gate G1.** Any required criterion failing → **stop and report**. Do not adjust binning to pass.
No selection among discretisations by downstream performance, without exception.

Both extractions are retained. The corrected one is written to a **new filename under
`JIIM_Revision/`** — never over `radiomics_all739.csv` (§12 H7).

---

## 8. Feature rebuild and RAD-DINO

Order fixed: **BiomedCLIP → radiomics → RAD-DINO.**

**8.1 BiomedCLIP (R2a, blocking).** `open_clip` (**not** transformers),
`hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224` @ `9f341de2…`, `encode_image` →
512-d, max-tumour-area axial slice, **whole-slice** min–max → uint8, grey→RGB,
Resize(224, bicubic) + CenterCrop(224) + CLIP mean/std. Re-extract to match **the code, not the
Methods** — the Supplement's "224×224 patch centered on the tumor" is false; the crop is image-centred
and segmentation only selects the slice index. Document the discrepancy.

**8.2 RAD-DINO reconstruction.** The `extract_raddino()` body and run log survive in
`R0_freeze_audit/recovered/terminal_output_20260207_ver2:6114-6187`: max-tumour-area slice,
whole-slice min–max → uint8, grey→RGB, `BitImageProcessor` (fast, default), **pooling = CLS token**
(`last_hidden_state[:,0,:]`, annotated in source), 768-d, `raddino_{j:03d}`, device `mps`, zero
failures. Only the two-line `from_pretrained` preamble is lost. **Test the CLS form first.**

**8.3 Reproduction tolerance — approved [R1 §8]:**

| criterion | threshold |
|---|---|
| median per-patient cosine(archived, re-extracted) | ≥ 0.99999 |
| **minimum** per-patient cosine, all 980 | ≥ 0.9999 |
| max abs element-wise difference | ≤ 1e-4 |
| Spearman ρ, first 30 PCA scores | ≥ 0.99 |
| \|ΔAUTOC\| downstream | ≤ 0.005 |

**Bit-level reproduction retroactively pins model identity** [R1 §8]. The lost preamble contains the
model identifier and revision, separately listed as a withdrawal trigger — but if a candidate preamble
reproduces the archived 739×769 matrix within tolerance, **no further provenance evidence is needed or
obtainable**, and that trigger is satisfied.

**Gate G2.** min cosine ≥ 0.9999 → retained. In [0.99, 0.9999) → retained only with the discrepancy
quantified and disclosed **and** the downstream ΔAUTOC check passing. Below 0.99, or no determinable
reconstruction → **dropped**; remove all RAD-DINO figures, tables and claims, restructure as a
BiomedCLIP-centred proof-of-concept. **Do not adopt a near-match. Do not improvise partial retention.**

---

## 9. HER2+ cohort — two-tier trigger **[R1 §9 — AMENDED]**

"Underpowered" and "unreliable" are different problems and are handled differently.

| trigger | consequence |
|---|---|
| **Bootstrap 95 % CI width for the HER2+ primary AUTOC > 0.40** | **Retained as a descriptive supplementary analysis only.** All inferential content removed: no p-values, no "significant", no encoder comparison, no directional claim. Point estimates and intervals may be shown, labelled as insufficiently precise to support inference. |
| **Provenance or reproduction failure** (RAD-DINO not reproduced, extraction indeterminate) | **Dropped entirely.** |
| Any reported quartile cell with control-arm n < 8 | that cell marked unstable; with 31 controls quartiles average ≈ 7.75, so this is expected to fire |

The width criterion is a **precision** bound, independent of the effect's direction, so it cannot be
gamed by the result.

**Stated as an expectation, not discovered as a surprise:** the archived HER2+ principal bootstrap CI
is [0.113, 0.544], width **0.431** — already past the 0.40 bound. With n = 241 and 31 controls the
rebuild is unlikely to narrow it materially, so **this criterion is expected to fire**, and HER2+ is
expected to become descriptive-only. Deleting an honestly-reported underpowered analysis would discard
information the field can use; reporting it without inference is more honest and more useful.

---

## 10. Permutation testing **[R1 §4 — REPLACED: sequential Monte Carlo]**

**Primary comparison — Besag–Clifford sequential Monte Carlo:**

- draw permutations until **h = 20 exceedances**, or **n_max = 10,000**, whichever comes first
- p = **h / n** at stopping
- if n_max is reached without h exceedances, p = **(1 + exceedances) / (1 + n_max)**
- **retain all null draws regardless of stopping point**

**Secondary comparisons:** flat **2,000**, resolution floor **p ≥ 4.998e-04** (= 1/2001).
**Purely descriptive configurations:** no permutation — AUTOC + 95 % CI + paired differences suffice.

Per iteration i: `RandomState(42 + i)`; permute **T only** (Y and X untouched, (X,Y) pairing
preserved); **re-stratify** folds on `2·T_perm + Y`; **re-fit scaler + PCA per fold**; re-fit both
nuisances and the forest per fold; predict OOF CATE; score AUTOC against `T_perm`.
**Each permutation refits the full pipeline including the PCA stage** — the previous implementation
froze `X`, so it never tested the representation.

Rationale: if the observed statistic is unremarkable — the likely case under strict OOF — exceedances
accumulate fast and the run stops after a few hundred iterations. If it is extreme, the procedure
spends the full budget, which is exactly when the precision matters. Valid either way; the stopping
rule is fixed in advance.

**R3 must report the expected wall-clock under this design alongside the flat-10,000 figure.**

**Fallback, pre-specified:** if even this busts the schedule, the answer is an **extension request,
not a reduced primary budget.** Decided now; not revisited when results are in view. Reducing the
primary after criticising the previous run for being 1,000-while-described-as-10,000 would be
indefensible whatever its statistical merits.

---

## 11. Inference **[R1 §6]**

**Bootstrap — evaluation-only is primary.** B = **2,000**, stratified by treatment arm, **identical
resample indices across all configurations** so differences are paired. Computed: per-configuration
AUTOC; ΔAUTOC for principal − clinical-only (primary) and principal − (clinical + radiomics); the same
for Gap and top/bottom quartile effects. Percentile CI, BCa alongside where straightforward;
two-sided bootstrap p = 2·min(P(Δ* ≤ 0), P(Δ* ≥ 0)).

Full-refit bootstrap is 2,000 × a complete pipeline fit per configuration per cohort and is not
expected to be feasible. If R3 shows otherwise it may be **added** as a bonus sensitivity; **the
primary does not change.**

**Caveat text — fixed now, to appear verbatim in Methods and again at the first reported interval:**

> This procedure resamples the evaluation while holding the fitted CATE predictions fixed; it
> therefore characterises evaluation uncertainty and not uncertainty arising from model fitting.

**BLP.** OLS of Y − m̂(X) on (T − ê(X)) and (T − ê(X))·(τ̂(X) − E[τ̂(X)]), HC1 robust SE, τ̂ from the
**strict-OOF** vector. Report θ₂ with CI and p. The submitted BLP p = 3.5e-44 is anti-conservative;
the permutation-based p is the one to report.

**Confidence intervals are reported for every performance metric, without exception.**

---

## 12. Seeds, folds, and write discipline

| seed | value | scope |
|---|---|---|
| `SEED` | 42 | outer `StratifiedKFold`, `PCA`, both nuisance models, `CausalForestDML` |
| permutation | `42 + i` | `RandomState` per iteration |
| bootstrap | 20260725 | resample index generation |

**Fold assignment is computed once and saved to disk** as an explicit index array
(`StratifiedKFold(5, shuffle=True, random_state=42)` on `2·T + Y`), then **loaded** by every
configuration, so all configurations are evaluated on identical, auditable splits. Under permutation
folds are re-stratified on `2·T_perm + Y`.

**Stratification on `2·T + Y` — approved [R1 §7].** Justification to appear in Methods: with 31
controls in HER2+, stratifying on treatment alone risks folds containing no control-arm events. It is
standard stratified cross-validation with no individual-level leakage, **but fold composition
therefore depends on the outcome** — stated by us rather than discovered by a reviewer.

**Write discipline [R1 §11].** Before any extraction: the cohort is defined **explicitly from the
canonical patient-ID list**, never from directory state, and all output goes to **new filenames under
`JIIM_Revision/`**. Confirmed in the R2 return block. None of these may run unmodified:
`radiomics_all.py`, `extract_embeddings.py` (cohort by `os.listdir`, write back to archived names);
`save_patient_ids.py` (writes into the frozen T2 `artifacts/`);
`recalculate_autoc_unified.py`, `save_figure_data.py`, `bootstrap_agent_ci.py` (overwrite
`figure_data.json` in place — why both canonical JSONs are now `a-w`).

Every result file records the environment, the plan commit hash, and the seeds.

---

## 13. Open sign-off points

All eight points from v2 are now resolved by the R1 rulings. Three items remain, none blocking R2a.

| # | § | item | status |
|---|---|---|---|
| 1 | 7.2 | Radiomics binning | ✅ **RESOLVED by rule** — primary `binCount=64`, sensitivity 32, `normalize=False`, 1 mm isotropic. Measured, not chosen. |
| 2 | 7.3 | QC thresholds Q1–Q9 | ✅ **RESOLVED** — Q1/Q2 redefined to effective non-empty bins; Q3 as `abs()<1e-12`; Q9 added |
| 3 | 8.3 | RAD-DINO tolerance | ✅ **RESOLVED** — approved as proposed, plus the bit-reproduction-pins-identity clarification |
| 4 | 9 | HER2+ trigger | ✅ **RESOLVED** — two-tier: width > 0.40 → descriptive-only; provenance failure → dropped |
| 5 | 10 | Permutation budget | ✅ **RESOLVED** — Besag–Clifford SMC, h=20 / n_max=10,000; fallback is an extension request |
| 6 | 11 | Bootstrap | ✅ **RESOLVED** — evaluation-only primary, caveat text fixed verbatim |
| 7 | 12 | Fold stratification | ✅ **RESOLVED** — keep `2·T+Y`, documented with justification |
| 8 | 4 | `discrete_treatment` | ✅ **RESOLVED by override** — `True` primary, `False` prespecified sensitivity |
| **A** | 4(a) | Nuisance hyperparameters | ✅ **RESOLVED [R1 §A1–A3]** — RF regressor/classifier, `n_estimators=500`, `min_samples_leaf=5`, **`max_features='sqrt'` for both** (defaults differ between the two estimators), `random_state=42`. Sensitivity isolates `discrete_treatment` only; archive not re-run. ê(x) diagnostics for both configurations including the proportion outside [0.05, 0.95]. |
| **B** | — | Version control and third-party timestamp | ✅ **RESOLVED [R1 §B1–B2]** — repository at `~/JIIM_Revision/` (outside every sync root), snapshots excluded via `.gitignore`; commit hash, UTC time and third-party timestamp recorded in the header above. |
| **C** | 9 | **HER2+ CI width is measured on the archived (in-sample) run.** The 0.431 figure comes from the Option-B bootstrap. The strict-OOF CI will differ and is not yet known. The 0.40 threshold is retained as fixed; noting only that the *expectation* it fires rests on an in-sample precedent. | ⬜ informational |

---

## 14. Deviations

Any departure after commit requires sign-off and a `DECISION_LOG.md` entry recording what changed,
why, when, and what it would otherwise have been. **Selecting among discretisations, seeds or
configurations by downstream performance is prohibited.**
