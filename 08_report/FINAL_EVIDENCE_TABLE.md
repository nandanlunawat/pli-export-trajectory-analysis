# Final Evidence Table — Complete Project

**Date:** 3 September 2026
**Status:** All statistical/econometric modelling is **permanently frozen** as of this date. Every number below is transcribed from the stored results files (`06_results/*.csv`); nothing was re-estimated. This document is the numerical evidence base underlying `FINAL_REPORT.md`.

Sources: `ITS_robustness_matrix.csv`, `ITS_prelim_growth_companion.csv`, `ITS_R12_quadratic_pretrend.csv`, `ITS_structural_breaks.csv`, `volatility_results.csv`, `forecast_validation.csv`, `forecast_counterfactual.csv`.

Notation: β₃ in lgp/month = log-growth points per month (100·coefficient); "p" is HAC(12) unless labelled; ARMA p-values are ML z-based (flagged `se_type` in the matrix); Δσ in lgp from the locked primary volatility variant (symmetric ±24-month windows, break-straddling observation excluded).

---

## 1. Evidence table

| Item | B1 Mobile (8517.1x proxy) | B2 Pharma (3003+3004) | B3 Air conditioners (8415) | B4 Textiles (MMF, 14 codes) |
|---|---|---|---|---|
| Intervention date D_s | 2020-08 | 2022-04 | 2022-04 | 2024-04 |
| Pre / post observations | **28** / 68 | 48 / 48 | 48 / 48 | 72 / **24** |
| Baseline ITS β₃ (lgp/mo), p | −2.92, p = 0.148 | −0.13, p = 0.379 | **+0.87, p = 0.0013** | +0.05, p = 0.829 |
| ARMA-errors β₃, p | AIC-best ARMA(1,1): −1.55, p = 0.387 | AR(1): −0.15, p = 0.551 | AIC-best AR(2): +0.85, p = 0.029; **fixed AR(1): +0.88, p = 0.152** | AIC-best AR(1)×SAR(1): −0.34, p = 0.769 (lowest-AIC MA(1) did **not converge** — disclosed) |
| Stationary-growth companion α₁, p | −4.15, p = 0.505 | +0.53, p = 0.590 | **+0.66, p = 0.610** | −1.27, p = 0.467 |
| R12 quadratic pre-trend | β₃ flips to +1.27, p = 0.430; T² = −4.20, p < 0.0001 | β₃ flips to +1.32, p = 0.0002; T² = −1.52, p < 0.0001 | **β₃ flips to −1.13, p = 0.215; T² = +2.09, p = 0.026; partial corr(T², TimeAfter) = 0.970** | β₃ −0.90, p = 0.303; T² p = 0.230 (n.s.) |
| Alternative-date robustness | Mixed: notification 2020-04 −4.42 (p = 0.003) and −3m (p = 0.029) significant negative; locked date and later dates n.s. → no stable dated pattern | Notification 2021-03 −0.55 (p < 0.0001); locked date and all later dates n.s. → baseline null stands | **Positive and significant at the locked date (p = 0.0013) and at all five alternative dates spanning 2021-04 to 2023-04 (all p ≤ 0.0007) → date-invariance is evidence against a dated break, consistent with smooth curvature** | Notification 2021-09 +0.60 (p = 0.032) nominal; locked date and ±3m n.s. → null stands |
| Structural-break diagnostic + limitations | supF argmax 2020-10 (near D_s); Bai–Perron 2018-09 \| 2025-07 (not near D_s) | supF argmax 2021-02; B-P 2019-02 \| 2025-07 — neither at D_s | supF argmax 2021-07; B-P 2018-09 \| 2024-09 — **neither at D_s 2022-04** | supF argmax 2020-10; B-P 2020-12 \| 2021-10 — pre-scheme, not at D_s |
| — break limitations (all baskets) | *Diagnostic only, per the locked downgrade: unknown-date tests on trending seasonal series with many regressors; trim/candidate-set sensitivity; a detected (or absent) break neither proves nor disproves a policy link.* | | | |
| Volatility Δσ (±24m, excl. straddle) | −24.0 lgp (−39.4%) | −0.5 lgp (−4.2%) | **−52.7 lgp (−69.3%)** | +3.2 lgp (+23.6%) |
| — COVID-excluded Δσ | **+1.1 lgp (+2.9%) — decline vanishes** | −0.5 lgp (−4.6%) | **+6.2 lgp (+36.2%) — sign flips** | +3.2 lgp (+23.6%) — unchanged (COVID outside windows) |
| — MBB 95% CI excludes zero? | No (any variant) | No | No | No |
| Final forecasting model | Seasonal naïve — **LOCKED benchmark, not model-selected** | Seasonal naïve — only coverage-eligible candidate (ets 0.483 ✗, ets_damped 0.779 ✗, **sarima 0.839 ✗**) and lowest RMSE | Seasonal naïve — via pre-specified simplicity clause (SARIMA RMSE win indistinguishable: paired t = 0.45) | Seasonal naïve — via simplicity clause (ETS-damped indistinguishable: paired t = 0.03) |
| Validation origins (h = 12) | n/a (not validated) | **7** | **7** | 31 |
| h = 12 gap (actual − pre-policy counterfactual) | +23.2% (no claim made) | +2.6% | +23.2% (**pre-stated restatement of R12 curvature**) | −2.2% (h = 18: −1.9%) |
| Any actual outside 95% forecast interval? | No (0/12) | No (0/12) | No (0/12) | No (0/18) |
| **Final verdict** | **No robust evidence of a trajectory change.** Baseline n.s.; attenuates further under ARMA errors; growth companion null; COVID-drop variant significant (−5.60, p < 0.001) but sign-consistent with an n.s. baseline, not a finding under the interpretation rule. Volatility decline is COVID-composition, not policy-period stabilisation. 28-month pre-period limits everything. | **Robust null.** No specification, date, volatility measure or forecast gap departs from the pre-policy pattern. | **Non-robust levels significance; the totality of evidence indicates smooth trend acceleration beginning around late 2021 — not a dated trajectory break at D_s.** Fails growth companion and fixed AR(1); flat across six dates over two years; R12 absorbs it into curvature with near-perfect collinearity (0.970); break diagnostics do not locate 2022-04; the −52.7 lgp volatility decline reverses to +6.2 when COVID is excluded; the +23.2% forecast gap restates the curvature. | **Robust null, with limited post-period power** (24 post months, though the best-validated forecasting case, 31 origins). Small negative forecast gap consistent with the ITS null. |

