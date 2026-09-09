#!/usr/bin/env Rscript
# R7 step 3 - standard centred doubly robust RATE/AUTOC (grf 2.6.1).
# Common evaluation forest on imaging-free Z, held-out evaluation half only.
suppressPackageStartupMessages({library(grf); library(jsonlite)})
RELEASE_ROOT <- Sys.getenv("JIIM_RELEASE_ROOT", unset = getwd())   # run from the repository root, or set JIIM_RELEASE_ROOT
OUT <- file.path(RELEASE_ROOT, "reproduction", "rate_primary"); dir.create(OUT, recursive = TRUE, showWarnings = FALSE)
SEED <- 42; BOOTSEED <- 20260906; RB <- 2000
REFERENCE <- "Clin + Rad + BiomedCLIP"; BASELINE <- "Clinical only"

read_Z <- function(f) {
  d <- read.csv(file.path(OUT, f), check.names = FALSE)
  list(Z = as.matrix(d[, setdiff(names(d), c("patient_id","T","Y")), drop = FALSE]),
       T = d$T, Y = d$Y, id = d$patient_id)
}
eval_forest <- function(e) {
  set.seed(SEED)
  causal_forest(X = e$Z, Y = e$Y, W = e$T, num.trees = 2000, seed = SEED)
}
overlap <- function(cf) {
  w <- cf$W.hat
  list(n = length(w), min = min(w), q = as.numeric(quantile(w, c(.05,.25,.5,.75,.95))), max = max(w),
       prop_outside_0.05_0.95 = mean(w < .05 | w > .95), prop_outside_0.01_0.99 = mean(w < .01 | w > .99))
}
rate1 <- function(cf, s) {                       # single rule
  set.seed(BOOTSEED)
  r <- rank_average_treatment_effect(cf, priorities = s, target = "AUTOC", R = RB)
  est <- as.numeric(r$estimate); se <- as.numeric(r$std.err)
  list(estimate = est, std_err = se, ci = c(est - 1.96*se, est + 1.96*se),
       z = est/se, p = 2*pnorm(-abs(est/se)))
}
rate2 <- function(cf, s1, s2, n1, n2) {          # paired: column1 - column2
  pri <- data.frame(a = s1, b = s2); colnames(pri) <- c(n1, n2)
  set.seed(BOOTSEED)
  r <- rank_average_treatment_effect(cf, priorities = pri, target = "AUTOC", R = RB)
  est <- as.numeric(r$estimate); se <- as.numeric(r$std.err); nm <- names(r$estimate)
  if (is.null(nm)) nm <- r$TOC$priority[!duplicated(r$TOC$priority)]
  out <- list()
  for (i in seq_along(est)) out[[nm[i]]] <- list(estimate = est[i], std_err = se[i],
      ci = c(est[i] - 1.96*se[i], est[i] + 1.96*se[i]), z = est[i]/se[i], p = 2*pnorm(-abs(est[i]/se[i])))
  list(target_labels = nm, results = out)
}
get_prio <- function(f, cfg, id) {
  d <- read.csv(file.path(OUT, f)); d <- d[d$configuration == cfg, ]
  stopifnot(identical(as.character(d$patient_id), as.character(id)))
  d$priority
}

# ---------------- primary evaluation half (n = 369) ----------------
e  <- read_Z("Z_eval_primary.csv"); cf <- eval_forest(e); DR <- get_scores(cf)
ov <- overlap(cf)
cat(sprintf("eval forest: n=%d  W.hat [%.4f, %.4f]  outside[.05,.95]=%.4f\n",
            ov$n, ov$min, ov$max, ov$prop_outside_0.05_0.95))

cfgs <- c("Clinical only","Clin + Radiomics","Clin + BiomedCLIP","Clin + RAD-DINO",
          "Clin + Rad + BiomedCLIP","Clin + Rad + RAD-DINO")
q1 <- list()
for (cg in cfgs) {
  s <- get_prio("priorities_primary_heldout.csv", cg, e$id)
  q1[[cg]] <- rate1(cf, s)
  cat(sprintf("  Q1 %-26s RATE %+.4f  SE %.4f  p %.4g\n", cg, q1[[cg]]$estimate, q1[[cg]]$std_err, q1[[cg]]$p))
}
praw <- sapply(cfgs, function(cg) q1[[cg]]$p)
pholm <- p.adjust(praw, method = "holm")
for (cg in cfgs) q1[[cg]]$p_holm <- unname(pholm[cg])

