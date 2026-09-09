# Supplement Table S-R1 — corrected radiomics extraction versus the originally submitted extraction

**Cohorts pooled, n = 980** (HER2− 739 + HER2+ 241). Outcome-blinded: no Y, T, CATE or AUTOC.

## Panel A — degeneracy under the originally submitted settings

| metric | originally submitted<br>`binWidth=25`, `normalize=True`, `normalizeScale=1`, no resampling | corrected<br>`binCount=64`, `normalize=False`, 1 mm isotropic |
|---|---|---|
| first-order Entropy numerically zero (\|·\| < 1e-12) | **39.80 %** | **0.00 %** |
| GLCM JointEnergy exactly 1.0 | **39.80 %** | **0.00 %** |
| first-order Uniformity exactly 1.0 | **39.80 %** | **0.00 %** |
| first-order Uniformity > 0.99 | **88.37 %** | **0.00 %** |
| texture features with zero variance | **0.00 %** | **0.00 %** |
| texture features near-zero variance | **0.00 %** | **0.00 %** |

Median effective (non-empty) bins per tumour: **2** originally → **63** corrected.
Tumours within the IBSI 30–130 reference band: **0 %** → **100 %**.

## Panel B — feature-wise Spearman between the two extractions

| feature family | n | ρ median | ρ min | ρ < 0.5 | ρ < 0.9 |
|---|---|---|---|---|---|
| shape | 14 | 0.999 | 0.989 | 0 | 0 |
| firstorder | 18 | 0.237 | -0.223 | 15 | 16 |
| glcm | 24 | -0.095 | -0.170 | 24 | 24 |
| glrlm | 16 | 0.177 | -0.263 | 10 | 16 |
| glszm | 16 | 0.210 | -0.254 | 14 | 16 |
| ngtdm | 5 | -0.038 | -0.193 | 5 | 5 |
| gldm | 14 | 0.067 | -0.653 | 7 | 13 |
| **all** | **107** | **0.155** | -0.653 | **75** | **90** |

**Interpretation.** Shape descriptors are invariant (ρ median 0.999) — resampling is the only
thing that touches them. Every texture family is decorrelated from its originally submitted
counterpart; GLCM has all 24 features below ρ = 0.5 with a median of −0.095, i.e. no rank
information in common.

> The originally submitted comparison did not test foundation-model embeddings against conventional
> radiomic texture. It tested them against a degenerate feature set in which, for approximately 40 %
> of tumours, the texture families carried shape and size information only.

Per-feature values: `g1_feature_correlations_binCount64.csv`.