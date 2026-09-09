# Amendment R7 — standard centred, doubly robust RATE/AUTOC (Path A), Q1 and Q2 only

**Manuscript:** JDIM-D-26-02440
**Status:** protocol-locked post-audit. **Not prespecified.** Committed and hashed **before any
model was fitted.** Outputs to `R7_rate_primary/` only.
**All `FROZEN_*` sets (R2B, R2C, EPOCH, R4, EVALBIAS, DECOMP, STABILITY) and the recovered Linux
2x2 freeze are INPUT ONLY. Nothing writes into any of them.**
**Instruction of record:** `~/Downloads/JIIM_CC_R7_PathA_Primary_RATE_Computation.md`
(preceded by the AUTOC read-only audit, the remediation feasibility audit, and the Path-A method
lock, in that order).

---

## 1. Why this amendment exists — the discovery

The statistic reported as `AUTOC` in Q1-Q4 of every frozen production path is **not** the
Yadlowsky et al. rank-weighted average treatment effect, and is **not**
`grf::rank_average_treatment_effect`. One single implementation is used everywhere
(whitespace-normalised sha256 of the function body `36ae3d43342cf66e`, identical across
`r4_stageA.py`, `r4_stageBC.py`, `run_evalbias.py`, `run_B.py`, `calibrate*.py`,
`run_2x2_linux.py`, and imported by `run_mammaprint_gate1.py`):

```python
def autoc(cate,T,Y):
    i=np.argsort(-cate); Ts,Ys=T[i],Y[i]; nt=nc=0; st=sc=s=0.0
    for j in range(len(cate)):
        if Ts[j]==1: nt+=1; st+=Ys[j]
        else: nc+=1; sc+=Ys[j]
        if nt and nc: s+=st/nt-sc/nc
    return s/len(cate)
```

Writing `D(j)` for the raw treated-minus-control mean difference inside the top-`j` prefix and
`S = {j : both arms present} = {j0..n}`, `m = |S|`:

```
autoc = (1/n) * sum_{j in S} D(j)
      = (m/n) * tau_naive  +  (1/n) * sum_{j in S} [ D(j) - tau_naive ]
```

where `tau_naive = D(n) = Ybar_1 - Ybar_0` does not depend on the ranking at all. Three
departures from standard AUTOC, all confirmed against the grf 2.6.1 source
(`grf/R/rank_average_treatment.R`, `estimate_rate`):

1. **No ATE centering.** grf computes `TOC = cumsum(Gamma_sorted*w)/cumsum(w) - ATE` and
   `RATE = sum(TOC*w)/sum(w)`; the frozen code omits the `- ATE` term entirely. Consequence: under
   an uninformative ranking the frozen statistic's expectation is approximately `tau_naive`, not 0.
   Frozen count table, `FROZEN_R4/cate_PRIMARY__her2neg.npz`, n = 739: control 31/178 pCR
   (0.1742), experimental 174/561 (0.3102), `tau_naive = +0.136003`. Reported strict-OOF values
   span 0.0961-0.2451.
2. **Raw arm-mean differences in place of doubly robust scores.** grf uses per-patient AIPW
   scores `Gamma_i`; the frozen code uses an unadjusted difference of arm means inside each
   covariate-selected prefix, with **no propensity information anywhere in the evaluation stage**.
   In an adaptively randomised platform trial whose assignment probability varies with enrolment
   epoch, that is not a valid subgroup effect estimator.
3. **Prefix skipping with an uncorrected denominator.** Prefixes before both arms appear
   contribute 0 but remain in the denominator `n`, leaving an `m/n` scale factor. grf has no
   such term, because `Gamma_i` is defined per patient.

This reopens and supersedes ledger item **D20** (`HIGH`, `OPEN`), which recorded the same defect
for the withdrawn Stage-1 pipeline. D20's required action was *"R1 must either adopt grf's centred
RATE/AUTOC or rename this statistic and define it in the Methods."* This amendment takes the
first branch.

## 2. Retirement of the old Q1 permutation test as ranking inference

Within-stratum treatment-label permutation destroys the treatment effect, so `E[tau_naive] ~ 0`
under the null while the observed statistic retains it. The frozen strict-OOF null means are
-0.0074 to +0.0075 against observed 0.1621-0.2451. The test therefore rejects

```
H0-A: no treatment effect at all      (rejected; supported)
```

and is silent on

```
H0-B: constant treatment effect       (not tested; its predicted value is ~ tau_naive ~ 0.136)
H0-C: the score carries no heterogeneity information   (not tested)
```

