# Corrected RATE/AUTOC analysis of treatment-effect prioritization with clinical, radiomic and foundation-model breast MRI features

Code, frozen analysis specifications and amendments, the fixed sample-split design (code, seeds and verification
digests), model settings, machine-readable derived analysis outputs and figure-source data for reproducing the
corrected analyses reported in the revised manuscript **JDIM-D-26-02440** (*Journal of Imaging Informatics in
Medicine*).

The analysis asks whether treatment-prioritization rules built from harmonized clinical variables, with or without
pretreatment DCE-MRI features (conventional radiomics, BiomedCLIP and RAD-DINO image representations), rank
HER2-negative patients of the I-SPY2 trial (MAMA-MIA curation, n = 739) by their benefit from experimental
neoadjuvant therapy, with pathologic complete response as the outcome. The corrected framework fits every rule on a
fixed development half (H1, n = 370) and evaluates it on the independent held-out half (H2, n = 369) with the
standard centred, doubly robust rank-weighted average treatment effect (RATE, target AUTOC) of the R package `grf`
(version 2.6.1), using one common doubly robust score vector for all rules.

## What is included

| folder | content |
|---|---|
| `amendments/` | the three protocol amendments that define the corrected analysis (primary Q1/Q2, diagnostic Q3, diagnostic Q4), byte-identical to the frozen record |
| `analysis_specs/` | the frozen analysis plan under which the feature pipeline, enrolment epochs and populations were fixed, and the pre-specification of 2026-07-25 with its OpenTimestamps proof (historical record) |
| `config/` | model settings and covariate definitions transcribed from the code (`configurations.json`, `MODEL_SETTINGS.md`); enrolment-epoch design records |
| `seeds/` | every random seed used |
| `splits/` | the split design as code, seeds and SHA-256 verification digests: the fixed H1/H2 split, the sequential 5-fold partition, the enrolment epochs and the cohort membership are regenerated from the public clinical workbook, not distributed as identifier tables |
| `src/` | the scripts that produced the results: feature extraction (`src/features/`), enrolment epochs, prioritization models and RATE analysis (`src/rate_analysis/`), figure data and figures (`src/figures/`) |
| `scripts/` | execution wrapper, checksum verification, split-digest verification, and a verification that recomputes the reported RATE quantities from the released per-patient scores without any source data |
| `derived_data/` | per-patient derived outputs, labelled by position rather than identifier: the common doubly robust evaluation scores and the prioritization scores of every configuration and regime |
| `results/` | machine-readable result files (JSON), results and environment records, provenance records, and the manifests of the frozen record |
| `figure_data/` | canonical figure-source data for Figures 1 to 5 (JSON and MATLAB `.mat`) |
| `figures/` | the final figures (vector PDF, 600 dpi TIFF, MATLAB `.fig`) |
| `checksums/` | sha256 manifests: this release, the input provenance of the analysis, and the frozen-record manifests |
| `environment/` | conda environment and lock files for the two Python environments; R and MATLAB versions in `environment/README.md` |
| `docs/` | reproduction guide, data-access guide, and the record of every modification relative to the frozen files |

## What is not included

- **Patient-level source data and patient identifiers.** No images, segmentations or clinical variables are
  redistributed, and no MAMA-MIA / I-SPY2 patient identifier appears in this repository. The per-patient derived
  files carry positional row labels and no outcome, treatment or covariate columns; the split, partition, epoch and
  cohort tables are regenerated from the public clinical workbook by the released code and checked against
  digests (`splits/README.md`).
- **Feature matrices** (per-patient radiomics, BiomedCLIP and RAD-DINO features). They are regenerated from the
  source images with the scripts in `src/features/`; their sha256 values are recorded in
  `checksums/INPUT_PROVENANCE.txt` so that a regeneration can be verified.
- **Manuscript submission materials** and the private development record. Earlier analyses that the corrected
  framework superseded are not part of this release.

## External data sources

The source data must be obtained from their official repositories, subject to the access conditions and terms of
use of each repository:

- **I-SPY2 TRIAL DCE-MRI collection**, The Cancer Imaging Archive (TCIA): https://doi.org/10.7937/TCIA.D8Z0-9T85
- **MAMA-MIA dataset** (expert tumour segmentations, preprocessed images and harmonized clinical variables), Synapse:
  https://doi.org/10.7303/syn60868042

