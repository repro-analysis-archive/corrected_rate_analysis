#!/bin/bash
# Stage 0 Part 3 — extend the clean environment to cover feature extraction.
#
# jiim-r0 already covers the causal pipeline and is verified bit-exact against the archived
# Option-B numbers. R2 additionally needs PyRadiomics, SimpleITK, torch, transformers and
# open_clip_torch. PyRadiomics is the risk: the archived features came from the dev build
# 3.1.1.dev111+g8ed579383 (not a PyPI release), and PyRadiomics has historically been awkward
# to build on Python 3.12 / arm64.
#
# Strategy: extend a CLONE, never jiim-r0 itself, so a failed PyRadiomics install cannot
# damage the verified analysis environment.
set -uo pipefail

CONDA="conda"
SRC="jiim-r0"
ENV_NAME="jiim-r0-features"
OUT="$(cd "$(dirname "$0")" && pwd)"

echo "=== cloning $SRC -> $ENV_NAME ==="
$CONDA env remove -n "$ENV_NAME" -y 2>/dev/null || true
$CONDA create -n "$ENV_NAME" --clone "$SRC" -y

PY="$(conda run -n "$ENV_NAME" python -c 'import sys; print(sys.executable)')"

echo "=== imaging + DL stack ==="
"$PY" -m pip install --no-cache-dir \
    "SimpleITK==2.4.1" \
    "nibabel==5.3.2" \
    "torch==2.10.0" \
    "transformers==4.57.6" \
    "open_clip_torch==3.2.0" \
    "pillow" || echo "!! imaging/DL install had failures"

echo "=== pyradiomics (expected to be the hard one) ==="
"$PY" -m pip install --no-cache-dir "pyradiomics" 2>&1 | tail -25 \
  || echo "!! pyradiomics PyPI install FAILED - see PYRADIOMICS_STATUS below"

echo "=== resulting versions ==="
"$PY" - <<'PYEOF'
import sys, platform
print("python      ", sys.version.split()[0])
print("platform    ", platform.platform())
for m in ["numpy","scipy","pandas","sklearn","statsmodels","joblib","econml",
          "SimpleITK","nibabel","torch","transformers","open_clip","radiomics","PIL"]:
    try:
        mod = __import__(m)
        print(f"{m:14s}", getattr(mod, "__version__", "(no __version__)"))
    except Exception as e:
        print(f"{m:14s} NOT AVAILABLE -- {type(e).__name__}: {str(e)[:70]}")
PYEOF

echo "=== lockfiles ==="
"$PY" -m pip freeze > "$OUT/requirements_features.lock.txt"
$CONDA env export -n "$ENV_NAME" > "$OUT/environment_features.yml"

echo "=== DONE ==="
