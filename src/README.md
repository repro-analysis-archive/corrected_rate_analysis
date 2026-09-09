# Source code

Every analysis script is the file that produced the released results, modified only in how it resolves file
locations and in reading cohort membership from the clinical workbook instead of a distributed identifier list
(`docs/CODE_MODIFICATIONS.md` lists each change with the hashes of the frozen original and the released copy).
Paths are resolved through `JIIM_RELEASE_ROOT` (repository root) and `JIIM_DATA_ROOT` (source data, default
`external_data/`); outputs are written under `reproduction/`.

## features/ (stage 0)

| script | role | output |
|---|---|---|
| `cohort_ids.py` | cohort membership from the workbook filter of the frozen loader (added for the release) | |
| `roi_voxel_distribution.py` | ROI voxel counts after 1 mm isotropic resampling; applies the pre-fixed rule that selected binCount 64 | `reproduction/features/roi_voxel_distribution.json` |
| `r2b_radiomics_reextract.py` | corrected radiomics: pyradiomics, binCount 64, normalize False, 1 mm isotropic B-spline resampling, 3-D, label 1; also the per-patient effective-bin count | `features/radiomics_{her2neg,her2pos}_binCount64_20260725.csv`, `r2b_effective_bins_binCount64.csv`, `r2b_extraction_meta_binCount64.json` |
| `r2a_biomedclip_reextract.py` | BiomedCLIP image embedding of the maximum-tumour-area axial slice (512-d); compares with the archived embeddings when present | `features/biomedclip_{her2neg,her2pos}_reextract_20260725.csv` |
| `r2c_usefast_test.py` | RAD-DINO CLS-token embedding (768-d) with `use_fast = True`; this script produced the RAD-DINO features used by the analysis | `features/raddino_{her2neg,her2pos}_reextract_cls_usefast_20260725.csv` |
| `r2c_raddino_reextract.py` | RAD-DINO pooling-trial verification against the archived embeddings (requires them) | verification record |
| `g1_qc_report.py`, `r2b_effective_bins_fix.py`, `pca_variance_retention.py` | QC gate of the radiomics correction and PCA variance retained; the first and last compare with the original-study matrices (requires them) | QC records |

## rate_analysis/ (stages 1 and 2)

| script | role |
|---|---|
| `derive_epochs.py` | regenerates the 22 relative-enrolment epochs from the workbook by the documented rule (added for the release; verified against the frozen table) |
| `r4_stageA.py` | frozen data-loader module: assembles the analysis frame from the clinical workbook, the feature matrices and the epoch assignment; defines the clinical block, nuisance-learner hyperparameters and the six configurations. Its own analysis routines belong to the superseded design and are not executed by the released pipeline |
| `r7_common.py` | shared constants (seeds, configuration names) and the 50/50 split rule |
| `fit_priorities.py` | prioritization rules fitted on H1, priorities predicted on H2; primary and MammaPrint / no-epoch / alternative-nuisance / empty-arm sensitivities; writes the split |
| `build_Z.py` | imaging-free evaluation covariates on H2, the empty-arm evaluation subset and the sequential folds |
| `rate_primary.R` | H2 evaluation forest, doubly robust scores, Q1 RATE/AUTOC with Holm, Q2 paired contrast, sensitivities, overlap diagnostics |
| `fit_priorities_sequential.py`, `rate_sequential.R` | Q1 sequential cross-fold sensitivity |
| `crosscheck.py` | direct re-implementation of the grf RATE definition and the econml `calc_uplift` cross-check |
| `fit_q3_priorities.py`, `rate_q3.R` | Q3 opposite-half versus same-sample diagnostic in both directions |
| `fit_q4_priorities.py`, `rate_q4.R`, `extract_q4_contrasts.py` | Q4 preprocessing-placement regimes A / D1 / D2 / B in both directions; contrasts |

## figures/ (stage 3)

| file | role |
|---|---|
| `freeze_figure_data.py` | hash-verified extraction of figure values from `results/` into `figure_data` JSON and `.mat` |
| `build_all.m`, `make_Fig1.m` … `make_Fig5.m` | figure rendering (MATLAB R2025b, Arial) |
| `jiim_style_r7.m`, `jiim_axes_r7.m`, `jiim_ylabels_r7.m`, `jiim_wrap_r7.m`, `jiim_wrap_check_r7.m`, `jiim_export_r7.m` | house style, axes, label wrapping and export helpers |
