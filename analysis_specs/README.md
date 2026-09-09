# Analysis specifications

| file | status |
|---|---|
| `ANALYSIS_PLAN.md` | The frozen analysis plan (final working version of the development record). It fixed the elements that the corrected analysis inherits unchanged: the corrected radiomics extraction (§7), the feature rebuild and RAD-DINO reproduction rules (§8), the HER2-positive cohort status (§9), the enrolment-epoch definition (§9a), the empty-arm-epoch sensitivity population (§9b), the six configurations (§5), and seeds and write discipline (§12). Its evaluation and inference sections (§3, §10, §11: cross-fitted evaluation, permutation testing, bootstrap inference) describe the earlier design that the amendments under `amendments/` replaced; they are retained because the amendments refer to them. Two local-directory references were removed from this copy (`docs/CODE_MODIFICATIONS.md`). |
| `historical_prespecification_2026-07-25/` | The pre-specification committed and timestamped on 2026-07-25, before any rebuilt result existed, with its OpenTimestamps proof. Historical record: it specified the earlier cross-fitted design. The released plan copy is redacted for privacy; the proof authenticates the original private unredacted record, not the bytes of the public copy (see the README in that folder). |

The definitive specification of the analysis reported in the manuscript is the set of amendments under
`amendments/`; the machine-readable settings actually used are transcribed in `config/configurations.json` and
`config/MODEL_SETTINGS.md`, and the scripts under `src/` govern where wording and code could differ.
