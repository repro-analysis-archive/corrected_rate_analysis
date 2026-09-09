# Code and record modifications relative to the frozen analysis record

Every released script is the file that produced the reported results, changed only where the frozen record
hard-coded machine-specific locations or read patient-identifier lists. The table lists each modified file with the
sha256 of the frozen original (as recorded in the frozen manifests, `results/*/ORIGINAL_SHA256SUMS.txt` and
`checksums/`) and of the released copy, followed by the exact unified diff. Files listed under *Released verbatim*
are byte-identical to the record. Local directories quoted in removed lines are shown as `<workspace>`, `<archive>`,
`<conda>`, `<figure-workspace>` or `<home>`.

Path resolution convention introduced by these edits:

- `JIIM_RELEASE_ROOT` (default: the repository root, derived from the script location; R scripts default to the working directory)
- `JIIM_DATA_ROOT` (default: `<repository>/external_data`) for the source data and feature matrices that are not redistributed
- all regenerated outputs are written under `<repository>/reproduction/` so that the released record is never overwritten
- cohort membership and the enrolment-epoch table are regenerated from the clinical workbook (`src/features/cohort_ids.py`,
  `src/rate_analysis/derive_epochs.py`, both added for the release) instead of being read from distributed identifier tables

## Modified files

| released file | frozen record | sha256 (record) | sha256 (released) | change |
|---|---|---|---|---|
| `analysis_specs/ANALYSIS_PLAN.md` | `ANALYSIS_PLAN.md` | `da4012df49f31316…` | `a242ef1c9ef7354e…` | Frozen plan (final working version). Two local-directory references removed; no scientific content changed. |
| `analysis_specs/historical_prespecification_2026-07-25/ANALYSIS_PLAN_as_committed_2026-07-25.md` | `OSF_UPLOAD/ANALYSIS_PLAN_as_committed_bb70d54.md` | `87a2da6275033531…` | `2c5a4d81d14dbc7f…` | Timestamped pre-specification: three workstation strings redacted (two directory names, one sync-service name); the sha256 therefore differs from the stamped value 87a2da62…; every other character is identical. |
| `results/rate_primary/ENVIRONMENT_RECORD.md` | `R7_rate_primary/ENVIRONMENT_RECORD.md` | `ea3e6a6c7517ac56…` | `47cb43e942b2aa3c…` | Environment record. One sentence edited: the retained tarball and install log are not redistributed. |
| `results/rate_q4/ENVIRONMENT_RECORD.md` | `R7_rate_q4/ENVIRONMENT_RECORD.md` | `505137f8db01751e…` | `df78ed3c1c0ceb2c…` | Environment record. Absolute local path prefixes removed from five hash lines; hashes unchanged. |
| `results/feature_extraction/r2a_biomedclip_verification.json` | `R2_features/r2a_biomedclip_verification.json` | `480e3253515144ed…` | `5d70be554d99fec6…` | Absolute local path prefix removed from two output fields. |
| `results/feature_extraction/BIOMEDCLIP_PROVENANCE_RECORD.json` | `R2_features/BIOMEDCLIP_PROVENANCE_RECORD.json` | `b3999f4cb112dfcc…` | `967f2773eee5e8f9…` | One internal editorial note (field MANUSCRIPT_DISCREPANCY, a comparison with the originally submitted supplement text) removed; all provenance fields unchanged. |
| `src/rate_analysis/r4_stageA.py` | `R4_main/FROZEN_R4/r4_stageA.py` | `2a87198a75834c3f…` | `691befda7be49a61…` | Frozen data-loader module reused by the corrected pipeline (load(), CLIN, NUIS, CONFIGS). Path resolution only; BiomedCLIP inputs named by their re-extraction filenames (byte-identical to the archived files); epoch table read from the regenerated location. |
| `src/rate_analysis/r7_common.py` | `R7_rate_primary/r7_common.py` | `a64dc9226a4fb187…` | `22781fd06dd79952…` | Path resolution only. |
| `src/rate_analysis/build_Z.py` | `R7_rate_primary/build_Z.py` | `ea2a3bef826505b2…` | `91467a7915362cf5…` | Path resolution only. |
| `src/rate_analysis/fit_priorities.py` | `R7_rate_primary/fit_priorities.py` | `49303d1b421ade38…` | `57f2682a88b80416…` | Path resolution only. |
| `src/rate_analysis/rate_primary.R` | `R7_rate_primary/rate_primary.R` | `e870d2a4f4529493…` | `1c282c0ece794c6d…` | Path resolution only. |
| `src/rate_analysis/rate_sequential.R` | `R7_rate_primary/rate_sequential.R` | `2d3e10befe21b043…` | `174625391fa6652a…` | Path resolution only. |
| `src/rate_analysis/fit_q3_priorities.py` | `R7_rate_q3/fit_q3_priorities.py` | `c0505576f5968a6c…` | `d2d34edb09b70396…` | Path resolution only. |
| `src/rate_analysis/rate_q3.R` | `R7_rate_q3/rate_q3.R` | `0d7e1639d5e494ff…` | `6cebf7902838ac9c…` | Path resolution only. |
| `src/rate_analysis/fit_q4_priorities.py` | `R7_rate_q4/fit_q4_priorities.py` | `b7d500412ba5463d…` | `d4c2f981f6cd47c4…` | Path resolution only. |
| `src/rate_analysis/rate_q4.R` | `R7_rate_q4/rate_q4.R` | `a63602fc804a4686…` | `bfd3895efd68e2ee…` | Path resolution only. |
| `src/features/r2a_biomedclip_reextract.py` | `R2_features/r2a_biomedclip_reextract.py` | `f5766313695779dd…` | `eb0eb6c966e56cd9…` | Path resolution; cohort membership derived from the workbook (cohort_ids) instead of an identifier list; the archive comparison is skipped when the original-study embeddings are absent. |
| `src/features/r2b_radiomics_reextract.py` | `R2_features/r2b_radiomics_reextract.py` | `794636f6ec8652c9…` | `744ab5d2a097d9d9…` | Path resolution; cohort membership derived from the workbook (cohort_ids). |
| `src/features/r2c_raddino_reextract.py` | `R2_features/r2c_raddino_reextract.py` | `f7f7ce99ebb919e7…` | `2056e168f326e4ef…` | Path resolution; cohort membership derived from the workbook (cohort_ids). Pooling-trial verification script; requires the original-study embeddings. |
| `src/features/r2c_usefast_test.py` | `R2_features/r2c_usefast_test.py` | `0b89da73d4187b97…` | `8bd6975ca179a70b…` | Path resolution; cohort membership derived from the workbook (cohort_ids); the archive comparison is skipped when the original-study embeddings are absent (extraction itself unchanged). This script produced the RAD-DINO features used by the analysis. |
| `src/features/roi_voxel_distribution.py` | `R2_features/roi_voxel_distribution.py` | `3209d372b9c45d5a…` | `a6b96891698e6a12…` | Path resolution; cohort membership derived from the workbook (cohort_ids). |
| `src/features/g1_qc_report.py` | `R2_features/g1_qc_report.py` | `b02d5c028c6f7c4e…` | `29d71855dd074bc2…` | Path resolution only. QC gate comparing the corrected radiomics with the original-study extraction; requires the original-study feature matrices. |
| `src/features/pca_variance_retention.py` | `R2_features/pca_variance_retention.py` | `4d322eccdfb0712e…` | `a484a66fa0d75367…` | Path resolution only. Requires the original-study feature matrices for the ORIGINAL rows. |
| `src/features/r2b_effective_bins_fix.py` | `R2_features/r2b_effective_bins_fix.py` | `c61919774c5a25b8…` | `c3b4332695da4f18…` | Path resolution; cohort membership derived from the workbook (cohort_ids). |
| `src/figures/freeze_figure_data.py` | `figure round: freeze_figure_data_r7.py` | `c0866f8d30ace107…` | `f593eee8a4c7b1be…` | Path resolution; reads the released results (single copy) and verifies them against the manifest of the frozen record; cohort and split counts taken from the provenance record because the split and epoch tables are not distributed; three descriptive label strings for regime A use the manuscript term 'opposite-half' instead of the working term 'honest' (display text only; no value is affected). |
| `src/figures/jiim_export_r7.m` | `figure round: matlab/jiim_export_r7.m` | `8000a0189c764991…` | `e80e6ff053bdf495…` | Creates the output directory if absent. |
| `src/figures/make_Fig1.m` | `figure round: matlab/make_Fig1.m` | `e611dff66e87df6a…` | `026c8e016c807b51…` | Path resolution only. |
| `src/figures/make_Fig2.m` | `figure round: matlab/make_Fig2.m` | `b97fff9117334112…` | `f0904820e512fbfe…` | Path resolution only. |
| `src/figures/make_Fig3.m` | `figure round: matlab/make_Fig3.m` | `e1f7d02a0264bbd5…` | `96f22481af4c2dee…` | Path resolution only. |
| `src/figures/make_Fig4.m` | `figure round: matlab/make_Fig4.m` | `6e84d0fe540699ca…` | `1b8bbb4d35b85ea4…` | Path resolution; the header comment uses the manuscript term 'opposite-half' (comment only). |
| `src/figures/make_Fig5.m` | `figure round: matlab/make_Fig5.m` | `85f1ee3fd9629dc1…` | `482505ea0528ab13…` | Path resolution only. |
| `figure_data/Fig1_data.json` | `figure round: canonical/Fig1_data.json` | `12e9e92c05230ab3…` | `b04ed923cbb48c79…` | Provenance paths rewritten from local absolute paths to repository-relative paths; descriptive label text for regime A changed from the working term 'honest' to the manuscript term 'opposite-half'; all plotted values unchanged. |
| `figure_data/Fig2_data.json` | `figure round: canonical/Fig2_data.json` | `8ced680185e9b0a2…` | `0958f08263e996f9…` | Provenance paths rewritten from local absolute paths to repository-relative paths; all plotted values unchanged. |
| `figure_data/Fig3_data.json` | `figure round: canonical/Fig3_data.json` | `d44841a78c6f3a55…` | `5faae2a0af6e87c0…` | Provenance paths rewritten from local absolute paths to repository-relative paths; all plotted values unchanged. |
| `figure_data/Fig4_data.json` | `figure round: canonical/Fig4_data.json` | `2abd9ccdcbd9cdda…` | `d969fb757b5bed1d…` | Provenance paths rewritten from local absolute paths to repository-relative paths; descriptive label text for regime A changed from the working term 'honest' to the manuscript term 'opposite-half'; all plotted values unchanged. |
| `figure_data/Fig5_data.json` | `figure round: canonical/Fig5_data.json` | `363453e773cfb8f3…` | `9cd45842640b9b8f…` | Provenance paths rewritten from local absolute paths to repository-relative paths; all plotted values unchanged. |
| `environment/environment.yml` | `R0_freeze_audit/env/environment.yml` | `7b5bd477172e9f79…` | `e9fe53bd49939114…` | conda `prefix:` line (local path) removed. |
| `environment/environment_features.yml` | `R0_freeze_audit/env/environment_features.yml` | `2e6bdbbc13f271b1…` | `9fe1687d4a3953c2…` | conda `prefix:` line (local path) removed. |
| `environment/build_env.sh` | `R0_freeze_audit/env/build_env.sh` | `719e2ecee2c8509f…` | `0f8555db70c9a64b…` | Local conda and output paths replaced by PATH lookups and the script directory. |
| `environment/build_env_full.sh` | `R0_freeze_audit/env/build_env_full.sh` | `c882b49454ae63e3…` | `813ef2a11246c454…` | Local conda and output paths replaced by PATH lookups and the script directory. |

## Files added for the release

