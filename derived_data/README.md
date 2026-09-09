# Per-patient derived outputs

These files are the per-patient quantities the reported RATE/AUTOC values are computed from: the common doubly
robust evaluation scores and the prioritization scores of every configuration and regime. They contain derived
model outputs only. Relative to the frozen originals, the patient identifier, outcome (`Y`), treatment (`T`) and
covariate columns were removed; rows are labelled by their position in the analysis frame instead (see
`splits/README.md`), so nothing in these files can be joined to the public clinical data without regenerating the
split from the source data. Numeric text and row order are unchanged. `scripts/verify_rate_from_released_scores.R`
recomputes the reported estimates from these files alone.

Row labels: `h2_row` = position within the evaluation half H2 (1 to 369); `h1_row` = position within the
development half H1 (1 to 370); `fold_row` = position within a sequential fold; all in analysis-frame order.

## rate_primary/

| file | rows | columns |
|---|---|---|
| `dr_scores_primary_heldout.csv` | 369 (H2) | `h2_row`; `e_hat` estimated P(T = 1 \| Z); `Y_hat` estimated E[Y \| Z]; `dr_score` doubly robust score Γ̂ from the H2 evaluation forest |
| `priorities_primary_heldout.csv` | 6 × 369 | `h2_row`, `configuration`, `priority` (predicted CATE from the H1-trained rule) |
| `priorities_sens_mammaprint.csv` | 2 × 369 | configurations `Clinical + MammaPrint`, `Historical reference + MammaPrint` |
| `priorities_sens_no_epoch.csv` | 2 × 369 | `Clinical only`, `Clin + Rad + BiomedCLIP` without epoch nuisance covariates |
| `priorities_sens_alt_nuisance.csv` | 2 × 369 | the same two configurations with the alternative treatment-nuisance learner |
| `priorities_sens_empty_arm.csv` | 2 × 366 | the same two configurations on the empty-arm-epoch exclusion population; `h2_row` refers to the H2 position of each retained patient (its evaluation forest and scores are not released; reproduced by the full pipeline) |
| `priorities_sequential.csv` | 6 × 591 | `seq_fold` (2 to 5), `fold_row`, `configuration`, `priority` (rule fitted on folds 1..k−1) |

## rate_q3/

| file | rows | columns |
|---|---|---|
| `dr_scores_H1.csv` | 370 (H1) | `h1_row`, `e_hat`, `Y_hat`, `dr_score` from the common imaging-free H1 evaluation forest |
| `priorities_q3_H1.csv` | 6 × 370 | `h1_row`, `configuration`, `priority_A` (rule fitted on H2), `priority_C` (rule fitted on H1 itself) |
| `priorities_q3_H2.csv` | 6 × 369 | `h2_row`, `configuration`, `priority_A` (the primary H1-trained rule, reused), `priority_C` (rule fitted on H2 itself) |

## rate_q4/

| file | rows | columns |
|---|---|---|
| `priorities_q4_H1.csv`, `priorities_q4_H2.csv` | 6 × 370, 6 × 369 | `h1_row` / `h2_row`, `configuration`, `priority_A`, `priority_D1`, `priority_D2`, `priority_B` (regimes defined in `config/MODEL_SETTINGS.md`) |

## Aligning with a regenerated run

Regenerated files under `reproduction/` carry the patient identifiers and the outcome and treatment columns (they
are produced from the source data on the user's machine). Their rows are in the same analysis-frame order, so the
released `h2_row` / `h1_row` labels correspond to the row positions of the regenerated H2 and H1 files; for the
empty-arm file, to the H2 position of each retained patient.

Configuration keys map to the manuscript labels as follows: `Clinical only`; `Clin + Radiomics` = clinical +
radiomics; `Clin + BiomedCLIP` = clinical + BiomedCLIP; `Clin + RAD-DINO` = clinical + RAD-DINO;
`Clin + Rad + BiomedCLIP` = clinical + radiomics + BiomedCLIP (historically designated reference configuration);
`Clin + Rad + RAD-DINO` = clinical + radiomics + RAD-DINO.
