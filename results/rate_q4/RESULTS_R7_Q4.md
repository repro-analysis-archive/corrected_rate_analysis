# R7-Q4 — corrected preprocessing-placement diagnostic under standard RATE/AUTOC

**Manuscript:** JDIM-D-26-02440 · **Amendment:** `AMENDMENT_R7_Q4.md`, committed **before
execution** at `0f48a334`, sha256 `5d06197c…22139`.
**Descriptive preprocessing-leakage diagnostic on observed data. Additive RATE point-estimate
contrasts. No confirmatory p-values, no variance ratios, no exponentiation.**
**This does not reproduce, replace or approximate the retired permutation null-variance analysis.**

## Design executed

| regime | imaging block (scaler + PCA) | clinical scaler | causal forest | evaluated on |
|---|---|---|---|---|
| A | training half | training half | training half | held-out half |
| D1 | **full n = 739** | training half | training half | held-out half |
| D2 | training half | **full n = 739** | training half | held-out half |
| B | **full n = 739** | **full n = 739** | training half | held-out half |

Run in both directions on the frozen R7 50/50 split (H1 = R7 training half n = 370, H2 = R7
evaluation half n = 369). Evaluation scores reused byte-for-byte: H2 from
`FROZEN_R7/dr_scores_primary_heldout.csv`, H1 from `FROZEN_R7Q3/dr_scores_H1.csv` — both
configuration-independent and imaging-free.

**Factor P is the whole imaging-block preprocessing placement, scaling *and* PCA together.**

### QA
- Fit-row provenance, all 48 runs: A fits both preprocessing blocks on the training half; D1 fits
  imaging on 739 and clinical on the training half; D2 the reverse; B fits both on 739. The causal
  forest fit-row count equals the training-half size in **every** regime.
- **Causal-forest fit rows falling in a held-out half: 0.** Held-out `Y` and `T` never enter a fit.
- **Structural control (clinical only, factor P absent):** max |D1 − A| = 6.9 × 10⁻¹⁷ (H2) and
  2.2 × 10⁻¹⁶ (H1); max |B − D2| = 8.3 × 10⁻¹⁷ (H2) and 1.7 × 10⁻¹⁶ (H1). The identities hold.
- **Reproduction checks:** `A` on H2 reproduces the frozen R7 Q1 estimates to 3.4 × 10⁻¹⁴; `A` on
  H1 reproduces the frozen Q3 `A_H1` estimates to 2.6 × 10⁻¹⁴.

## Table A — regime RATE values

| Configuration | A_H1 | D1_H1 | D2_H1 | B_H1 | A_H2 | D1_H2 | D2_H2 | B_H2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Clinical only | +0.0514 | *=A* | +0.0458 | +0.0458 | −0.0668 | *=A* | −0.0655 | −0.0655 |
| Clinical + radiomics | +0.1098 | +0.0441 | +0.1081 | +0.0431 | −0.0454 | −0.0277 | −0.0431 | −0.0282 |
| Clinical + BiomedCLIP | +0.0984 | +0.1106 | +0.0978 | +0.1101 | +0.0975 | +0.0477 | +0.0971 | +0.0634 |
| Clinical + RAD-DINO | +0.0569 | +0.0293 | +0.0556 | +0.0309 | −0.1088 | −0.0116 | −0.1104 | −0.0111 |
| Clinical + radiomics + BiomedCLIP | +0.1023 | +0.0437 | +0.1000 | +0.0441 | +0.0464 | +0.0623 | +0.0467 | +0.0592 |
| Clinical + radiomics + RAD-DINO | +0.1062 | +0.0106 | +0.1073 | +0.0107 | −0.0591 | −0.0381 | −0.0597 | −0.0363 |
For clinical only, D1 is structurally identical to A and B to D2 (factor P absent), shown as *=A*.

## Table B — pooled preprocessing contrasts

