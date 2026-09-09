# Final figures

Figures 1 to 5 of the revised manuscript as vector PDF, 600 dpi TIFF (174 mm wide) and MATLAB `.fig`,
rendered with `src/figures/make_Fig1.m` … `make_Fig5.m` (MATLAB R2025b, Arial) from `figure_data/fig_data_r7.mat`.
`matlab -batch "cd('src/figures'); build_all"` regenerates them under `reproduction/figures/`.

| figure | content | inference |
|---|---|---|
| Fig. 1 | analytic framework: cohort 980 → HER2-negative 739 (primary) / HER2-positive 241 (exploratory); fixed 50/50 split H1 = 370 / H2 = 369; empty-arm sensitivity 728; questions Q1 to Q4 | design |
| Fig. 2 | Q1: six standard centred doubly robust RATE/AUTOC estimates with 95 % CI, independent held-out evaluation | inferential |
| Fig. 3 | Q2: (A) clinical-only versus reference held-out RATE; (B) paired ΔRATE, primary and four sensitivities | inferential / sensitivity |
| Fig. 4 | Q3: change in the RATE point estimate, same-sample minus opposite-half, H1 / H2 / pooled | descriptive |
| Fig. 5 | Q4: (A) regimes A / D1 / D2 / B; (B) half-specific B − A; (C) pooled additive P / S / P×S contrasts | descriptive |
