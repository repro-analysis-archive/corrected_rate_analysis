# Software environments

## Python: analysis environment (`environment.yml`, `requirements.lock.txt`, `build_env.sh`)

Used for the prioritization models, the split, the evaluation covariates and the cross-check (stages 1 to 3).

| package | version |
|---|---|
| python | 3.12.8 |
| numpy | 2.2.3 |
| scipy | 1.15.3 |
| pandas | 2.2.3 |
| scikit-learn | 1.6.1 |
| econml | 0.16.0 |
| joblib | 1.4.2 |
| statsmodels | 0.14.6 |
| openpyxl | 3.1.5 |

## Python: feature-extraction environment (`environment_features.yml`, `requirements_features.lock.txt`, `build_env_full.sh`)

The analysis environment plus:

| package | version |
|---|---|
| pyradiomics | 3.1.1.dev111+g8ed579383, installed from `git+https://github.com/AIM-Harvard/pyradiomics.git@8ed579383b44806651c463d5e691f3b2b57522ab` (the PyPI source distribution does not build on Python 3.12 / arm64) |
| SimpleITK | 2.4.1 |
| nibabel | 5.3.2 |
| torch | 2.10.0 |
| torchvision | 0.25.0 |
| transformers | 4.57.6 |
| open_clip_torch | 3.2.0 |
| timm | 1.0.28 |
| pillow | 12.3.0 |

Model checkpoints (pinned by repository revision; weight-file hashes in `results/feature_extraction/*_PROVENANCE_RECORD.json`):

| model | repository | revision |
|---|---|---|
| BiomedCLIP | `microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224` (loaded with open_clip) | `9f341de24bfb00180f1b847274256e9b65a3a32e` |
| RAD-DINO | `microsoft/rad-dino` (transformers `AutoModel`; `AutoImageProcessor(..., use_fast = True)`) | `2ec9ca0e7a73c23aded999b844acd2f07c7e46b9` |

## R (RATE/AUTOC, stage 2)

| package | version |
|---|---|
| R | 4.5.3 |
| grf | 2.6.1 (CRAN; source tarball sha256 `826583c4af20307814045d8db02cec715b376a0eee4cbcf4e2d97df055859ac2`) |
| jsonlite | 2.0.0 |
| dependencies at run time | lmtest 0.9.40, sandwich 3.1.3, DiceKriging 1.6.1, zoo 1.9.0, Matrix 1.7.4 |

## MATLAB (figures, stage 3)

MATLAB R2025b with the Arial font available (`build_all.m` stops otherwise); figures exported with
`exportgraphics` as vector PDF and 600 dpi TIFF at the 174 mm design width.

## Hardware of the recorded runs

macOS on Apple silicon (arm64, 14 logical cores); Apple MPS was used for embedding extraction only. Run dates and
per-run records: `results/*/ENVIRONMENT_RECORD.md`.
