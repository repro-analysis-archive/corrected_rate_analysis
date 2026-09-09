# Reproduction guide

All commands are run from the repository root. Regenerated outputs are written under `reproduction/`
(ignored by git); the released record under `results/`, `derived_data/`, `figure_data/` and `figures/` is never
overwritten, so regenerated and released files can be compared directly.

## 1. Environments

| purpose | definition | key versions |
|---|---|---|
| analysis (stages 1 to 3) | `environment/environment.yml`, `environment/requirements.lock.txt`, `environment/build_env.sh` | Python 3.12.8, numpy 2.2.3, scipy 1.15.3, pandas 2.2.3, scikit-learn 1.6.1, econml 0.16.0, joblib 1.4.2, openpyxl |
| feature extraction (stage 0) | `environment/environment_features.yml`, `environment/requirements_features.lock.txt`, `environment/build_env_full.sh` | the analysis stack plus pyradiomics 3.1.1.dev111+g8ed579383 (installed from the git commit named in `environment/README.md`), SimpleITK 2.4.1, torch 2.10.0, transformers 4.57.6, open_clip_torch 3.2.0, timm 1.0.28 |
| RATE/AUTOC (stage 2) | `environment/README.md` | R 4.5.3, grf 2.6.1, jsonlite 2.0.0 |
| figures (stage 3) | `environment/README.md` | MATLAB R2025b with the Arial font |

Set two environment variables (both have defaults, shown here):

```bash
export JIIM_RELEASE_ROOT="$(pwd)"                    # repository root; R scripts default to the working directory
export JIIM_DATA_ROOT="$(pwd)/external_data"         # source data and feature matrices (not redistributed)
```

## 2. Source data and expected layout

See `docs/DATA_ACCESS.md`. In short, `external_data/` must contain the MAMA-MIA clinical workbook
`clinical_and_imaging_info.xlsx`, `images/<ID>/<ID>_0001.nii.gz` and `segmentations/<ID>.nii.gz` for the 980
patients defined by the workbook filter (`dataset == "ISPY2"`, `her2` in {0, 1}, non-missing `pcr`), and, after
stage 0, `features/` with the six feature matrices whose sha256 values are given in
`checksums/INPUT_PROVENANCE.txt`.

## 3. Execution order

`bash scripts/run_pipeline.sh` runs everything below; `bash scripts/run_pipeline.sh analysis` runs stages 1 and
2 only (requires the feature matrices), `... features` and `... figures` run one stage. The interpreters are taken
from `PYTHON` and `PYTHON_FEATURES` (default `python`).

### Stage 0 — feature extraction (feature environment)

```bash
python src/features/roi_voxel_distribution.py      # ROI voxel counts after 1 mm resampling; applies the pre-fixed binCount rule
python src/features/r2b_radiomics_reextract.py 64  # corrected radiomics, binCount 64, 3-D, 1 mm isotropic  -> features/radiomics_*_binCount64_20260725.csv
python src/features/r2a_biomedclip_reextract.py    # BiomedCLIP 512-d embeddings                             -> features/biomedclip_*_reextract_20260725.csv
python src/features/r2c_usefast_test.py            # RAD-DINO CLS-token 768-d embeddings (use_fast = True)    -> features/raddino_*_reextract_cls_usefast_20260725.csv
```

The cohorts are derived from the clinical workbook by `src/features/cohort_ids.py` (same rule as the analysis
loader), in workbook row order, which on the recorded workbook version equals the row order of the frozen feature
matrices, so a regeneration can be checked against the recorded hashes. Embeddings were extracted on Apple-silicon
MPS; the scripts fall back to CPU, and small floating-point differences on other hardware propagate to the PCA
inputs and therefore to the priorities.

`r2c_raddino_reextract.py`, `g1_qc_report.py`, `pca_variance_retention.py` and `r2b_effective_bins_fix.py` are the
verification and QC scripts of the feature round; they compare against the feature matrices of the original study
(expected under `external_data/archive/`, not redistributed) and are included for completeness of the record.

### Stage 1 — enrolment epochs, prioritization scores, split and evaluation covariates (analysis environment)

```bash
python src/rate_analysis/derive_epochs.py          # 22 enrolment epochs from acquisition_date and nac_agent -> reproduction/splits/epoch_assignment.csv
python src/rate_analysis/fit_priorities.py          # split_739.csv; priorities_primary_heldout.csv; priorities_sens_*.csv; priorities_provenance.json
python src/rate_analysis/build_Z.py                 # Z_eval_primary.csv, Z_eval_empty_arm.csv, seq_folds_739.csv, Z_eval_seqfold{2..5}.csv, Z_provenance.json
python scripts/verify_split_digests.py              # regenerated split, folds, epochs and cohorts against splits/SPLIT_DIGESTS.json
```

### Stage 2 — RATE/AUTOC (R) and cross-check