| Configuration | pooled P | pooled S | pooled P×S | pooled B−A |
|---|---:|---:|---:|---:|
| Clinical only | **N/A** | −0.0022 | **N/A** | −0.0022 |
| Clinical + radiomics | −0.0246 | −0.0002 | −0.0010 | −0.0248 |
| Clinical + BiomedCLIP | −0.0147 | +0.0035 | +0.0081 | −0.0112 |
| Clinical + RAD-DINO | +0.0359 | −0.0002 | +0.0024 | +0.0358 |
| Clinical + radiomics + BiomedCLIP | −0.0216 | −0.0012 | −0.0004 | −0.0228 |
| Clinical + radiomics + RAD-DINO | −0.0370 | +0.0006 | +0.0007 | −0.0365 |
`P = ½[(D1−A)+(B−D2)]`, `S = ½[(D2−A)+(B−D1)]`, `P×S = (B−D2)−(D1−A)`, all additive RATE
point-estimate contrasts, pooled as `(370·H1 + 369·H2)/739`. For clinical only, P and P×S are
**structural N/A** and were not manufactured.

## Table C — relation to corrected Q3

| Configuration | Q3 pooled C−A | Q4 pooled B−A | \|Q4/Q3\| |
|---|---:|---:|---:|
| Clinical only | +0.1570 | −0.0022 | 0.014 |
| Clinical + radiomics | +0.2101 | −0.0248 | 0.118 |
| Clinical + BiomedCLIP | +0.1846 | −0.0112 | 0.061 |
| Clinical + RAD-DINO | +0.2792 | +0.0358 | 0.128 |
| Clinical + radiomics + BiomedCLIP | +0.2271 | −0.0228 | 0.100 |
| Clinical + radiomics + RAD-DINO | +0.2451 | −0.0365 | 0.149 |
## Table D — direction across the two split halves

| Configuration | P_H1 | P_H2 | same sign? | B−A_H1 | B−A_H2 | same sign? |
|---|---:|---:|:--:|---:|---:|:--:|
| Clinical only | N/A | N/A | N/A | −0.0056 | +0.0013 | **no** |
| Clinical + radiomics | −0.0654 | +0.0163 | **no** | −0.0667 | +0.0172 | **no** |
| Clinical + BiomedCLIP | +0.0123 | −0.0418 | **no** | +0.0117 | −0.0341 | **no** |
| Clinical + RAD-DINO | −0.0262 | +0.0982 | **no** | −0.0260 | +0.0977 | **no** |
| Clinical + radiomics + BiomedCLIP | −0.0573 | +0.0142 | **no** | −0.0583 | +0.0128 | **no** |
| Clinical + radiomics + RAD-DINO | −0.0962 | +0.0222 | **no** | −0.0955 | +0.0228 | **no** |
## Readout

- **Pooled P** spans −0.0370 to +0.0359 across the five imaging-containing configurations;
  four of five are negative.
- **Pooled S** spans −0.0022 to +0.0035 across all six.
- **Pooled P×S** spans −0.0010 to +0.0081 across the five.
- **Pooled B − A** spans −0.0365 to +0.0358 across all six.
- **|Q4 pooled B−A| / |Q3 pooled C−A|** spans **0.014 to 0.149**.
- **The direction was inconsistent across split halves in every configuration:** the sign of P
  agrees between H1 and H2 in **0 of 5** imaging configurations, and the sign of B − A agrees in
  **0 of 6**. In the H1 direction B − A is negative in five of six; in the H2 direction it is
  positive in five of six. Which half serves as the evaluation half, not the preprocessing
  placement, determines the sign.

**Full-sample imaging preprocessing changed the RATE point estimate by at most 0.037 in pooled
terms**, and in opposite directions in the two halves. **Clinical-scaler placement had little
apparent effect** — every pooled S value lies within ±0.0036, and for clinical only, where S is the
only factor that exists, the pooled effect is −0.0022. **The preprocessing-only change was small
relative to the total same-sample evaluation increase** measured in corrected Q3: between 1.4 % and
14.9 % of it in absolute magnitude, and of inconsistent sign, against a Q3 effect that was positive
in 6 of 6 configurations and in 12 of 12 individual half-specific values.

## Not claimed

No significance is attached to any Q4 quantity; grf half-sample bootstrap SEs are stored in
`rate_q4_regimes.json` for reference only and are not used to claim that any A-versus-D1/D2/B
difference is supported. The |Q4/Q3| fraction is a magnitude comparison, not a decomposition: Q3
and Q4 follow different paths and no share-of-optimism claim can be built on it. Nothing here
identifies a cause, and P is never described as PCA alone.
