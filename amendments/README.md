# Protocol amendments of the corrected analysis

These three documents specify the corrected analysis. Each was committed and hashed before the analysis it
governs was executed, and each is reproduced here byte-for-byte; the sha256 of each file is the one cited in the
corresponding results and environment records under `results/`.

| file | scope | sha256 (first 16 hex) |
|---|---|---|
| `AMENDMENT_R7_RATE.md` | standard centred doubly robust RATE/AUTOC on an independent held-out half: Q1 (configuration-specific prioritization) and Q2 (paired incremental comparison), sensitivities, sequential cross-fold sensitivity | `2c4fafd07bbb80c7` |
| `AMENDMENT_R7_Q3.md` | two-way opposite-half versus same-sample evaluation-induced-optimism diagnostic (point estimates only) | `769670d37893e738` |
| `AMENDMENT_R7_Q4.md` | preprocessing-placement diagnostic, regimes A / D1 / D2 / B, both split directions (additive point-estimate contrasts) | `5d06197c3130bf30` |

Reading notes:

- The amendments refer to the rounds and frozen sets of the private development record (`R7_rate_primary/`,
  `FROZEN_R7`, `FROZEN_R4`, `R3_smoke/…`, decision numbers such as D20, D45a, D52, D53) and to internal task
  documents ("instruction of record"). Those references are retained as written; the corresponding released
  material is mapped in the top-level `README.md` ("Where to find items cited in the manuscript") and in
  `results/README.md`.
- Regime A of the Q3 diagnostic is called "honest" in the amendments and results records and "opposite-half" in
  the manuscript and figures; regime C is "apparent" or "same-sample". The quantities are identical.
- The amendments were not prospectively pre-registered; they were protocol-locked after a reproducibility audit
  and before execution, as their headers state. The pre-specification of 2026-07-25 that preceded the audit is
  kept under `analysis_specs/historical_prespecification_2026-07-25/` as a historical record.