# internal check: forest interface vs .fit with explicitly extracted DR scores
s_ref <- get_prio("priorities_primary_heldout.csv", REFERENCE, e$id)
set.seed(BOOTSEED); chk <- rank_average_treatment_effect.fit(DR, s_ref, target = "AUTOC", R = RB)
fit_check <- list(forest_interface = q1[[REFERENCE]]$estimate,
                  dot_fit_interface = as.numeric(chk$estimate),
                  abs_diff = abs(q1[[REFERENCE]]$estimate - as.numeric(chk$estimate)),
                  se_forest = q1[[REFERENCE]]$std_err, se_dot_fit = as.numeric(chk$std.err))
cat(sprintf("  interface check: forest %+.6f vs .fit %+.6f  |diff| %.2e\n",
            fit_check$forest_interface, fit_check$dot_fit_interface, fit_check$abs_diff))

# ---------------- Q2 primary paired contrast ----------------
s_clin <- get_prio("priorities_primary_heldout.csv", BASELINE, e$id)
q2 <- rate2(cf, s_ref, s_clin, "reference", "clinical_only")
cat("  Q2 labels: ", paste(q2$target_labels, collapse = " | "), "\n")
for (nm in names(q2$results)) cat(sprintf("     %-28s %+.4f  SE %.4f  p %.4g\n",
    nm, q2$results[[nm]]$estimate, q2$results[[nm]]$std_err, q2$results[[nm]]$p))

# ---------------- Q2 sensitivities ----------------
sens <- list()
mk <- function(file, a, b, la, lb, cfx, ex) {
  s1 <- get_prio(file, a, ex$id); s2 <- get_prio(file, b, ex$id)
  rate2(cfx, s1, s2, la, lb)
}
sens[["mammaprint"]] <- mk("priorities_sens_mammaprint.csv", "Historical reference + MammaPrint",
                           "Clinical + MammaPrint", "reference_plus_MP", "clinical_plus_MP", cf, e)
sens[["no_epoch"]]   <- mk("priorities_sens_no_epoch.csv", REFERENCE, BASELINE,
                           "reference", "clinical_only", cf, e)
sens[["alt_nuisance"]] <- mk("priorities_sens_alt_nuisance.csv", REFERENCE, BASELINE,
                           "reference", "clinical_only", cf, e)
e2 <- read_Z("Z_eval_empty_arm.csv"); cf2 <- eval_forest(e2); ov2 <- overlap(cf2)
sens[["empty_arm_728"]] <- mk("priorities_sens_empty_arm.csv", REFERENCE, BASELINE,
                           "reference", "clinical_only", cf2, e2)
for (k in names(sens)) {
  cat(sprintf("  SENS %-14s", k))
  for (nm in names(sens[[k]]$results)) cat(sprintf("  %s %+.4f(SE %.4f)", nm, sens[[k]]$results[[nm]]$estimate, sens[[k]]$results[[nm]]$std_err))
  cat("\n")
}

write_json(list(design = list(seed = SEED, boot_seed = BOOTSEED, R = RB, target = "AUTOC",
                              grf_version = as.character(packageVersion("grf")),
                              eval_forest = "causal_forest(X=Z_nonimaging, Y, W=T, num.trees=2000)",
                              se_method = "half-sample bootstrap (grf boot_grf half.sample=TRUE), sd over R replicates",
                              ci = "estimate +/- 1.96*SE", p = "2*pnorm(-|estimate/SE|)"),
                overlap_primary = ov, overlap_empty_arm = ov2,
                interface_check = fit_check, q1 = q1),
           file.path(OUT, "rate_q1_primary.json"), auto_unbox = TRUE, digits = 12, pretty = TRUE)
write_json(list(comparison = "historically designated reference configuration - clinical only",
                n_eval = length(e$id), primary = q2),
           file.path(OUT, "rate_q2_primary.json"), auto_unbox = TRUE, digits = 12, pretty = TRUE)
write_json(list(sensitivities = sens, n_eval_primary = length(e$id), n_eval_empty_arm = length(e2$id)),
           file.path(OUT, "rate_q2_sensitivities.json"), auto_unbox = TRUE, digits = 12, pretty = TRUE)
write_json(list(primary = ov, empty_arm = ov2), file.path(OUT, "overlap_diagnostics.json"),
           auto_unbox = TRUE, digits = 12, pretty = TRUE)
dr <- data.frame(patient_id = e$id, T = e$T, Y = e$Y, e_hat = cf$W.hat, Y_hat = cf$Y.hat, dr_score = as.numeric(DR))
write.csv(dr, file.path(OUT, "dr_scores_primary_heldout.csv"), row.names = FALSE)
cat("\nwrote rate_q1_primary.json, rate_q2_primary.json, rate_q2_sensitivities.json, overlap_diagnostics.json, dr_scores_primary_heldout.csv\n")