**Cross-cutting facts.** Two of nine descriptive control regressions were nominally significant at the 5% level (C2 at 2020-08 p = 0.032; C3 at 2022-04 p = 0.037; C1 at 2020-08 p = 0.062 marginal), illustrating that individual nominal p-values should be interpreted cautiously in this design. B1's Transition_t control moves β₃ by 0.65% (−2.92 → −2.90) — the 2022 HS reclassification does not drive the B1 estimate.

**Standing conclusion (unchanged since Phase 6): no basket shows a trajectory change that survives the pre-specified robustness framework.**

---

## 2. What can I say / What can I NOT say

| Topic | CAN say | CANNOT say |
|---|---|---|
| **Trajectory changes** | "I evaluated changes in export trajectories around PLI implementation with a segmented ITS on monthly GoI data. Under the pre-specified robustness framework — ARMA errors, a stationary growth companion, alternative dates, COVID windows, quadratic pre-trend — **no basket shows a robust dated trajectory change.** The null is an informative finding: the pre-specified framework did not identify a trajectory change that remained robust across alternative error structures, differenced-space inference, alternative dates and curvature specifications." | "PLI changed (or failed to change) export trajectories." Any claim that the analysis *established* a trajectory effect in either direction; any claim resting on a single specification. |
| **B3 (the key case)** | "B3 shows the strongest apparent post-policy pattern: baseline β₃ = +0.87 lgp/mo (p = 0.0013) and the largest volatility decline. But it fails the growth companion (p = 0.61) and fixed AR(1) (p = 0.15), is significant at *every* one of six candidate dates spanning two years, and a quadratic pre-trend absorbs it (β₃ → −1.13, n.s.) with partial correlation 0.970 between T² and TimeAfter. The evidence indicates **smooth acceleration from around late 2021, not a break at the scheme date** — and with a partial correlation of 0.97 between the competing terms, the data have very limited ability to distinguish the two." | "AC exports accelerated *because of* PLI." "B3 is the sector where PLI worked." "The ITS detected a significant trajectory change in B3" (without immediately stating it is non-robust). |
| **B1** | "B1 is an HS-based telephone-set export **proxy** aligned to the mobile-phone PLI scope, with only **28 pre-policy months ending inside the COVID disruption** — every B1 estimate is reported under that caveat, its forecast is a non-selected benchmark, and no substantive claim is made." | Any substantive B1 finding — positive, negative, or null-as-evidence. "B1's exports fell/stabilised after PLI." Treating the +23.2% B1 forecast gap as information. |
| **Volatility** | "Using the SD of monthly log growth in ±24-month windows, B3 (−52.7 lgp) and B1 (−24.0) show the largest declines, B4 (+3.2) and B2 (−0.5) little change — this ranking answers the CV bullet **descriptively**. But no moving-block-bootstrap CI excludes zero, and excluding COVID months **flips B3 to +6.2 and B1 to +1.1**: the large declines are COVID-window composition, not demonstrable post-policy stabilisation." | "PLI reduced export volatility." "The volatility decline is statistically significant." Reporting the ranking without the COVID-exclusion reversal. Annualised figures (unless explicitly labelled). |
| **Forecasting** | "An exploratory pre-policy counterfactual: seasonal naïve was selected for all four baskets by three routes — locked for B1; sole coverage-eligible model for B2 (SARIMA failed at 0.839); pre-specified simplicity clause for B3/B4 (paired t = 0.45, 0.03). Every post-policy actual lies inside the 95% interval at every horizon. B2/B3 rest on only 7 validation origins; B4 (31 origins) is the only well-validated case. The tie-break *clause* was pre-specified; its *t < 1 operationalisation* was fixed after seeing raw RMSEs — direction-safe, and both raw-winner counterfactuals are retained." | "The forecast counterfactual measures the PLI effect." "Actuals significantly exceeded/undershot forecasts." Any gap described as an effect, impact, or estimate. Presenting B2/B3 model selection as well-identified. Omitting the tie-break timing disclosure. |
| **Causal interpretation** | "The design is observational — a single-series ITS with descriptive controls. It characterises **associations around implementation dates** and rules out interpretations the data cannot support. Confounders (global demand, China+1 reorientation, prices, the rupee, COVID) are inseparable from any policy contribution." | "PLI caused / did not cause anything." "Effect", "impact", "treatment effect" for any estimate. That controls provide difference-in-differences identification (a stacked DiD was considered and **not run**, by design). |
| **Sector ranking** | "On the pre-specified descriptive measures, B3 shows the strongest post-policy trend *and* volatility change, B1 second on volatility, B2 and B4 essentially unchanged — with the immediate qualification that B3's pattern is smooth curvature rather than a dated break and both large volatility declines are COVID-driven." | An unqualified league table of "PLI winners". Any ranking presented as effect sizes rather than descriptive magnitudes. Ranking B1 substantively at all. |

