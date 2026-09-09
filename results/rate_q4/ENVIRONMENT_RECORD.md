# R7-Q4 environment record

**Run date (UTC):** 2026-09-06T07:38:32Z
**Amendment commit (frozen BEFORE execution):** `0f48a3349c9210df0dcf2332aaa5bbdad22466cb`
**Amendment sha256:** `5d06197c3130bf30446f6826935334d490f692ae77d9c4853d8b6ad3cca22139`
**Predecessors:** R7 `755aecb2` / `2e87fa6f`; Q3 `709a9c39` / `54881e3a`

Identical toolchain to R7 and Q3: python 3.12.8 / numpy 2.2.3 / scipy 1.15.3 / pandas 2.2.3 /
scikit-learn 1.6.1 / econml 0.16.0 / joblib 1.4.2 in `jiim-r0`; R 4.5.3 with grf 2.6.1 and
jsonlite 2.0.0. Seeds 42 (models, PCA, forests) and 20260906 (grf half-sample bootstrap, reference
only), R = 2000. 48 causal-forest fits (6 configurations x 4 regimes x 2 split directions).

## Inputs reused (read-only)
```
a373e92d704ef7c7d54eacab99e3107dfb6b8ef378aa3040441d9c70ff078ab5  R7_rate_primary/FROZEN_R7/split_739.csv
17c6a0db7532b3f1e762308b0fba3e41d97165d0e6e76313d34ca5086f7d3a8d  R7_rate_primary/FROZEN_R7/dr_scores_primary_heldout.csv
106e6cbb68b70a0882166f1efe1839fd8f72e31e2a2b32135fc067a60710c816  R7_rate_primary/FROZEN_R7/rate_q1_primary.json
1f1c3d248e73d9cffbc4481bc10129a0fd567efe352a862986bc01a85929bd66  R7_rate_q3/FROZEN_R7Q3/dr_scores_H1.csv
1aea51dbb1819789ad181c73fe99945fbdc7c9512d6d5dfe9eb57698c403e888  R7_rate_q3/FROZEN_R7Q3/rate_q3.json
```
Verification chain, run before use: each file's **working copy** matches its directory manifest,
and each **FROZEN_\* copy is byte-identical to that working copy**. Recorded explicitly because each
`SHA256SUMS.txt` was generated before its `FROZEN_*` copy existed and therefore covers the working
copies only — the sealed copies are verified by identity to them, not by an entry in the manifest.

## Frozen-set integrity, verified AFTER the run
R7_rate_primary: 41 OK, 0 FAILED
R7_rate_q3: 11 OK, 0 FAILED
FROZEN_R4: 34 OK, 0 FAILED
FROZEN_EVALBIAS: 15 OK, 0 FAILED
FROZEN_DECOMP: 19 OK, 0 FAILED
Linux 2x2 freeze: 31 OK, 0 FAILED

No file under `R7_rate_primary/`, `R7_rate_q3/` or any `FROZEN_*` set was created or modified.
No manuscript, figure or supplement file was touched.
