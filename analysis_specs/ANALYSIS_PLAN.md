# ANALYSIS_PLAN.md

**Manuscript:** JDIM-D-26-02440 (JIIM major revision) · **Deadline:** 2026-09-07
**Status:** ✅ **COMMITTED AND TIMESTAMPED — this is the pre-specification of record.**
**Version:** v4, 2026-07-25 — incorporates *R1 Consolidated Sign-off* and *R1 Final Approval* in full.

```
COMMIT HASH           : bb70d54a7511d552374e6e1b6af1a989ff2a69a0
COMMIT TIME           : 2026-07-25T01:14:41Z  (UTC)
TREE HASH             : 5d8da7e8cf810896206da0abdc719b25c87621a3
PLAN sha256 AS COMMITTED: 87a2da6275033531449a8d668865f2d02916eee5f11cdd96cee2703c9cfea2d7
THIRD-PARTY TIMESTAMP : OpenTimestamps, PRESPEC_STAMP.txt.ots (4 calendars, pending Bitcoin confirmation)
SIGNED OFF            : R1 Final Approval, 2026-07-25
```

The header at commit `bb70d54` necessarily carries blank hash fields — a commit cannot contain its
own hash. **`bb70d54` is the authoritative pre-specification;** this filled-in header is a later
commit pointing back to it. Full chain of evidence in `COMMIT_RECORD.md`.

**No rebuilt analysis had been run at that commit.** R2 may now begin.

**Paths relocated 2026-07-25 [R1 §B1, §D]** — both project trees were moved outside every cloud-sync
root, because folder synchronisation reverted the archive freeze three times. (The table of local
directory paths is omitted from this public copy.)

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
| **Primary** | `discrete_treatment=True` — `RandomForestClassifier` for ê(x) = P(T=1\|X) |
| **Prespecified sensitivity** | **alternative treatment-nuisance and treatment-handling specification** — the primary with `discrete_treatment=False` |

One additional main run per cohort. **No additional permutation cost** — permutation runs on the
primary only. This converts a documented defect into a robustness result.

**Naming [R1 §5].** This is **not** a "single-factor sensitivity". The flag changes **three** things
at once: classifier vs regressor for ê, the range of the probability output, and stratified vs
unstratified inner CV (see (d)). It is therefore called an **alternative treatment-nuisance and
treatment-handling specification** in the plan and in Methods. The sensitivity is **not** "the archived configuration": the archive additionally used
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

**Wording [R1 pre-R3 §E].** `RandomForestClassifier.predict_proba` returns **estimated
treatment-assignment probabilities**. They are *not* calibrated — no `CalibratedClassifierCV` is
applied anywhere in this plan, and the earlier phrase "calibrated probabilities" is withdrawn.
Calibration is **not** added now. The reasons of record are: the specification is locked;
`predict_proba` returns bounded estimates; and outer-fold diagnostics are reported in detail.
DML's robustness to nuisance misspecification is deliberately **not** invoked — that would introduce
a theoretical claim this paper does not need to defend.

**Propensity / positivity diagnostics — reported for BOTH configurations [R1 §A3]:**

| diagnostic | purpose |
|---|---|
| min, max, and quantiles of ê(x) | distributional summary |
| proportion outside **[0, 1]** | structurally zero under `predict_proba` — so for the primary this is a **check that it behaves as expected**, and for the sensitivity it quantifies a real defect |
| **proportion outside [0.05, 0.95]** | **positivity / overlap** |
| histogram / density plot of ê(x) | Supplement figure |

**All propensity diagnostics are computed on OUTER HELD-OUT FOLD predictions, never in-fold**
[R1 pre-R3 §E].

The last is not a formality. In HER2+, 31 controls out of 241 with `min_samples_leaf=5` can produce
leaves that are entirely treated, so `predict_proba` can return values at or near 1. That is a
**positivity failure, not a numerical nuisance**, and it is reported rather than clipped — a reviewer
will ask about overlap, and this answers the question before it is put.

**(d) The two nested cross-validation layers — documented separately [R1 pre-R3 §G(b)]**

