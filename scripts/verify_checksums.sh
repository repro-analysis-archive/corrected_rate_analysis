#!/usr/bin/env bash
# Verify every released file against checksums/SHA256SUMS.txt.
set -euo pipefail
cd "$(dirname "$0")/.."
if command -v sha256sum >/dev/null 2>&1; then
  sha256sum -c checksums/SHA256SUMS.txt
else
  shasum -a 256 -c checksums/SHA256SUMS.txt
fi
