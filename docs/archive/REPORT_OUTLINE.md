# Final Report — Detailed Outline (for review before prose drafting)

**Date:** 3 September 2026
**Numerical source of truth:** `08_report/FINAL_EVIDENCE_TABLE.md` (as corrected). No new empirical results anywhere.
**Central conclusion, verbatim, to appear in the abstract, §7 and §12:**
> "Across four PLI-linked product groups, the analysis finds no robust evidence of a trajectory change specifically timed to PLI implementation over the study period; the results therefore do not establish either a positive or negative causal effect of the schemes on sector-level exports."

Working title: *"PLI Scheme: Export Competitiveness and Export Trajectory Analysis — An Interrupted Time-Series Study of PLI-Linked Sector Exports, 2018–2026."* (title amended per approval, 3 Sep 2026)

Front matter: title page; one-paragraph abstract (research question → data → method → central conclusion verbatim → one sentence on descriptive rankings with the smooth-curvature and COVID qualifications).

---

## §1. Research question and economic motivation

**Purpose.** State the observational research question ("How did the export trajectories and volatility of selected PLI-linked sectors evolve around the implementation of the relevant PLI schemes?"), motivate why PLI matters (scale of the programme, export-competitiveness objective), and pre-commit the reader to the association-not-causation frame in the first page.

**Figures/tables.** Figure 1: `eda_00_overview_log_all_baskets.png` (all four log series with D_s markers) — orients the reader before any method.

**Exact results.** None. No numbers beyond series descriptions.

**Limitations stated here.** One sentence: the design is observational; "post-implementation change" and "association around implementation" are the strongest claims the report will make. (Full treatment deferred to §11.)

**Appendix routing.** None.

---

## §2. PLI institutional context and intervention-date logic

**Purpose.** Describe the four schemes (LSEM mobile, Pharmaceuticals, White Goods ACs, Textiles MMF), and justify each locked D_s as the scheme's operationally relevant start — with the 5-way date taxonomy (notification / effective / elected-year / gestation / sensitivity) explaining why notification dates were *not* used as primary.

**Figures/tables.** Table 1: scheme → basket → D_s → date rationale → primary source (condensed from `02_policy_sources/pli_intervention_dates.csv`).

**Exact results.** D_s values only: B1 2020-08, B2 2022-04, B3 2022-04, B4 2024-04. The alternative dates listed here (they become the §8 robustness set) — flagged as pre-specified in the registry before estimation.

**Limitations stated here.** The LSEM Round-1 opening date is not stated in the gazette (documented gap); date choice for multi-round schemes involves judgement, which is why §8 re-estimates at every registry date.

**Appendix routing.** Full intervention-date registry (all columns, all sensitivity dates, sources) → Appendix A. The source log reference (S01–S42) → Appendix A.

---

## §3. Data, HS-code construction, and classification-continuity work

**Purpose.** Document the data (DGCI&S MEIDB monthly HS-6 exports, US$ mn, Apr 2018–Mar 2026, retrieval 2026-08-29), basket construction, and the classification-continuity investigation — the project's main data-engineering contribution.

**Figures/tables.** Table 2: basket definitions (basket → HS codes → n codes → PLI scheme → mapping confidence). Table 3: the B1 two-stage HS transition evidence (Dec-21/Jan-22/Apr-22 values for 851712/851718/851713/851770) — the empirical detection that motivated the five-code union.

**Exact results.** 96 months × 7 baskets = 672 rows; B1 = five-code union 851711–14+851718; B2 = 3003+3004; B3 = 8415; B4 = 14 Annexure-II codes; C1 = Ch 42 (20 codes), C2 = Ch 64 (25), C3 = 5208–5212 (70). The two HS transitions (Customs Tariff HS2022 Jan-2022; DGCI&S directory Apr-2022); MEIDB does not re-map history. Reconciliation: parser spot-check within 0.002% of MEIDB's own totals; 15/15 validation assertions passed.

**Writing rule enforced here.** B1 is introduced as an **HS-based telephone-set export proxy aligned to the mobile-phone PLI scope** — never as "PLI-covered output". This label then travels with B1 through every later section.

