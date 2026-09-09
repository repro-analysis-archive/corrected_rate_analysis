# Random seeds

Machine-readable copy: `seeds.json`.

| use | seed | generator / call |
|---|---|---|
| fixed 50/50 split (H1 = 370 / H2 = 369) | 42 | `numpy.random.default_rng(42).permutation(739)`; the first 370 permuted indices form H1; outcome and treatment not used, no stratification (`src/rate_analysis/r7_common.py`, `split_739`) |
| sequential 5-fold partition (Q1 sensitivity) | 42 | `numpy.random.default_rng(42).permutation(739)` split into five nearly equal folds with `numpy.array_split` (`build_Z.py`) |
| PCA, random forests, causal forests (prioritization rules) | 42 | `PCA(random_state = 42)`, `RandomForest*(random_state = 42)`, `CausalForestDML(random_state = 42)` |
| grf evaluation causal forest | 42 | `set.seed(42); causal_forest(..., num.trees = 2000, seed = 42)` |
| grf half-sample bootstrap of every RATE estimate | 20260906 | `set.seed(20260906)` immediately before each `rank_average_treatment_effect` / `.fit` call; `R = 2000` |
| econml cross-check (`calc_uplift`) | 200 bootstrap draws | sign / ordering / gross-error check only |

The split and partition are stored explicitly in `splits/split_739.csv` and `splits/seq_folds_739.csv`; they are
loaded, not re-derived, by the Q3 and Q4 scripts.