---

## 3. Caveat register (all preserved — none may be dropped in the final report)

1. **No causal identification** anywhere in the project; gaps are "actual minus pre-policy time-series counterfactual".
2. **B1: 28-month pre-period** ending inside COVID; proxy basket; benchmark-only forecast; no substantive claims.
3. **B2/B3: 7 forecast-validation origins** at h = 12 — selection weakly identified, counterfactuals exploratory.
4. **B3 curvature / collinearity**: partial corr(T², TimeAfter) = 0.970 — data cannot separate smooth acceleration from a dated break.
5. **COVID drives the volatility comparison**: B3 −52.7 → +6.2, B1 −24.0 → +1.1 under COVID exclusion; no MBB CI excludes zero.
6. **Control nominal significance**: two of nine descriptive control regressions nominally significant at 5% — individual nominal p-values should be interpreted cautiously in this design (not described as an estimated Type I error rate or proof of over-rejection).
7. **Structural-break diagnostics are diagnostics only** (downgraded per audit): unknown-date tests on trending seasonal series; trim/candidate sensitivity; corroborative at most.
8. **Forecasting tie-break operationalisation** (t < 1) fixed after seeing raw RMSEs; clause itself pre-specified; direction-safe; B3 threshold-sensitive below t < 0.4 with immaterial consequence (+21.4% vs +23.2%); raw winners retained.
9. **B2 SARIMA coverage failure at 0.839** — below the hard [0.85, 1.00] eligibility bound; must carry the ✗ in the final report's validation table (audit correction C1), alongside the other C-items: precise "three routes" selection wording, B1 figure-caption label, coverage-persistence housekeeping note.
10. ARMA p-values are ML z-based, not HAC; B4's lowest-AIC MA(1) non-convergence disclosed; n_eff-style arguments are heuristics, not effective sample sizes.

---

*This table is the numerical source of truth for `FINAL_REPORT.md`.*