Verified from source, not inferred. Forest instantiation quoted verbatim from
`run_pca_in_fold.py:54` / `optionA/run_pca_in_fold_optionA.py:49` /
`recalculate_autoc_unified.py:40` — all three identical:

```python
CF_P = dict(n_estimators=500, min_samples_leaf=20, random_state=42, cv=5)
```

**n_estimators is 500.** (An earlier report rendered this as `n_estima=20` through column
truncation; twenty trees would not support stable CATE estimation and that value never existed.)

| | **OUTER — strict out-of-fold** | **INNER — `CausalForestDML(cv=5)` cross-fitting** |
|---|---|---|
| purpose | held-out CATE evaluation | nuisance cross-fitting inside each outer training set |
| folds | 5 | 5 |
| splitter | `StratifiedKFold` (explicit, in our code) | generated internally by `check_cv` — see below |
| stratified by | `2·T + Y` | **`T` only, and only when `discrete_treatment=True`** |
| shuffle | `True` | `True` (set at `_ortho_learner.py:955`) |
| `random_state` | 42 (saved to disk) | the estimator's `random_state` = 42 (`:956`) |

econml 0.16.0 `_ortho_learner.py`:
- `:927` `stratify = self.discrete_treatment or self.discrete_instrument or self.discrete_outcome`
- `:946` `splitter = check_cv(self.cv, [0], classifier=stratify)`
- `:955-956` `splitter.shuffle = True; splitter.random_state = self._random_state`

**Consequence not previously recorded:** the `discrete_treatment` override changes the inner
splitter as well as the propensity model.

| configuration | inner splitter |
|---|---|
| **primary** (`discrete_treatment=True`) | **`StratifiedKFold(5)`, stratified by T**, shuffle, seed 42 |
| **sensitivity** (`discrete_treatment=False`) | **`KFold(5)`, NOT stratified**, shuffle, seed 42 |

**Runtime consequence for R3:** one configuration costs 5 outer folds × [5 inner nuisance
cross-fits × 2 models + one 500-tree forest fit], not "5 forest fits". Any per-iteration projection
built on the latter understates the cost. **R3 must measure, not extrapolate.**

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

**PCA compression check [R1 pre-R3 §F].** Measured per fold, both cohorts:

> The corrected radiomics block retained more than 98 % of variance at the prespecified 20 components
> and was therefore not disadvantaged relative to the FM blocks by PCA compression.

HER2− 98.12 %, HER2+ 98.67 % at 20 PCs, against BiomedCLIP 82.62 % / 86.30 % at 30 PCs.
**This is a fairness check only.** High variance retention is **not** the same as retaining
treatment-effect-relevant information, and it **must not** be used to explain any R4 performance
difference in either direction. No mechanism for the compressibility is asserted — no correlation
matrix or eigenvalue spectrum was examined.

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

**8.3a AMENDMENT — mechanism requirement [R1 post-R2a §3, added 2026-07-25 after R2a, before R2c runs]**

R2a recalibrated what "reproduced" looks like on this machine: BiomedCLIP came back at **cosine
1.000000000000000 and max element-wise difference 3.55e-15** — text round-trip noise, nothing more.
That is new evidence, and it sharpens this criterion *before* the test it governs.

**The numeric thresholds above are NOT tightened.** RAD-DINO uses torch/transformers where BiomedCLIP
used open_clip, and if the archive was produced on MPS while the rebuild runs on CPU, float32
differences of order 1e-5–1e-6 are legitimate. The 1e-4 bound accounts for that correctly.

**What is added is a requirement that any residual be *explained*, not merely tolerated:**

| max abs element-wise difference | ruling |
|---|---|
| **≤ 1e-12** | **Reproduced.** No explanation needed — this is the BiomedCLIP class. |
| **1e-12 to 1e-4** | Passes the numeric threshold, but reproduction is confirmed **only if the residual is mechanistically accounted for** — e.g. re-run on MPS and demonstrate convergence, or otherwise identify the source. **An unexplained residual at this magnitude is not reproduction**; it indicates a *similar but different* preprocessing was found. |
| **cosine in [0.99, 0.9999)** | **No longer "retain with disclosure."** Given that correct reconstruction produces 1e-15, a cosine of 0.995 means a **different pipeline that happens to resemble the original.** Treat as **NOT reproduced** → RAD-DINO withdrawn per §9, unless the mechanism is identified and it resolves into the band above. |
| **cosine < 0.99** | **Dropped**, as planned. |

