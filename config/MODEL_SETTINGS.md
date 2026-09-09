# Model settings

Transcribed from the released scripts; `configurations.json` holds the same content machine-readably. Where this
page and the code could differ, the code governs (`src/rate_analysis/r4_stageA.py`, `fit_priorities.py`,
`build_Z.py`, `rate_primary.R`, `fit_q3_priorities.py`, `fit_q4_priorities.py`).

## Populations

| population | n | definition |
|---|---|---|
| HER2-negative primary cohort | 739 | `dataset == "ISPY2"`, `her2 == 0`, non-missing `pcr`; control arm `Paclitaxel` (178 controls, 561 experimental; 205 pCR) |
| H1 (development half) | 370 | first 370 indices of `numpy.random.default_rng(42).permutation(739)` |
| H2 (evaluation half) | 369 | the remaining indices; 81 controls |
| empty-arm exclusion sensitivity | 728 | HER2-negative patients not in enrolment epochs 1 and 21 (the epochs with no experimental patient observed); evaluated on 366 H2 patients |
| HER2-positive cohort | 241 | `her2 == 1`, control arm `Paclitaxel + Trastuzumab`; 31 controls in total; **not estimated for inference** (`results/rate_primary/rate_her2pos_not_estimated.json`) |

## Prioritization rules (fitted on H1 only)

| element | setting |
|---|---|
| estimator | `econml.dml.CausalForestDML`, `n_estimators = 500`, `min_samples_leaf = 20`, `cv = 5`, `discrete_treatment = True`, `random_state = 42` |
| outcome nuisance | `RandomForestRegressor(n_estimators = 500, min_samples_leaf = 5, max_features = "sqrt", random_state = 42)` |
| treatment nuisance | `RandomForestClassifier` with the same hyperparameters (`RandomForestRegressor` and `discrete_treatment = False` in the alternative treatment-nuisance sensitivity) |
| effect modifiers X, clinical block | `age`, `tumor_subtype_enc`, `ethnicity_enc`, `bmi_group_enc`, `menopause_enc`; `StandardScaler` fitted on H1 (plus `mammaprint` in the MammaPrint-expanded sensitivity) |
| effect modifiers X, imaging blocks | radiomics 107 features → PCA 20 components; BiomedCLIP 512-d → PCA 30; RAD-DINO 768-d → PCA 30; each block `StandardScaler` then `PCA(k, random_state = 42)`, both fitted on H1 only |
| nuisance covariates W | 22 relative-enrolment-epoch indicators (omitted in the no-epoch sensitivity) |
| priority score | predicted CATE for each H2 patient; larger = higher priority for experimental treatment |

## Configurations (fixed order)

1. Clinical only · 2. Clinical + radiomics · 3. Clinical + BiomedCLIP · 4. Clinical + RAD-DINO ·
5. Clinical + radiomics + BiomedCLIP (historically designated reference configuration) · 6. Clinical + radiomics + RAD-DINO.
Internal keys in the code and data files: `Clinical only`, `Clin + Radiomics`, `Clin + BiomedCLIP`, `Clin + RAD-DINO`,
`Clin + Rad + BiomedCLIP`, `Clin + Rad + RAD-DINO`.

## Evaluation (H2 only)

| element | setting |
|---|---|
| evaluation covariates Z | imaging-free: `age` (median-imputed within the set, plus missingness indicator), `hr`, `mammaprint`, one-hot `ethnicity`, `bmi_group`, `menopause` ("pre" whitespace variants merged), epoch indicators from a fixed 22-level basis (levels absent from the set dropped); `tumor_subtype` excluded (collinear with `hr`), `her2` excluded (constant); 40 columns on H2 |
| evaluation forest | `grf::causal_forest(X = Z, Y, W = T, num.trees = 2000, seed = 42)`; doubly robust scores `get_scores()`; one common score vector for all rules |
| RATE | `grf::rank_average_treatment_effect` / `rank_average_treatment_effect.fit`, `target = "AUTOC"`, half-sample bootstrap `R = 2000`, `set.seed(20260906)` before every call; SE = SD over replicates; 95 % CI = estimate ± 1.96 SE; p = 2Φ(−|estimate/SE|) |
| multiplicity | Holm across the six Q1 tests; none for the single designated Q2 contrast |
| Q2 paired contrast | both priorities supplied jointly to the two-priority interface (paired bootstrap); ΔRATE = RATE(reference) − RATE(clinical only) |
| Q1 sequential sensitivity | new Y-independent random 5-fold partition (seed 42); for k = 2..5 fit on folds 1..k−1, evaluate on fold k with a fold-k evaluation forest; z = Σ t_k / √(K−1), K = 5; degenerate (constant) rules contribute t_k = 0 |

## Diagnostics (both split directions, point estimates)

| diagnostic | regimes |
|---|---|
| Q3 | A: rule and preprocessing fitted on the opposite half; C: rule and preprocessing fitted on the evaluated half itself. Optimism = RATE(C) − RATE(A); pooled = (370·H1 + 369·H2)/739. H2 uses the primary score vector; H1 uses one common imaging-free score vector built with the same specification |
| Q4 | causal forest always fitted on the opposite half; A: both preprocessing blocks on the training half; D1: imaging preprocessing on all 739; D2: clinical scaler on all 739; B: both on all 739. P = ½[(D1−A)+(B−D2)], S = ½[(D2−A)+(B−D1)], P×S = (B−D2)−(D1−A); pooled as above; P and P×S are structurally absent for clinical only |
