#!/bin/bash
# R0 — clean environment build for the JIIM revision rebuild.
#
# WHY: the base miniforge env has scikit-learn 1.9.0, installed 2026-07-17 by
# scikit-survival 0.28.0. That violates econml 0.16.0's `scikit-learn<1.7` pin and
# raises TypeError: LassoCV.__init__() got an unexpected keyword argument 'n_alphas'.
# No causal forest can be fitted in the base env, so R3/R4 are blocked until this exists.
#
# The environment reconstructs the versions attested by dist-info mtime in the Stage-1
# audit. scikit-learn is the one package whose runtime version was never recorded; it is
# pinned here to 1.6.1 as the newest release satisfying econml's constraint, and
# verify_env.py tests whether that choice reproduces the archived Option-B numbers.
set -euo pipefail

ENV_NAME="jiim-r0"
CONDA="conda"
MAMBA="mamba"

echo "=== removing any prior $ENV_NAME ==="
$CONDA env remove -n "$ENV_NAME" -y 2>/dev/null || true

echo "=== creating $ENV_NAME (python 3.12.8) ==="
$MAMBA create -n "$ENV_NAME" -y python=3.12.8 pip

PY="$(conda run -n "$ENV_NAME" python -c 'import sys; print(sys.executable)')"

echo "=== installing pinned analysis stack ==="
"$PY" -m pip install --no-cache-dir \
    "numpy==2.2.3" \
    "scipy==1.15.3" \
    "pandas==2.2.3" \
    "scikit-learn==1.6.1" \
    "statsmodels==0.14.6" \
    "joblib==1.4.2" \
    "econml==0.16.0" \
    "openpyxl" \
    "shap"

echo "=== resulting versions ==="
"$PY" -c "
import sys, platform
import numpy, scipy, pandas, sklearn, statsmodels, joblib, econml
print('python      ', sys.version.split()[0])
print('platform    ', platform.platform())
print('numpy       ', numpy.__version__)
print('scipy       ', scipy.__version__)
print('pandas      ', pandas.__version__)
print('scikit-learn', sklearn.__version__)
print('statsmodels ', statsmodels.__version__)
print('joblib      ', joblib.__version__)
print('econml      ', econml.__version__)
"

echo "=== freezing lockfile ==="
"$PY" -m pip freeze > $(cd "$(dirname "$0")" && pwd)/requirements.lock.txt
$CONDA env export -n "$ENV_NAME" > $(cd "$(dirname "$0")" && pwd)/environment.yml

echo "=== DONE: $ENV_NAME ==="