Rationale for recording this as an amendment rather than a judgement call at test time: it is a
*tightening* based on evidence from a different arm, made before the governed test runs. Amendments
that predate results are legitimate and are logged; amendments after them are not.

**Gate G2.** Reproduced (per 8.3a) → retained. Not reproduced, or no determinable reconstruction →
**dropped**; remove all RAD-DINO figures, tables and claims, restructure as a BiomedCLIP-centred
proof-of-concept. **Do not adopt a near-match. Do not improvise partial retention.**

---

## 9. HER2+ cohort — descriptive and exploratory, unconditionally [R1 pre-R3 §D]

> The HER2-positive analysis is descriptive and exploratory because the control group contains only
> 31 patients. No HER2-positive arm-specific quartile treatment-effect estimates are used for
> inference. The analysis is limited to descriptive AUTOC estimates, confidence intervals, and
> continuous-score summaries. No confirmatory P values, no significance claims, and no
> encoder-superiority claims are made.

**This is unconditional. It does not depend on any measured quantity.**

### Withdrawn: the 0.40 CI-width trigger

The previous formulation made HER2+ status conditional on a bootstrap CI width exceeding 0.40.
**It is withdrawn, and the phrase "prespecified precision trigger" must not be used.** The threshold
was set knowing the archived CI width was 0.431 — i.e. chosen after seeing the quantity it tests,
which is not pre-specification however precision-based the criterion looks.

Also withdrawn: the replacement wording marking quartile cells "unstable or suppressed" when a
control cell fell below n = 8. That reintroduced a judgement about what counts as small. **HER2+
quartile treatment-effect estimates are not used for inference at all**, so no threshold is needed.

The **provenance** trigger is separate, was never conditional on a measured effect, and **did not
fire** — R2c reproduced the archived RAD-DINO embeddings at 4.441e-16.

---

## 9a. Enrolment epoch — enters `W`, not `X` [R1 enrolment-epoch ruling]

### 9a.1 Definition

A **categorical relative enrolment epoch**, one-hot encoded, with boundaries defined by **changes in
active-arm composition** — the mechanism that makes time matter is which randomisation options were
open. Derived from `acquisition_date` (the MRI date), itself a proxy for enrolment.

**Rule, saved in code (`epoch_assignment.csv`, generator in `R3_smoke/`) and reproduced in the
Supplement:** change points are every arm-open start date and every (arm-open end + 1 day); epochs
are the intervals between consecutive change points, labelled by **relative index only**.

- **`nac_agent` is used ONLY to reconstruct epoch boundaries.** It never enters `X`, `W`, or the
  permutation strata.
- Epochs are **never** interpreted or reported as real calendar years. The shifted 1998–2004 dates
  were used **solely** to recover relative ordering and arm windows; **absolute dates are not
  interpretable and are not used.**

**Canonicalisation.** Merge **only adjacent** intervals with an identical reconstructed active-arm
set — such intervals are not distinct assignment environments. **Non-adjacent intervals with the same
arm set are NEVER merged**: if an arm set recurs later, the adaptive-randomisation *state* (the
accumulated response data driving assignment probabilities) differs, and merging would pool distinct
assignment environments under one indicator. **No interval is ever merged because of sample size,
treatment counts, propensity diagnostics, or downstream results.**

Applied: 22 change points → 23 raw intervals → **0 adjacent merges** (every change point alters the
active set by construction) → **22 epoch levels with ≥ 1 patient**. The prohibition was load-bearing:
the empty active-arm set recurs in **3 non-adjacent epochs**, which are kept separate.

| cohort | levels present | min | median | max | levels < 5 | levels < 10 |
|---|---:|---:|---:|---:|---:|---:|
| HER2− | 22 | 1 | 13 | 143 | 8 | 10 |
| HER2+ | 17 | 1 | 7 | 46 | 6 | 8 |

