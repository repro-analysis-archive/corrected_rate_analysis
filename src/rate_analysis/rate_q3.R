#!/usr/bin/env Rscript
# R7-Q3 - two-way honest-vs-apparent RATE/AUTOC optimism diagnostic. POINT ESTIMATES for C.
# grf bootstrap SEs are retained for the HONEST A rates only and are labelled as such.
suppressPackageStartupMessages({library(grf); library(jsonlite)})
RELEASE_ROOT <- Sys.getenv("JIIM_RELEASE_ROOT", unset = getwd())   # run from the repository root, or set JIIM_RELEASE_ROOT
R7  <- file.path(RELEASE_ROOT, "reproduction", "rate_primary"); FZ <- R7   # primary-stage outputs (the frozen R7 set in the original run)
OUT <- file.path(RELEASE_ROOT, "reproduction", "rate_q3"); dir.create(OUT, recursive = TRUE, showWarnings = FALSE)
SEED <- 42; BOOTSEED <- 20260906; RB <- 2000
cfgs <- c("Clinical only","Clin + Radiomics","Clin + BiomedCLIP","Clin + RAD-DINO",
          "Clin + Rad + BiomedCLIP","Clin + Rad + RAD-DINO")
rate_pt <- function(G, s) { set.seed(BOOTSEED)
  r <- rank_average_treatment_effect.fit(G, s, target = "AUTOC", R = 2)   # R=2: point estimate only
  as.numeric(r$estimate) }
rate_se <- function(G, s) { set.seed(BOOTSEED)
  r <- rank_average_treatment_effect.fit(G, s, target = "AUTOC", R = RB)
  c(as.numeric(r$estimate), as.numeric(r$std.err)) }

# ---- H2: frozen R7 DR vector, reused byte-for-byte ----
drH2 <- read.csv(file.path(FZ, "dr_scores_primary_heldout.csv"))
p2   <- read.csv(file.path(OUT, "priorities_q3_H2.csv"))
stopifnot(identical(as.character(drH2$patient_id),
                    as.character(p2$patient_id[p2$configuration == cfgs[1]])))
G2 <- drH2$dr_score
# ---- H1: one new common DR vector, same locked spec ----
d1 <- read.csv(file.path(OUT, "Z_H1.csv"), check.names = FALSE)
Z1 <- as.matrix(d1[, setdiff(names(d1), c("patient_id","T","Y")), drop = FALSE])
set.seed(SEED); cf1 <- causal_forest(X = Z1, Y = d1$Y, W = d1$T, num.trees = 2000, seed = SEED)
G1 <- get_scores(cf1); w1 <- cf1$W.hat
p1 <- read.csv(file.path(OUT, "priorities_q3_H1.csv"))
stopifnot(identical(as.character(d1$patient_id), as.character(p1$patient_id[p1$configuration == cfgs[1]])))
cat(sprintf("H1 eval forest: n=%d  W.hat [%.4f, %.4f]  outside[.05,.95]=%.4f\n",
            nrow(d1), min(w1), max(w1), mean(w1 < .05 | w1 > .95)))

frozen_q1 <- fromJSON(file.path(FZ, "rate_q1_primary.json"))$q1
nH1 <- nrow(d1); nH2 <- nrow(drH2); res <- list(); maxdiff <- 0
for (cg in cfgs) {
  s2A <- p2$priority_A[p2$configuration == cg]; s2C <- p2$priority_C[p2$configuration == cg]
  s1A <- p1$priority_A[p1$configuration == cg]; s1C <- p1$priority_C[p1$configuration == cg]
  aH2 <- rate_se(G2, s2A); cH2 <- rate_pt(G2, s2C)
  aH1 <- rate_se(G1, s1A); cH1 <- rate_pt(G1, s1C)
  # run check: A_H2 must reproduce the frozen R7 Q1 estimate exactly
  fz <- frozen_q1[[cg]]$estimate; d <- abs(aH2[1] - fz); maxdiff <- max(maxdiff, d)
  o1 <- cH1 - aH1[1]; o2 <- cH2 - aH2[1]
  res[[cg]] <- list(A_H1 = aH1[1], A_H1_se_heldout = aH1[2], C_H1 = cH1, optimism_H1 = o1,
                    A_H2 = aH2[1], A_H2_se_heldout = aH2[2], C_H2 = cH2, optimism_H2 = o2,
                    pooled_optimism = (nH1*o1 + nH2*o2)/739,
                    frozen_R7_A_H2 = fz, abs_diff_vs_frozen_R7 = d,
                    both_halves_positive = (o1 > 0 && o2 > 0))
  cat(sprintf("  %-26s A_H1 %+.4f C_H1 %+.4f (C-A %+.4f) | A_H2 %+.4f C_H2 %+.4f (C-A %+.4f) | pooled %+.4f  |chk %.1e\n",
              cg, aH1[1], cH1, o1, aH2[1], cH2, o2, res[[cg]]$pooled_optimism, d))
}
cat(sprintf("\nrun check: max |RATE(A_H2) - frozen R7 Q1| = %.3e\n", maxdiff))
pooled <- sapply(cfgs, function(cg) res[[cg]]$pooled_optimism)
write_json(list(design = list(
    question = "change in the standard RATE/AUTOC POINT ESTIMATE under same-sample versus independent evaluation",
    kind = "descriptive evaluation-induced-optimism diagnostic; NOT a test of treatment-effect heterogeneity",
    split = "frozen R7 50/50 split reused verbatim; H1 = R7 training half n=370, H2 = R7 evaluation half n=369",
    H2_dr = "FROZEN_R7/dr_scores_primary_heldout.csv reused byte-for-byte",
    H1_dr = "new common vector, same locked spec: causal_forest(X=Z_H1 imaging-free, Y, W=T, 2000 trees, seed 42), get_scores()",
    pooled = "(370*optimism_H1 + 369*optimism_H2)/739, predeclared in AMENDMENT_R7_Q3.md section 5",
    uncertainty = "grf half-sample bootstrap SE retained for the HONEST A rates only (R=2000, seed 20260906); NO SE, CI or p-value for C, for C-A, or for pooled optimism",
    grf_version = as.character(packageVersion("grf"))),
  overlap_H1 = list(n = nrow(d1), W_hat_min = min(w1), W_hat_max = max(w1),
                    prop_outside_0.05_0.95 = mean(w1 < .05 | w1 > .95),
                    prop_outside_0.01_0.99 = mean(w1 < .01 | w1 > .99)),
  run_check = list(max_abs_diff_A_H2_vs_frozen_R7 = maxdiff, passed = maxdiff < 1e-9),
  n_H1 = nH1, n_H2 = nH2, results = res,
  summary = list(pooled_min = min(pooled), pooled_max = max(pooled),
                 n_pooled_gt_0 = sum(pooled > 0), n_configs = length(cfgs),
                 n_both_halves_positive = sum(sapply(cfgs, function(cg) res[[cg]]$both_halves_positive)))),
  file.path(OUT, "rate_q3.json"), auto_unbox = TRUE, digits = 12, pretty = TRUE)
write.csv(data.frame(patient_id = d1$patient_id, T = d1$T, Y = d1$Y,
                     e_hat = w1, Y_hat = cf1$Y.hat, dr_score = as.numeric(G1)),
          file.path(OUT, "dr_scores_H1.csv"), row.names = FALSE)
cat("wrote rate_q3.json, dr_scores_H1.csv\n")