The project's own frozen `R3_smoke/PERMUTATION_DESIGN_PROPOSAL.md` already recorded this, under
the heading *"to appear verbatim in Methods"*: *"Permuting treatment labels breaks the null of no
treatment effect at all; it is not a specific test of the absence of heterogeneity... Rejection is
consistent with a main effect alone."* That sentence never reached the manuscript.

**The old permutation p-values are retired as treatment-effect-ranking evidence and are not
carried forward, reused, or relabelled.** They remain valid as a test of H0-A.

Separately recorded as a factual error to be corrected in the manuscript regardless of method:
Methods 2.5, the Table 2 note and the Fig. 2 legend state 10,000 permutations for **each**
configuration. `r4_stageBC.py` ran Besag-Clifford `M = 10000` for the historically designated
reference configuration only (stage B) and a flat `NSEC = 2000` for the other five (stage C).
Corroborated by `null_principal_693.npy` (80,128 B = 10,000 float64) vs the five
`null_*_693.npy` (16,128 B = 2,000 float64), by `n_draws` in `r4_stageBC_results.json`, by
`n_draws` in the frozen `canonical/Fig2_data.json` rows, and arithmetically by the reported
p floor 0.0005 = 1/2001.

## 3. Q1 population change: 693 -> 739

The n = 693 permutation-overlap population exists solely because `load693()` retains only
HR x MammaPrint x epoch cells containing at least one patient per arm, which is required for
within-stratum label permutation to be defined. With that test retired, the restriction has no
remaining function, and retaining it would carry a treatment-dependent exclusion of 46 patients
(33 experimental, 13 control; outcome-blind by construction per
`R3_smoke/r4_population_verification.json`) into an analysis that does not need it.

**Q1 primary population is now n = 739, identical to Q2.** The frozen n = 693 results are
retired, not converted. `FROZEN_R4/population_sensitivity.json` remains available as a documented
composition sensitivity.

## 4. Independent held-out primary RATE analysis

grf 2.6.1 roxygen, `rank_average_treatment_effect` and `rank_average_treatment_effect.fit`:
*"WARNING: for valid statistical performance, these scores should be constructed independently
from the evaluation forest training data."* grf's canonical example splits
`train <- sample(1:n, n/2)`, fits the CATE on the training half, predicts on the held-out half,
and estimates the AIPW nuisances **on the held-out half**. The grf RATE-CV article shows that
naive reuse of the same data across folds rejects at **16.8 %** against a nominal 5 % (n = 1500,
p = 5, no heterogeneity), while sequential cross-fold estimation attains 5.4 %.

The six frozen OOF priority vectors were produced by ordinary 5-fold cross-fitting, in which
each fold's training set overlaps every other fold's evaluation set. They therefore **cannot**
support a valid RATE = 0 test, either pooled or aggregated across folds.

**Primary design: one independent 50/50 train/evaluation split, seed 42, constructed without
using Y.** Priorities are fitted on the training half only, with every data-adaptive
preprocessing step (clinical scaler, imaging scaler, PCA) fitted on the training half only. The
common doubly robust evaluation score is built on the evaluation half only, from non-imaging
baseline/design covariates, and is shared by all six prioritization rules so that the six
comparisons differ **only** in the ranking.

The old outcome-stratified `StratifiedKFold(2*T + Y)` assignment is **not** reused as the new
inferential split. The split is not re-drawn, re-seeded, or adjusted after its composition is
inspected.

**Sequential cross-fold is used for a Q1-only sensitivity analysis**, on a new Y-independent
random 5-fold partition at seed 42, aggregated as `z = sum(t_k)/sqrt(K-1)`,
`p = 2*Phi(-|z|)`. It is **not** used to produce the primary Q2 paired-difference p-value: the
RATE-CV martingale argument is established for the RATE = 0 heterogeneity test, not for a
difference between two learned prioritization rules.

## 5. Nuisance / evaluation covariate set Z — configuration-independent, no imaging

Count tables from the hash-verified source workbook (sha256 `0d95c6af...31f1c`, matching
`FROZEN_R4/input_provenance.sha256`), HER2-negative n = 739:

- **`tumor_subtype` is exactly collinear with `hr`**: luminal_a <-> hr = 1 (381),
  triple_negative <-> hr = 0 (358), zero off-diagonal. `tumor_subtype` is therefore **excluded**
  from Z and `hr` retained. (Note for the record: this means HR status was already present in the
  frozen **X** under the name `tumor_subtype_enc`.)