**Small epochs are retained.** Epoch enters `W` only and is never an effect modifier in the final
CATE forest; the nuisance forests carry `min_samples_leaf=5`, so an epoch of n = 1–4 cannot form its
own leaf; 22 indicators against 739 HER2− patients is not excessive; and changing boundaries for
small-sample reasons is the more dangerous option. Complete memorisation is structurally prevented;
residual influence in combination with other features remains possible.

**Diagnostics are reported regardless:** epoch size distribution (above), and outer-fold ê(x, w)
including the proportion outside [0.05, 0.95], **with and without epoch**. **If positivity fails it is
reported as a finding, not repaired.** The diagnostics exist so it cannot pass unnoticed, not so it
can be corrected after the fact.

**The epoch mapping is FROZEN** at `R3_smoke/epoch_assignment.csv` /
`epoch_canonical_mapping.json` before R3.

### 9a.2 Primary specification

```python
est.fit(Y, T, X=clinical_and_imaging_effect_modifiers, W=epoch_controls)
```

**This is a specification change.** The archived code passes no `W` at all
(`run_pca_in_fold.py:220`, `optionA:175` are both `cf.fit(Y, T, X=X)`), so every covariate was an
effect modifier. Under the amendment, epoch controls confounding through the nuisance models without
becoming a dimension the CATE varies over.

**Verified from econml 0.16.0 source before implementation** — all three hold:

| requirement | evidence |
|---|---|
| `W` enters both nuisance models | `dml/_rlearner.py:297` — `self._model.fit(np.hstack([X, W]), Y)`, reached for both `model_y` and `model_t` via `_ModelNuisance.train` |
| `W` is **not** available to the forest as a splitting variable | `_ModelFinal.fit(Y, T, X, W, …)` receives `W` and calls `self._model_final.fit(X, T, T_res, Y_res, …)` — `W` is dropped; `_CausalForestFinalWrapper.fit(self, X, …)` takes `X` only |
| θ is a function of `X` alone | `_ModelFinal.predict(self, X)` → `self._model_final.predict(X)`; econml's own docstring: `Y − E[Y\|X,W] = θ(X)·(T − E[T\|X,W])`, "at predict time returns θ(X)" |

### 9a.3 No-epoch sensitivity — a **diagnostic**, not a robustness footnote

- **Primary:** epoch in `W` · **Sensitivity:** epoch excluded from `W`
- **No permutation** for the sensitivity; compare AUTOC, paired ΔAUTOC and propensity diagnostics only
- If compute is tight, restrict to the principal model and clinical-only

**Interpretation, written before the numbers exist so it cannot be reframed afterwards.** MAMA-MIA is
multi-centre and imaging protocol and scanner characteristics change over time; foundation-model
embeddings can encode those. Epoch is also correlated with which agent was available, and therefore
with treatment effect.

> If FM performance is materially stronger when epoch controls are excluded, this will be interpreted
> as evidence that the apparent FM signal is **sensitive to temporal or acquisition-related
> structure** and may partly reflect protocol or trial-period variation rather than treatment-relevant
> tumour biology. **This pattern would not, by itself, prove acquisition confounding.**

**This is a sensitivity signal, not a confirmatory diagnosis.** Other explanations produce the same
pattern: scanner and site composition changes, correlation with treatment availability, increased
nuisance-model variance, and estimation instability from positivity or small epochs. Reported either
way, and **the language is not upgraded once the numbers exist.**

---

## 9b. Empty-arm epochs — retained; prespecified exclusion sensitivity [Item 6 ruling]

**All 739 HER2− and 241 HER2+ participants are retained in the primary analyses.** True
experimental-arm unavailability cannot be distinguished from sparse observation or dataset selection
using the available source, and **the burden of proof lies with exclusion.**

**Constraints on wording, binding:**

- **These epochs are NOT described as a proven structural positivity violation.**
- **ê(x, w) is NOT cited as evidence of design positivity in either direction.** Empty-arm median
  0.7537 vs 0.7565 for the rest is statistically indistinguishable; the estimate demonstrates
  nothing. Description only.
- Limitations note that epoch 1 (n = 2, the dataset's opening week — a boundary artefact of the
  observation window) and epoch 21 (n = 9, an interior 40-day gap) differ in structure.
  **Their handling is not differentiated; the eleven are treated as one group.**

