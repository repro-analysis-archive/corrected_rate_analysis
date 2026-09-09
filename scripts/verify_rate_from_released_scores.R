#!/usr/bin/env Rscript
# verify_rate_from_released_scores.R
#
# Recomputes every reported RATE/AUTOC quantity that depends only on the released per-patient doubly robust
# scores (derived_data/*/dr_scores_*.csv) and prioritization scores (derived_data/*/priorities_*.csv), using
# grf::rank_average_treatment_effect.fit exactly as the analysis scripts do (target = "AUTOC", half-sample
# bootstrap R = 2000, set.seed(20260906) immediately before every call), and compares the results with the
# released results/*.json files. No source data and no patient identifiers are needed: the files are aligned by
# their positional row labels (h2_row, h1_row).
#
# Not covered (each needs an evaluation forest whose covariates are not redistributed; both are reproduced by
# the full pipeline, see docs/REPRODUCTION.md): the empty-arm exclusion sensitivity and the Q1 sequential
# cross-fold sensitivity.
suppressPackageStartupMessages({library(grf); library(jsonlite)})
RELEASE_ROOT <- Sys.getenv("JIIM_RELEASE_ROOT", unset = getwd())
D  <- function(...) file.path(RELEASE_ROOT, "derived_data", ...)
RS <- function(...) file.path(RELEASE_ROOT, "results", ...)
BOOTSEED <- 20260906; RB <- 2000; TOL <- 1e-9
cfgs <- c("Clinical only", "Clin + Radiomics", "Clin + BiomedCLIP", "Clin + RAD-DINO",
          "Clin + Rad + BiomedCLIP", "Clin + Rad + RAD-DINO")
cat(sprintf("grf %s | %s | tolerance %.0e\n", as.character(packageVersion("grf")), R.version$version.string, TOL))

n_ok <- 0; n_fail <- 0; worst <- 0
chk <- function(label, got, want) {
  d <- abs(got - want); worst <<- max(worst, d)
  if (is.na(d) || d > TOL) { n_fail <<- n_fail + 1
    cat(sprintf("  FAIL %-64s got %+.12f  want %+.12f  |diff| %.2e\n", label, got, want, d)) }
  else n_ok <<- n_ok + 1
}
rate1 <- function(G, s, R = RB) {
  set.seed(BOOTSEED); r <- rank_average_treatment_effect.fit(G, s, target = "AUTOC", R = R)
  c(as.numeric(r$estimate), as.numeric(r$std.err))
}
rate2 <- function(G, s1, s2, n1, n2) {
  pri <- data.frame(a = s1, b = s2); colnames(pri) <- c(n1, n2)
  set.seed(BOOTSEED); r <- rank_average_treatment_effect.fit(G, pri, target = "AUTOC", R = RB)
  nm <- names(r$estimate); if (is.null(nm)) nm <- r$TOC$priority[!duplicated(r$TOC$priority)]
  out <- list(); for (i in seq_along(nm)) out[[nm[i]]] <- c(as.numeric(r$estimate)[i], as.numeric(r$std.err)[i]); out
}
prio <- function(df, cfg, key, keyvals, col = "priority") {   # align on the positional row label
  d <- df[df$configuration == cfg, ]
  stopifnot(identical(as.integer(d[[key]]), as.integer(keyvals)))
  d[[col]]
}

# ---------------- Q1 and Q2 on the primary evaluation half (H2, n = 369) ----------------
cat("\n== Q1 primary: six configurations, estimate and SE ==\n")
dr  <- read.csv(D("rate_primary", "dr_scores_primary_heldout.csv")); G2 <- dr$dr_score
pri <- read.csv(D("rate_primary", "priorities_primary_heldout.csv"))
q1  <- fromJSON(RS("rate_primary", "rate_q1_primary.json"))$q1
for (cg in cfgs) { v <- rate1(G2, prio(pri, cg, "h2_row", dr$h2_row))
  chk(paste("Q1", cg, "estimate"), v[1], q1[[cg]]$estimate); chk(paste("Q1", cg, "SE"), v[2], q1[[cg]]$std_err) }

cat("== Q2 primary paired contrast ==\n")
q2 <- fromJSON(RS("rate_primary", "rate_q2_primary.json"))$primary$results
v  <- rate2(G2, prio(pri, "Clin + Rad + BiomedCLIP", "h2_row", dr$h2_row), prio(pri, "Clinical only", "h2_row", dr$h2_row),
            "reference", "clinical_only")
for (nm in names(q2)) { chk(paste("Q2", nm, "estimate"), v[[nm]][1], q2[[nm]]$estimate); chk(paste("Q2", nm, "SE"), v[[nm]][2], q2[[nm]]$std_err) }

