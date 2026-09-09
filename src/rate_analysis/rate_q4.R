#!/usr/bin/env Rscript
# R7-Q4 - standard RATE/AUTOC point estimates for regimes A/D1/D2/B in both split directions.
# Additive point-estimate contrasts. NO variance ratios, no exponentiation, no confirmatory p-values.
suppressPackageStartupMessages({library(grf); library(jsonlite)})
RELEASE_ROOT <- Sys.getenv("JIIM_RELEASE_ROOT", unset = getwd())   # run from the repository root, or set JIIM_RELEASE_ROOT
R7 <- file.path(RELEASE_ROOT, "reproduction", "rate_primary"); Q3 <- file.path(RELEASE_ROOT, "reproduction", "rate_q3")   # outputs of the earlier stages
OUT <- file.path(RELEASE_ROOT, "reproduction", "rate_q4"); dir.create(OUT, recursive = TRUE, showWarnings = FALSE)
BOOTSEED <- 20260906; RB <- 2000
cfgs <- c("Clinical only","Clin + Radiomics","Clin + BiomedCLIP","Clin + RAD-DINO",
          "Clin + Rad + BiomedCLIP","Clin + Rad + RAD-DINO")
rgs <- c("A","D1","D2","B")
rate <- function(G, s) { set.seed(BOOTSEED)
  r <- rank_average_treatment_effect.fit(G, s, target = "AUTOC", R = RB)
  c(as.numeric(r$estimate), as.numeric(r$std.err)) }

drH2 <- read.csv(file.path(R7, "dr_scores_primary_heldout.csv"))   # frozen R7
drH1 <- read.csv(file.path(Q3, "dr_scores_H1.csv"))              # frozen Q3
p2 <- read.csv(file.path(OUT, "priorities_q4_H2.csv"))
p1 <- read.csv(file.path(OUT, "priorities_q4_H1.csv"))
stopifnot(identical(as.character(drH2$patient_id), as.character(p2$patient_id[p2$configuration == cfgs[1]])),
          identical(as.character(drH1$patient_id), as.character(p1$patient_id[p1$configuration == cfgs[1]])))
G <- list(H1 = drH1$dr_score, H2 = drH2$dr_score); P <- list(H1 = p1, H2 = p2)
nH <- c(H1 = nrow(drH1), H2 = nrow(drH2))

fz_q1 <- fromJSON(file.path(R7, "rate_q1_primary.json"))$q1
fz_q3 <- fromJSON(file.path(Q3, "rate_q3.json"))
est <- se <- array(NA_real_, c(length(cfgs), 4, 2), dimnames = list(cfgs, rgs, c("H1","H2")))
chk <- c(A_H2 = 0, A_H1 = 0)
for (h in c("H1","H2")) for (cg in cfgs) {
  d <- P[[h]][P[[h]]$configuration == cg, ]
  for (rg in rgs) { v <- rate(G[[h]], d[[paste0("priority_", rg)]]); est[cg, rg, h] <- v[1]; se[cg, rg, h] <- v[2] }
}
for (cg in cfgs) {
  chk["A_H2"] <- max(chk["A_H2"], abs(est[cg,"A","H2"] - fz_q1[[cg]]$estimate))
  chk["A_H1"] <- max(chk["A_H1"], abs(est[cg,"A","H1"] - fz_q3$results[[cg]]$A_H1))
}
cat(sprintf("run checks: max|A_H2 - frozen R7 Q1| = %.2e   max|A_H1 - frozen Q3 A_H1| = %.2e\n", chk[1], chk[2]))

