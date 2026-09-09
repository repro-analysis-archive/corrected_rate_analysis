#!/usr/bin/env Rscript
# R7 step 5 - Q1-ONLY sequential cross-fold sensitivity (grf RATE-CV aggregation).
suppressPackageStartupMessages({library(grf); library(jsonlite)})
RELEASE_ROOT <- Sys.getenv("JIIM_RELEASE_ROOT", unset = getwd())   # run from the repository root, or set JIIM_RELEASE_ROOT
OUT <- file.path(RELEASE_ROOT, "reproduction", "rate_primary"); dir.create(OUT, recursive = TRUE, showWarnings = FALSE)
SEED <- 42; BOOTSEED <- 20260906; RB <- 2000
cfgs <- c("Clinical only","Clin + Radiomics","Clin + BiomedCLIP","Clin + RAD-DINO",
          "Clin + Rad + BiomedCLIP","Clin + Rad + RAD-DINO")
pri <- read.csv(file.path(OUT, "priorities_sequential.csv"))
tstat <- matrix(NA_real_, length(cfgs), 4, dimnames = list(cfgs, paste0("fold", 2:5)))
est <- tstat; se <- tstat; degen <- matrix(FALSE, length(cfgs), 4, dimnames = dimnames(tstat)); ovl <- list()
for (k in 2:5) {
  d <- read.csv(file.path(OUT, sprintf("Z_eval_seqfold%d.csv", k)), check.names = FALSE)
  Z <- as.matrix(d[, setdiff(names(d), c("patient_id","T","Y")), drop = FALSE])
  set.seed(SEED); cf <- causal_forest(X = Z, Y = d$Y, W = d$T, num.trees = 2000, seed = SEED)
  w <- cf$W.hat
  ovl[[paste0("fold", k)]] <- list(n = nrow(d), n_treated = sum(d$T), n_control = sum(1 - d$T),
      W_hat_min = min(w), W_hat_max = max(w), prop_outside_0.05_0.95 = mean(w < .05 | w > .95))
  for (cg in cfgs) {
    s <- pri[pri$seq_fold == k & pri$configuration == cg, ]
    stopifnot(identical(as.character(s$patient_id), as.character(d$patient_id)))
    set.seed(BOOTSEED)
    r <- rank_average_treatment_effect(cf, priorities = s$priority, target = "AUTOC", R = RB)
    e_ <- as.numeric(r$estimate); s_ <- as.numeric(r$std.err)
    est[cg, k-1] <- e_; se[cg, k-1] <- s_
    # A DEGENERATE (constant) prioritization rule has RATE identically 0 with no ranking
    # variability: grf returns estimate 0 and std.err 0, so the t-statistic is 0/0. Such a fold
    # carries exactly zero evidence for heterogeneity, so its t-statistic is set to 0 while the
    # locked sqrt(K-1) denominator is retained. This DILUTES the aggregate and is conservative.
    degen[cg, k-1] <- (length(unique(s$priority)) <= 1)
    tstat[cg, k-1] <- if (degen[cg, k-1] || s_ == 0) 0 else e_ / s_
  }
  cat(sprintf("  fold %d done (n=%d, control=%d)\n", k, nrow(d), sum(1 - d$T)))
}
z <- rowSums(tstat) / sqrt(5 - 1)                 # locked rule: K = 5, denominator sqrt(K-1) = 2
p <- 2 * pnorm(-abs(z)); ph <- p.adjust(p, method = "holm")
# secondary, clearly labelled: restricted to the folds whose rule is non-degenerate
nz <- rowSums(!degen)
z2 <- rowSums(tstat) / sqrt(pmax(nz, 1)); p2 <- 2 * pnorm(-abs(z2)); ph2 <- p.adjust(p2, method = "holm")
res <- list()
for (cg in cfgs) res[[cg]] <- list(fold_estimates = as.numeric(est[cg, ]), fold_se = as.numeric(se[cg, ]),
    fold_t = as.numeric(tstat[cg, ]), fold_degenerate = as.logical(degen[cg, ]),
    n_nondegenerate_folds = unname(nz[cg]),
    z = unname(z[cg]), p = unname(p[cg]), p_holm = unname(ph[cg]),
    z_restricted = unname(z2[cg]), p_restricted = unname(p2[cg]), p_holm_restricted = unname(ph2[cg]))
for (cg in cfgs) cat(sprintf("  %-26s t = [%s]  z %+.3f  p %.4g  Holm %.4g   | restricted(k=%d) z %+.3f p %.4g Holm %.4g\n", cg,
    paste(sprintf("%+.2f%s", tstat[cg, ], ifelse(degen[cg, ], "*", "")), collapse = ", "),
    z[cg], p[cg], ph[cg], nz[cg], z2[cg], p2[cg], ph2[cg]))
write_json(list(design = list(partition = "new Y-independent random 5-fold, seed 42",
   rule = "for k=2..5 fit on folds 1..k-1, evaluate on fold k; DR scores from a causal forest on fold k only",
   aggregation = "z = sum(t_k)/sqrt(K-1) with K=5; p = 2*pnorm(-|z|); Holm across six configurations",
   degenerate_fold_rule = "a fold whose fitted rule is constant contributes t_k = 0 with the sqrt(K-1) denominator retained (conservative); a secondary z_restricted divides by sqrt(number of non-degenerate folds) and is reported alongside, clearly labelled",
   scope = "Q1 heterogeneity sensitivity ONLY; never used for the Q2 paired difference",
   grf_version = as.character(packageVersion("grf")), R = RB, boot_seed = BOOTSEED),
   overlap_by_fold = ovl, results = res),
   file.path(OUT, "rate_q1_sequential_sensitivity.json"), auto_unbox = TRUE, digits = 12, pretty = TRUE)
cat("\nwrote rate_q1_sequential_sensitivity.json\n")