`docs/DATA_ACCESS.md` gives the expected local layout, the file the clinical variables are read from
(`clinical_and_imaging_info.xlsx`, sha256 recorded), and how the cohorts, treatment and outcome are derived.

## Execution overview

| stage | scripts | environment | needs |
|---|---|---|---|
| 0. Feature extraction | `src/features/` | `environment/environment_features.yml` (PyTorch, open_clip, transformers, pyradiomics) | source images, segmentations, clinical workbook |
| 1. Enrolment epochs, prioritization models, split, evaluation covariates | `src/rate_analysis/derive_epochs.py`, `fit_priorities.py`, `build_Z.py`, `fit_priorities_sequential.py`, `fit_q3_priorities.py`, `fit_q4_priorities.py` | `environment/environment.yml` (econml 0.16.0, scikit-learn 1.6.1) | clinical workbook, feature matrices |
| 2. RATE/AUTOC | `src/rate_analysis/rate_primary.R`, `rate_sequential.R`, `rate_q3.R`, `rate_q4.R`, `crosscheck.py`, `extract_q4_contrasts.py` | R 4.5.3, grf 2.6.1, jsonlite 2.0.0 | stage-1 outputs |
| 3. Figure data and figures | `src/figures/freeze_figure_data.py`, `build_all.m` | Python; MATLAB R2025b with Arial | `results/`, `figure_data/` |

`bash scripts/run_pipeline.sh` runs the stages in order and writes everything under `reproduction/`, so the
released record is never overwritten. `docs/REPRODUCTION.md` gives the commands, the expected outputs and the
determinism notes; `python scripts/verify_split_digests.py` confirms that a regenerated split, partition and epoch
table match the digests of the record.

**Verification without source data.** `Rscript scripts/verify_rate_from_released_scores.R` recomputes every
reported RATE/AUTOC estimate and bootstrap standard error that depends only on the released per-patient scores and
priorities (Q1 primary, Q2 primary, three of the four Q2 sensitivities, all of Q3, all of Q4) with the same `grf`
call and seed, and compares them with `results/`. `bash scripts/verify_checksums.sh` verifies every released file
against `checksums/SHA256SUMS.txt`.

## Where to find items cited in the manuscript

| cited item | location in this repository |
|---|---|
| `R7_rate_primary/AMENDMENT_R7_RATE.md`, the specification of the replacement analysis | `amendments/AMENDMENT_R7_RATE.md` (sha256 `2c4fafd0…b0d13a`, as recorded in `results/rate_primary/RESULTS_R7_RATE.md`) |
| analysis plan timestamped on 2026-07-25 (historical record) | `analysis_specs/historical_prespecification_2026-07-25/` (redacted copy; the OpenTimestamps proof authenticates the original private unredacted record, not the bytes of the public copy) |
| fixed split (H1 = 370, H2 = 369) | `splits/` (generation code `src/rate_analysis/r7_common.py`, seed 42, digests in `splits/SPLIT_DIGESTS.json`) |
| per-patient priorities and common evaluation scores | `derived_data/` |
| model settings and seeds | `config/`, `seeds/` |
| result summaries behind the tables | `results/rate_primary/rate_q1_primary.json`, `rate_q2_primary.json`, `rate_q2_sensitivities.json`; `results/rate_q3/rate_q3.json`; `results/rate_q4/rate_q4_regimes.json` |
| figure-source data, Figures 1 to 5 | `figure_data/Fig1_data.json` … `Fig5_data.json` |
| input provenance | `checksums/INPUT_PROVENANCE.txt` |

## Reproducibility note

This repository corresponds to the **corrected revision analysis**: standard centred doubly robust RATE/AUTOC
(grf 2.6.1) on an independent held-out half, with the two-way Q3 and Q4 diagnostics as point-estimate
descriptions. It does not contain the retired earlier analyses.

The record documents under `results/` and `amendments/` are reproduced verbatim. Identifiers inside them, such as
Git commit hashes (for example `755aecb2`), decision numbers (for example D45a) and round labels (R7, `FROZEN_R7`),
refer to the private development record from which this release was assembled; they are kept because the documents
cite them, and they cannot be resolved here. The scripts were changed only where they hard-coded machine-specific
locations or read distributed identifier tables; `docs/CODE_MODIFICATIONS.md` lists every modified file with the
sha256 of the frozen original and of the released copy, together with the exact diff.

## License

Code is released under the MIT License; data, figures and documentation under CC BY 4.0. See `LICENSE`.
