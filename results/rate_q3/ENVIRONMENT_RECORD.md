# R7-Q3 environment record

**Run date (UTC):** 2026-09-06T07:27:22Z
**Amendment commit (frozen BEFORE execution):** `709a9c399bfa239b5eae43ab7cb48163e694e0c0`
**Amendment sha256:** `769670d37893e7387628d9b59d055a05b42290382b236b5c5793b462a5e72edf`
**Predecessor:** R7 amendment `755aecb2`, R7 results `2e87fa6f`

Identical toolchain to R7 (`R7_rate_primary/ENVIRONMENT_RECORD.md`): python 3.12.8 / numpy 2.2.3 /
scipy 1.15.3 / pandas 2.2.3 / scikit-learn 1.6.1 / econml 0.16.0 / joblib 1.4.2 in `jiim-r0`;
R 4.5.3 with grf 2.6.1 and jsonlite 2.0.0. Seeds: 42 (models, PCA, forests), 20260906 (grf
half-sample bootstrap, honest A rates only), R = 2000.

## Inputs reused from R7 (read-only)
```
a373e92d704ef7c7d54eacab99e3107dfb6b8ef378aa3040441d9c70ff078ab5  FROZEN_R7/split_739.csv
c5b8ffb2ef6965825668a5b1200cfb964ffc584749b91c98eb26eb77297457b1  FROZEN_R7/priorities_primary_heldout.csv
17c6a0db7532b3f1e762308b0fba3e41d97165d0e6e76313d34ca5086f7d3a8d  FROZEN_R7/dr_scores_primary_heldout.csv
106e6cbb68b70a0882166f1efe1839fd8f72e31e2a2b32135fc067a60710c816  FROZEN_R7/rate_q1_primary.json
a64dc9226a4fb1875a02fc8283de37418932b30c9df45e7fb8e779484e1d5125  r7_common.py
ea2a3bef826505b25a35ba1e2c640223ade4478a022882b7a5dfc81ee626111d  build_Z.py
```

## Frozen-set integrity, verified AFTER the run
R7_rate_primary manifest: 41 OK, 0 FAILED
FROZEN_R4: 34 OK, 0 FAILED
FROZEN_EVALBIAS: 15 OK, 0 FAILED
FROZEN_DECOMP: 19 OK, 0 FAILED
Linux 2x2 freeze: 31 OK, 0 FAILED

No file under `R7_rate_primary/` or any `FROZEN_*` set was created or modified. No manuscript,
figure or supplement file was touched.
