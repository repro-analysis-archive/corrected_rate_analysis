# R7 environment record

**Run date (UTC):** 2026-09-06T07:15:33Z
**Amendment commit (frozen BEFORE execution):** `755aecb2525365e18c7224d509dd03e12a944ac6`
**Amendment sha256:** `2c4fafd07bbb80c7485404e925ab9cbc05f3d760c6ee68d653426a02d6b0d13a`

## Hardware / OS
Darwin 25.6.0 arm64 · Mac15,10 · 14 logical cores

## Python — CATE prioritization models (unchanged `jiim-r0`, the env that produced every frozen result)
| package | version |
|---|---|
| python | 3.12.8 |
| numpy | 2.2.3 |
| scipy | 1.15.3 |
| pandas | 2.2.3 |
| sklearn | 1.6.1 |
| econml | 0.16.0 |
| joblib | 1.4.2 |

## R — standard RATE/AUTOC (NEW: installed for R7, recorded here)
| package | version | source |
|---|---|---|
| R | 4.5.3 | homebrew /opt/homebrew/bin/R |
| grf | 2.6.1 | CRAN |
| jsonlite | 2.0.0 | CRAN |
| lmtest | 0.9.40 | CRAN |
| sandwich | 3.1.3 | CRAN |
| DiceKriging | 1.6.1 | CRAN |
| zoo | 1.9.0 | CRAN |
| Matrix | 1.7.4 | CRAN |
| methods | 4.5.3 | CRAN |

grf 2.6.1 was installed from the CRAN source tarball `grf_2.6.1.tar.gz` (sha256
826583c4af20307814045d8db02cec715b376a0eee4cbcf4e2d97df055859ac2; available from the CRAN archive, not
redistributed here). Its `R/rank_average_treatment.R` is the primary source
against which the RATE definition, the half-sample bootstrap and the paired two-priority
interface were verified.

## Seeds
| use | value |
|---|---|
| 50/50 split, sequential 5-fold partition | 42 (`numpy.random.default_rng`) |
| PCA / random forests / causal forests / grf forests | 42 |
| grf half-sample bootstrap | 20260906 (R `set.seed` before every RATE call) |
| bootstrap replicates R | 2000 |

## Frozen-set integrity, verified AFTER the run
FROZEN_R4 34/34 OK · FROZEN_EVALBIAS 15/15 OK · FROZEN_DECOMP 19/19 OK ·
recovered Linux 2x2 freeze 31/31 OK · 0 FAILED. No file outside
`R7_rate_primary/` was created or modified. No manuscript or figure file was touched.