cat("== Q2 sensitivities on the primary evaluation half ==\n")
sens <- fromJSON(RS("rate_primary", "rate_q2_sensitivities.json"))$sensitivities
S <- list(mammaprint   = list(file = "priorities_sens_mammaprint.csv", a = "Historical reference + MammaPrint", b = "Clinical + MammaPrint", la = "reference_plus_MP", lb = "clinical_plus_MP"),
          no_epoch     = list(file = "priorities_sens_no_epoch.csv",   a = "Clin + Rad + BiomedCLIP", b = "Clinical only", la = "reference", lb = "clinical_only"),
          alt_nuisance = list(file = "priorities_sens_alt_nuisance.csv", a = "Clin + Rad + BiomedCLIP", b = "Clinical only", la = "reference", lb = "clinical_only"))
for (k in names(S)) { p <- read.csv(D("rate_primary", S[[k]]$file))
  v <- rate2(G2, prio(p, S[[k]]$a, "h2_row", dr$h2_row), prio(p, S[[k]]$b, "h2_row", dr$h2_row), S[[k]]$la, S[[k]]$lb)
  for (nm in names(sens[[k]]$results)) { chk(paste("Q2", k, nm, "estimate"), v[[nm]][1], sens[[k]]$results[[nm]]$estimate)
                                         chk(paste("Q2", k, nm, "SE"), v[[nm]][2], sens[[k]]$results[[nm]]$std_err) } }
cat("  empty_arm_728: not recomputable from the released files (own evaluation forest); covered by the full pipeline\n")

# ---------------- Q3: both halves ----------------
cat("== Q3: A and C in both halves, held-out SEs of A, pooled optimism ==\n")
drH1 <- read.csv(D("rate_q3", "dr_scores_H1.csv")); G1 <- drH1$dr_score
p1 <- read.csv(D("rate_q3", "priorities_q3_H1.csv")); p2 <- read.csv(D("rate_q3", "priorities_q3_H2.csv"))
q3 <- fromJSON(RS("rate_q3", "rate_q3.json"))
for (cg in cfgs) { r <- q3$results[[cg]]
  aH1 <- rate1(G1, prio(p1, cg, "h1_row", drH1$h1_row, "priority_A")); cH1 <- rate1(G1, prio(p1, cg, "h1_row", drH1$h1_row, "priority_C"), R = 2)
  aH2 <- rate1(G2, prio(p2, cg, "h2_row", dr$h2_row,   "priority_A")); cH2 <- rate1(G2, prio(p2, cg, "h2_row", dr$h2_row,   "priority_C"), R = 2)
  chk(paste("Q3", cg, "A_H1"), aH1[1], r$A_H1); chk(paste("Q3", cg, "A_H1 SE"), aH1[2], r$A_H1_se_heldout); chk(paste("Q3", cg, "C_H1"), cH1[1], r$C_H1)
  chk(paste("Q3", cg, "A_H2"), aH2[1], r$A_H2); chk(paste("Q3", cg, "A_H2 SE"), aH2[2], r$A_H2_se_heldout); chk(paste("Q3", cg, "C_H2"), cH2[1], r$C_H2)
  chk(paste("Q3", cg, "pooled optimism"), (q3$n_H1 * (cH1[1] - aH1[1]) + q3$n_H2 * (cH2[1] - aH2[1])) / (q3$n_H1 + q3$n_H2), r$pooled_optimism) }

# ---------------- Q4: 48 regime values ----------------
cat("== Q4: regimes A / D1 / D2 / B in both halves, estimate and reference SE ==\n")
p4  <- list(H1 = read.csv(D("rate_q4", "priorities_q4_H1.csv")), H2 = read.csv(D("rate_q4", "priorities_q4_H2.csv")))
G   <- list(H1 = G1, H2 = G2); key <- list(H1 = "h1_row", H2 = "h2_row"); keyvals <- list(H1 = drH1$h1_row, H2 = dr$h2_row)
q4  <- fromJSON(RS("rate_q4", "rate_q4_regimes.json"))$results
for (h in c("H1", "H2")) for (cg in cfgs) for (rg in c("A", "D1", "D2", "B")) {
  v <- rate1(G[[h]], prio(p4[[h]], cg, key[[h]], keyvals[[h]], paste0("priority_", rg)))
  chk(paste("Q4", h, cg, rg, "estimate"), v[1], q4[[cg]]$by_half[[h]][[rg]])
  chk(paste("Q4", h, cg, rg, "SE"), v[2], q4[[cg]]$by_half[[h]][[paste0("se_", rg)]]) }

cat(sprintf("\n%d comparisons: %d agree within %.0e, %d differ; largest |difference| %.2e\n", n_ok + n_fail, n_ok, TOL, n_fail, worst))
cat(if (n_fail == 0) "VERIFICATION PASS\n" else "VERIFICATION FAIL\n")
quit(status = if (n_fail == 0) 0 else 1)
