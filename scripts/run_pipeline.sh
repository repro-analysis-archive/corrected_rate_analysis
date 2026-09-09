#!/usr/bin/env bash
# Run the corrected analysis end to end. See docs/REPRODUCTION.md for the environments and the data layout.
#   bash scripts/run_pipeline.sh            # all stages
#   bash scripts/run_pipeline.sh features   # stage 0 only (feature-extraction environment)
#   bash scripts/run_pipeline.sh analysis   # stages 1-2 (analysis environment + R)
#   bash scripts/run_pipeline.sh figures    # stage 3 (Python + MATLAB)
# Interpreters: PYTHON (analysis environment) and PYTHON_FEATURES (feature environment), default "python".
set -euo pipefail
cd "$(dirname "$0")/.."
export JIIM_RELEASE_ROOT="$(pwd)"
export JIIM_DATA_ROOT="${JIIM_DATA_ROOT:-$(pwd)/external_data}"
PY="${PYTHON:-python}"
PYF="${PYTHON_FEATURES:-$PY}"
STAGE="${1:-all}"
run() { echo; echo "== $*"; "$@"; }

if [[ "$STAGE" == "features" || "$STAGE" == "all" ]]; then
  run "$PYF" src/features/roi_voxel_distribution.py
  run "$PYF" src/features/r2b_radiomics_reextract.py 64
  run "$PYF" src/features/r2a_biomedclip_reextract.py
  run "$PYF" src/features/r2c_usefast_test.py
fi

if [[ "$STAGE" == "analysis" || "$STAGE" == "all" ]]; then
  run "$PY" src/rate_analysis/derive_epochs.py          # enrolment epochs from the clinical workbook (input of every fit)
  run "$PY" src/rate_analysis/fit_priorities.py
  run "$PY" src/rate_analysis/build_Z.py
  run "$PY" scripts/verify_split_digests.py             # regenerated split / folds / epochs against splits/SPLIT_DIGESTS.json
  run Rscript src/rate_analysis/rate_primary.R
  run "$PY" src/rate_analysis/fit_priorities_sequential.py
  run Rscript src/rate_analysis/rate_sequential.R
  run "$PY" src/rate_analysis/crosscheck.py
  run "$PY" src/rate_analysis/fit_q3_priorities.py
  run Rscript src/rate_analysis/rate_q3.R
  run "$PY" src/rate_analysis/fit_q4_priorities.py
  run Rscript src/rate_analysis/rate_q4.R
  run "$PY" src/rate_analysis/extract_q4_contrasts.py
fi

if [[ "$STAGE" == "figures" || "$STAGE" == "all" ]]; then
  run "$PY" src/figures/freeze_figure_data.py
  if command -v matlab >/dev/null 2>&1; then
    run matlab -batch "cd('$(pwd)/src/figures'); build_all"
  else
    echo "MATLAB not found: figure rendering skipped (figure data written to reproduction/figure_data)"
  fi
fi
echo; echo "done: outputs under reproduction/"