res <- list()
for (cg in cfgs) {
  has_img <- cg != "Clinical only"
  e <- function(rg, h) est[cg, rg, h]
  half <- list()
  for (h in c("H1","H2")) {
    P_e  <- 0.5 * ((e("D1",h) - e("A",h)) + (e("B",h) - e("D2",h)))
    S_e  <- 0.5 * ((e("D2",h) - e("A",h)) + (e("B",h) - e("D1",h)))
    PS_e <- (e("B",h) - e("D2",h)) - (e("D1",h) - e("A",h))
    half[[h]] <- list(A = e("A",h), D1 = e("D1",h), D2 = e("D2",h), B = e("B",h),
                      se_A = se[cg,"A",h], se_D1 = se[cg,"D1",h], se_D2 = se[cg,"D2",h], se_B = se[cg,"B",h],
                      P_effect = if (has_img) P_e else "N/A (factor P structurally absent)",
                      S_effect = S_e,
                      PS = if (has_img) PS_e else "N/A (factor P structurally absent)",
                      Total_B_minus_A = e("B",h) - e("A",h))
  }
  pool <- function(k) (nH["H1"] * half$H1[[k]] + nH["H2"] * half$H2[[k]]) / 739
  res[[cg]] <- list(has_imaging_block = has_img, by_half = half,
    pooled_P  = if (has_img) unname(pool("P_effect")) else "N/A (factor P structurally absent)",
    pooled_S  = unname(pool("S_effect")),
    pooled_PS = if (has_img) unname(pool("PS")) else "N/A (factor P structurally absent)",
    pooled_B_minus_A = unname(pool("Total_B_minus_A")),
    q3_pooled_C_minus_A = fz_q3$results[[cg]]$pooled_optimism)
  res[[cg]]$preprocessing_fraction_of_Q3 <-
    abs(res[[cg]]$pooled_B_minus_A) / abs(res[[cg]]$q3_pooled_C_minus_A)
  cat(sprintf("  %-26s pooled P %-9s S %+.4f  PxS %-9s  B-A %+.4f | Q3 C-A %+.4f  |Q4/Q3| %.3f\n", cg,
     if (has_img) sprintf("%+.4f", res[[cg]]$pooled_P) else "N/A",
     res[[cg]]$pooled_S,
     if (has_img) sprintf("%+.4f", res[[cg]]$pooled_PS) else "N/A",
     res[[cg]]$pooled_B_minus_A, res[[cg]]$q3_pooled_C_minus_A,
     res[[cg]]$preprocessing_fraction_of_Q3))
}
write_json(list(design = list(
    question = "change in the observed standard RATE/AUTOC POINT ESTIMATE when evaluation-patient covariates enter unsupervised preprocessing only, with the causal forest always fitted on the opposite half",
    kind = "descriptive preprocessing-leakage diagnostic; NOT a test; NO confirmatory p-values; NOT the retired permutation null-variance analysis",
    regimes = "A=(img train, clin train) D1=(img FULL739, clin train) D2=(img train, clin FULL739) B=(img FULL739, clin FULL739)",
    split = "frozen R7 50/50 split reused verbatim; H1 n=370, H2 n=369",
    dr_H2 = "FROZEN_R7/dr_scores_primary_heldout.csv reused byte-for-byte",
    dr_H1 = "FROZEN_R7Q3/dr_scores_H1.csv reused byte-for-byte",
    contrasts = "additive RATE point-estimate contrasts; pooled = (370*H1 + 369*H2)/739; never exponentiated, never ratios",
    se_note = "grf half-sample bootstrap SEs stored for REFERENCE ONLY and not used to claim any A-vs-D1/D2/B difference is supported",
    grf_version = as.character(packageVersion("grf"))),
  run_checks = list(max_abs_A_H2_vs_frozen_R7_Q1 = unname(chk[1]),
                    max_abs_A_H1_vs_frozen_Q3 = unname(chk[2]),
                    passed = all(chk < 1e-9)),
  n_H1 = unname(nH["H1"]), n_H2 = unname(nH["H2"]), results = res),
  file.path(OUT, "rate_q4_regimes.json"), auto_unbox = TRUE, digits = 12, pretty = TRUE)
cat("wrote rate_q4_regimes.json\n")