```bash
Rscript src/rate_analysis/rate_primary.R            # rate_q1_primary.json, rate_q2_primary.json, rate_q2_sensitivities.json, overlap_diagnostics.json, dr_scores_primary_heldout.csv
python  src/rate_analysis/fit_priorities_sequential.py
Rscript src/rate_analysis/rate_sequential.R         # rate_q1_sequential_sensitivity.json
python  src/rate_analysis/crosscheck.py             # crosscheck_implementations.json
python  src/rate_analysis/fit_q3_priorities.py      # priorities_q3_H1.csv, priorities_q3_H2.csv, Z_H1.csv, q3_provenance.json
Rscript src/rate_analysis/rate_q3.R                 # rate_q3.json, dr_scores_H1.csv
python  src/rate_analysis/fit_q4_priorities.py      # priorities_q4_H1.csv, priorities_q4_H2.csv, q4_provenance.json
Rscript src/rate_analysis/rate_q4.R                 # rate_q4_regimes.json
python  src/rate_analysis/extract_q4_contrasts.py   # rate_q4_contrasts.json (re-serialization of the regimes file)
```

Outputs go to `reproduction/rate_primary/`, `reproduction/rate_q3/` and `reproduction/rate_q4/`. The Q3 and Q4
scripts read the split, priorities and scores produced by the earlier stages of the same run (in the original run
these were the frozen primary outputs); their built-in run checks compare regime A against the Q1 estimates of the
same run.

### Stage 3 — figure data and figures

```bash
python src/figures/freeze_figure_data.py            # reads results/ (the released record) -> reproduction/figure_data/{Fig1..5_data.json, fig_data_r7.mat, FIGURE_DATA_SHA256.txt}
matlab -batch "cd('src/figures'); build_all"        # reads figure_data/fig_data_r7.mat -> reproduction/figures/Fig1..5.{fig,pdf,tif}
```

`freeze_figure_data.py` verifies each released result file against the manifest of the frozen record
(`results/*/ORIGINAL_SHA256SUMS.txt`) before extracting values; it performs no statistics.

## 4. Expected outputs

Key values of the released record (full precision in the JSON files):

| quantity | value |
|---|---|
| Q1 RATE/AUTOC, held-out H2 (estimate, SE) | Clinical only −0.0668 (0.0542); Clinical + radiomics −0.0454 (0.0560); Clinical + BiomedCLIP +0.0975 (0.0407); Clinical + RAD-DINO −0.1088 (0.0557); Clinical + radiomics + BiomedCLIP +0.0464 (0.0412); Clinical + radiomics + RAD-DINO −0.0591 (0.0610) |
| Q2 ΔRATE, reference − clinical only | +0.1132, SE 0.0737, 95 % CI −0.0314 to +0.2577, p = .125 |
| Q3 pooled C − A (same-sample minus opposite-half), by configuration | +0.1570, +0.2101, +0.1846, +0.2792, +0.2271, +0.2451 |
| Q4 pooled B − A (full-sample preprocessing minus training-half preprocessing) | −0.0022, −0.0248, −0.0112, +0.0358, −0.0228, −0.0365 |
| evaluation-half propensity range (H2) | 0.5498 to 0.8634, none outside [0.05, 0.95] |

Determinism: every random element is seeded (`seeds/seeds.json`). Re-running the released pipeline (stages 1 to 3)
in the recorded environments on the platform of the record, from the clinical workbook and the six feature matrices,
regenerated the split, the sequential partition and the epoch table exactly (digests and file hashes match), reproduced
every result JSON under `results/` byte for byte, the doubly robust scores and the figure data exactly, and the
figures with every graphics-object property identical (positions, strings, fonts, colours, sizes). Figures 1 to 4
were also pixel-identical as TIFFs; for Figure 5 one MATLAB session rasterized one text band differently (glyph
anti-aliasing), so pixel identity of the TIFF renders is not guaranteed across sessions although the vector content
is. The prioritization scores agreed to within 3.1e-16 (relative 3e-14) with no change of rank, the expected
floating-point variation of parallel forest fitting; it propagates only into the identity-check residuals recorded
in `q4_provenance.json`. On other platforms the forest fits may differ at floating-point level and the RATE
estimates in the fourth or later decimal.

## 5. Verification without the source data

```bash
Rscript scripts/verify_rate_from_released_scores.R
```

recomputes, from `derived_data/` alone, every RATE/AUTOC estimate and half-sample-bootstrap standard error of the
Q1 primary analysis, the Q2 primary contrast, the MammaPrint, no-epoch and alternative-treatment-nuisance
sensitivities, all Q3 quantities and all 48 Q4 regime values, using `grf::rank_average_treatment_effect.fit`
with `target = "AUTOC"`, `R = 2000` and `set.seed(20260906)` before each call, exactly as in the analysis scripts,
and compares them with `results/` at a tolerance of 1e-9 (on the platform of the record: 174 comparisons, largest
difference 5e-14). The files are aligned by their positional row labels. Two quantities need an evaluation forest
that is not released with the scores and are therefore covered only by the full pipeline: the empty-arm exclusion
sensitivity (its own evaluation half of 366 patients) and the Q1 sequential cross-fold sensitivity (fold-wise
evaluation forests).

```bash
bash scripts/verify_checksums.sh
```

verifies every released file against `checksums/SHA256SUMS.txt`.
