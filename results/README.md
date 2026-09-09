# Results of the corrected analysis

All JSON files are byte-identical to the frozen record; their hashes appear in the `ORIGINAL_SHA256SUMS.txt`
manifest of each folder (the manifests also list working files of the record that are not released, such as the
covariate matrices). The Markdown records are the results and environment records written with the analysis.

## rate_primary/ (Q1 and Q2; amendment `AMENDMENT_R7_RATE.md`)

| file | content |
|---|---|
| `rate_q1_primary.json` | six configuration-specific RATE/AUTOC estimates on H2 with SE, CI, z, raw and Holm p; design, overlap diagnostics, forest-versus-`.fit` interface check |
| `rate_q2_primary.json` | paired contrast reference − clinical only (both components and the difference) |
| `rate_q2_sensitivities.json` | MammaPrint-expanded, no-epoch, alternative treatment-nuisance and empty-arm-exclusion sensitivities |
| `rate_q1_sequential_sensitivity.json` | Q1 sequential cross-fold sensitivity, fold t-statistics, locked and restricted aggregations |
| `rate_her2pos_not_estimated.json` | HER2-positive cohort: split composition and the "not estimated for inference" decision |
| `overlap_diagnostics.json` | estimated propensity distribution on the primary and empty-arm evaluation sets |
| `crosscheck_implementations.json` | grf versus a direct re-implementation of the RATE definition (agreement ≤ 3.4e−14) and the econml `calc_uplift` cross-check |
| `Z_provenance.json`, `priorities_provenance.json`, `priorities_sequential_provenance.json` | covariate columns, fit-row counts and shapes of every fit |
| `RESULTS_R7_RATE.md`, `ENVIRONMENT_RECORD.md` | results and environment records of the run |

## rate_q3/ (amendment `AMENDMENT_R7_Q3.md`)

| file | content |
|---|---|
| `rate_q3.json` | A (opposite-half) and C (same-sample) RATE point estimates in both halves, C − A per half, pooled contrast; held-out SEs for A only; run check against Q1 |
| `q3_provenance.json`, `RESULTS_R7_Q3.md`, `ENVIRONMENT_RECORD.md` | provenance and records |

## rate_q4/ (amendment `AMENDMENT_R7_Q4.md`)

| file | content |
|---|---|
| `rate_q4_regimes.json` | regime RATE values A, D1, D2, B per configuration and half, with reference-only SEs, P / S / P×S / B − A contrasts and pooled values |
| `rate_q4_contrasts.json` | the pooled and half-specific contrasts of the regimes file re-serialized with a summary block (`src/rate_analysis/extract_q4_contrasts.py`) |
| `q4_provenance.json`, `RESULTS_R7_Q4.md`, `ENVIRONMENT_RECORD.md` | provenance (fit-row counts of all 48 fits) and records |

## feature_extraction/

Records of the feature round: model checkpoints and revisions (`BIOMEDCLIP_PROVENANCE_RECORD.json`,
`RADDINO_PROVENANCE_RECORD.json`), reproduction of the archived embeddings (`r2a_biomedclip_verification.json`,
`r2c_raddino_verification.json`, `r2c_usefast_result.json`), the corrected radiomics settings and QC gate
(`r2b_extraction_meta_binCount64.json`, `roi_voxel_distribution.json`, `g1_qc_report_binCount64.json`,
`g1_feature_correlations_binCount64.csv`, `SUPPLEMENT_TABLE_radiomics_correction.md`), the 107 feature names
(`feature_names.json`) and the PCA variance retained per block (`pca_variance_retention.json`).

## Terminology

Regime A is called "honest" in these records and "opposite-half" in the manuscript and figures; regime C is
"apparent" or "same-sample". References to `FROZEN_*` sets, round labels and decision numbers point to the
private development record (see the top-level README).