**Limitations stated here.** Basket-to-scheme mapping is approximate (HS codes ≠ scheme beneficiary output); the CBIC correlation Annexure verification gap for B4 letter codes (NOT VERIFIED items); provisional/revised data vintage all (R).

**Appendix routing.** Full HS-6 code lists for C1–C3 and B4 → Appendix B. Extraction mechanics (`fetch_meidb.py`, 48-request plan, raw-cache policy) → Appendix B. Full `DATASET_VALIDATION_REPORT.md` content → cite, don't reproduce.

---

## §4. Why monthly time-series data are appropriate

**Purpose.** Short section (half page) answering the interview question directly: monthly frequency gives 96 observations vs 8 annual ones, resolves within-year seasonality, allows the intervention to be placed at the correct month, and supports autocorrelation-aware inference. Also justify the 2018–2026 window (MEIDB starts Jan 2018; backward extension investigated and infeasible — EIDB annual, FTPA cumulative).

**Figures/tables.** None.

**Exact results.** Pre/post splits: B1 28/68, B2 48/48, B3 48/48, B4 72/24.

**Limitations stated here.** **B1's 28-month pre-period is a hard data-availability constraint — the MEIDB monthly series begins January 2018 and the scheme date is August 2020 — not a chosen truncation.** State this here, at first mention of the 28 months. B4's 24-month post-period likewise flagged.

**Appendix routing.** The backward-extension feasibility investigation → Appendix C (summarised in one sentence in main text).

---

## §5. Research design and primary ITS specification

**Purpose.** Present the locked segmented ITS: ln(Y_t) = β₀ + β₁T + β₂Post + β₃TimeAfter + month FE + Covid + ε; define every variable (TimeAfter = max(0, T−T_Ds); April reference month; COVID dummy Apr–Jun 2020; B1 Transition_t Jan–Apr 2022); interpret β₁/β₂/β₃; state HAC(3, 12) inference; state that the design, dates, and robustness set were locked before estimation; explain the role of controls C1–C3 as **descriptive comparators only — explicitly not a difference-in-differences design and providing no causal identification** (a stacked DiD was considered and deliberately not run).

**Figures/tables.** Design-summary box (specification + coefficient interpretation). No results.

**Exact results.** None (specification only).

**Limitations stated here.** Single-series design; β₃ is "change in post-intervention trajectory", an association parameter; the interpretation rule (non-robust ≠ finding) quoted verbatim as a design commitment.

**Appendix routing.** The full locked research-design memo → cited, not reproduced.

---

## §6. Exploratory analysis: seasonality, trend, autocorrelation, stationarity

**Purpose.** Establish the series properties that justify the specification choices: month fixed effects (seasonality), log transform, HAC/ARMA-aware inference (autocorrelation), and the growth companion (stationarity evidence).

**Figures/tables.** Figure 2: 2×2 panel from `eda_01_*` (levels/log/growth per basket; or one representative + rest to appendix). Figure 3: `eda_03_B3_AC_stl.png` (B3 STL — the visually smooth acceleration the reader must see before §7). Table 4: compact EDA summary (seasonal strength F_s, trend strength F_t, ADF/KPSS conclusions phrased as "evidence consistent with").

**Exact results.** From `EDA_summary.csv`: seasonal/trend strengths; unit-root conclusions in the locked language; B3's low STL seasonal strength attributed to the large remainder (per the approved correction — not "no seasonality"). Growth in lgp notation throughout, defined at first use: g = 100·Δln(Y), log-growth points, not % growth.