### Reconstructed empty-arm-epoch exclusion sensitivity analysis

Prespecified **before R4**. Deliberately **not** called a common-support analysis — that would assert
the positivity claim just declined.

| | |
|---|---|
| population | HER2−, **n = 728** |
| configurations | all six |
| specification | full strict OOF, epoch in `W`, hyperparameters identical to primary |
| permutation | **none** |
| report | AUTOC, 95 % CI, paired ΔAUTOC (principal − clinical-only), held-out propensity diagnostics |
| status | **cannot replace the full-cohort primary; never promoted to primary regardless of direction** |

**Folds:** the saved fold labels with those 11 removed — **folds are not re-derived**.
**Verified before running:** every fold retains both arms (test-fold controls 32–35, train 132–135;
all five OK). Had any degenerated, the run would have stopped.

**Containment verified, not assumed:** all **11/11** empty-arm participants are among the 46 excluded
from the permutation population. (The deduction was correct; the check is now on record.)

### Three populations — labelled everywhere

| population | n | role |
|---|---:|---|
| Full HER2− cohort | **739** | **primary analysis** |
| Empty-epoch exclusion | **728** | design-support sensitivity |
| Permutation overlap | **693** | permutation sensitivity only |

**Three distinct principal-model AUTOCs will exist.** Every appearance — tables, figures, text,
results file — carries its population label. **One is never presented as another.**

### Manuscript wording, fixed now

> Eleven HER2-negative control participants occurred in reconstructed enrolment epochs in which no
> experimental assignments were observed. Because arm availability could not be independently
> verified from the de-identified public dataset, these participants were retained in the full-cohort
> primary analysis. A prespecified sensitivity analysis repeated the complete strict out-of-fold
> analysis after excluding these 11 participants.

### Composition of the 46 permutation-excluded (no outcomes)

subtype luminal_a 30 / TNBC 16 · arm experimental 33 / control 13 · HR+ 30 / HR− 16 ·
MammaPrint 1 = 26 / 0 = 20 · spread across 15 epochs (largest: epoch 21 n = 9, epoch 3 n = 8).

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

**Source and adopted variant.** Besag J, Clifford P. Sequential Monte Carlo p-values.
*Biometrika* 1991;78(2):301–304. The adopted variant is stated explicitly rather than by reference:

```
early stop — h exceedances observed at permutation l < M :   P = h / l
M reached with b < h exceedances                          :   P = (b + 1) / (M + 1)
```

with h = 20 (the value the original authors suggest) and M = 10,000. **This is the formula as
committed at `bb70d54` and it is correct; it is not to be changed.** See ledger D39.

**Validity properties — these bound what the p-value may claim:**

- the estimate is valid **only at the stopping time**. **No interim value may be reported or acted
  on**, and none is computed for inspection.
- it is **unconditionally valid** but carries **no conditional validity guarantee**.

**Implementation validation, before the production run.** Synthetic data with no treatment effect,
a cheap statistic, ≥1,000 replications of the *full sequential procedure*; confirm the p-values are
approximately uniform and that P(p ≤ α) ≈ α at α = 0.05 and 0.01. This verifies the **code**, not the
formula. Minutes of compute on synthetic data. The R package `MChtest` (Fay) implements the
Besag–Clifford boundary and may serve as an independent cross-check.

**R3 must report the expected wall-clock under this design alongside the flat-10,000 figure.**

### 10.1 What the permutation can and cannot claim [R1 pre-R3 §C]

I-SPY2 assignment probabilities vary with HER2 status, hormone-receptor status, the 70-gene
signature, results accumulated up to enrolment, and which arms are open. **A uniform permutation of
T within a cohort does not reconstruct that mechanism.**

**C1 — what the paired bootstrap does and does not escape.** The earlier wording "the primary
comparison is unaffected" was too strong and is withdrawn. Correct statement:

> The paired bootstrap comparison does not rely on permutation exchangeability; however, its causal
> interpretation still depends on the validity of the treatment-assignment model, on overlap, and on
> the underlying identification assumptions.