- `src/rate_analysis/derive_epochs.py` — regenerates the enrolment-epoch table from the workbook by the documented rule (verified against the frozen table)
- `src/features/cohort_ids.py` — cohort membership from the workbook filter of the frozen loader
- `src/rate_analysis/extract_q4_contrasts.py` — re-serialises the Q4 contrasts file from the regimes file (the record's file was produced interactively from the same fields; byte-identical output)
- `scripts/verify_rate_from_released_scores.R`, `scripts/verify_split_digests.py`, `scripts/verify_checksums.sh`, `scripts/run_pipeline.sh` — verification and execution wrappers

## Reduced data files

- derived_data/rate_primary/dr_scores_primary_heldout.csv: from R7_rate_primary/dr_scores_primary_heldout.csv (sha256 17c6a0db7532b3f1…); patient_id replaced by `h2_row` (analysis-frame position), columns kept ['h2_row', 'e_hat', 'Y_hat', 'dr_score'], 369 rows
- derived_data/rate_primary/priorities_primary_heldout.csv: from R7_rate_primary/priorities_primary_heldout.csv (sha256 c5b8ffb2ef696582…); patient_id replaced by `h2_row` (analysis-frame position), columns kept ['h2_row', 'configuration', 'priority'], 2214 rows
- derived_data/rate_primary/priorities_sens_alt_nuisance.csv: from R7_rate_primary/priorities_sens_alt_nuisance.csv (sha256 196ff59e3aebe144…); patient_id replaced by `h2_row` (analysis-frame position), columns kept ['h2_row', 'configuration', 'priority'], 738 rows
- derived_data/rate_primary/priorities_sens_empty_arm.csv: from R7_rate_primary/priorities_sens_empty_arm.csv (sha256 d4c156cbd1f476ad…); patient_id replaced by `h2_row` (analysis-frame position), columns kept ['h2_row', 'configuration', 'priority'], 732 rows
- derived_data/rate_primary/priorities_sens_mammaprint.csv: from R7_rate_primary/priorities_sens_mammaprint.csv (sha256 5b7ccf0fd0519fb5…); patient_id replaced by `h2_row` (analysis-frame position), columns kept ['h2_row', 'configuration', 'priority'], 738 rows
- derived_data/rate_primary/priorities_sens_no_epoch.csv: from R7_rate_primary/priorities_sens_no_epoch.csv (sha256 7a965169fdeee835…); patient_id replaced by `h2_row` (analysis-frame position), columns kept ['h2_row', 'configuration', 'priority'], 738 rows
- derived_data/rate_primary/priorities_sequential.csv: from R7_rate_primary/priorities_sequential.csv (sha256 5b5a5460f606a8a2…); patient_id replaced by `fold_row` (analysis-frame position), columns kept ['seq_fold', 'fold_row', 'configuration', 'priority'], 3546 rows
- derived_data/rate_q3/dr_scores_H1.csv: from R7_rate_q3/dr_scores_H1.csv (sha256 1f1c3d248e73d9cf…); patient_id replaced by `h1_row` (analysis-frame position), columns kept ['h1_row', 'e_hat', 'Y_hat', 'dr_score'], 370 rows
- derived_data/rate_q3/priorities_q3_H1.csv: from R7_rate_q3/priorities_q3_H1.csv (sha256 a354768dbd3308df…); patient_id replaced by `h1_row` (analysis-frame position), columns kept ['h1_row', 'configuration', 'priority_A', 'priority_C'], 2220 rows
- derived_data/rate_q3/priorities_q3_H2.csv: from R7_rate_q3/priorities_q3_H2.csv (sha256 caaec537acfd6ea4…); patient_id replaced by `h2_row` (analysis-frame position), columns kept ['h2_row', 'configuration', 'priority_A', 'priority_C'], 2214 rows
- derived_data/rate_q4/priorities_q4_H1.csv: from R7_rate_q4/priorities_q4_H1.csv (sha256 15cd1383ceb20225…); patient_id replaced by `h1_row` (analysis-frame position), columns kept ['h1_row', 'configuration', 'priority_A', 'priority_D1', 'priority_D2', 'priority_B'], 2220 rows
- derived_data/rate_q4/priorities_q4_H2.csv: from R7_rate_q4/priorities_q4_H2.csv (sha256 c6581d6076131c3d…); patient_id replaced by `h2_row` (analysis-frame position), columns kept ['h2_row', 'configuration', 'priority_A', 'priority_D1', 'priority_D2', 'priority_B'], 2214 rows
- the per-file manifest of the source images and masks of the frozen record is NOT distributed: its file paths carry patient identifiers
- splits/: the split, sequential partition, epoch and cohort tables of the record are NOT distributed (they carry patient identifiers); splits/SPLIT_DIGESTS.json holds their verification digests

## Released verbatim

| released file | source of record | sha256 |
|---|---|---|
| `amendments/AMENDMENT_R7_RATE.md` | `R7_rate_primary/AMENDMENT_R7_RATE.md` | `2c4fafd07bbb80c7485404e925ab9cbc05f3d760c6ee68d653426a02d6b0d13a` |
| `amendments/AMENDMENT_R7_Q3.md` | `R7_rate_q3/AMENDMENT_R7_Q3.md` | `769670d37893e7387628d9b59d055a05b42290382b236b5c5793b462a5e72edf` |
| `amendments/AMENDMENT_R7_Q4.md` | `R7_rate_q4/AMENDMENT_R7_Q4.md` | `5d06197c3130bf30446f6826935334d490f692ae77d9c4853d8b6ad3cca22139` |
| `analysis_specs/historical_prespecification_2026-07-25/PRESPEC_STAMP.txt` | `PRESPEC_STAMP.txt` | `af1a46389c2c2f8466355a4a004edf153d270c177a0150fe7b2e231d1a51a72e` |
| `analysis_specs/historical_prespecification_2026-07-25/PRESPEC_STAMP.txt.ots` | `PRESPEC_STAMP.txt.ots` | `24b99d5e0a7905e4b1322fc52130a9f296d67e4973e5441316f7f57f1f40e741` |
| `results/rate_primary/rate_q1_primary.json` | `R7_rate_primary/rate_q1_primary.json` | `106e6cbb68b70a0882166f1efe1839fd8f72e31e2a2b32135fc067a60710c816` |
| `results/rate_primary/rate_q1_sequential_sensitivity.json` | `R7_rate_primary/rate_q1_sequential_sensitivity.json` | `99c932d39fd45574c6a8b23de7107043f91e5168509f2c3c9ee7701736097b20` |
| `results/rate_primary/rate_q2_primary.json` | `R7_rate_primary/rate_q2_primary.json` | `f52d009189cd1199ce5a7a781de8603d39ad8a0783ee071121c605ca1d4da8d6` |
| `results/rate_primary/rate_q2_sensitivities.json` | `R7_rate_primary/rate_q2_sensitivities.json` | `3ef481c0cfb9b74e2a7d3c1b073a53e01341fa551891cbb66eda66a406450ed4` |
| `results/rate_primary/rate_her2pos_not_estimated.json` | `R7_rate_primary/rate_her2pos_not_estimated.json` | `0410328de8a08e4bc2e5f050a7ad717f0ab7a143866e9fc65061e96d18140bb4` |
| `results/rate_primary/overlap_diagnostics.json` | `R7_rate_primary/overlap_diagnostics.json` | `a1b5b3295774d6bdea988c479521c3ebf843c826fc7fe61eca78e9ca244e0879` |
| `results/rate_primary/crosscheck_implementations.json` | `R7_rate_primary/crosscheck_implementations.json` | `9d80a8c790951631ad3d5044942250d4ec1f58fc4fb6bb17f7182e8d06c17a96` |
| `results/rate_primary/Z_provenance.json` | `R7_rate_primary/Z_provenance.json` | `049e6f692120e613651d821ef689192395a27629ad9cd4874759e24b8fefb38f` |
| `results/rate_primary/priorities_provenance.json` | `R7_rate_primary/priorities_provenance.json` | `5e5d18a3b717510eefeea57270d2108cd0c03793232a3a8aca3561710bc63138` |
| `results/rate_primary/priorities_sequential_provenance.json` | `R7_rate_primary/priorities_sequential_provenance.json` | `0bb7101c7fd996eae6654d5e9d880ff44e23361c4919aeaa3c05c44ac7a06d20` |
| `results/rate_primary/RESULTS_R7_RATE.md` | `R7_rate_primary/RESULTS_R7_RATE.md` | `42b03784f11ccd6a4a5da584a7800162682690012ae01187c7654dcc9cb62958` |
| `results/rate_primary/ORIGINAL_SHA256SUMS.txt` | `R7_rate_primary/SHA256SUMS.txt` | `940f20635ffbbe56696ef0c78f8dc141c386cfa303877f7db6f20387b62beee3` |
| `results/rate_q3/rate_q3.json` | `R7_rate_q3/rate_q3.json` | `1aea51dbb1819789ad181c73fe99945fbdc7c9512d6d5dfe9eb57698c403e888` |
| `results/rate_q3/q3_provenance.json` | `R7_rate_q3/q3_provenance.json` | `17c652d3410630b661d93b8b810c358a0a82e350203f580952f0b3127bf66bc7` |
| `results/rate_q3/RESULTS_R7_Q3.md` | `R7_rate_q3/RESULTS_R7_Q3.md` | `bbcb4760960cce4b520cc519f3517c4145ff574d945f07673f86083467df86ee` |
| `results/rate_q3/ENVIRONMENT_RECORD.md` | `R7_rate_q3/ENVIRONMENT_RECORD.md` | `7f9ae66e14dc5208ee84c150106bbbfb81e65a277d9cf0d0c40e9e52c7605b29` |
| `results/rate_q3/ORIGINAL_SHA256SUMS.txt` | `R7_rate_q3/SHA256SUMS.txt` | `34809ef9b536e54a3a1e0a57f78fdd8774c2a2909ad5f4bd70e4b4705c912532` |
| `results/rate_q4/rate_q4_regimes.json` | `R7_rate_q4/rate_q4_regimes.json` | `4e4b6fb65f6c86adb979b3c6e750dc7bce258a3a79a76af80c0f47e393260459` |
| `results/rate_q4/rate_q4_contrasts.json` | `R7_rate_q4/rate_q4_contrasts.json` | `4b46b2410d3ba9a8250934b96ff2e858454f93e1f0c92775ca1f6435a0e6b209` |
| `results/rate_q4/q4_provenance.json` | `R7_rate_q4/q4_provenance.json` | `0ae7e13ccadfa979660ee5e6d7a8012f0674ce9bc4d7bba9aeaeb4e2125fa066` |
| `results/rate_q4/RESULTS_R7_Q4.md` | `R7_rate_q4/RESULTS_R7_Q4.md` | `f7dc6cf6b28e86763f2e996616e00e37791f335ec3b53a73de12be51dd2008f8` |
| `results/rate_q4/ORIGINAL_SHA256SUMS.txt` | `R7_rate_q4/SHA256SUMS.txt` | `dbff05b03070b4c8c74d2e3feb16c78d3edb6baecfc8f3bf0b9e3862ffded3bd` |
| `results/feature_extraction/r2c_raddino_verification.json` | `R2_features/r2c_raddino_verification.json` | `1f87ee166df468541ab8d1ad1a4ea736d97d93fb14612eed62a4387989ef317c` |
| `results/feature_extraction/r2c_usefast_result.json` | `R2_features/r2c_usefast_result.json` | `b832f9c19c38e5fed3d0afc5f5028b333fbf08049691894a21f0d99d64b9bda4` |
| `results/feature_extraction/RADDINO_PROVENANCE_RECORD.json` | `R2_features/RADDINO_PROVENANCE_RECORD.json` | `49e02df6e13c25912800704b33cefe1463543bb96e12ab5f482bb08dcf16242f` |
| `results/feature_extraction/g1_qc_report_binCount64.json` | `R2_features/g1_qc_report_binCount64.json` | `8cf56369150eb781041e521e6a9c1f0f63cb69e831e735a06877bbde094161bb` |
| `results/feature_extraction/roi_voxel_distribution.json` | `R2_features/roi_voxel_distribution.json` | `5132a7d2d5463581908c54ac4bf07889eca7eb97c7ba3d25c41500b4c7cc9a5e` |
| `results/feature_extraction/pca_variance_retention.json` | `R2_features/pca_variance_retention.json` | `fb8e7626a1ec8ecb4149e09ab08b64d2f57b2ab1be12457c015d27f6b427bf71` |
| `results/feature_extraction/SUPPLEMENT_TABLE_radiomics_correction.md` | `R2_features/SUPPLEMENT_TABLE_radiomics_correction.md` | `6ee37f66ea252209f2d482fb4d8184a2f09fedad198adc38a9c3974613dfe93f` |
| `results/feature_extraction/r2b_extraction_meta_binCount64.json` | `R2_features/FROZEN_R2B/r2b_extraction_meta_binCount64.json` | `177584ce2f026d034164d87e60a4cedb366066d939bd1104965f004531cf94ac` |
| `results/feature_extraction/g1_feature_correlations_binCount64.csv` | `R2_features/FROZEN_R2B/g1_feature_correlations_binCount64.csv` | `bd65d730d694608eae5e0f715ed4069159e3d90d27f3a0fd9ec2e036532dfee4` |
| `results/feature_extraction/feature_names.json` | `R2_features/FROZEN_R2B/feature_names.json` | `bff5e350ee343aa8f2d6932b3f61f9bfdfc0337fdfa5d58693c0c1e394b4dcda` |
| `config/epoch_canonical_mapping.json` | `R3_smoke/epoch_canonical_mapping.json` | `7f745a7659d21ef753b7914b9c0df620c540811262f95bb6a98e26d0f8af2834` |
| `config/empty_arm_epochs.json` | `R3_smoke/empty_arm_epochs.json` | `2b37af3a0e56d4f00b636d757869a9186c61e2467125b2005c05a0af52a74531` |
| `src/rate_analysis/fit_priorities_sequential.py` | `R7_rate_primary/fit_priorities_sequential.py` | `155043baf966d572edb76b2bafbae32b7a9c7f386fbe206fdf7927ca0c6b3e7f` |
| `src/rate_analysis/crosscheck.py` | `R7_rate_primary/crosscheck.py` | `a3f076bc89214d0b3d5f8d99d4f3a1845d6f54107697ca94a48f3c2a619fc6be` |
| `src/figures/build_all.m` | `figure round: matlab/build_all.m` | `c5750e35e1761f2959d0b52d3d97acd7206c9f0de08fd835284d922f38b73cfc` |
| `src/figures/jiim_axes_r7.m` | `figure round: matlab/jiim_axes_r7.m` | `b0e1f8cfcba671069cec9a59ff32f4599956af894ef9f14a630ba9fe04a2a969` |
| `src/figures/jiim_style_r7.m` | `figure round: matlab/jiim_style_r7.m` | `a407e1a043f4068abb8ee2166e549bedcb84f5c5f784e0101826598078fe6d26` |
| `src/figures/jiim_wrap_r7.m` | `figure round: matlab/jiim_wrap_r7.m` | `2cca2180b790cea35604c537400ea67c9473309e12deebe1178c52025f0102ad` |
| `src/figures/jiim_wrap_check_r7.m` | `figure round: matlab/jiim_wrap_check_r7.m` | `9941d0c237a621cbacd4f11d0045c1c58fbcb4d1eed7ff65e72c2cbf52443e88` |
| `src/figures/jiim_ylabels_r7.m` | `figure round: matlab/jiim_ylabels_r7.m` | `39e7ce346146b3882b7cc7bd3e372c688e78c1c23aa2aeab2815f5a9c5bbd0ac` |
| `figure_data/fig_data_r7.mat` | `figure round: canonical/fig_data_r7.mat` | `eddaafcb0bac8323ac097d9c5c6777ec440ad101d605b9e31bde96c7af2db6a1` |
| `figures/Fig1.pdf` | `figure round: output/Fig1.pdf` | `a4a72419847bd1c34bd77e3c9a37aa99a1d856e3dafdfb55f9df6324689d27b7` |
| `figures/Fig1.tif` | `figure round: output/Fig1.tif` | `d17b373be551d184416f2b2e4ed9c54cebe52311ef9c624e9de86a265f810402` |
| `figures/Fig1.fig` | `figure round: output/Fig1.fig` | `eff2a91d524a5ba15eb588e0dcca8fa0d69bdd3ba8fb6ab5336f9235d8c9fd92` |
| `figures/Fig2.pdf` | `figure round: output/Fig2.pdf` | `524ea297f6114c694ef5489a1f369741ad10d07851a5644eb4509cbca55a0e68` |
| `figures/Fig2.tif` | `figure round: output/Fig2.tif` | `7f572bfab94d7eee9ce89d57e63bc3393b617d4fd8405e1f0f5dc3627179dc17` |
| `figures/Fig2.fig` | `figure round: output/Fig2.fig` | `1eb3bc829761cb817839d0813869dc12ff9a720f3e056d96fc35252dffd7d018` |
| `figures/Fig3.pdf` | `figure round: output/Fig3.pdf` | `797de4f83256bef0d31d9cd6bb379e0127449e84fe5b6819ad6ef53cbc916723` |
| `figures/Fig3.tif` | `figure round: output/Fig3.tif` | `6ca77963741fc4d4da368e7660636ed4453b9e1dab353932f77ef067535d7ccb` |
| `figures/Fig3.fig` | `figure round: output/Fig3.fig` | `0ea6f4cc52557f5e7293c13b196f273833acd93a6c65f25fd575b3ad305dd27b` |
| `figures/Fig4.pdf` | `figure round: output/Fig4.pdf` | `b56f020ff77340616c1dc8be96c5bf39d110322671d908c237ed8bca98058c88` |
| `figures/Fig4.tif` | `figure round: output/Fig4.tif` | `632d0771f22695b8e91a9b6d24096654bdbae034519a3d6bc9ef21d796f102dd` |
| `figures/Fig4.fig` | `figure round: output/Fig4.fig` | `950d1babe5ea68a468153f8ce9dcbb71648eaf2ddb64f587ecaee5cfc58fda3c` |
| `figures/Fig5.pdf` | `figure round: output/Fig5.pdf` | `f9fba7f3e95984ef7c4aff01913dca4dfb8bd588abc583d035a2221420336d3c` |
| `figures/Fig5.tif` | `figure round: output/Fig5.tif` | `a81555e74b407ce29b15b8b5fe89e4684fa339f3f0df408bf484aa5809952128` |
| `figures/Fig5.fig` | `figure round: output/Fig5.fig` | `f7c89300965fd88125ff86d83c9bc00ca431daf518e0a33da7f510adf7d9a971` |
| `environment/requirements.lock.txt` | `R0_freeze_audit/env/requirements.lock.txt` | `00fc15312ce55b0af2f8a30565526b6587812c8665ada9fd1c72a876537ea285` |
| `environment/requirements_features.lock.txt` | `R0_freeze_audit/env/requirements_features.lock.txt` | `35b2f53a45434233abe32c3fbf91b47c2b9616f862819a71644ecd061a8c76f5` |
| `checksums/original_frozen_manifests/FROZEN_R2B_SHA256SUMS.txt` | `R2_features/FROZEN_R2B/SHA256SUMS.txt` | `1be73c7c3a38ad05178415ff2d4c81ad2fa31882717ea1e4da97410546a1ea09` |
| `checksums/original_frozen_manifests/FROZEN_R2C_SHA256SUMS.txt` | `R2_features/FROZEN_R2C/SHA256SUMS.txt` | `33c336f446f41ec428f0cd7aa739df6fd68987c27ad7df75287490f225bbd583` |
| `checksums/original_frozen_manifests/FROZEN_EPOCH_SHA256SUMS.txt` | `R3_smoke/FROZEN_EPOCH/SHA256SUMS.txt` | `7e873c7e500398d56be0c8814daa4449e8252c527f36ebbd19d030280dd61252` |

## Unified diffs

### `analysis_specs/ANALYSIS_PLAN.md`

```diff
--- original/ANALYSIS_PLAN.md
+++ release/analysis_specs/ANALYSIS_PLAN.md
@@ -19,13 +19,9 @@
 
 **No rebuilt analysis had been run at that commit.** R2 may now begin.
 
-**Paths relocated 2026-07-25 [R1 §B1, §D]** — both project trees are now outside every cloud-sync
-root, because folder synchronisation reverted the archive freeze three times:
-
-| was | now |
-|---|---|
-| `~/<former-workspace>/` | **`~/JIIM_Revision/`** |
-| `~/<former-archive>/` | **`~/研究保存用/RIC_Breast/`** |
+**Paths relocated 2026-07-25 [R1 §B1, §D]** — both project trees were moved outside every cloud-sync
+root, because folder synchronisation reverted the archive freeze three times. (The table of local
+directory paths is omitted from this public copy.)
 
 Freeze verified by attempted write in the new location: create and delete both `Operation not
 permitted`; 238/238 files verify against the manifest. Earlier documents in this workspace cite the
@@ -757,7 +753,7 @@
 | 7 | 12 | Fold stratification | ✅ **RESOLVED** — keep `2·T+Y`, documented with justification |
 | 8 | 4 | `discrete_treatment` | ✅ **RESOLVED by override** — `True` primary, `False` prespecified sensitivity |
 | **A** | 4(a) | Nuisance hyperparameters | ✅ **RESOLVED [R1 §A1–A3]** — RF regressor/classifier, `n_estimators=500`, `min_samples_leaf=5`, **`max_features='sqrt'` for both** (defaults differ between the two estimators), `random_state=42`. Sensitivity isolates `discrete_treatment` only; archive not re-run. ê(x) diagnostics for both configurations including the proportion outside [0.05, 0.95]. |
-| **B** | — | Version control and third-party timestamp | ✅ **RESOLVED [R1 §B1–B2]** — repository at `~/JIIM_Revision/` (outside every sync root), snapshots excluded via `.gitignore`; commit hash, UTC time and third-party timestamp recorded in the header above. |
+| **B** | — | Version control and third-party timestamp | ✅ **RESOLVED [R1 §B1–B2]** — repository kept outside every sync root, snapshots excluded via `.gitignore`; commit hash, UTC time and third-party timestamp recorded in the header above. |
 | **C** | 9 | **HER2+ CI width is measured on the archived (in-sample) run.** The 0.431 figure comes from the Option-B bootstrap. The strict-OOF CI will differ and is not yet known. The 0.40 threshold is retained as fixed; noting only that the *expectation* it fires rests on an in-sample precedent. | ⬜ informational |
 
 ---
```

### `analysis_specs/historical_prespecification_2026-07-25/ANALYSIS_PLAN_as_committed_2026-07-25.md`

```diff
--- original/ANALYSIS_PLAN_as_committed_bb70d54.md
+++ release/analysis_specs/historical_prespecification_2026-07-25/ANALYSIS_PLAN_as_committed_2026-07-25.md
@@ -15,12 +15,12 @@
 **Nothing is re-analysed until that commit exists.**
 
 **Paths relocated 2026-07-25 [R1 §B1, §D]** — both project trees are now outside every cloud-sync
-root, because folder synchronisation reverted the archive freeze three times:
+root, because folder synchronisation reverted the archive freeze three times:
 
 | was | now |
 |---|---|
-| `~/<former-workspace>/` | **`~/JIIM_Revision/`** |
-| `~/<former-archive>/` | **`~/研究保存用/RIC_Breast/`** |
+| `~/<former-workspace>/` | **`~/JIIM_Revision/`** |
+| `~/<former-archive>/` | **`~/研究保存用/RIC_Breast/`** |
 
 Freeze verified by attempted write in the new location: create and delete both `Operation not
 permitted`; 238/238 files verify against the manifest. Earlier documents in this workspace cite the
```

### `results/rate_primary/ENVIRONMENT_RECORD.md`

```diff
--- original/ENVIRONMENT_RECORD.md
+++ release/results/rate_primary/ENVIRONMENT_RECORD.md
@@ -31,9 +31,9 @@
 | Matrix | 1.7.4 | CRAN |
 | methods | 4.5.3 | CRAN |
 
-grf 2.6.1 was installed from the CRAN source tarball retained at
-`logs/grf_2.6.1_src.tar.gz` (sha256 826583c4af20307814045d8db02cec715b376a0eee4cbcf4e2d97df055859ac2).
-Build log: `logs/grf_install.log`. Its `R/rank_average_treatment.R` is the primary source
+grf 2.6.1 was installed from the CRAN source tarball `grf_2.6.1.tar.gz` (sha256
+826583c4af20307814045d8db02cec715b376a0eee4cbcf4e2d97df055859ac2; available from the CRAN archive, not
+redistributed here). Its `R/rank_average_treatment.R` is the primary source
 against which the RATE definition, the half-sample bootstrap and the paired two-priority
 interface were verified.
 
```

### `results/rate_q4/ENVIRONMENT_RECORD.md`

```diff
--- original/ENVIRONMENT_RECORD.md
+++ release/results/rate_q4/ENVIRONMENT_RECORD.md
@@ -12,11 +12,11 @@
 
 ## Inputs reused (read-only)
 ```
-a373e92d704ef7c7d54eacab99e3107dfb6b8ef378aa3040441d9c70ff078ab5  <workspace>/R7_rate_primary/FROZEN_R7/split_739.csv
-17c6a0db7532b3f1e762308b0fba3e41d97165d0e6e76313d34ca5086f7d3a8d  <workspace>/R7_rate_primary/FROZEN_R7/dr_scores_primary_heldout.csv
-106e6cbb68b70a0882166f1efe1839fd8f72e31e2a2b32135fc067a60710c816  <workspace>/R7_rate_primary/FROZEN_R7/rate_q1_primary.json
-1f1c3d248e73d9cffbc4481bc10129a0fd567efe352a862986bc01a85929bd66  <workspace>/R7_rate_q3/FROZEN_R7Q3/dr_scores_H1.csv
-1aea51dbb1819789ad181c73fe99945fbdc7c9512d6d5dfe9eb57698c403e888  <workspace>/R7_rate_q3/FROZEN_R7Q3/rate_q3.json
+a373e92d704ef7c7d54eacab99e3107dfb6b8ef378aa3040441d9c70ff078ab5  R7_rate_primary/FROZEN_R7/split_739.csv
+17c6a0db7532b3f1e762308b0fba3e41d97165d0e6e76313d34ca5086f7d3a8d  R7_rate_primary/FROZEN_R7/dr_scores_primary_heldout.csv
+106e6cbb68b70a0882166f1efe1839fd8f72e31e2a2b32135fc067a60710c816  R7_rate_primary/FROZEN_R7/rate_q1_primary.json
+1f1c3d248e73d9cffbc4481bc10129a0fd567efe352a862986bc01a85929bd66  R7_rate_q3/FROZEN_R7Q3/dr_scores_H1.csv
+1aea51dbb1819789ad181c73fe99945fbdc7c9512d6d5dfe9eb57698c403e888  R7_rate_q3/FROZEN_R7Q3/rate_q3.json
 ```
 Verification chain, run before use: each file's **working copy** matches its directory manifest,
 and each **FROZEN_\* copy is byte-identical to that working copy**. Recorded explicitly because each
```

### `results/feature_extraction/r2a_biomedclip_verification.json`

```diff
--- original/r2a_biomedclip_verification.json
+++ release/results/feature_extraction/r2a_biomedclip_verification.json
@@ -34,7 +34,7 @@
    "pca30_spearman_median": 1.0,
    "pca30_components_below_0.99": 0,
    "elapsed_s": 60.5,
-   "output": "<workspace>/R2_features/biomedclip_her2neg_reextract_20260725.csv",
+   "output": "biomedclip_her2neg_reextract_20260725.csv",
    "PASS_median_cosine_ge_0.99999": true,
    "PASS_min_cosine_ge_0.9999": true,
    "PASS_maxabs_le_1e-4": true,
@@ -70,7 +70,7 @@
    "pca30_spearman_median": 1.0,
    "pca30_components_below_0.99": 0,
    "elapsed_s": 20.1,
-   "output": "<workspace>/R2_features/biomedclip_her2pos_reextract_20260725.csv",
+   "output": "biomedclip_her2pos_reextract_20260725.csv",
    "PASS_median_cosine_ge_0.99999": true,
    "PASS_min_cosine_ge_0.9999": true,
    "PASS_maxabs_le_1e-4": true,
```

### `src/rate_analysis/r4_stageA.py`

```diff
--- original/r4_stageA.py
+++ release/src/rate_analysis/r4_stageA.py
@@ -20,8 +20,13 @@
 from joblib import Parallel, delayed
 import warnings; warnings.filterwarnings("ignore")
 
-ROOT=os.path.expanduser("~/mama_mia"); R2=os.path.expanduser("~/JIIM_Revision/R2_features")
-R3=os.path.expanduser("~/JIIM_Revision/R3_smoke"); R4=os.path.expanduser("~/JIIM_Revision/R4_main")
+# --- public-release path resolution (the only edits relative to the frozen module; see docs/CODE_MODIFICATIONS.md) ---
+RELEASE_ROOT=os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
+DATA=os.environ.get("JIIM_DATA_ROOT", os.path.join(RELEASE_ROOT, "external_data"))   # source data and feature matrices (not redistributed)
+ROOT=os.path.join(DATA, "features"); R2=os.path.join(DATA, "features")
+R3=os.path.join(RELEASE_ROOT, "reproduction", "splits")   # epoch assignment regenerated by derive_epochs.py
+R4=os.path.join(RELEASE_ROOT, "reproduction", "r4_legacy")
+CLINICAL_XLSX=os.path.join(DATA, "clinical_and_imaging_info.xlsx")
 SEED=42; K=5; NBOOT=2000; PLAN="fdf7e35"
 CLIN=["age","tumor_subtype_enc","ethnicity_enc","bmi_group_enc","menopause_enc"]
 NUIS=dict(n_estimators=500,min_samples_leaf=5,max_features="sqrt",random_state=SEED)
@@ -29,16 +34,16 @@
 
 def load(cohort):
     hv,ctrl=COH[cohort]
-    df=pd.read_excel(os.path.expanduser("~/clinical_and_imaging_info.xlsx"))
+    df=pd.read_excel(CLINICAL_XLSX)
     c=df[df.dataset=="ISPY2"]; c=c[c.her2==hv].dropna(subset=["pcr"]).copy()
     c["T"]=(c.nac_agent!=ctrl).astype(int); c["age"]=c.age.fillna(c.age.median())
     for x in ["bmi_group","menopause","ethnicity"]: c[x]=c[x].fillna("unknown")
     for x in ["tumor_subtype","ethnicity","bmi_group","menopause"]:
         c[x+"_enc"]=LabelEncoder().fit_transform(c[x].astype(str))
-    c=c.merge(pd.read_csv(f"{R3}/FROZEN_EPOCH/epoch_assignment.csv")[["patient_id","epoch"]],on="patient_id")
-    rad=pd.read_csv(f"{R2}/FROZEN_R2B/radiomics_{cohort}_binCount64_20260725.csv")
-    clip=pd.read_csv(f"{ROOT}/biomedclip_embeddings_739.csv" if cohort=="her2neg" else f"{ROOT}/biomedclip_her2pos.csv")
-    dino=pd.read_csv(f"{R2}/FROZEN_R2C/raddino_{cohort}_reextract_cls_usefast_20260725.csv")
+    c=c.merge(pd.read_csv(f"{R3}/epoch_assignment.csv")[["patient_id","epoch"]],on="patient_id")
+    rad=pd.read_csv(f"{R2}/radiomics_{cohort}_binCount64_20260725.csv")
+    clip=pd.read_csv(f"{ROOT}/biomedclip_her2neg_reextract_20260725.csv" if cohort=="her2neg" else f"{ROOT}/biomedclip_her2pos_reextract_20260725.csv")
+    dino=pd.read_csv(f"{R2}/raddino_{cohort}_reextract_cls_usefast_20260725.csv")
     c=c.merge(rad,on="patient_id").merge(clip,on="patient_id",suffixes=("","_c")).merge(dino,on="patient_id",suffixes=("","_d"))
     cols={"rad":[x for x in rad.columns if x!="patient_id"],
           "clip":[x for x in clip.columns if x!="patient_id"],
@@ -126,8 +131,9 @@
     return res
 
 if __name__=="__main__":
+    os.makedirs(R4,exist_ok=True)   # legacy stage-A entry point; not part of the released pipeline
     runs=[]
-    empty=set(pd.read_csv(f"{R3}/FROZEN_EPOCH/epoch_assignment.csv").query("epoch in [1,21]").patient_id)
+    empty=set(pd.read_csv(f"{R3}/epoch_assignment.csv").query("epoch in [1,21]").patient_id)
     for coh in ["her2neg","her2pos"]:
         pop="full_"+coh
         runs.append(("PRIMARY",coh,pop,dict(use_W=True,discrete=True,drop_ids=None)))
```

### `src/rate_analysis/r7_common.py`

```diff
--- original/r7_common.py
+++ release/src/rate_analysis/r7_common.py
@@ -2,13 +2,15 @@
 merge order and row order are bit-identical to the frozen R4 pipeline. INPUT ONLY."""
 import os, sys, json, hashlib
 import numpy as np, pandas as pd
-sys.path.insert(0, os.path.expanduser("~/JIIM_Revision/R4_main/FROZEN_R4"))
+sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # the frozen loader module ships alongside
 import r4_stageA as r4a                      # frozen module; __main__ block not executed
 
 SEED     = 42          # model / PCA / split seed, unchanged from R4
 BOOTSEED = 20260906    # grf half-sample bootstrap seed, R7-specific
 R_BOOT   = 2000
-OUT      = os.path.expanduser("~/JIIM_Revision/R7_rate_primary")
+RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
+OUT      = os.path.join(RELEASE_ROOT, "reproduction", "rate_primary"); os.makedirs(OUT, exist_ok=True)
+EPOCH_CSV = os.path.join(RELEASE_ROOT, "reproduction", "splits", "epoch_assignment.csv")   # regenerated by derive_epochs.py
 CLIN     = r4a.CLIN
 NUIS     = r4a.NUIS
 CONFIGS  = r4a.CONFIGS
```

### `src/rate_analysis/build_Z.py`

```diff
--- original/build_Z.py
+++ release/src/rate_analysis/build_Z.py
@@ -61,8 +61,7 @@
     Z, m = build_Z(c, te); meta["primary_eval_369"] = m
     Z.assign(patient_id=c.patient_id.values[te], T=T[te], Y=Y[te]).to_csv(f"{OUT}/Z_eval_primary.csv", index=False)
     # (b) empty-arm sensitivity evaluation subset
-    empty = set(pd.read_csv(os.path.expanduser(
-        "~/JIIM_Revision/R3_smoke/FROZEN_EPOCH/epoch_assignment.csv")).query("epoch in [1,21]").patient_id)
+    empty = set(pd.read_csv(EPOCH_CSV).query("epoch in [1,21]").patient_id)
     keep = ~c.patient_id.isin(empty).values
     te2 = np.where((~is_train) & keep)[0]
     Z2, m2 = build_Z(c, te2); meta["empty_arm_eval_366"] = m2
```

### `src/rate_analysis/fit_priorities.py`

```diff
--- original/fit_priorities.py
+++ release/src/rate_analysis/fit_priorities.py
@@ -84,8 +84,7 @@
     d4, m4, *_ = run("ALT_NUISANCE", "her2neg", SUB, discrete=False)
     d4.to_csv(f"{OUT}/priorities_sens_alt_nuisance.csv", index=False); allmeta["ALT_NUISANCE"] = m4
 
-    empty = set(pd.read_csv(os.path.expanduser(
-        "~/JIIM_Revision/R3_smoke/FROZEN_EPOCH/epoch_assignment.csv")).query("epoch in [1,21]").patient_id)
+    empty = set(pd.read_csv(EPOCH_CSV).query("epoch in [1,21]").patient_id)
     d5, m5, *_ = run("EMPTY_ARM_728", "her2neg", SUB, drop_ids=empty)
     d5.to_csv(f"{OUT}/priorities_sens_empty_arm.csv", index=False); allmeta["EMPTY_ARM_728"] = m5
 
```

### `src/rate_analysis/rate_primary.R`

```diff
--- original/rate_primary.R
+++ release/src/rate_analysis/rate_primary.R
@@ -2,7 +2,8 @@
 # R7 step 3 - standard centred doubly robust RATE/AUTOC (grf 2.6.1).
 # Common evaluation forest on imaging-free Z, held-out evaluation half only.
 suppressPackageStartupMessages({library(grf); library(jsonlite)})
-OUT <- path.expand("~/JIIM_Revision/R7_rate_primary")
+RELEASE_ROOT <- Sys.getenv("JIIM_RELEASE_ROOT", unset = getwd())   # run from the repository root, or set JIIM_RELEASE_ROOT
+OUT <- file.path(RELEASE_ROOT, "reproduction", "rate_primary"); dir.create(OUT, recursive = TRUE, showWarnings = FALSE)
 SEED <- 42; BOOTSEED <- 20260906; RB <- 2000
 REFERENCE <- "Clin + Rad + BiomedCLIP"; BASELINE <- "Clinical only"
 
```

### `src/rate_analysis/rate_sequential.R`

```diff
--- original/rate_sequential.R
+++ release/src/rate_analysis/rate_sequential.R
@@ -1,7 +1,8 @@
 #!/usr/bin/env Rscript
 # R7 step 5 - Q1-ONLY sequential cross-fold sensitivity (grf RATE-CV aggregation).
 suppressPackageStartupMessages({library(grf); library(jsonlite)})
-OUT <- path.expand("~/JIIM_Revision/R7_rate_primary")
+RELEASE_ROOT <- Sys.getenv("JIIM_RELEASE_ROOT", unset = getwd())   # run from the repository root, or set JIIM_RELEASE_ROOT
+OUT <- file.path(RELEASE_ROOT, "reproduction", "rate_primary"); dir.create(OUT, recursive = TRUE, showWarnings = FALSE)
 SEED <- 42; BOOTSEED <- 20260906; RB <- 2000
 cfgs <- c("Clinical only","Clin + Radiomics","Clin + BiomedCLIP","Clin + RAD-DINO",
           "Clin + Rad + BiomedCLIP","Clin + Rad + RAD-DINO")
```

### `src/rate_analysis/fit_q3_priorities.py`

```diff
--- original/fit_q3_priorities.py
+++ release/src/rate_analysis/fit_q3_priorities.py
@@ -3,9 +3,10 @@
 A_H2 is reused verbatim from the frozen R7 output. C_H2, A_H1, C_H1 are new fits.
 The retired bespoke autoc() is never computed."""
 import os, sys, json, time, hashlib
-R7 = os.path.expanduser("~/JIIM_Revision/R7_rate_primary")
-OUT3 = os.path.expanduser("~/JIIM_Revision/R7_rate_q3")
-sys.path.insert(0, R7)
+RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
+R7 = os.path.join(RELEASE_ROOT, "reproduction", "rate_primary")     # primary-stage outputs (the frozen R7 set in the original run)
+OUT3 = os.path.join(RELEASE_ROOT, "reproduction", "rate_q3"); os.makedirs(OUT3, exist_ok=True)
+sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
 from r7_common import *                                   # frozen R7 loader + constants
 from build_Z import build_Z                               # frozen R7 Z spec, unmodified
 from sklearn.preprocessing import StandardScaler
@@ -13,7 +14,7 @@
 from sklearn.decomposition import PCA
 from econml.dml import CausalForestDML
 import warnings; warnings.filterwarnings("ignore")
-FZ = f"{R7}/FROZEN_R7"
+FZ = R7
 
 def make_cf():
     return CausalForestDML(model_y=RandomForestRegressor(**NUIS),
```

### `src/rate_analysis/rate_q3.R`

```diff
--- original/rate_q3.R
+++ release/src/rate_analysis/rate_q3.R
@@ -2,8 +2,9 @@
 # R7-Q3 - two-way honest-vs-apparent RATE/AUTOC optimism diagnostic. POINT ESTIMATES for C.
 # grf bootstrap SEs are retained for the HONEST A rates only and are labelled as such.
 suppressPackageStartupMessages({library(grf); library(jsonlite)})
-R7  <- path.expand("~/JIIM_Revision/R7_rate_primary"); FZ <- file.path(R7, "FROZEN_R7")
-OUT <- path.expand("~/JIIM_Revision/R7_rate_q3")
+RELEASE_ROOT <- Sys.getenv("JIIM_RELEASE_ROOT", unset = getwd())   # run from the repository root, or set JIIM_RELEASE_ROOT
+R7  <- file.path(RELEASE_ROOT, "reproduction", "rate_primary"); FZ <- R7   # primary-stage outputs (the frozen R7 set in the original run)
+OUT <- file.path(RELEASE_ROOT, "reproduction", "rate_q3"); dir.create(OUT, recursive = TRUE, showWarnings = FALSE)
 SEED <- 42; BOOTSEED <- 20260906; RB <- 2000
 cfgs <- c("Clinical only","Clin + Radiomics","Clin + BiomedCLIP","Clin + RAD-DINO",
           "Clin + Rad + BiomedCLIP","Clin + Rad + RAD-DINO")
```

### `src/rate_analysis/fit_q4_priorities.py`

```diff
--- original/fit_q4_priorities.py
+++ release/src/rate_analysis/fit_q4_priorities.py
@@ -3,16 +3,17 @@
 The causal forest is ALWAYS fitted on the training (opposite) half. Only unsupervised
 preprocessing placement varies. Held-out Y and T never enter any fit. autoc() is never called."""
 import os, sys, json, time
-R7  = os.path.expanduser("~/JIIM_Revision/R7_rate_primary")
-OUT4 = os.path.expanduser("~/JIIM_Revision/R7_rate_q4")
-sys.path.insert(0, R7)
+RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
+R7  = os.path.join(RELEASE_ROOT, "reproduction", "rate_primary")     # primary-stage outputs (the frozen R7 set in the original run)
+OUT4 = os.path.join(RELEASE_ROOT, "reproduction", "rate_q4"); os.makedirs(OUT4, exist_ok=True)
+sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
 from r7_common import *
 from sklearn.preprocessing import StandardScaler
 from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
 from sklearn.decomposition import PCA
 from econml.dml import CausalForestDML
 import warnings; warnings.filterwarnings("ignore")
-FZ = f"{R7}/FROZEN_R7"
+FZ = R7
 REGIMES = {"A": (False, False), "D1": (True, False), "D2": (False, True), "B": (True, True)}  # (img_full, clin_full)
 
 def regime(c, cols, W, blocks, T, Y, tr, te, img_full, clin_full):
```

### `src/rate_analysis/rate_q4.R`

```diff
--- original/rate_q4.R
+++ release/src/rate_analysis/rate_q4.R
@@ -2,8 +2,9 @@
 # R7-Q4 - standard RATE/AUTOC point estimates for regimes A/D1/D2/B in both split directions.
 # Additive point-estimate contrasts. NO variance ratios, no exponentiation, no confirmatory p-values.
 suppressPackageStartupMessages({library(grf); library(jsonlite)})
-R7 <- path.expand("~/JIIM_Revision/R7_rate_primary"); Q3 <- path.expand("~/JIIM_Revision/R7_rate_q3")
-OUT <- path.expand("~/JIIM_Revision/R7_rate_q4")
+RELEASE_ROOT <- Sys.getenv("JIIM_RELEASE_ROOT", unset = getwd())   # run from the repository root, or set JIIM_RELEASE_ROOT
+R7 <- file.path(RELEASE_ROOT, "reproduction", "rate_primary"); Q3 <- file.path(RELEASE_ROOT, "reproduction", "rate_q3")   # outputs of the earlier stages
+OUT <- file.path(RELEASE_ROOT, "reproduction", "rate_q4"); dir.create(OUT, recursive = TRUE, showWarnings = FALSE)
 BOOTSEED <- 20260906; RB <- 2000
 cfgs <- c("Clinical only","Clin + Radiomics","Clin + BiomedCLIP","Clin + RAD-DINO",
           "Clin + Rad + BiomedCLIP","Clin + Rad + RAD-DINO")
@@ -12,8 +13,8 @@
   r <- rank_average_treatment_effect.fit(G, s, target = "AUTOC", R = RB)
   c(as.numeric(r$estimate), as.numeric(r$std.err)) }
 
-drH2 <- read.csv(file.path(R7, "FROZEN_R7/dr_scores_primary_heldout.csv"))   # frozen R7
-drH1 <- read.csv(file.path(Q3, "FROZEN_R7Q3/dr_scores_H1.csv"))              # frozen Q3
+drH2 <- read.csv(file.path(R7, "dr_scores_primary_heldout.csv"))   # frozen R7
+drH1 <- read.csv(file.path(Q3, "dr_scores_H1.csv"))              # frozen Q3
 p2 <- read.csv(file.path(OUT, "priorities_q4_H2.csv"))
 p1 <- read.csv(file.path(OUT, "priorities_q4_H1.csv"))
 stopifnot(identical(as.character(drH2$patient_id), as.character(p2$patient_id[p2$configuration == cfgs[1]])),
@@ -21,8 +22,8 @@
 G <- list(H1 = drH1$dr_score, H2 = drH2$dr_score); P <- list(H1 = p1, H2 = p2)
 nH <- c(H1 = nrow(drH1), H2 = nrow(drH2))
 
-fz_q1 <- fromJSON(file.path(R7, "FROZEN_R7/rate_q1_primary.json"))$q1
-fz_q3 <- fromJSON(file.path(Q3, "FROZEN_R7Q3/rate_q3.json"))
+fz_q1 <- fromJSON(file.path(R7, "rate_q1_primary.json"))$q1
+fz_q3 <- fromJSON(file.path(Q3, "rate_q3.json"))
 est <- se <- array(NA_real_, c(length(cfgs), 4, 2), dimnames = list(cfgs, rgs, c("H1","H2")))
 chk <- c(A_H2 = 0, A_H1 = 0)
 for (h in c("H1","H2")) for (cg in cfgs) {
```

### `src/features/r2a_biomedclip_reextract.py`

```diff
--- original/r2a_biomedclip_reextract.py
+++ release/src/features/r2a_biomedclip_reextract.py
@@ -22,16 +22,18 @@
 import torch
 import open_clip
 
-ROOT = os.path.expanduser("~/mama_mia")
-IMG, SEG = f"{ROOT}/images", f"{ROOT}/segmentations"
-OUT = os.path.expanduser("~/JIIM_Revision/R2_features")
+RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
+DATA = os.environ.get("JIIM_DATA_ROOT", os.path.join(RELEASE_ROOT, "external_data"))   # source data and feature matrices (not redistributed)
+CLINICAL_XLSX = os.path.join(DATA, "clinical_and_imaging_info.xlsx")
+import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from cohort_ids import cohort_ids   # cohorts derived from the workbook; no identifier list is distributed
+IMG, SEG = f"{DATA}/images", f"{DATA}/segmentations"
+OUT = f"{DATA}/features"
 os.makedirs(OUT, exist_ok=True)
 
-ARCHIVE = {"her2neg": f"{ROOT}/biomedclip_embeddings_739.csv",
-           "her2pos": f"{ROOT}/biomedclip_her2pos.csv"}
-# canonical cohort definition — explicit ID lists, NOT os.listdir
-CANON = {"her2neg": f"{ROOT}/radiomics_all739.csv",
-         "her2pos": f"{ROOT}/radiomics_her2pos.csv"}
+# archived embeddings of the original study: comparison targets only, not redistributed (comparison is skipped if absent)
+ARCHIVE = {"her2neg": f"{DATA}/archive/biomedclip_embeddings_739.csv",
+           "her2pos": f"{DATA}/archive/biomedclip_her2pos.csv"}
+# cohort membership: derived from the clinical workbook by cohort_ids(); no identifier list is read or distributed
 
 device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
 print(f"Device: {device}", flush=True)
@@ -65,10 +67,11 @@
           "cohort_source": "explicit canonical ID lists (H7 fix)", "cohorts": {}}
 
 for coh in ("her2neg", "her2pos"):
-    ids = list(pd.read_csv(CANON[coh], usecols=["patient_id"])["patient_id"])
-    arch = pd.read_csv(ARCHIVE[coh])
-    cols = [c for c in arch.columns if c != "patient_id"]
-    print(f"\n=== {coh}: {len(ids)} patients (canonical), archive {arch.shape} ===", flush=True)
+    ids = cohort_ids(coh, CLINICAL_XLSX)
+    have_archive = os.path.exists(ARCHIVE[coh])          # public release: comparison only if the archive is present
+    arch = pd.read_csv(ARCHIVE[coh]) if have_archive else None
+    cols = [c for c in arch.columns if c != "patient_id"] if have_archive else None
+    print(f"\n=== {coh}: {len(ids)} patients (canonical), archive {arch.shape if have_archive else "not available"} ===", flush=True)
 
     rows, failed, t0 = [], [], time.time()
     for i, pid in enumerate(ids):
@@ -85,6 +88,11 @@
 
     newpath = f"{OUT}/biomedclip_{coh}_reextract_20260725.csv"
     new.to_csv(newpath, index=False)
+    if not have_archive:
+        report["cohorts"][coh] = {"n_canonical": len(ids), "n_extracted": int(len(new)), "n_failed": len(failed),
+                                  "failures": failed[:10], "elapsed_s": round(dt, 1), "output": newpath,
+                                  "comparison": "SKIPPED: archived embeddings of the original study not available"}
+        continue
 
     # ---- comparison ----
     a = arch.set_index("patient_id").loc[new["patient_id"]]        # align archive to new order
```

### `src/features/r2b_radiomics_reextract.py`

```diff
--- original/r2b_radiomics_reextract.py
+++ release/src/features/r2b_radiomics_reextract.py
@@ -22,10 +22,13 @@
 radiomics.logger.setLevel(logging.ERROR)
 import warnings; warnings.filterwarnings("ignore")
 
-ROOT = os.path.expanduser("~/mama_mia")
-IMG, SEG = f"{ROOT}/images", f"{ROOT}/segmentations"
-OUT = os.path.expanduser("~/JIIM_Revision/R2_features")
-CANON = {"her2neg": f"{ROOT}/radiomics_all739.csv", "her2pos": f"{ROOT}/radiomics_her2pos.csv"}
+RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
+DATA = os.environ.get("JIIM_DATA_ROOT", os.path.join(RELEASE_ROOT, "external_data"))   # source data and feature matrices (not redistributed)
+CLINICAL_XLSX = os.path.join(DATA, "clinical_and_imaging_info.xlsx")
+import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from cohort_ids import cohort_ids   # cohorts derived from the workbook; no identifier list is distributed
+IMG, SEG = f"{DATA}/images", f"{DATA}/segmentations"
+OUT = f"{DATA}/features"; os.makedirs(OUT, exist_ok=True)
+# cohort membership: derived from the clinical workbook by cohort_ids(); no identifier list is read or distributed
 
 BIN_COUNT = int(sys.argv[1]) if len(sys.argv) > 1 else 64
 SETTINGS = {
@@ -57,8 +60,8 @@
 
 
 allrows, allbins, failed = {}, [], {}
-for coh, canon in CANON.items():
-    ids = list(pd.read_csv(canon, usecols=["patient_id"])["patient_id"])
+for coh in ("her2neg", "her2pos"):
+    ids = cohort_ids(coh, CLINICAL_XLSX)
     print(f"\n=== {coh}: {len(ids)} patients (canonical) ===", flush=True)
     rows, fails, t0 = [], [], time.time()
     for i, pid in enumerate(ids):
```

### `src/features/r2c_raddino_reextract.py`

```diff
--- original/r2c_raddino_reextract.py
+++ release/src/features/r2c_raddino_reextract.py
@@ -28,12 +28,16 @@
 import torch
 from transformers import AutoImageProcessor, AutoModel
 
-ROOT = os.path.expanduser("~/mama_mia")
-IMG, SEG = f"{ROOT}/images", f"{ROOT}/segmentations"
-OUT = os.path.expanduser("~/JIIM_Revision/R2_features")
+RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
+DATA = os.environ.get("JIIM_DATA_ROOT", os.path.join(RELEASE_ROOT, "external_data"))   # source data and feature matrices (not redistributed)
+CLINICAL_XLSX = os.path.join(DATA, "clinical_and_imaging_info.xlsx")
+import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from cohort_ids import cohort_ids   # cohorts derived from the workbook; no identifier list is distributed
+IMG, SEG = f"{DATA}/images", f"{DATA}/segmentations"
+OUT = f"{DATA}/features"; os.makedirs(OUT, exist_ok=True)
 REPO, REV = "microsoft/rad-dino", "2ec9ca0e7a73c23aded999b844acd2f07c7e46b9"
-ARCHIVE = {"her2neg": f"{ROOT}/raddino_embeddings_739.csv", "her2pos": f"{ROOT}/raddino_her2pos.csv"}
-CANON = {"her2neg": f"{ROOT}/radiomics_all739.csv", "her2pos": f"{ROOT}/radiomics_her2pos.csv"}
+# archived embeddings of the original study (comparison targets, not redistributed): this verification script requires them
+ARCHIVE = {"her2neg": f"{DATA}/archive/raddino_embeddings_739.csv", "her2pos": f"{DATA}/archive/raddino_her2pos.csv"}
+# cohort membership: derived from the clinical workbook by cohort_ids(); no identifier list is read or distributed
 
 device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")   # transcript: mps
 print(f"Device: {device}", flush=True)
@@ -98,7 +102,7 @@
           "pooling_trial_order": ["cls", "mean_patch", "pooler"], "cohorts": {}}
 
 for coh in ("her2neg", "her2pos"):
-    ids = list(pd.read_csv(CANON[coh], usecols=["patient_id"])["patient_id"])
+    ids = cohort_ids(coh, CLINICAL_XLSX)
     arch = pd.read_csv(ARCHIVE[coh]).set_index("patient_id").loc[ids]
     cols = list(arch.columns)
     A = arch.values.astype(np.float64)
```

### `src/features/r2c_usefast_test.py`

```diff
--- original/r2c_usefast_test.py
+++ release/src/features/r2c_usefast_test.py
@@ -29,11 +29,16 @@
 import torch
 from transformers import AutoImageProcessor, AutoModel
 
-ROOT = os.path.expanduser("~/mama_mia")
-OUT = os.path.expanduser("~/JIIM_Revision/R2_features")
+RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
+DATA = os.environ.get("JIIM_DATA_ROOT", os.path.join(RELEASE_ROOT, "external_data"))   # source data and feature matrices (not redistributed)
+CLINICAL_XLSX = os.path.join(DATA, "clinical_and_imaging_info.xlsx")
+import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from cohort_ids import cohort_ids   # cohorts derived from the workbook; no identifier list is distributed
+IMG, SEG = f"{DATA}/images", f"{DATA}/segmentations"
+OUT = f"{DATA}/features"; os.makedirs(OUT, exist_ok=True)
 REPO, REV = "microsoft/rad-dino", "2ec9ca0e7a73c23aded999b844acd2f07c7e46b9"
-ARCHIVE = {"her2neg": f"{ROOT}/raddino_embeddings_739.csv", "her2pos": f"{ROOT}/raddino_her2pos.csv"}
-CANON = {"her2neg": f"{ROOT}/radiomics_all739.csv", "her2pos": f"{ROOT}/radiomics_her2pos.csv"}
+# archived embeddings of the original study: comparison targets only, not redistributed (comparison is skipped if absent)
+ARCHIVE = {"her2neg": f"{DATA}/archive/raddino_embeddings_739.csv", "her2pos": f"{DATA}/archive/raddino_her2pos.csv"}
+# cohort membership: derived from the clinical workbook by cohort_ids(); no identifier list is read or distributed
 
 device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
 proc_fast = AutoImageProcessor.from_pretrained(REPO, revision=REV, use_fast=True)
@@ -42,8 +47,8 @@
 
 
 def embed(pid, processor):
-    img_arr = sitk.GetArrayFromImage(sitk.ReadImage(f"{ROOT}/images/{pid}/{pid}_0001.nii.gz"))
-    seg_arr = sitk.GetArrayFromImage(sitk.ReadImage(f"{ROOT}/segmentations/{pid}.nii.gz"))
+    img_arr = sitk.GetArrayFromImage(sitk.ReadImage(f"{IMG}/{pid}/{pid}_0001.nii.gz"))
+    seg_arr = sitk.GetArrayFromImage(sitk.ReadImage(f"{SEG}/{pid}.nii.gz"))
     ta = [(seg_arr[z] > 0).sum() for z in range(seg_arr.shape[0])]
     bz = np.argmax(ta) if max(ta) > 0 else seg_arr.shape[0] // 2
     sl = img_arr[bz]
@@ -84,11 +89,20 @@
        "hypothesis_fixed_in_advance": True, "cohorts": {}}
 
 for coh in ("her2neg", "her2pos"):
-    ids = list(pd.read_csv(CANON[coh], usecols=["patient_id"])["patient_id"])
+    ids = cohort_ids(coh, CLINICAL_XLSX)
+    have_archive = os.path.exists(ARCHIVE[coh])          # public release: comparison only if the archive is present
+    t0 = time.time()
+    B = np.vstack([embed(p, proc_fast) for p in ids]).astype(np.float64)
+    if not have_archive:
+        cols = [f"raddino_{j:03d}" for j in range(B.shape[1])]
+        pd.DataFrame(B, columns=cols).assign(patient_id=ids)[["patient_id"] + cols].to_csv(
+            f"{OUT}/raddino_{coh}_reextract_cls_usefast_20260725.csv", index=False)
+        rep["cohorts"][coh] = {"n": len(ids), "elapsed_s": round(time.time() - t0, 1),
+                               "comparison": "SKIPPED: archived embeddings of the original study not available"}
+        print(f"{coh}: extracted {B.shape}; archive comparison skipped", flush=True)
+        continue
     arch = pd.read_csv(ARCHIVE[coh]).set_index("patient_id").loc[ids]
     A = arch.values.astype(np.float64)
-    t0 = time.time()
-    B = np.vstack([embed(p, proc_fast) for p in ids]).astype(np.float64)
     m = compare(A, B); v, why = verdict(m)
     m.update({"verdict": v, "reason": why, "n": len(ids), "elapsed_s": round(time.time() - t0, 1)})
     rep["cohorts"][coh] = m
@@ -106,8 +120,9 @@
         print(f"  rerun consistency: identical={np.array_equal(B, B2)} "
               f"maxdiff={np.abs(B-B2).max():.3e}", flush=True)
 
-vs = [c["verdict"] for c in rep["cohorts"].values()]
-rep["OVERALL"] = ("REPRODUCED" if all(v == "REPRODUCED" for v in vs)
+vs = [c.get("verdict", "SKIPPED") for c in rep["cohorts"].values()]
+rep["OVERALL"] = ("EXTRACTED_NO_COMPARISON" if any(v == "SKIPPED" for v in vs)
+                  else "REPRODUCED" if all(v == "REPRODUCED" for v in vs)
                   else "REPRODUCED_MECHANISM_ACCOUNTED" if all(v.startswith("REPRODUCED") for v in vs)
                   else "NOT_REPRODUCED")
 with open(f"{OUT}/r2c_usefast_result.json", "w") as f:
```

### `src/features/roi_voxel_distribution.py`

```diff
--- original/roi_voxel_distribution.py
+++ release/src/features/roi_voxel_distribution.py
@@ -19,13 +19,16 @@
 import pandas as pd
 import SimpleITK as sitk
 
-ROOT = os.path.expanduser("~/mama_mia")
-SEG = f"{ROOT}/segmentations"
-OUT = os.path.expanduser("~/JIIM_Revision/R2_features/roi_voxel_distribution.json")
+RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
+DATA = os.environ.get("JIIM_DATA_ROOT", os.path.join(RELEASE_ROOT, "external_data"))   # source data and feature matrices (not redistributed)
+CLINICAL_XLSX = os.path.join(DATA, "clinical_and_imaging_info.xlsx")
+import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from cohort_ids import cohort_ids   # cohorts derived from the workbook; no identifier list is distributed
+SEG = f"{DATA}/segmentations"
+OUT = f"{RELEASE_ROOT}/reproduction/features/roi_voxel_distribution.json"; os.makedirs(os.path.dirname(OUT), exist_ok=True)
 LABEL = 1  # radiomics_all.py settings: {'label': 1}
 
-ids_neg = list(pd.read_csv(f"{ROOT}/radiomics_all739.csv", usecols=["patient_id"])["patient_id"])
-ids_pos = list(pd.read_csv(f"{ROOT}/radiomics_her2pos.csv", usecols=["patient_id"])["patient_id"])
+ids_neg = cohort_ids("her2neg", CLINICAL_XLSX)
+ids_pos = cohort_ids("her2pos", CLINICAL_XLSX)
 print(f"HER2- {len(ids_neg)}   HER2+ {len(ids_pos)}   union {len(set(ids_neg) | set(ids_pos))}")
 
 
```

### `src/features/g1_qc_report.py`

```diff
--- original/g1_qc_report.py
+++ release/src/features/g1_qc_report.py
@@ -13,13 +13,16 @@
 import pandas as pd
 from scipy.stats import spearmanr
 
-ROOT = os.path.expanduser("~/mama_mia")
-OUT = os.path.expanduser("~/JIIM_Revision/R2_features")
+RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
+DATA = os.environ.get("JIIM_DATA_ROOT", os.path.join(RELEASE_ROOT, "external_data"))   # source data and feature matrices (not redistributed)
+ROOT = f"{DATA}/archive"      # original-study radiomics (comparison baseline; not redistributed)
+FEAT = f"{DATA}/features"
+OUT = f"{RELEASE_ROOT}/reproduction/features"; os.makedirs(OUT, exist_ok=True)
 BC = int(sys.argv[1]) if len(sys.argv) > 1 else 64
 
 OLD = {"her2neg": f"{ROOT}/radiomics_all739.csv", "her2pos": f"{ROOT}/radiomics_her2pos.csv"}
-NEW = {c: f"{OUT}/radiomics_{c}_binCount{BC}_20260725.csv" for c in OLD}
-BINS = pd.read_csv(f"{OUT}/r2b_effective_bins_binCount{BC}.csv")
+NEW = {c: f"{FEAT}/radiomics_{c}_binCount{BC}_20260725.csv" for c in OLD}
+BINS = pd.read_csv(f"{FEAT}/r2b_effective_bins_binCount{BC}.csv")
 
 FAMS = ["shape", "firstorder", "glcm", "glrlm", "glszm", "ngtdm", "gldm"]
 fam_of = lambda c: next((f for f in FAMS if c.startswith(f"original_{f}_")), "other")
@@ -95,7 +98,7 @@
 nzv_tot = col_NEW["prop_texture_zero_variance"] + col_NEW["prop_texture_near_zero_variance"]
 q["Q6"] = dict(metric="zero/near-zero-variance texture features (share of 75)", measured=float(nzv_tot),
                threshold="<= 0.05", **{"pass": bool(nzv_tot <= 0.05)})
-meta = json.load(open(f"{OUT}/r2b_extraction_meta_binCount{BC}.json"))
+meta = json.load(open(f"{FEAT}/r2b_extraction_meta_binCount{BC}.json"))
 nfail = sum(len(v) for v in meta["failures"].values())
 nan_inf = int(np.isnan(n_all[common].values).sum() + np.isinf(n_all[common].values).sum())
 q["Q7"] = dict(metric="extraction failures + NaN + Inf", measured=int(nfail + nan_inf),
```

### `src/features/pca_variance_retention.py`

```diff
--- original/pca_variance_retention.py
+++ release/src/features/pca_variance_retention.py
@@ -15,11 +15,14 @@
 from sklearn.decomposition import PCA
 from sklearn.model_selection import StratifiedKFold
 
-ROOT = os.path.expanduser("~/mama_mia")
-R2 = os.path.expanduser("~/JIIM_Revision/R2_features")
+RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
+DATA = os.environ.get("JIIM_DATA_ROOT", os.path.join(RELEASE_ROOT, "external_data"))   # source data and feature matrices (not redistributed)
+ROOT = f"{DATA}/archive"      # original-study feature matrices (not redistributed)
+R2 = f"{DATA}/features"
+OUTDIR = f"{RELEASE_ROOT}/reproduction/features"; os.makedirs(OUTDIR, exist_ok=True)
 FZ = f"{R2}/FROZEN_R2B"
 SEED, N_OUTER = 42, 5
-CLIN = os.path.expanduser("~/clinical_and_imaging_info.xlsx")
+CLIN = f"{DATA}/clinical_and_imaging_info.xlsx"
 
 
 def prep(her2, ctrl):
@@ -74,7 +77,7 @@
             "full_data_reference": round(float(np.sum(pf.explained_variance_ratio_)), 6),
         }
 
-with open(f"{R2}/pca_variance_retention.json", "w") as f:
+with open(f"{OUTDIR}/pca_variance_retention.json", "w") as f:
     json.dump(out, f, indent=1)
 
 print("=" * 86)
```

### `src/features/r2b_effective_bins_fix.py`

```diff
--- original/r2b_effective_bins_fix.py
+++ release/src/features/r2b_effective_bins_fix.py
@@ -22,21 +22,25 @@
 radiomics.logger.setLevel(logging.ERROR)
 import warnings; warnings.filterwarnings("ignore")
 
-ROOT = os.path.expanduser("~/mama_mia")
-OUT = os.path.expanduser("~/JIIM_Revision/R2_features")
+RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
+DATA = os.environ.get("JIIM_DATA_ROOT", os.path.join(RELEASE_ROOT, "external_data"))   # source data and feature matrices (not redistributed)
+CLINICAL_XLSX = os.path.join(DATA, "clinical_and_imaging_info.xlsx")
+import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from cohort_ids import cohort_ids   # cohorts derived from the workbook; no identifier list is distributed
+IMG, SEG = f"{DATA}/images", f"{DATA}/segmentations"
+OUT = f"{DATA}/features"; os.makedirs(OUT, exist_ok=True)
 BC = int(sys.argv[1]) if len(sys.argv) > 1 else 64
 SETTINGS = {"binCount": BC, "normalize": False, "resampledPixelSpacing": [1.0, 1.0, 1.0],
             "interpolator": sitk.sitkBSpline, "force2D": False, "label": 1}
-CANON = {"her2neg": f"{ROOT}/radiomics_all739.csv", "her2pos": f"{ROOT}/radiomics_her2pos.csv"}
+# cohort membership: derived from the clinical workbook by cohort_ids(); no identifier list is read or distributed
 
 rows, errs = [], []
-for coh, canon in CANON.items():
-    ids = list(pd.read_csv(canon, usecols=["patient_id"])["patient_id"])
+for coh in ("her2neg", "her2pos"):
+    ids = cohort_ids(coh, CLINICAL_XLSX)
     print(f"{coh}: {len(ids)}", flush=True)
     for i, pid in enumerate(ids):
         try:
-            img = sitk.ReadImage(f"{ROOT}/images/{pid}/{pid}_0001.nii.gz")
-            mask = sitk.ReadImage(f"{ROOT}/segmentations/{pid}.nii.gz")
+            img = sitk.ReadImage(f"{IMG}/{pid}/{pid}_0001.nii.gz")
+            mask = sitk.ReadImage(f"{SEG}/{pid}.nii.gz")
             mask = sitk.Cast(mask, sitk.sitkUInt8)            # <-- the fix
             i2, m2 = imageoperations.resampleImage(img, mask, **SETTINGS)
             a = sitk.GetArrayFromImage(i2)[sitk.GetArrayFromImage(m2) == 1]
```

### `src/figures/freeze_figure_data.py`

```diff
--- original/freeze_figure_data_r7.py
+++ release/src/figures/freeze_figure_data.py
@@ -9,12 +9,11 @@
 import json, os, hashlib, sys
 import scipy.io as sio
 
-HOME = os.path.expanduser("~")
-R7   = f"{HOME}/JIIM_Revision/R7_rate_primary"
-Q3   = f"{HOME}/JIIM_Revision/R7_rate_q3"
-Q4   = f"{HOME}/JIIM_Revision/R7_rate_q4"
-EP   = f"{HOME}/JIIM_Revision/R3_smoke/FROZEN_EPOCH/epoch_assignment.csv"
-OUT  = f"{HOME}/<figure-workspace>/canonical"
+RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
+R7   = f"{RELEASE_ROOT}/results/rate_primary"
+Q3   = f"{RELEASE_ROOT}/results/rate_q3"
+Q4   = f"{RELEASE_ROOT}/results/rate_q4"
+OUT  = f"{RELEASE_ROOT}/reproduction/figure_data"; os.makedirs(OUT, exist_ok=True)
 
 ORDER = ["Clinical only", "Clin + Radiomics", "Clin + BiomedCLIP", "Clin + RAD-DINO",
          "Clin + Rad + BiomedCLIP", "Clin + Rad + RAD-DINO"]
@@ -30,7 +29,7 @@
 
 def manifest(d):
     m = {}
-    for l in open(f"{d}/SHA256SUMS.txt"):
+    for l in open(f"{d}/ORIGINAL_SHA256SUMS.txt"):      # manifest of the frozen record; the released copies are byte-identical
         if l.startswith("#") or not l.strip(): continue
         hh, p = l.split(); m[p.lstrip("./")] = hh
     return m
@@ -38,14 +37,14 @@
 PROV = []
 def canon(base, name, sealed_dir):
     """Return path to the SEALED copy after (a) working copy vs manifest, (b) sealed vs working."""
-    work = f"{base}/{name}"; seal = f"{base}/{sealed_dir}/{name}"
+    work = f"{base}/{name}"; seal = os.path.normpath(f"{base}/{sealed_dir}/{name}")
     m = manifest(base); hw = sha(work)
     if m.get(name) != hw:
         sys.exit(f"HALT: manifest mismatch for {work}")
     if sha(seal) != hw:
         sys.exit(f"HALT: sealed copy differs from working copy for {name}")
     PROV.append({"file": name, "sealed_path": seal, "sha256": hw,
-                 "manifest": f"{base}/SHA256SUMS.txt",
+                 "manifest": f"{base}/ORIGINAL_SHA256SUMS.txt",
                  "verified": "working-copy==manifest AND sealed-copy==working-copy"})
     return seal
 
@@ -56,36 +55,28 @@
     return p
 
 # ---------------- sources ----------------
-p_q1   = canon(R7, "rate_q1_primary.json", "FROZEN_R7")
-p_q2   = canon(R7, "rate_q2_primary.json", "FROZEN_R7")
-p_q2s  = canon(R7, "rate_q2_sensitivities.json", "FROZEN_R7")
-p_spl  = canon(R7, "split_739.csv", "FROZEN_R7")
-p_pri  = canon(R7, "priorities_provenance.json", "FROZEN_R7")
-p_q3   = canon(Q3, "rate_q3.json", "FROZEN_R7Q3")
-p_q4r  = canon(Q4, "rate_q4_regimes.json", "FROZEN_R7Q4")
-p_q4c  = canon(Q4, "rate_q4_contrasts.json", "FROZEN_R7Q4")
-p_ep   = plain(EP)
+p_q1   = canon(R7, "rate_q1_primary.json", ".")
+p_q2   = canon(R7, "rate_q2_primary.json", ".")
+p_q2s  = canon(R7, "rate_q2_sensitivities.json", ".")
+p_pri  = canon(R7, "priorities_provenance.json", ".")
+p_q3   = canon(Q3, "rate_q3.json", ".")
+p_q4r  = canon(Q4, "rate_q4_regimes.json", ".")
+p_q4c  = canon(Q4, "rate_q4_contrasts.json", ".")
 
 q1 = json.load(open(p_q1)); q2 = json.load(open(p_q2)); q2s = json.load(open(p_q2s))
 q3 = json.load(open(p_q3)); q4r = json.load(open(p_q4r)); q4c = json.load(open(p_q4c))
 pri = json.load(open(p_pri))
 
-# counts only
-rows = [l for l in open(p_spl).read().splitlines() if l.strip()][1:]
-n739 = len(rows)
-hdr  = open(p_spl).readline().strip().split(","); si = hdr.index("split")
-n_H1 = sum(1 for l in rows if l.split(",")[si] == "train")
-n_H2 = sum(1 for l in rows if l.split(",")[si] == "eval")
-n980 = len([l for l in open(p_ep).read().splitlines() if l.strip()]) - 1
+# counts only (public release: from the provenance record; the split and epoch tables are regenerated, not distributed)
+n739 = pri["PRIMARY"]["n_total"]; n_H1 = pri["PRIMARY"]["n_train"]; n_H2 = pri["PRIMARY"]["n_eval"]
 n728 = pri["EMPTY_ARM_728"]["n_total"] - pri["EMPTY_ARM_728"]["dropped"]
 n241 = 241  # from the HER2-positive record below, asserted not typed
-her2pos = json.load(open(f"{Q4}/../R7_rate_primary/rate_her2pos_not_estimated.json")) \
-    if os.path.exists(f"{R7}/rate_her2pos_not_estimated.json") else None
-if her2pos is None: her2pos = json.load(open(f"{R7}/FROZEN_R7/rate_her2pos_not_estimated.json"))
+her2pos = json.load(open(f"{R7}/rate_her2pos_not_estimated.json"))
 n241 = her2pos["n_total"]
-PROV.append({"file": "rate_her2pos_not_estimated.json", "sealed_path": f"{R7}/FROZEN_R7/rate_her2pos_not_estimated.json",
-             "sha256": sha(f"{R7}/FROZEN_R7/rate_her2pos_not_estimated.json"),
-             "manifest": f"{R7}/SHA256SUMS.txt", "verified": "sha256 recorded"})
+n980 = n739 + n241          # both cohorts
+PROV.append({"file": "rate_her2pos_not_estimated.json", "sealed_path": f"{R7}/rate_her2pos_not_estimated.json",
+             "sha256": sha(f"{R7}/rate_her2pos_not_estimated.json"),
+             "manifest": f"{R7}/ORIGINAL_SHA256SUMS.txt", "verified": "sha256 recorded"})
 
 assert n739 == 739 and n_H1 == 370 and n_H2 == 369 and n980 == 980 and n728 == 728 and n241 == 241, \
     (n739, n_H1, n_H2, n980, n728, n241)
@@ -134,7 +125,7 @@
                        "role": "parallel sensitivity branch from HER2-negative, not a sequential exclusion"}},
     questions=[{"key": "Q1", "text": "Configuration-specific RATE/AUTOC on independent held-out evaluation"},
                {"key": "Q2", "text": "Paired incremental RATE comparison"},
-               {"key": "Q3", "text": "Honest vs same-sample model-development/evaluation diagnostic"},
+               {"key": "Q3", "text": "Opposite-half vs same-sample model-development/evaluation diagnostic"},
                {"key": "Q4", "text": "Preprocessing-placement diagnostic, opposite-half model fitting"}],
     directions={"Q1": "one direction (train H1 -> evaluate H2)", "Q2": "one direction (train H1 -> evaluate H2)",
                 "Q3": "both split directions", "Q4": "both split directions"},
@@ -193,11 +184,11 @@
 w("Fig3_data.json", f3)
 
 # ---------------- Fig 4 ----------------
-f4 = dict(BASE, figure="Fig4", question="Q3 same-sample versus honest model-development/evaluation",
+f4 = dict(BASE, figure="Fig4", question="Q3 same-sample versus opposite-half model-development/evaluation",
     kind="grouped dot/range plot", descriptive=True, inferential=False,
     interval="NONE", p_value="NONE", reference_line=0.0,
     analytic_n=n739, evaluation_n={"H1": n_H1, "H2": n_H2},
-    x_label="Change in RATE (same-sample - honest)",
+    x_label="Change in RATE (same-sample - opposite-half)",
     pooled_definition=q3["design"]["pooled"],
     rows=[{"key": k, "label": LABEL[i], "order": i + 1,
            "H1": q3["results"][k]["optimism_H1"], "H2": q3["results"][k]["optimism_H2"],
```

### `src/figures/jiim_export_r7.m`

```diff
--- original/jiim_export_r7.m
+++ release/src/figures/jiim_export_r7.m
@@ -3,6 +3,7 @@
 assert(any(strcmpi(listfonts,'Arial')), 'Arial is not available; stop before rendering.');
 set(findall(fig,'-property','FontName'),'FontName','Arial');
 set(fig,'Color',[1 1 1],'InvertHardcopy','off','PaperPositionMode','auto');
+if ~exist(outdir,'dir'), mkdir(outdir); end
 savefig(fig, fullfile(outdir, [name '.fig']));
 % 'Padding','figure' keeps the FULL declared canvas; the default tight crop
 % shrinks the exported width below the 174 mm design width (measured 158.5-167.3 mm).
```

### `src/figures/make_Fig1.m`

```diff
--- original/make_Fig1.m
+++ release/src/figures/make_Fig1.m
@@ -7,8 +7,8 @@
 S.softedge = [116 116 116]/255;   % #747474  secondary box outlines + empty-arm stub  (was #8A8A8A, L* 57.5 -> 48.8)
 S.gtext    = [ 90  90  90]/255;   % #5A5A5A  secondary-branch and caption text       (was #6B6B6B, L* 45.2 -> 38.2)
 here = fileparts(mfilename('fullpath'));
-D = load(fullfile(here,'..','canonical','fig_data_r7.mat'));
-outdir = fullfile(here,'..','output');
+D = load(fullfile(here,'..','..','figure_data','fig_data_r7.mat'));
+outdir = fullfile(here,'..','..','reproduction','figures');
 n980=D.n980; n739=D.n739; n241=D.n241; nH1=D.nH1; nH2=D.nH2; n728=D.n728;
 assert(n980==980 && n739==739 && n241==241 && nH1==370 && nH2==369 && n728==728, ...
        'Fig1: canonical cohort counts failed');
```

### `src/figures/make_Fig2.m`

```diff
--- original/make_Fig2.m
+++ release/src/figures/make_Fig2.m
@@ -2,8 +2,8 @@
 % independent held-out evaluation. Rendering source of truth. Class V.
 S = jiim_style_r7();
 here = fileparts(mfilename('fullpath'));
-D = load(fullfile(here,'..','canonical','fig_data_r7.mat'));
-outdir = fullfile(here,'..','output');
+D = load(fullfile(here,'..','..','figure_data','fig_data_r7.mat'));
+outdir = fullfile(here,'..','..','reproduction','figures');
 
 est = D.f2_est(:); lo = D.f2_lo(:); hi = D.f2_hi(:);
 labs = cellstr(D.labels); n = numel(est);
```

### `src/figures/make_Fig3.m`

```diff
--- original/make_Fig3.m
+++ release/src/figures/make_Fig3.m
@@ -2,8 +2,8 @@
 % Panel-B navy marks the PREDEFINED PRIMARY INFERENTIAL CONTRAST, not a historical status. Class V.
 S = jiim_style_r7();
 here = fileparts(mfilename('fullpath'));
-D = load(fullfile(here,'..','canonical','fig_data_r7.mat'));
-outdir = fullfile(here,'..','output');
+D = load(fullfile(here,'..','..','figure_data','fig_data_r7.mat'));
+outdir = fullfile(here,'..','..','reproduction','figures');
 
 aE=D.f3a_est(:); aL=D.f3a_lo(:); aH=D.f3a_hi(:); aLab=cellstr(D.f3a_lab);
 bE=D.f3b_est(:); bL=D.f3b_lo(:); bH=D.f3b_hi(:); bLab=cellstr(D.f3b_lab);
```

### `src/figures/make_Fig4.m`

```diff
--- original/make_Fig4.m
+++ release/src/figures/make_Fig4.m
@@ -1,9 +1,9 @@
-% make_Fig4.m — Q3: change in the RATE point estimate under same-sample versus honest
+% make_Fig4.m — Q3: change in the RATE point estimate under same-sample versus opposite-half
 % model development/evaluation. Descriptive; no interval, no p-value. Class V.
 S = jiim_style_r7();
 here = fileparts(mfilename('fullpath'));
-D = load(fullfile(here,'..','canonical','fig_data_r7.mat'));
-outdir = fullfile(here,'..','output');
+D = load(fullfile(here,'..','..','figure_data','fig_data_r7.mat'));
+outdir = fullfile(here,'..','..','reproduction','figures');
 
 H1 = D.f4_H1(:); H2 = D.f4_H2(:); PO = D.f4_pooled(:);
 labs = cellstr(D.labels); n = numel(PO);
```

### `src/figures/make_Fig5.m`

```diff
--- original/make_Fig5.m
+++ release/src/figures/make_Fig5.m
@@ -5,8 +5,8 @@
 % given EQUAL physical width (v9 section 5-B); one shared row-label column serves both.
 S = jiim_style_r7();
 here = fileparts(mfilename('fullpath'));
-D = load(fullfile(here,'..','canonical','fig_data_r7.mat'));
-outdir = fullfile(here,'..','output');
+D = load(fullfile(here,'..','..','figure_data','fig_data_r7.mat'));
+outdir = fullfile(here,'..','..','reproduction','figures');
 
 bH1=D.f5b_H1(:); bH2=D.f5b_H2(:);
 cP=D.f5c_P(:); cS=D.f5c_S(:); cPS=D.f5c_PS(:);
```

### `figure_data/Fig1_data.json`

```diff
--- original/Fig1_data.json
+++ release/figure_data/Fig1_data.json
@@ -22,72 +22,72 @@
  "provenance": [
   {
    "file": "rate_q1_primary.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/rate_q1_primary.json",
+   "sealed_path": "results/rate_primary/rate_q1_primary.json",
    "sha256": "106e6cbb68b70a0882166f1efe1839fd8f72e31e2a2b32135fc067a60710c816",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q2_primary.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/rate_q2_primary.json",
+   "sealed_path": "results/rate_primary/rate_q2_primary.json",
    "sha256": "f52d009189cd1199ce5a7a781de8603d39ad8a0783ee071121c605ca1d4da8d6",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q2_sensitivities.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/rate_q2_sensitivities.json",
+   "sealed_path": "results/rate_primary/rate_q2_sensitivities.json",
    "sha256": "3ef481c0cfb9b74e2a7d3c1b073a53e01341fa551891cbb66eda66a406450ed4",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "split_739.csv",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/split_739.csv",
+   "sealed_path": "frozen record R7_rate_primary/FROZEN_R7/split_739.csv (not distributed: regenerable, see splits/README.md)",
    "sha256": "a373e92d704ef7c7d54eacab99e3107dfb6b8ef378aa3040441d9c70ff078ab5",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "priorities_provenance.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/priorities_provenance.json",
+   "sealed_path": "results/rate_primary/priorities_provenance.json",
    "sha256": "5e5d18a3b717510eefeea57270d2108cd0c03793232a3a8aca3561710bc63138",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q3.json",
-   "sealed_path": "<workspace>/R7_rate_q3/FROZEN_R7Q3/rate_q3.json",
+   "sealed_path": "results/rate_q3/rate_q3.json",
    "sha256": "1aea51dbb1819789ad181c73fe99945fbdc7c9512d6d5dfe9eb57698c403e888",
-   "manifest": "<workspace>/R7_rate_q3/SHA256SUMS.txt",
+   "manifest": "results/rate_q3/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q4_regimes.json",
-   "sealed_path": "<workspace>/R7_rate_q4/FROZEN_R7Q4/rate_q4_regimes.json",
+   "sealed_path": "results/rate_q4/rate_q4_regimes.json",
    "sha256": "4e4b6fb65f6c86adb979b3c6e750dc7bce258a3a79a76af80c0f47e393260459",
-   "manifest": "<workspace>/R7_rate_q4/SHA256SUMS.txt",
+   "manifest": "results/rate_q4/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q4_contrasts.json",
-   "sealed_path": "<workspace>/R7_rate_q4/FROZEN_R7Q4/rate_q4_contrasts.json",
+   "sealed_path": "results/rate_q4/rate_q4_contrasts.json",
    "sha256": "4b46b2410d3ba9a8250934b96ff2e858454f93e1f0c92775ca1f6435a0e6b209",
-   "manifest": "<workspace>/R7_rate_q4/SHA256SUMS.txt",
+   "manifest": "results/rate_q4/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "epoch_assignment.csv",
-   "sealed_path": "<workspace>/R3_smoke/FROZEN_EPOCH/epoch_assignment.csv",
+   "sealed_path": "frozen record R3_smoke/FROZEN_EPOCH/epoch_assignment.csv (not distributed: regenerated by src/rate_analysis/derive_epochs.py)",
    "sha256": "b893a669f95ae1e92a346bbae23450fdb99fc6b899baad69b8679e0a42c99067",
    "manifest": "n/a (frozen read-only input outside the R7 rounds)",
    "verified": "sha256 recorded"
   },
   {
    "file": "rate_her2pos_not_estimated.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/rate_her2pos_not_estimated.json",
+   "sealed_path": "results/rate_primary/rate_her2pos_not_estimated.json",
    "sha256": "0410328de8a08e4bc2e5f050a7ad717f0ab7a143866e9fc65061e96d18140bb4",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "sha256 recorded"
   }
  ],
@@ -145,7 +145,7 @@
   },
   {
    "key": "Q3",
-   "text": "Honest vs same-sample model-development/evaluation diagnostic"
+   "text": "Opposite-half vs same-sample model-development/evaluation diagnostic"
   },
   {
    "key": "Q4",
```

### `figure_data/Fig2_data.json`

```diff
--- original/Fig2_data.json
+++ release/figure_data/Fig2_data.json
@@ -22,72 +22,72 @@
  "provenance": [
   {
    "file": "rate_q1_primary.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/rate_q1_primary.json",
+   "sealed_path": "results/rate_primary/rate_q1_primary.json",
    "sha256": "106e6cbb68b70a0882166f1efe1839fd8f72e31e2a2b32135fc067a60710c816",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q2_primary.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/rate_q2_primary.json",
+   "sealed_path": "results/rate_primary/rate_q2_primary.json",
    "sha256": "f52d009189cd1199ce5a7a781de8603d39ad8a0783ee071121c605ca1d4da8d6",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q2_sensitivities.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/rate_q2_sensitivities.json",
+   "sealed_path": "results/rate_primary/rate_q2_sensitivities.json",
    "sha256": "3ef481c0cfb9b74e2a7d3c1b073a53e01341fa551891cbb66eda66a406450ed4",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "split_739.csv",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/split_739.csv",
+   "sealed_path": "frozen record R7_rate_primary/FROZEN_R7/split_739.csv (not distributed: regenerable, see splits/README.md)",
    "sha256": "a373e92d704ef7c7d54eacab99e3107dfb6b8ef378aa3040441d9c70ff078ab5",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "priorities_provenance.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/priorities_provenance.json",
+   "sealed_path": "results/rate_primary/priorities_provenance.json",
    "sha256": "5e5d18a3b717510eefeea57270d2108cd0c03793232a3a8aca3561710bc63138",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q3.json",
-   "sealed_path": "<workspace>/R7_rate_q3/FROZEN_R7Q3/rate_q3.json",
+   "sealed_path": "results/rate_q3/rate_q3.json",
    "sha256": "1aea51dbb1819789ad181c73fe99945fbdc7c9512d6d5dfe9eb57698c403e888",
-   "manifest": "<workspace>/R7_rate_q3/SHA256SUMS.txt",
+   "manifest": "results/rate_q3/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q4_regimes.json",
-   "sealed_path": "<workspace>/R7_rate_q4/FROZEN_R7Q4/rate_q4_regimes.json",
+   "sealed_path": "results/rate_q4/rate_q4_regimes.json",
    "sha256": "4e4b6fb65f6c86adb979b3c6e750dc7bce258a3a79a76af80c0f47e393260459",
-   "manifest": "<workspace>/R7_rate_q4/SHA256SUMS.txt",
+   "manifest": "results/rate_q4/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q4_contrasts.json",
-   "sealed_path": "<workspace>/R7_rate_q4/FROZEN_R7Q4/rate_q4_contrasts.json",
+   "sealed_path": "results/rate_q4/rate_q4_contrasts.json",
    "sha256": "4b46b2410d3ba9a8250934b96ff2e858454f93e1f0c92775ca1f6435a0e6b209",
-   "manifest": "<workspace>/R7_rate_q4/SHA256SUMS.txt",
+   "manifest": "results/rate_q4/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "epoch_assignment.csv",
-   "sealed_path": "<workspace>/R3_smoke/FROZEN_EPOCH/epoch_assignment.csv",
+   "sealed_path": "frozen record R3_smoke/FROZEN_EPOCH/epoch_assignment.csv (not distributed: regenerated by src/rate_analysis/derive_epochs.py)",
    "sha256": "b893a669f95ae1e92a346bbae23450fdb99fc6b899baad69b8679e0a42c99067",
    "manifest": "n/a (frozen read-only input outside the R7 rounds)",
    "verified": "sha256 recorded"
   },
   {
    "file": "rate_her2pos_not_estimated.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/rate_her2pos_not_estimated.json",
+   "sealed_path": "results/rate_primary/rate_her2pos_not_estimated.json",
    "sha256": "0410328de8a08e4bc2e5f050a7ad717f0ab7a143866e9fc65061e96d18140bb4",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "sha256 recorded"
   }
  ],
```

### `figure_data/Fig3_data.json`

```diff
--- original/Fig3_data.json
+++ release/figure_data/Fig3_data.json
@@ -22,72 +22,72 @@
  "provenance": [
   {
    "file": "rate_q1_primary.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/rate_q1_primary.json",
+   "sealed_path": "results/rate_primary/rate_q1_primary.json",
    "sha256": "106e6cbb68b70a0882166f1efe1839fd8f72e31e2a2b32135fc067a60710c816",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q2_primary.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/rate_q2_primary.json",
+   "sealed_path": "results/rate_primary/rate_q2_primary.json",
    "sha256": "f52d009189cd1199ce5a7a781de8603d39ad8a0783ee071121c605ca1d4da8d6",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q2_sensitivities.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/rate_q2_sensitivities.json",
+   "sealed_path": "results/rate_primary/rate_q2_sensitivities.json",
    "sha256": "3ef481c0cfb9b74e2a7d3c1b073a53e01341fa551891cbb66eda66a406450ed4",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "split_739.csv",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/split_739.csv",
+   "sealed_path": "frozen record R7_rate_primary/FROZEN_R7/split_739.csv (not distributed: regenerable, see splits/README.md)",
    "sha256": "a373e92d704ef7c7d54eacab99e3107dfb6b8ef378aa3040441d9c70ff078ab5",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "priorities_provenance.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/priorities_provenance.json",
+   "sealed_path": "results/rate_primary/priorities_provenance.json",
    "sha256": "5e5d18a3b717510eefeea57270d2108cd0c03793232a3a8aca3561710bc63138",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q3.json",
-   "sealed_path": "<workspace>/R7_rate_q3/FROZEN_R7Q3/rate_q3.json",
+   "sealed_path": "results/rate_q3/rate_q3.json",
    "sha256": "1aea51dbb1819789ad181c73fe99945fbdc7c9512d6d5dfe9eb57698c403e888",
-   "manifest": "<workspace>/R7_rate_q3/SHA256SUMS.txt",
+   "manifest": "results/rate_q3/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q4_regimes.json",
-   "sealed_path": "<workspace>/R7_rate_q4/FROZEN_R7Q4/rate_q4_regimes.json",
+   "sealed_path": "results/rate_q4/rate_q4_regimes.json",
    "sha256": "4e4b6fb65f6c86adb979b3c6e750dc7bce258a3a79a76af80c0f47e393260459",
-   "manifest": "<workspace>/R7_rate_q4/SHA256SUMS.txt",
+   "manifest": "results/rate_q4/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q4_contrasts.json",
-   "sealed_path": "<workspace>/R7_rate_q4/FROZEN_R7Q4/rate_q4_contrasts.json",
+   "sealed_path": "results/rate_q4/rate_q4_contrasts.json",
    "sha256": "4b46b2410d3ba9a8250934b96ff2e858454f93e1f0c92775ca1f6435a0e6b209",
-   "manifest": "<workspace>/R7_rate_q4/SHA256SUMS.txt",
+   "manifest": "results/rate_q4/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "epoch_assignment.csv",
-   "sealed_path": "<workspace>/R3_smoke/FROZEN_EPOCH/epoch_assignment.csv",
+   "sealed_path": "frozen record R3_smoke/FROZEN_EPOCH/epoch_assignment.csv (not distributed: regenerated by src/rate_analysis/derive_epochs.py)",
    "sha256": "b893a669f95ae1e92a346bbae23450fdb99fc6b899baad69b8679e0a42c99067",
    "manifest": "n/a (frozen read-only input outside the R7 rounds)",
    "verified": "sha256 recorded"
   },
   {
    "file": "rate_her2pos_not_estimated.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/rate_her2pos_not_estimated.json",
+   "sealed_path": "results/rate_primary/rate_her2pos_not_estimated.json",
    "sha256": "0410328de8a08e4bc2e5f050a7ad717f0ab7a143866e9fc65061e96d18140bb4",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "sha256 recorded"
   }
  ],
```

### `figure_data/Fig4_data.json`

```diff
--- original/Fig4_data.json
+++ release/figure_data/Fig4_data.json
@@ -22,77 +22,77 @@
  "provenance": [
   {
    "file": "rate_q1_primary.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/rate_q1_primary.json",
+   "sealed_path": "results/rate_primary/rate_q1_primary.json",
    "sha256": "106e6cbb68b70a0882166f1efe1839fd8f72e31e2a2b32135fc067a60710c816",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q2_primary.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/rate_q2_primary.json",
+   "sealed_path": "results/rate_primary/rate_q2_primary.json",
    "sha256": "f52d009189cd1199ce5a7a781de8603d39ad8a0783ee071121c605ca1d4da8d6",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q2_sensitivities.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/rate_q2_sensitivities.json",
+   "sealed_path": "results/rate_primary/rate_q2_sensitivities.json",
    "sha256": "3ef481c0cfb9b74e2a7d3c1b073a53e01341fa551891cbb66eda66a406450ed4",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "split_739.csv",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/split_739.csv",
+   "sealed_path": "frozen record R7_rate_primary/FROZEN_R7/split_739.csv (not distributed: regenerable, see splits/README.md)",
    "sha256": "a373e92d704ef7c7d54eacab99e3107dfb6b8ef378aa3040441d9c70ff078ab5",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "priorities_provenance.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/priorities_provenance.json",
+   "sealed_path": "results/rate_primary/priorities_provenance.json",
    "sha256": "5e5d18a3b717510eefeea57270d2108cd0c03793232a3a8aca3561710bc63138",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q3.json",
-   "sealed_path": "<workspace>/R7_rate_q3/FROZEN_R7Q3/rate_q3.json",
+   "sealed_path": "results/rate_q3/rate_q3.json",
    "sha256": "1aea51dbb1819789ad181c73fe99945fbdc7c9512d6d5dfe9eb57698c403e888",
-   "manifest": "<workspace>/R7_rate_q3/SHA256SUMS.txt",
+   "manifest": "results/rate_q3/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q4_regimes.json",
-   "sealed_path": "<workspace>/R7_rate_q4/FROZEN_R7Q4/rate_q4_regimes.json",
+   "sealed_path": "results/rate_q4/rate_q4_regimes.json",
    "sha256": "4e4b6fb65f6c86adb979b3c6e750dc7bce258a3a79a76af80c0f47e393260459",
-   "manifest": "<workspace>/R7_rate_q4/SHA256SUMS.txt",
+   "manifest": "results/rate_q4/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q4_contrasts.json",
-   "sealed_path": "<workspace>/R7_rate_q4/FROZEN_R7Q4/rate_q4_contrasts.json",
+   "sealed_path": "results/rate_q4/rate_q4_contrasts.json",
    "sha256": "4b46b2410d3ba9a8250934b96ff2e858454f93e1f0c92775ca1f6435a0e6b209",
-   "manifest": "<workspace>/R7_rate_q4/SHA256SUMS.txt",
+   "manifest": "results/rate_q4/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "epoch_assignment.csv",
-   "sealed_path": "<workspace>/R3_smoke/FROZEN_EPOCH/epoch_assignment.csv",
+   "sealed_path": "frozen record R3_smoke/FROZEN_EPOCH/epoch_assignment.csv (not distributed: regenerated by src/rate_analysis/derive_epochs.py)",
    "sha256": "b893a669f95ae1e92a346bbae23450fdb99fc6b899baad69b8679e0a42c99067",
    "manifest": "n/a (frozen read-only input outside the R7 rounds)",
    "verified": "sha256 recorded"
   },
   {
    "file": "rate_her2pos_not_estimated.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/rate_her2pos_not_estimated.json",
+   "sealed_path": "results/rate_primary/rate_her2pos_not_estimated.json",
    "sha256": "0410328de8a08e4bc2e5f050a7ad717f0ab7a143866e9fc65061e96d18140bb4",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "sha256 recorded"
   }
  ],
  "figure": "Fig4",
- "question": "Q3 same-sample versus honest model-development/evaluation",
+ "question": "Q3 same-sample versus opposite-half model-development/evaluation",
  "kind": "grouped dot/range plot",
  "descriptive": true,
  "inferential": false,
@@ -104,7 +104,7 @@
   "H1": 370,
   "H2": 369
  },
- "x_label": "Change in RATE (same-sample - honest)",
+ "x_label": "Change in RATE (same-sample - opposite-half)",
  "pooled_definition": "(370*optimism_H1 + 369*optimism_H2)/739, predeclared in AMENDMENT_R7_Q3.md section 5",
  "rows": [
   {
```

### `figure_data/Fig5_data.json`

```diff
--- original/Fig5_data.json
+++ release/figure_data/Fig5_data.json
@@ -22,72 +22,72 @@
  "provenance": [
   {
    "file": "rate_q1_primary.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/rate_q1_primary.json",
+   "sealed_path": "results/rate_primary/rate_q1_primary.json",
    "sha256": "106e6cbb68b70a0882166f1efe1839fd8f72e31e2a2b32135fc067a60710c816",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q2_primary.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/rate_q2_primary.json",
+   "sealed_path": "results/rate_primary/rate_q2_primary.json",
    "sha256": "f52d009189cd1199ce5a7a781de8603d39ad8a0783ee071121c605ca1d4da8d6",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q2_sensitivities.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/rate_q2_sensitivities.json",
+   "sealed_path": "results/rate_primary/rate_q2_sensitivities.json",
    "sha256": "3ef481c0cfb9b74e2a7d3c1b073a53e01341fa551891cbb66eda66a406450ed4",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "split_739.csv",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/split_739.csv",
+   "sealed_path": "frozen record R7_rate_primary/FROZEN_R7/split_739.csv (not distributed: regenerable, see splits/README.md)",
    "sha256": "a373e92d704ef7c7d54eacab99e3107dfb6b8ef378aa3040441d9c70ff078ab5",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "priorities_provenance.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/priorities_provenance.json",
+   "sealed_path": "results/rate_primary/priorities_provenance.json",
    "sha256": "5e5d18a3b717510eefeea57270d2108cd0c03793232a3a8aca3561710bc63138",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q3.json",
-   "sealed_path": "<workspace>/R7_rate_q3/FROZEN_R7Q3/rate_q3.json",
+   "sealed_path": "results/rate_q3/rate_q3.json",
    "sha256": "1aea51dbb1819789ad181c73fe99945fbdc7c9512d6d5dfe9eb57698c403e888",
-   "manifest": "<workspace>/R7_rate_q3/SHA256SUMS.txt",
+   "manifest": "results/rate_q3/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q4_regimes.json",
-   "sealed_path": "<workspace>/R7_rate_q4/FROZEN_R7Q4/rate_q4_regimes.json",
+   "sealed_path": "results/rate_q4/rate_q4_regimes.json",
    "sha256": "4e4b6fb65f6c86adb979b3c6e750dc7bce258a3a79a76af80c0f47e393260459",
-   "manifest": "<workspace>/R7_rate_q4/SHA256SUMS.txt",
+   "manifest": "results/rate_q4/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "rate_q4_contrasts.json",
-   "sealed_path": "<workspace>/R7_rate_q4/FROZEN_R7Q4/rate_q4_contrasts.json",
+   "sealed_path": "results/rate_q4/rate_q4_contrasts.json",
    "sha256": "4b46b2410d3ba9a8250934b96ff2e858454f93e1f0c92775ca1f6435a0e6b209",
-   "manifest": "<workspace>/R7_rate_q4/SHA256SUMS.txt",
+   "manifest": "results/rate_q4/ORIGINAL_SHA256SUMS.txt",
    "verified": "working-copy==manifest AND sealed-copy==working-copy"
   },
   {
    "file": "epoch_assignment.csv",
-   "sealed_path": "<workspace>/R3_smoke/FROZEN_EPOCH/epoch_assignment.csv",
+   "sealed_path": "frozen record R3_smoke/FROZEN_EPOCH/epoch_assignment.csv (not distributed: regenerated by src/rate_analysis/derive_epochs.py)",
    "sha256": "b893a669f95ae1e92a346bbae23450fdb99fc6b899baad69b8679e0a42c99067",
    "manifest": "n/a (frozen read-only input outside the R7 rounds)",
    "verified": "sha256 recorded"
   },
   {
    "file": "rate_her2pos_not_estimated.json",
-   "sealed_path": "<workspace>/R7_rate_primary/FROZEN_R7/rate_her2pos_not_estimated.json",
+   "sealed_path": "results/rate_primary/rate_her2pos_not_estimated.json",
    "sha256": "0410328de8a08e4bc2e5f050a7ad717f0ab7a143866e9fc65061e96d18140bb4",
-   "manifest": "<workspace>/R7_rate_primary/SHA256SUMS.txt",
+   "manifest": "results/rate_primary/ORIGINAL_SHA256SUMS.txt",
    "verified": "sha256 recorded"
   }
  ],
```

### `environment/environment.yml`

```diff
--- original/environment.yml
+++ release/environment/environment.yml
@@ -50,4 +50,3 @@
       - tqdm==4.69.1
       - typing-extensions==4.16.0
       - tzdata==2026.3
-prefix: <conda>/envs/jiim-r0
```

### `environment/environment_features.yml`

```diff
--- original/environment_features.yml
+++ release/environment/environment_features.yml
@@ -83,4 +83,3 @@
       - tzdata==2026.3
       - urllib3==2.7.0
       - wcwidth==0.8.2
-prefix: <conda>/envs/jiim-r0-features
```

### `environment/build_env.sh`

```diff
--- original/build_env.sh
+++ release/environment/build_env.sh
@@ -13,8 +13,8 @@
 set -euo pipefail
 
 ENV_NAME="jiim-r0"
-CONDA="<conda>/bin/conda"
-MAMBA="<conda>/bin/mamba"
+CONDA="conda"
+MAMBA="mamba"
 
 echo "=== removing any prior $ENV_NAME ==="
 $CONDA env remove -n "$ENV_NAME" -y 2>/dev/null || true
@@ -22,7 +22,7 @@
 echo "=== creating $ENV_NAME (python 3.12.8) ==="
 $MAMBA create -n "$ENV_NAME" -y python=3.12.8 pip
 
-PY="<conda>/envs/$ENV_NAME/bin/python"
+PY="$(conda run -n "$ENV_NAME" python -c 'import sys; print(sys.executable)')"
 
 echo "=== installing pinned analysis stack ==="
 "$PY" -m pip install --no-cache-dir \
@@ -52,7 +52,7 @@
 "
 
 echo "=== freezing lockfile ==="
-"$PY" -m pip freeze > <workspace>/R0_freeze_audit/env/requirements.lock.txt
-$CONDA env export -n "$ENV_NAME" > <workspace>/R0_freeze_audit/env/environment.yml
+"$PY" -m pip freeze > $(cd "$(dirname "$0")" && pwd)/requirements.lock.txt
+$CONDA env export -n "$ENV_NAME" > $(cd "$(dirname "$0")" && pwd)/environment.yml
 
 echo "=== DONE: $ENV_NAME ==="
```

### `environment/build_env_full.sh`

```diff
--- original/build_env_full.sh
+++ release/environment/build_env_full.sh
@@ -11,16 +11,16 @@
 # damage the verified analysis environment.
 set -uo pipefail
 
-CONDA="<conda>/bin/conda"
+CONDA="conda"
 SRC="jiim-r0"
 ENV_NAME="jiim-r0-features"
-OUT="<workspace>/R0_freeze_audit/env"
+OUT="$(cd "$(dirname "$0")" && pwd)"
 
 echo "=== cloning $SRC -> $ENV_NAME ==="
 $CONDA env remove -n "$ENV_NAME" -y 2>/dev/null || true
 $CONDA create -n "$ENV_NAME" --clone "$SRC" -y
 
-PY="<conda>/envs/$ENV_NAME/bin/python"
+PY="$(conda run -n "$ENV_NAME" python -c 'import sys; print(sys.executable)')"
 
 echo "=== imaging + DL stack ==="
 "$PY" -m pip install --no-cache-dir \
```