**Limitations stated here.** COVID months visibly dominate 2020 growth for B1/B3 (foreshadows §9's exclusion variant).

**Appendix routing.** Remaining `eda_01/02/03/04` panels for baskets not shown → Appendix D. ACF/PACF plots → Appendix D (referenced from §8 diagnostics).

---

## §7. Main ITS findings

**Purpose.** Report the four baseline estimates and state the central conclusion. Structure: B2/B4 nulls first, B1 with its caveat, **then B3 last with its non-robustness explained in the same paragraph as its p-value** — the p = 0.0013 never stands alone.

**Figures/tables.** Figure 4: `its_01_*_fit.png` four-panel (fitted segments over actuals). Table 5: baseline coefficients — β₁, β₂ (p), β₃ in lgp/mo with HAC(12) p and CI, per basket.

**Exact results (from the frozen table).** β₃: B1 −2.92 lgp/mo (p = 0.148); B2 −0.13 (p = 0.379); B3 +0.87 (p = 0.0013); B4 +0.05 (p = 0.829). B1's Transition_t control moves β₃ by 0.65% — the HS reclassification does not drive B1. **B3's baseline significance is immediately followed (same paragraph) by the three-sentence preview of §8:** fails the stationary growth companion (p = 0.61) and fixed AR(1) (p = 0.152), significant at all six candidate dates spanning two years, absorbed by a quadratic pre-trend — full evidence in §8. Then the central conclusion verbatim.

**Limitations stated here.** B1's estimate carries the 28-month/COVID-tail caveat inline (cross-reference §4). No causal language anywhere; "trajectory change" and "post-implementation" wording only.

**Appendix routing.** Full regression output (all coefficients incl. month FE, both HAC lags, OLS SEs) → Appendix E. Residual plots `its_02_*` → Appendix E.

---

## §8. Robustness and model diagnostics

**Purpose.** The evidentiary core: show that the pre-specified robustness framework overturns B3 and confirms the other verdicts. Sub-structure: (a) ARMA-errors; (b) stationary growth companion; (c) COVID-window drop; (d) alternative intervention dates; (e) R12 quadratic pre-trend; (f) structural-break diagnostics; (g) descriptive controls; (h) residual diagnostics.

**Figures/tables.** Figure 5: `rob_01_B3_AC_beta3_forest.png` (B3 forest plot — the single most persuasive figure; other baskets' forests → appendix). Table 6: condensed robustness matrix (β₃ + p across specifications × baskets). Table 7: R12 results (β₃ before/after, T² coefficient, the 0.970 partial correlation).

**Exact results.**
- ARMA: B1 −1.55 (p = 0.387); B2 −0.15 (p = 0.551); B3 AIC-best AR(2) +0.85 (p = 0.029) vs fixed AR(1) +0.88 (p = 0.152); B4 −0.34 (p = 0.769) with the **MA(1) non-convergence disclosure**. ARMA p-values labelled ML z-based.
- Growth companion: α₁ n.s. for all four (B3 p = 0.61) — synthetic-data-verified that α₁ recovers β₃.
- COVID-drop: B3 +0.90 (p = 0.0008) stable; B1 turns −5.60 (p < 0.001) — reported, not promoted to a finding under the interpretation rule.
- Alternative dates — **labelled "alternative-date robustness exercise", never "formal placebo test"**: B3 significant positive at all six dates spanning 2021-04 to 2023-04 (all p ≤ 0.0007) → date-invariance is evidence *against* a break specifically timed to D_s; B1 mixed (early dates negative-significant, locked and later n.s.); B2/B4 nulls stand (isolated notification-date nominal hits noted).
- R12: B3 flips to −1.13 (p = 0.215), T² +2.09 (p = 0.026), partial corr 0.970 — approved wording: "Within this sample and specification, the dated trajectory-change parameter is highly collinear with smooth curvature, limiting the ability to distinguish the two"; B1/B2 also flip sign under T² (reported to show R12's global behaviour, not only B3's).
- Breaks — **with the locked limitations paragraph**: diagnostic only; unknown-date tests on trending seasonal series; trim/candidate-set sensitivity; neither supF argmax nor Bai–Perron dates fall at D_s for B2/B3/B4; B1's supF argmax 2020-10 near D_s noted as corroborative-at-most.
- Controls — the approved sentence verbatim: "Two of nine descriptive control regressions were nominally significant at the 5% level, illustrating that individual nominal p-values should be interpreted cautiously in this design." No Type-I-rate or over-rejection claim.
- Diagnostics: Ljung-Box/BG results summarised; motivation for HAC + ARMA cross-checks.

**Limitations stated here.** Break-diagnostic limitations (above); ARMA se-type; the interpretation-rule application to B3 and to B1's COVID-drop result stated explicitly.

**Appendix routing.** Full 45-row robustness matrix → Appendix F. AIC scan table → Appendix F. Remaining forest plots → Appendix F. Diagnostics detail → Appendix E.

---

## §9. Volatility analysis

**Purpose.** Answer the CV volatility clause descriptively: define σ as SD of monthly log growth (lgp), ±24-month symmetric windows, break-straddling observation excluded; present the ranking; then **immediately** show the COVID-exclusion reversal and the MBB result so the ranking cannot be read as policy stabilisation.

**Figures/tables.** Figure 6: `eda_05_rolling_volatility_all.png` or `vol_01_rolling_sd_windows.png` (rolling 6-month SD with D_s markers). Table 8: σ_pre, σ_post, Δσ, %Δσ, COVID-excluded Δσ, MBB 95% CI, per basket.

**Exact results.** Baseline Δσ: B3 −52.7 lgp (−69.3%), B1 −24.0 (−39.4%), B4 +3.2 (+23.6%), B2 −0.5 (−4.2%). COVID-excluded: **B3 +6.2 (+36.2%), B1 +1.1 (+2.9%)**, B2 −0.5, B4 unchanged. No MBB CI excludes zero, any variant. Ranking language: "largest descriptive changes", explicitly not "stabilisation caused by PLI". No annualisation.

**Limitations stated here.** The COVID composition point is the section's own conclusion, not a footnote: the two large declines exist only because the pre-window contains Mar–Sep 2020. Bootstrap CIs wide; descriptive throughout.

**Appendix routing.** Full 32-row volatility grid (both window schemes, straddle variants) → Appendix G.

---

## §10. Exploratory historical counterfactual forecasting

**Purpose.** Present the pre-planned counterfactual component as a methodological demonstration, framed by its own scope statement: gaps are "actual minus pre-policy time-series counterfactual", never treatment effects; the exercise cannot revise the §7 conclusion.

**Figures/tables.** Figure 7: `fc_01_B4_TEXTILE_counterfactual.png` (the best-validated case leads) and `fc_01_B3_AC_counterfactual.png` (with the curvature pre-statement in the caption); B1/B2 panels → appendix. Table 9: validation table (RMSE/coverage per candidate per basket, **✗ on every coverage failure including B2 SARIMA at 0.839**). Table 10: h = 12 (and h = 18 for B4) gaps with interval-exceedance counts.

**Exact results.** Selection by three routes (verbatim audit wording): B1 locked benchmark not model-selected; B2 sole coverage-eligible candidate (ets 0.483 ✗, ets_damped 0.779 ✗, sarima 0.839 ✗) and lowest RMSE; B3/B4 by the pre-specified simplicity clause (paired t = 0.45, 0.03). **Tie-break timing disclosure verbatim:** clause pre-specified in the memo; the t < 1 operationalisation fixed after seeing raw RMSEs; direction-safe; B3 threshold-sensitive below t < 0.4 with immaterial consequence (+21.4% vs +23.2%); raw winners retained in the results file. Origins: 7/7/31 (B2/B3/B4) — B2/B3 selection weakly identified. Gaps: B1 +23.2% (no claim), B2 +2.6%, B3 +23.2% (pre-stated restatement of the R12 curvature), B4 −2.2% (h18 −1.9%). Every actual inside the 95% interval, all baskets, all horizons.

**Limitations stated here.** All six from the forecasting memo, condensed: weak B2/B3 selection; B1 excluded from inference; wide naïve intervals make "inside the PI" a weak test; the counterfactual inherits every confounder; B3's gap mechanically entangled with the curvature; no significance tests on gaps.

**Appendix routing.** Full validation grid (all models × horizons) → Appendix H. B1/B2 counterfactual figures → Appendix H.

---

## §11. Limitations and identification boundaries

**Purpose.** Consolidate every caveat in one place (each already stated at point of use; this section is the register). Order: (1) no causal identification — single-series ITS, no counterfactual sector delivering identification; controls descriptive only; (2) confounders (global demand, China+1, prices, exchange rate, COVID) inseparable from any policy contribution; (3) B1 proxy status + 28-month data-constrained pre-period; (4) B3's 0.970 curvature/collinearity boundary — the data *cannot* distinguish smooth acceleration from a dated break; (5) COVID's dominance of the volatility comparison; (6) B4's 24-month post-window; (7) mapping approximation (HS ≠ beneficiary output) and the B4 verification gap; (8) nominal-p caution (approved sentence, cross-referenced); (9) break-diagnostic limitations; (10) forecasting disclosures (origins, tie-break timing, coverage failure). Closes with the identification boundary: what design *would* identify a causal effect (firm-level beneficiary data, credible comparison units) and why it was out of scope.

**Figures/tables.** None.

**Exact results.** None new — cross-references only.

**Appendix routing.** None.

---

## §12. Conclusion

**Purpose.** One page. Restate the research question; the central conclusion **verbatim**; then the three defensible positives: (a) the descriptive ranking — "B3 shows the largest estimated trajectory and volatility changes among the four baskets under the descriptive measures, but neither change is attributable to PLI: the trajectory acceleration is smooth rather than dated, and the volatility decline reverses when COVID months are excluded" (approved wording); (b) the methodological contribution (HS-continuity resolution, locked pre-specified robustness framework, disciplined null); (c) "The null is an informative finding: the pre-specified framework did not identify a trajectory change that remained robust across alternative error structures, differenced-space inference, alternative dates and curvature specifications" (approved wording). End on what the evidence *is* consistent with (B3's acceleration from late 2021 as an association bundling policy and confounders) without causal attribution.

**Figures/tables.** None.

---

## Appendix map

| Appendix | Contents | Source files |
|---|---|---|
| A | Intervention-date registry (full), source log index | `02_policy_sources/*.csv` |
| B | Full HS-6 code lists (B4, C1–C3), extraction protocol, validation summary | `03_mapping/*`, `fetch_meidb.py`, validation report |
| C | Backward-extension feasibility summary | `backward_extension_feasibility.md` |
| D | Remaining EDA figures (levels/seasonality/STL/ACF-PACF panels not in main text) | `07_figures/eda_*` |
| E | Full baseline regression output; residual diagnostics figures & tests | `ITS_prelim_*`, `its_02_*` |
| F | Full 45-row robustness matrix; AIC scan; remaining forest plots | `ITS_robustness_matrix.csv`, `ITS_arma_aic_scan.csv`, `rob_01_*` |
| G | Full volatility grid (32 rows: both window schemes × variants × straddle) | `volatility_results.csv` |
| H | Full forecast validation grid; B1/B2 counterfactual figures | `forecast_validation.csv`, `fc_01_*` |

**Main-text vs appendix rule applied:** the main text carries one representative figure per analytical step and condensed tables limited to β₃/σ/gap columns; anything enumerative (full matrices, per-basket figure sets, code lists, month FE coefficients) goes to the appendix. Main-text target length ~15–20 pages plus appendices.

## Writing-rules checklist (binding on the prose draft)

1. B3 never described as a PLI effect; p = 0.0013 never appears without its non-robustness in the same paragraph (§7, §8).
2. B1's 28 pre-months always "data-availability constraint", never truncation (§4, first mention).
3. Volatility declines never "policy stabilisation"; COVID reversal adjacent to the ranking (§9).
4. Forecast gaps never treatment effects; "actual minus pre-policy time-series counterfactual" at every use (§10).
5. Controls never DiD identification (§5, §8, §11).
6. "Alternative-date robustness exercise", never "placebo test" (§8).
7. Break-diagnostic limitations preserved (§8f).
8. Tie-break timing disclosure preserved (§10).
9. B2 SARIMA 0.839 ✗ preserved (§10, Table 9).
10. Descriptive ranking vs robust effect distinction preserved (§9, §12).
11. Controls sentence in the approved wording only; no Type-I-rate/over-rejection framing (§8g).
12. No new empirical result anywhere; every number traces to `FINAL_EVIDENCE_TABLE.md`.

---

**STOP.** Outline complete. Awaiting approval before writing the polished report prose.