Adaptive randomisation bears on those assumptions directly: if assignment probability depends on
enrolment time and time is not in X, **conditional ignorability given X alone may not hold.** That is
an **identification** concern, not merely a permutation concern, and it belongs in the Limitations
regardless of what the permutation analysis becomes.

**C2 — `nac_agent` is NOT a permutation stratum.** It *is* the assigned treatment. Within any agent
stratum everyone is experimental and controls have no agent, so permutation degenerates. Its only
legitimate use is **reconstructive**: inferring which agents were open in which periods and whether a
concurrent-control structure can be recovered.

Strata must be variables fixed **before** assignment: HR status, HER2 status, MammaPrint / 70-gene
category, enrolment date or period, and the set of arms active at randomisation.

**C3 — naming and interpretive limits.** Per-patient assignment probabilities do not exist even with
the achievable stratification. The analysis is named a **model-based permutation sensitivity
analysis**, and the text must state that *it is not an exact reconstruction of the I-SPY2 adaptive
randomisation procedure.* Further: **permuting treatment labels breaks the null of no treatment
effect at all** — it is not a specific test of the absence of heterogeneity, nor of the absence of
incremental FM value, and **rejection is consistent with a main effect alone.**

**C4 — condition for abandoning it.** If adequate biomarker and temporal strata cannot be
reconstructed, **omit permutation p-values entirely rather than present an inadequately justified
approximation.** The paired ΔAUTOC confidence interval and the BLP test carry the inference on their
own. The permutation analysis is not preserved for its own sake.

**Strata are computed WITHIN EACH COHORT [R1 §4].** The analyses are split by HER2 status, so HER2 is
constant within a cohort and adds nothing. Effective strata: **HR × MammaPrint × relative epoch**.

**"Usable" = the cell contains BOTH at least one treated and at least one control patient.**

| cohort | n | cells | usable | included | **excluded** |
|---|---:|---:|---:|---:|---:|
| HER2− | 739 | 66 | 43 | **693 (93.8 %)** | 46 |
| HER2+ | 241 | 45 | 12 | **124 (51.5 %)** | **117** |

The earlier union figure (91.0 %) masked the HER2+ result and is superseded. **Cells are never merged
after seeing results.** Permutation results apply to that **restricted population** and are a
**sensitivity analysis**, kept distinct from the full-cohort primary inference; excluded counts are
reported per cohort with every p-value.

**HER2+ needs no permutation.** Under §9 the HER2+ analysis makes no confirmatory P-value or
significance claims, so the 51.5 % coverage does not gate anything — it is recorded, not worked
around.

**The proposed design and the stratum reconstruction it rests on are reported before the production
run.** R3's smoke test may proceed in parallel.

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

**Fold convention — observed vs permutation [R1 post-R2c §6a]. These are not in conflict.**

| | folds |
|---|---|
| **observed analysis** | the **single saved** fold assignment, computed once from `2·T + Y` and loaded by every configuration, so all configurations are evaluated on identical, auditable splits |
| **each permutation** | folds **recomputed** from `2·T_perm + Y` |

The stratification depends on T, so the null procedure *must* recompute it — otherwise the permuted
treatment would be evaluated against folds built from the original assignment, and the null would
not be exchangeable with the observed procedure. In every other respect the permutation pipeline is
identical to the observed one. **Implementation requirement for R4: the observed run loads the saved
fold file; the permutation loop calls the same fold-construction function on `2·T_perm + Y`.** Both
paths must call one shared function, not two copies.

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
| **B** | — | Version control and third-party timestamp | ✅ **RESOLVED [R1 §B1–B2]** — repository kept outside every sync root, snapshots excluded via `.gitignore`; commit hash, UTC time and third-party timestamp recorded in the header above. |
| **C** | 9 | **HER2+ CI width is measured on the archived (in-sample) run.** The 0.431 figure comes from the Option-B bootstrap. The strict-OOF CI will differ and is not yet known. The 0.40 threshold is retained as fixed; noting only that the *expectation* it fires rests on an in-sample precedent. | ⬜ informational |

---

## 14. Deviations

Any departure after commit requires sign-off and a `DECISION_LOG.md` entry recording what changed,
why, when, and what it would otherwise have been. **Selecting among discretisations, seeds or
configurations by downstream performance is prohibited.**