- `mammaprint` is **not** collinear with `hr` (56/276, 302/105) and is **retained**.
- `her2` is constant within the primary population and is **excluded**.
- **`menopause` carries two near-duplicate levels differing by a single space**:
  `pre (<6 months since LMP ...)` n = 263 and `pre (< 6 months since LMP ...)` n = 108. The frozen
  `LabelEncoder` in `r4_stageA.load()` treats them as two distinct ordinal codes inside **X**.
  **The two levels are merged in the R7 Z matrix only.** The frozen CATE feature pipeline is
  **not** altered, because doing so would invalidate every frozen ranking; the split of 371
  premenopausal patients across two arbitrary codes in X is recorded as a pre-existing limitation
  of the feature set.
- Missingness carried as an explicit level / indicator, not imputed away: bmi_group 138/739
  (18.7 %), menopause 129/739 (17.5 %), ethnicity 3, age 3.

**Z = age (median-imputed within the set in which it is used, plus a missingness indicator),
hr, mammaprint, ethnicity (one-hot incl. unknown), bmi_group (one-hot incl. unknown), menopause
(one-hot, "pre" merged, incl. unknown), enrollment epoch (one-hot).** All categoricals are
one-hot encoded rather than label-encoded as ordinal integers, because ordinal coding of nominal
categories imposes an arbitrary ordering; this is a nuisance-model choice and does not touch X.
Radiomics, BiomedCLIP and RAD-DINO are excluded by construction.

The epoch one-hot basis is taken from the full 739-row epoch column (22 fixed levels, from
`FROZEN_EPOCH/epoch_assignment.csv`, sha256 `b893a669...c99067`) so that the encoding is
identical on both halves. Epoch level membership is fixed design metadata containing no outcome
or treatment information; this matches the frozen `r4_stageA.load()` behaviour and is recorded
here rather than left implicit.

## 6. Propensity wording — binding

The propensity used inside the evaluation score is an **estimated observed treatment-assignment
mechanism conditional on the available design and baseline covariates**. It is **not** a
reconstruction of the actual I-SPY2 randomization probabilities: per-patient assignment
probabilities do not exist in the released data, all 50 columns of the source workbook were
checked (`R3_smoke/ITEM6_ARM_AVAILABILITY.md`), and the acquisition dates are shifted for
de-identification so published arm schedules cannot be joined. Any wording implying recovery of
the design propensity is prohibited.

## 7. Naming — binding

Configuration 5, `Clin + Rad + BiomedCLIP`, is called the **historically designated reference
configuration** and nothing else. It is never *prespecified*, *primary model*, *selected model*,
*best model* or *best-performing* (decision D52).

## 8. Scope of this amendment

**Q1 and Q2 only.** Corrected Q3 and corrected Q4 are deferred until these results are reviewed.
Q4, when run, is Option 2 (an observed-data preprocessing-placement diagnostic under the
corrected framework) and must never be described as a recovery of the old null-variance ratios:
null-distribution variance, sampling standard error, and evaluation-induced optimism in point
estimates are three different quantities.

No figure is regenerated, no manuscript or supplement file is edited, no reviewer response is
drafted, and no frozen output is overwritten by this amendment.

## 9. Prohibited readings of the R7 output

- A confidence interval covering 0 is **failure to demonstrate**, never equivalence and never
  absence of treatment-effect heterogeneity. No equivalence margin is defined.
- No configuration-superiority claim between the five imaging-containing configurations.
- No relative-improvement figure for the FM-versus-clinical comparison.
- HER2-positive (n = 241, 31 controls) is exploratory/descriptive only. If an independent split
  leaves too few controls for stable RATE inference, the result is reported as
  `NOT ESTIMATED FOR INFERENCE` rather than forced into a p-value.
- grf and econml do not compute the same estimand (grf integrates the RATE over all n patient
  increments; `econml.validate.utils.calc_uplift` uses a 50-point left-Riemann sum truncated to
  q in [0.05, 0.95]). The econml run is a sign / ordering / gross-error cross-check only and
  exact numerical agreement is neither expected nor required.

## 10. Stop conditions

Halt and report rather than continue if: the split construction touches Y; evaluation priorities
are generated using evaluation outcomes or treatment; imaging enters the common evaluation score;
the grf paired two-priority comparison cannot be reproduced from the documented interface; any
result would be written into a frozen directory; or any manuscript/figure file would be modified.
