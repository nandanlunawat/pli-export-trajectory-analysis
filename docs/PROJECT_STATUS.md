# PROJECT STATUS

**Project:** PLI Scheme — Export Trajectory, Counterfactual and Volatility Analysis
**Last updated:** 29 August 2026
**Maintained under:** project-control rules issued 29 Aug 2026 (see §7)

---

## 0. WORKSPACE — RESOLVED

The control instruction named **`PLI_Citi_Project`**; no folder of that name was visible. **Confirmed 29 Aug 2026: `PLI_Citi_Project` and the mounted folder are the same project.** The working path is:

```
<project-root>
```

It already contains the exact structure described in the instruction (`01_raw_data/` … `99_legacy/`, `docs/`). All ten control rules apply to it. No folder was created, renamed or moved.

---

## 1. COMPLETED WORK

### Phase 1 — Forensic audit of the inherited project *(complete)*
- Audited the original notebook, dataset, DOCX/PDF report and README.
- Established the inherited data is **annual, six observations per sector** — the reason the CV claims were unsupported.
- Identified and documented the defects: SD-of-levels used as "volatility"; a "growth acceleration" figure subtracting a 1-year from a 3-year growth rate; a stray `savefig` silently blanking a chart; twelve cells of hardcoded `D:\PLI_Export_Project` paths; two report arithmetic errors (12.9 vs 12.09; a "7 pp" share rise that is 6.15 pp); a period mislabelled "2019–2024" for FY2019-20 → FY2024-25.
- Established that **three of the five sectors were not PLI sectors at all** (plastics, engineering goods, chemicals), against the official 14-sector list.
- Output: `docs/00_PHASE1_AUDIT_AND_DESIGN.md`, `docs/source_log.md`, `docs/archive/pli_sector_mapping_PROPOSED.csv`.

### Phase 2 — Research design and HS continuity *(design complete; two verification gates open)*
- **HS classification continuity resolved from Indian government primary sources** — DGFT Notification 54/2015-20 (09.02.2022), DGFT Notification 08/2023 (29.05.2023), DGCI&S ITC(HS)-2017 Chapter 85, Budget TRU letters 2025-26 and 2026-27.
- Scored five candidate sectors on the eight stated criteria; locked four baskets and dropped Telecom.
- Decomposed intervention dates five ways per scheme and selected one primary date each.
- Specified the forecasting counterfactual, the segmented time-series model, the volatility measure, the COVID treatment and the control basket.
- Output: `08_report/research_design_memo.md`, `08_report/data_quality_report.md`, `08_report/verification_status.md`, `03_mapping/hs_mapping_master.csv`, `02_policy_sources/pli_intervention_dates.csv`, `03_mapping/control_sector_mapping.csv`, `02_policy_sources/source_log.csv`.

---

## 2. CURRENT PHASE

**Phase 2 — closing the blocking verification gates. No data extraction. No modelling.**

Rule 9 governs: final modelling does not begin until the Phase 2 memo is signed off and the blocking HS/data issues are resolved. The memo is written; **sign-off has not been given**, and two gates (D1, D2 below) are open.

---

## 3. LOCKED DECISIONS

| Decision | Value |
|---|---|
| **Study window** | April 2018 – March 2026, 96 months, 8 complete fiscal years |
| **Core basket B1** | Telephone sets — `851711 + 851712 + 851713 + 851714 + 851718` (the complete 8517.1x group), D_s = **Aug 2020**. *Amended 29 Aug 2026 under approved CP-001.* |
| **Core basket B2** | Pharmaceutical formulations — `3003 + 3004`, D_s = **Apr 2022** |
| **Core basket B3** | Air conditioners — `8415`, D_s = **Apr 2022** |
| **Robustness basket B4** | MMF fabrics — the 14 PLI Annexure-II codes, D_s = **Apr 2024** |
| **Dropped** | Telecom — weakest mapping, not forecast-validatable, and its basket carves the same HS-4 heading as B1 |
| **Intervention-date rule** | D_s = start of the first period in which incremental sales accrue toward a claim. Never the Cabinet or notification date. |
| **Basket rule** | A basket is the *union* of every code carrying the product in any vintage, at the digit level that makes the union closed |
| **Outcome variable** | ln(monthly exports, US$ mn FOB) |
| **Trajectory model** | Segmented regression, `TimeAfter = max(0, T − T_Ds)`, month FE, COVID dummy, Newey–West HAC at lags 3 and 12, plus a stationary growth-rate companion |
| **Forecast horizon** | h = 12 primary, h = 6 secondary, h = 18 for B4 only |
| **Forecast candidates** | Seasonal naïve, ETS, SARIMA only if diagnostics justify. Selection strictly inside the pre-policy window. |
| **Electronics forecasting** | **Excluded from validated forecasting** — 28 pre-months yields zero validation origins. Seasonal-naïve only, labelled as not model-selected. |
| **Volatility** | SD of monthly log growth over **symmetric ±24-month windows**. Never SD of levels. |
| **COVID** | `Covid_t` = Apr–Jun 2020, fixed on the lockdown event, not on fit |
| **Controls (pre-registered)** | C1 leather goods (Ch 42, narrowed), **C2 footwear (Ch 64 — replaces ceramics/glassware)**, C3 cotton textiles (matched to B4). All three HS-6 continuity-clean. *Amended 29 Aug 2026 under approved CP-002.* |
| **B1 robustness** | `Transition_t` dummy for Jan 2022 – Apr 2022; β₃ reported with and without. Pre-specified before estimation. |
| **Claim language** | Association around implementation. Never *caused*, *impact* or *attributable*. |

---

## 4. UNRESOLVED QUESTIONS

**Blocking (must clear before extraction):**

| # | Question | Why it blocks |
|---|---|---|
| **U1** | CBIC SF/DF/NF/DP/NP correlation letter codes for Ch 29, 30, 54, 55, 58, 60, 61, 62, 84, 85 | DGFT Notn 54 rules out a **code-level** break but not a **scope change at an unchanged code**. **Largely superseded** by the D2 probe, which observes directly what the series does. |
| ~~CP-001~~ | ~~Sign-off on Change Proposal 001~~ | **APPROVED and IMPLEMENTED 29 Aug 2026.** See `docs/DECISION_LOG.md` D-001. |
| ~~NEW-2~~ | ~~C2 control basket~~ | **RESOLVED 29 Aug 2026 under CP-002** — replaced outright with **Footwear, Chapter 64**. See `docs/DECISION_LOG.md` D-002. |
| ~~O2b~~ | ~~Chapter 64 in DGFT Notification 08/2023~~ | **CLEARED 29 Aug 2026.** Full notification read end to end — **zero Chapter 64 entries** in Annexures I, II or III. Chapter 42 likewise zero. Source log S35–S37. |
| ~~O5~~ | ~~Exact HS-6 line lists for C1, C2, C3~~ | **DONE 29 Aug 2026.** Enumerated in `03_mapping/control_hs6_codes.csv` from the MEIDB code inventory at two vintages. C1 = 20 codes, C2 = 25 codes, C3 = 58 rows across four components. Zero overlap between controls and zero overlap with B4. |
| ~~CP-003~~ | ~~C3 composition~~ | **APPROVED (Option 1) and IMPLEMENTED 29 Aug 2026.** C3 = headings 5208–5212, 70 HS-6 codes. See `docs/DECISION_LOG.md` D-003. |

**Resolved by the D2/D3 probe, 29 Aug 2026:**

| # | Question | Resolution |
|---|---|---|
| **U2** | Jan-2022 vs Apr-2022 statistical switch | **RESOLVED — and the documented assumption was wrong. There are TWO transitions.** Jan-2022 (customs tariff; `851712` halves while `851718` rises 196-fold and `851711` 103-fold, with no new codes) and Apr-2022 (DGCI&S directory; `851713`/`851714`/`851771`/`851779`/`8524` appear, `851770` → 0.00). Jan–Mar 2022 is a contamination window. See `docs/CHANGE_PROPOSAL_001_mobile_basket.md`. |
| **U3** | Whether MEIDB re-maps history or relabels | **RESOLVED — it does NOT re-map.** `851712` returns values for pre-HS2022 months, `851713` returns none, and `851770` is displayed as `*PARTS:`. MEIDB retains codes as originally filed and stars those absent from the current directory. |
| **U6** | Continuity of control chapters | **RESOLVED.** Chapters **41, 42, 52, 64 have ZERO rows** in DGFT Notn 54 Annexure-II → fully unchanged, so **C1 leather and C3 cotton are clean**. **Chapter 69 changed** (heading 6903 restructured) and **Chapter 70 changed** (heading 7019 glass-fibre heavily restructured) → **C2 ceramics/glassware is NOT clean as specified** and must exclude headings 6903 and 7019, or be replaced. Raised as an open decision below. |
| **V3 / V4** | April-2024 directory change; 8415 and 3003/3004 continuity | **PASS.** No HS-6 change anywhere in 8517, 8524, 8415, 3003 or 3004 at the Mar→Apr 2024 boundary. The documented April-2024 changes are **8-digit only** and invisible at HS-6 — which vindicates building at HS-6 rather than HS-8. B2 and B3 confirmed clean at every boundary tested. |

**Non-blocking:**

| # | Question | Status |
|---|---|---|
| **NEW-1** | On the proposed wider basket, Jan-2022 still sits 31% below Dec-2021 against a 4% seasonal fall a year earlier — and the dip survives at HS-4, so it is not within-8517 leakage | Either genuine or leakage outside heading 8517. Four months cannot distinguish. Assess on the full series. A `Transition_t` dummy for Jan–Apr 2022 is pre-specified in CP-001. |
| **NEW-2** | C2 control basket needs headings 6903 and 7019 excluded, or a replacement control | Decision required before controls are used |
| **U4** | Date of the intermediate `851712` 8-digit change (2017–2021) | Immaterial at 6-digit; documented as a third reason not to work at 8-digit |
| **U5** | Heading `2941` after 01.05.2025 (Finance Act 2025, headings not itemised) | Not used in the locked design |
| **U7** | FTPA group list, start date, units | Only if the long-history electronics forecasting route is taken |

---

## 4b. PHASE 3 — EXTRACTION COMPLETE (30 Aug 2026)

| Step | Status |
|---|---|
| 1. Write `05_analysis/fetch_meidb.py` | **DONE** — resumable, rate-limited, refuses to overwrite raw files, `--build-only` and `--currency` modes |
| 2. Extract monthly HS-6 data only | **DONE** — 48 requests, 96 months, 7 baskets, 672 rows |
| 3. Preserve raw responses with retrieval dates | **DONE** — `01_raw_data/raw_trade_data/meidb_hs6_extract_2026-08-29/` (see validation report §9 on scope) |
| 4. Build `04_clean_data/master_monthly_exports.csv` | **DONE** — 672 rows, full schema |
| 5. Run A1–A9 / dataset-validation assertions | **DONE — 15/15 HARD ASSERTIONS PASS** |
| 6. STOP before modelling | **STOPPED** |

Two documentation clarifications were made before extraction, as instructed, and nothing else in the design was touched:

- **Control D_s** — memo §8.5 now states that each control is estimated once per treated date (2020-08, 2022-04, 2024-04), holding every other model element identical, with `Transition_t` applied to B1 only.
- **B1 framing** — memo §1.3 now carries a "What B1 is, and what it is not" subsection: B1 is an **HS-based export proxy** for the PLI-LSEM mobile-phone segment, not a measure of PLI-covered output. Required phrasing is specified; "PLI mobile-phone exports" is prohibited.

## 4c. PHASE 4 — EDA COMPLETE (30 Aug 2026)

Diagnosis only. **No ITS, forecasting, volatility inference, control or robustness model estimated. No locked specification altered.**

Deliverables: `05_analysis/01_EDA.ipynb`, `05_analysis/eda_core.py`, `06_results/EDA_summary.csv` (244 rows, 9 blocks), `07_figures/` (22 figures), `08_report/EDA_findings.md`.

| Question | Finding |
|---|---|
| Seasonality | **Strong and fiscal-year driven** — March high, April collapse in all four baskets, B3 included (B1 April = −65 log points). Month FE essential. B3's low STL seasonal *strength* (0.015) reflects its very large idiosyncratic remainder, **not** an absence of seasonality. |
| Log transform | **Appropriate** — proportional heteroskedasticity in levels for B1/B2/B3; 119× and 62× dynamic ranges. Qualification: logs slightly over-correct, leaving early low-level periods proportionally more volatile. |
| Autocorrelation | **Present in B1, B2, B3; not detected in B4.** B1's is almost purely at lag 12 (LB(6) p=0.54 but LB(12) p=0.0001). Validates HAC at both lag 3 and lag 12. |
| Stationarity | Growth consistent with stationarity throughout; the one exception (B3 KPSS p=0.042) is COVID-driven and resolves to p=0.100 excluding Mar–Sep 2020. **For B1 the evidence is consistent with I(1)-type behaviour in levels even when a break is allowed** (Zivot–Andrews fails to reject), making the growth companion essential for the primary endpoint. No single test establishes an integration order. |
| **Notation correction (30 Aug)** | `g = 100·Δln(Y)` is reported in **log-growth points (lgp)**, not percentage growth. Figures, findings doc, summary CSV and memo §6.1 all corrected. −275.8 lgp = −93.7% simple; +222.2 lgp = +822% simple. |
| Zivot–Andrews breaks | 2020-02, 2021-03, 2020-05, 2020-02 — **none coincides with its D_s**. Confirms the memo's prediction that break tests find COVID first. |
| Design-invalidating issues | **None.** Two interpretation caveats carried forward: residual level-dependence of B1 volatility (1.52× after removing COVID) and B4's weak trend strength (0.249). |

## 4d. PHASE 5 — PRELIMINARY ITS COMPLETE (30 Aug 2026)

Baseline ITS, residual diagnostics, growth companion, B1 `Transition_t` robustness. **No forecasting, volatility inference, controls or full robustness matrix.** Specification unchanged.

Deliverables: `05_analysis/02_ITS_diagnostics.ipynb`, `05_analysis/its_core.py`, `06_results/ITS_prelim_*.csv` (4), `07_figures/its_*.png` (13), `08_report/ITS_preliminary_findings.md`.

| Basket | β₁ (lgp/mo) | β₃ (lgp/mo) | p (HAC12) | α₁ growth (lgp/mo) | p | Verdict |
|---|---|---|---|---|---|---|
| B1_MOBILE | +6.538 (+119%/yr) | −2.921 | 0.148 | −4.148 | 0.505 | deceleration, not distinguishable from zero |
| B2_PHARMA | +0.765 | −0.134 | 0.379 | +0.529 | 0.590 | null |
| B3_AC | +0.934 | **+0.874** | **0.0013** | +0.662 | 0.718 | **significant in levels, NOT in stationary space** |
| B4_TEXTILE | +0.170 | +0.050 | 0.829 | −1.272 | 0.467 | null |

**Headline methodological finding.** Levels standard errors are 3–7.5× tighter than stationary-space ones for the same quantity. B3's only significant result does not survive the growth companion (p 0.0013 → 0.718). On present evidence **no basket shows a trajectory change distinguishable from zero once inference is done in stationary space.** ARMA-errors must adjudicate in Phase 6.

**Residual autocorrelation survives month FE in 3 of 4 baskets.** B1 severe (DW 1.06, all p < 0.001); HAC(12) is 2.20× the OLS SE there, so OLS inference would have been indefensible.

**B1 `Transition_t` passes cleanly:** coefficient p = 0.278, β₃ moves by 0.65% of itself. The CP-001 basket widening did its job.

## 4e. PHASE 6A–6C — ITS ROBUSTNESS COMPLETE (30 Aug 2026)

ARMA-errors, pre-specified robustness, controls. **No forecasting, volatility inference or stacked interaction model.** Specification unchanged; all 45 fits converged.

Deliverables: `05_analysis/03_robustness_ITS.ipynb`, `05_analysis/robustness_core.py`, `06_results/ITS_robustness_matrix.csv` (45 rows / 24 specs / 7 units), `06_results/ITS_structural_breaks.csv`, `06_results/ITS_arma_aic_scan.csv`, `07_figures/rob_01_*` (4), `08_report/ITS_robustness_findings.md`.

**HEADLINE: no basket shows a trajectory change that survives the pre-specified robustness set.**

| Basket | Baseline | ARMA-errors | Growth companion | Alt dates | Verdict |
|---|---|---|---|---|---|
| B1_MOBILE | n.s. | n.s., attenuates −2.92 → −1.55 → −0.97 | n.s. | sign stable, 3/10 sig | No robust change |
| B2_PHARMA | n.s. | n.s. | n.s. | 1/9 sig | No robust change |
| B3_AC | **sig (p 0.0013)** | sig under AR(2) (p 0.029), **n.s. under AR(1)** (p 0.152) | **n.s. (p 0.718)** | **sig at every date over a 2-year span** | **NON-ROBUST — not a finding** |
| B4_TEXTILE | n.s. | n.s., sign flips | n.s. | 1/8 sig | No robust change |

**Decisive evidence on B3:** β₃ is large, positive and significant at 2021-04, 2022-01, 2022-04, 2022-07, 2022-10 **and** 2023-04 — dates 24 months apart. A genuine dated break would peak at the true date and weaken away from it; this profile is flat. The model is fitting **smooth curvature, not a discontinuity**. The alternative-date battery functioned as the pre-specified placebo test and B3 fails it.

**Structural breaks:** no locked date recovered by supF or Bai–Perron on COVID-adjusted data. Closest is B1 (supF argmax 2020-10 vs locked 2020-08).

**Controls over-reject:** 2 of 9 placebo regressions significant at 5% against ~0.45 expected. C2 Footwear is significant at B1's own date. Nominal p-values in this design are optimistic — a genuine limitation for the write-up.

**B1 `Transition_t` carried forward unchanged:** p = 0.278, β₃ moves 0.65% of itself.

**Implication for the CV claims:** both bullets remain supportable — they require a correctly estimated *ranking*, not a positive result. B3 has the largest positive β₃, B1 the largest negative. What must not be claimed is statistical robustness.

## 4f. BACKWARD-EXTENSION FEASIBILITY — ANSWERED (2 Sep 2026)

**Question:** can the MEIDB monthly HS series be extended before April 2018 while preserving comparable product definitions?
**Answer: NO.** Full assessment in `08_report/backward_extension_feasibility.md`; sources S39–S42.

| Portal | Frequency | Granularity | Coverage |
|---|---|---|---|
| MEIDB | Monthly | HS 2/4/6/8 | **Jan 2018 – Jun 2026** |
| EIDB | **Annual (FY)** — no month field | HS 2/4/6/8 | 2017-18 – 2025-26 |
| FTPA | Monthly-indexed but **cumulative FY-to-date** | **191 Principal Commodity groups**, no HS | Jan 2010 – Jun 2026 |

**No official Indian source publishes monthly HS-level export data before January 2018.** B1's 28-month pre-period is therefore **irreducible**, not a design choice — memo §2.1 and §E.4 updated to say so.

**Open item O3 CLOSED as not viable.** The Phase-1 assumption of a usable FTPA "electronics group" was wrong: the nearest group is **P4 TELECOM INSTRUMENTS**, which merges handsets with base stations and transmission equipment — fusing B1 with the Telecom sector deliberately dropped in Phase 2. B3 air conditioners have **no** proxy group at all (buried in `15 MACHINERY` / `N4 ELECTRIC MACHINERY`). Only B2 has a near-match (`H8 DRUG FORMULATIONS, BIOLOGICALS`), and it adds biologicals with no HS concordance.

**Even with data, extension would not help:** it would cross a third classification boundary (ITC(HS)-2012 → 2017), import demonetisation (Nov 2016) and GST (Jul 2017) into the pre-period, and would not address the Phase-6 diagnosis — B3's problem is functional form (curvature), not sample length, and a longer pre-period makes a piecewise-linear fit to a curving series *worse*.

**Recommendation: do not extend.** No design change proposed or made.

## 4g. AUDIT ACCEPTED → R12 + VOLATILITY COMPLETE (2 Sep 2026)

Hostile audit accepted with corrections; all six reporting corrections applied (ARMA `se_type` column added to the matrix; B4 non-convergence fallback disclosed; "placebo test"→"alternative-date robustness test"; over-rejection claim softened to exact binomial p=0.071 caution; structural-break diagnostics downgraded to explicitly limited corroboration; unrun-items table added). Audit language corrected: n_eff figures reframed as a dependence-erosion **heuristic**, not a sample size; the uncited "12/24 per segment" threshold withdrawn in favour of segment-length arithmetic.

**R12 quadratic pre-trend — RUN.** One added term (T²) to the locked baseline; nothing else changed. **β₃ flips sign in all four baskets.** B3: +0.874 (p 0.0013) → **−1.126 (p 0.215)**, with the significance migrating to T² (+2.086, p 0.026); partial corr(T², TimeAfter | others) = **0.970**. **The curvature interpretation is decisively strengthened — β₃ and smooth curvature are not separately identified on this window.** B2's R12-only significance is non-robust by the symmetric application of the interpretation rule. Output: `06_results/ITS_R12_quadratic_pretrend.csv`.

**Pre-registered volatility — RUN, descriptive component complete.** Locked design only (±24 symmetric windows, lgp, MBB block-6 ×4000 fixed-seed, COVID-excluded variant, straddle obs separated, no annualisation, no GARCH). Ranking by |Δσ| (primary, straddle excluded): **B3 −52.7 lgp (−69%), B1 −24.0 (−39%), B4 +3.2 (+24%), B2 −0.5 (−4%)**. **No MBB CI excludes zero.** COVID-excluded variant reverses B3 to **+6.2** and B1 to **+1.1** — the headline declines are entirely COVID inside the pre-windows, exactly as pre-warned. **The frozen CV volatility clause is now covered by a genuine ranking with uncertainty.** Outputs: `06_results/volatility_results.csv`, `07_figures/vol_01_rolling_sd_windows.png`.

**Forecasting — ASSESSED, NOT RUN.** Recommendation: **RUN ONLY AS EXPLORATORY** (B2/B3/B4 full locked protocol with the mandatory 7-origin disclosure; B1 seasonal-naïve only, "not model-selected"; no causal reading of gaps; pre-stated note that a large B3 gap is the expected signature of the documented curvature). Defensible minimum alternative: B4 only. **Awaiting decision.**

Consolidated deliverable: `docs/archive/FINAL_findings_and_recommendation.md` (findings, drop-in methodology and limitations paragraphs, exact interview interpretation, forecasting recommendation).

## 5. NEXT ACTION

**STOPPED FOR SIGN-OFF.** Change Proposals 001 and 002 are decided, implemented and verified. The memo is amended. Nothing further proceeds without your approval.

**Design locked and signed off. Phase 3 extraction complete. Panel passes every hard validation check.**

**Awaiting: your decision on the forecasting recommendation in `docs/archive/FINAL_findings_and_recommendation.md` §3.**

Then, in order:

1. ~~EDA~~ — **DONE 30 Aug 2026.**
2. ~~Preliminary ITS~~ — **DONE 30 Aug 2026.**
3. ~~Phase 6A–6C robustness~~ — **DONE 30 Aug 2026.**
4. ~~Hostile audit + corrections~~ — **DONE 2 Sep 2026.**
5. ~~R12 quadratic pre-trend~~ — **DONE 2 Sep 2026.**
6. ~~Volatility analysis~~ — **DONE 2 Sep 2026.**
7. ~~Forecasting counterfactual~~ — **DONE 2 Sep 2026 (limited exploratory scope, as approved).**
8. Final report, README rewrite, interview-prep sheet, line-by-line CV claim audit — **awaiting instruction to begin.**

## 4h. PHASE 7 — EXPLORATORY FORECASTING COMPLETE (2 Sep 2026)

Locked protocol executed: pre-policy-only expanding-origin validation (m=30), candidates {seasonal naïve, ETS add/damped, pre-declared SARIMA airline}, h=12 primary / h=6 / h=18 (B4). Deliverables: `04_forecasting.ipynb`, `forecast_core.py`, `forecast_validation.csv`, `forecast_counterfactual.csv`, 4 `fc_01_*` figures, `08_report/FORECASTING_findings.md`.

**Selection outcome — seasonal naïve for all four baskets.** B1 by lock (benchmark only, not model-selected); B2 outright (RMSE 0.071 vs 0.109 next-best, and both ETS variants fail the coverage condition); B3 and B4 by the locked §4.5 tie-break — the SARIMA (t=0.45) and ETS-damped (t=0.03) RMSE wins are indistinguishable from naïve across origins, and the clause prefers the simpler model. The 7-origin B2/B3 disclosure is attached throughout. **Most instructive validation fact: nothing in the candidate set detectably beats last-year's-same-month on these series.**

**Counterfactual gaps ("actual minus pre-policy time-series counterfactual" — never a causal estimate):** B1 +23.2% (h=12; benchmark-only, no claim made), B2 +2.6%, B3 +23.2% (h=12; pre-stated as the forecast-space restatement of the R12 curvature), B4 −2.2% (h=12; −1.9% at h=18; the best-validated case runs slightly *below* counterfactual). **Every actual lies inside the 95% counterfactual interval in every basket at every horizon.** No significance tests on gaps. Standing conclusion unchanged: *no basket shows a trajectory change that survives the pre-specified robustness framework.*
3. Forecast counterfactual — B2, B3, B4 only; B1 seasonal-naïve, labelled as not model-selected.
4. Volatility — symmetric ±24-month windows.
5. Robustness R1–R13 → write-up → CV claim audit.

Non-blocking items still open: ₹ crore second pass for robustness R8 (`fetch_meidb.py --currency 3`); footwear Quality Control Order dates and scope for the limitations section.

**Optional, no longer blocking:**
- **D1** — read the CBIC correlation PDF locally for the SF/DF/NF letter codes. Would close the residual "scope change at an unchanged code" risk for B2/B3/B4. The D2 probe found no sign of such a change.
- **U7** — FTPA group list, start date and units, only if the long-history electronics forecasting route is wanted.

### Method note for future MEIDB work

The in-app browser drives MEIDB successfully. What works: the **All Commodities → 6 digit Level** route (the *Specific HSCode* route returns 404 without going through the modal picker); the results grid is a **DataTables** table holding all ~5,150 rows client-side, so the full result set can be read via the DataTables API without paging. A query for month M, year Y returns **both** M-(Y−1) and M-Y, which halves the number of requests needed.

---

## 6. FILES CREATED / MODIFIED

### Created this project (all still current)

| File | Purpose |
|---|---|
| `docs/PROJECT_STATUS.md` | **this file** |
| `docs/00_PHASE1_AUDIT_AND_DESIGN.md` | Phase 1 forensic audit and initial design |
| `docs/source_log.md` | Phase 1 source log (narrative form) |
| `docs/archive/pli_sector_mapping_PROPOSED.csv` | Phase 1 proposed mapping — **superseded** by `03_mapping/hs_mapping_master.csv` |
| `08_report/research_design_memo.md` | **The locked Phase 2 design.** One recommended specification. |
| `08_report/data_quality_report.md` | Provenance, known defects, validation gates A1–A9 |
| `08_report/verification_status.md` | A/B/C/D verification report — verified facts, unresolved facts, access problems, minimum steps |
| `03_mapping/hs_mapping_master.csv` | Per basket: old code → new code → continuity rationale → source |
| `03_mapping/control_sector_mapping.csv` | Pre-registered controls with justification |
| `02_policy_sources/pli_intervention_dates.csv` | Five-way date decomposition, primary D_s, sensitivities |
| `02_policy_sources/source_log.csv` | 34 sourced claims, confidence-graded |
| `04_clean_data/master_monthly_exports.csv` | **Schema only — deliberately empty.** Population blocked by §5. |
| `docs/DECISION_LOG.md` | **Chronological record of approved design decisions** (rule 8). D-001 and D-002 recorded. Nothing is implemented until it appears here as APPROVED. |
| `docs/CHANGE_PROPOSAL_001_mobile_basket.md` | B1 basket widened to the 8517.1x group. **APPROVED and IMPLEMENTED 29 Aug 2026.** |
| `docs/CHANGE_PROPOSAL_002_control_basket.md` | C2 replaced with Footwear (Ch 64); C1 narrowed to Ch 42. **Pre-registered, implemented, awaiting final sign-off with the memo.** |
| `docs/CHANGE_PROPOSAL_003_C3_composition.md` | C3 composition — spans four value-chain stages and its Ch 62 lines are discontinuous. **PROPOSED, NOT IMPLEMENTED.** |
| `docs/CHANGE_PROPOSAL_003_C3_composition.md` | C3 narrowed to headings 5208–5212. **APPROVED Option 1 and IMPLEMENTED 29 Aug 2026.** |
| `03_mapping/control_hs6_codes.csv` | **Enumerated HS-6 code list for all three controls** — C1 = 20, C2 = 25, C3 = 70, total **115**. Cross-checked at the Mar-2019 and Apr-2024 vintages. One row per code, with vintage validity and inclusion status, plus auditable records of the CP-003 exclusions. |
| `08_report/DATASET_VALIDATION_REPORT.md` | **Pre-extraction validation gate.** Sections 1–3 final and PASSING; sections 4–7 pending extraction with every hard assertion stated in advance. **Modelling is blocked until all assertions PASS.** |
| `01_raw_data/raw_trade_data/meidb_continuity_probe_2026-08-29.csv` | **Raw MEIDB observations**, retrieval-date stamped, with the coverage banner recorded verbatim. Evidence for V1–V4. Never overwrite — new pulls get a new dated file. |

### Structural change made BEFORE the control rules were issued — disclosed for the audit trail

On 28 Aug 2026, while building the folder architecture, the inherited artefacts were **moved** (not copied, not deleted) into `99_legacy/`:

- `export_analysis.ipynb.ipynb` → `99_legacy/export_analysis_ROOT_COPY.ipynb`
- `analysis/` → `99_legacy/analysis_original/`
- `figures/` → `99_legacy/figures_original/`
- `report/` → `99_legacy/report_original/`
- `data/` → `99_legacy/data_original/` (a copy was also placed at `01_raw_data/legacy_annual_data/`)

**All 14 files are intact and verified present.** Nothing was deleted or overwritten. Under rule 1, `99_legacy/` is now immutable and will not be touched again.

### Corrected finding — the "duplicate" intervention-dates file (29 Aug 2026)

**What I got wrong.** I flagged `docs/archive/pli_intervention_dates.csv (formerly 03_mapping/)` as a stale duplicate of `02_policy_sources/pli_intervention_dates.csv` and recommended deleting it. That recommendation was based on filename, byte size and modification date — **I had not diffed the contents.** The older file was in fact the *larger* one, and on inspection it held material the newer file did not:

- the **bulk-drugs PLI as a companion scheme** to the Pharmaceuticals PLI — its notification (2020-07-21), Gazette No. 172 / No. 31026/16/2020-Policy, revised guidelines (2020-10-29), 120-day application window, and the fermentation-route sensitivity date (2023-04);
- verbatim rationale quotes from the notifications (Pharmaceuticals para 3.3, bulk-drugs para 4.2);
- the flag that the LSEM **Round 1 opening date is NOT STATED in the gazette**;
- the analytical note behind the White Goods sensitivity date ("tests whether capacity build-out moved exports before the sales incentive began").

**Deleting it would have destroyed verified, sourced content.**

**Action taken instead — a strictly additive merge.** All unique content from the `03_mapping` copy was merged into the authoritative `02_policy_sources/pli_intervention_dates.csv`, which grew from 19 to 21 columns (adding `basket_id` and `role`, and splitting `sensitivity_dates` into three explicit columns).

**Verified after the merge:**
- All five `PRIMARY_Ds` values **unchanged** — `2020-08`, `2022-04`, `2022-04`, `2024-04`, `NOT SELECTED`. **No methodological change; rule 8 not triggered.**
- CSV parses cleanly, 21 fields on every row, no malformed rows.
- Content-preservation check passed on seven distinctive strings from the old file.

**Current disposition.** Deletion of the `03_mapping` copy was proposed and then **declined**. Both files remain on disk, untouched since the merge.

| File | Status |
|---|---|
| `02_policy_sources/pli_intervention_dates.csv` | **AUTHORITATIVE.** Referenced by the memo. Contains the union of both versions. |
| `docs/archive/pli_intervention_dates.csv (formerly 03_mapping/)` | **Superseded but retained.** No longer holds anything absent from the authoritative copy. Left byte-identical — no marker added, since that would itself be a modification. |

**Lesson recorded for this project:** never classify a file as redundant from metadata alone. Diff the contents first. This applies with force to anything in `01_raw_data/` and `99_legacy/`.

### Other housekeeping items flagged, NOT acted on (rule 5)

| Item | Observation | Proposed action |
|---|---|---|
| `docs/archive/pli_sector_mapping_PROPOSED.csv` / `.xlsx` | Phase 1 output, superseded by `03_mapping/hs_mapping_master.csv` | Retain as audit trail. No action proposed. |
| `README.md` / `SCHEMA.md` in `01_raw_data/raw_trade_data/`, `02_policy_sources/`, `04_clean_data/`, `05_analysis/` | Not created by me. Left untouched. | None. |

---

## 6b. MODELLING FREEZE AND REPORT-PREPARATION PHASE (3 Sep 2026)

**Forecasting audit accepted; ALL statistical/econometric modelling permanently frozen by user instruction (3 Sep 2026).** No new models, specifications, intervention dates, controls, transformations, forecasting methods, DiD/stacked interactions, GARCH, break tests, or significance-driven analyses may be run. Six reporting-layer corrections from the forecasting audit (C1–C6, recorded in the audit exchange and in the evidence table's caveat register item 9) are to be applied verbatim at report drafting — the key ones: ✗ marker on B2 SARIMA coverage 0.839; "three routes" selection wording replacing "won everywhere"; tie-break operationalisation timing disclosure; B1 figure-caption "not model-selected" label.

**Created:** `08_report/FINAL_EVIDENCE_TABLE.md` — the complete per-basket evidence table (14 items × 4 baskets, transcribed from `06_results/*.csv`, nothing re-estimated), the "What can I say / What can I NOT say" table (7 topics), and the 10-item caveat register that the final report may not drop.

**Current phase:** report preparation. Evidence base delivered and approved 3 Sep 2026 with one wording correction applied (controls sentence: "Two of nine descriptive control regressions were nominally significant at the 5% level, illustrating that individual nominal p-values should be interpreted cautiously in this design" — no Type-I-rate/over-rejection framing; applied in both the cross-cutting paragraph and caveat register item 6).

**Created:** `docs/archive/REPORT_OUTLINE.md` — detailed 12-section outline per the user's approved hierarchy: purpose, figures/tables, exact results, limitation placement per section; appendix map (A–H); binding 12-item writing-rules checklist; central conclusion fixed verbatim for abstract/§7/§12. Outline approved 3 Sep 2026 with four wording changes (applied to REPORT_OUTLINE.md and FINAL_EVIDENCE_TABLE.md): (1) "null is an informative finding" wording; (2) title "Policy Impact Analysis" → "Export Trajectory Analysis"; (3) approved B3 conclusion sentence; (4) approved 0.970 collinearity sentence.

**Created:** `08_report/FINAL_REPORT.md` — full 12-section report (~6,400 words), every number transcribed from FINAL_EVIDENCE_TABLE.md, appendix map A–H preserved. Internal QA performed: prohibited-phrase scan (no causal claims, no "policy impact", no "placebo test", no stabilisation claims outside negations); B3 p = 0.0013 appears only with immediate non-robustness explanation (§7, §8.7); B1 28-month constraint framed as data availability (§4); COVID volatility reversal adjacent to ranking (§9); gaps labelled "actual minus pre-policy time-series counterfactual"; tie-break timing disclosure in §10; B2 SARIMA 0.839 marked ✗ in Table 9; controls sentence in approved wording (§8.7). Report reviewed by user 3 Sep 2026; 14 mandatory corrections applied to FINAL_REPORT.md: (1) B1 growth "two orders of magnitude" (verified against master CSV: 26.65 → 2,792 US$ mn, ×105, endpoint months) — "tenfold" removed in both occurrences; (2) β₂ relabelled "Immediate level shift β₂ (log points)" — no lgp; (3) approved stationarity wording (no common integration order claim); (4) ARMA grid disclosure wording + Appendix F grid-reduction note (Phase-5 baselines known when grid reduced; no ARMA result inspected); (5) B1 COVID-drop wording; (6+12) trajectory ranking corrected to "largest POSITIVE estimated trajectory change" for B3, B1 noted as largest negative point estimate (abstract, §9, §12); (7) B4 verification wording (annexure-defined; CBIC letter-code subset unverified); (8) forecasting "pre-specified framework + tie-break sequencing" wording replacing "locked in advance"; (9) "AC exports exhibit a substantial acceleration in the observed series"; (10) residual-diagnostics wording; (11) §4 segment-information sentence added; (13/14) numerical + interpretation QA re-run via pattern scans — all pass. Final QA pass (user-directed, 3 Sep 2026) applied correction-and-freeze items to FINAL_REPORT.md: C-1 §8.4 date/p-value split (locked date p = 0.0013; five alternative dates all p ≤ 0.0007) — also corrected in FINAL_EVIDENCE_TABLE.md B3 alt-date cell; C-2 §7 "every robustness variant confirms" replaced with approved specification-dependent wording; C-3 §8.5 B2 R12 nominal significance (+1.32, p = 0.0002) disclosed as specification instability; C-4 "incremental production" → "incremental sales of goods manufactured in India" (§2 + Table 1 B1 date-logic cell), ₹2 lakh crore figure removed (unsourced in archive; fourteen-sectors claim retained, source-log supported); M-1 partial-correlation wording (report §11 + evidence-table say/not-say row); M-2 Table 9 pooled-coverage footnote; M-3 §8.6 break dates incl. 2018-09 candidate; M-4 Table 1 B3 date logic; M-5 "falls by roughly half"; phrase revisions 2–5 applied, phrase 1 kept verbatim. QA re-verified: no residual banned wording; all frozen numbers intact; central conclusion identical in 3 places; dates match registry; institutional wording matches gazette language in registry. Three final user corrections applied (3 Sep 2026): (1) confirmed FINAL_EVIDENCE_TABLE.md carries the locked-vs-alternative-dates split matching §8.4 (already fixed in prior pass, verified verbatim); (2) §11 softened to "does not interpret B3's acceleration as evidence of a dated break at the scheme's implementation date"; (3) §5 OLS-SE sentence replaced with the user's more precise formulation ("can therefore understate uncertainty and overstate precision").

**ANALYTICAL CONTENT FROZEN (user instruction).** No further methodological, numerical, or interpretive changes permitted. Only final formatting, consistency, typography, figure/table placement, cross-references, and proofreading remain, plus the queued README rewrite, interview-prep sheet, and CV claim audit (not yet authorized).

---

## 8. CONTROLLED CLEANUP EXECUTED (8 September 2026, user-approved)

Repository-maintenance pass per the approved cleanup instruction; all analytical results untouched and verified unchanged.

**Deleted (2, both pre-verified immediately before deletion):** `05_analysis/_tmp_6a.csv` (all 8 rows confirmed verbatim in `06_results/ITS_robustness_matrix.csv`); `01_raw_data/legacy_annual_data/india_exports_commodities.xlsx` (md5-identical to the immutable `99_legacy/data_original/` copy; zero pipeline references) — the emptied `legacy_annual_data/` directory removed.

**Archived to `docs/archive/` (6):** REPORT_OUTLINE.md, FINAL_findings_and_recommendation.md, HOSTILE_METHODOLOGICAL_AUDIT.md (from 08_report/); pli_sector_mapping_PROPOSED.csv/.xlsx (from docs/); pli_intervention_dates.csv (from 03_mapping/). Path references updated (paths only) in ITS_robustness_findings.md, 00_PHASE1_AUDIT_AND_DESIGN.md, and this file.

**Created (3):** root `README.md` (publication-facing; explicit associations-not-causal statement; appendix map; 99_legacy exclusion note); `.gitignore` (pycache/checkpoints/_tmp_*.csv/OS artifacts/*.gz/99_legacy//docs/archive//06_results_reproduction/); `05_analysis/05_volatility_R12.py` — F-1 closure.

**F-1 RESOLUTION:** the two original session scripts were recovered **verbatim** from the session transcript (not reverse-engineered) and consolidated into `05_volatility_R12.py` with identical specifications and RNG draw order (seed 20260902, MBB block 6, 4000 reps; R12 = locked baseline + (T/100)²). Validation run wrote to /tmp: **both `volatility_results.csv` (32 rows) and `ITS_R12_quadratic_pretrend.csv` (8 rows) reproduced BYTE-IDENTICALLY** against the frozen files. The script defaults to `06_results_reproduction/` so frozen results can never be overwritten. Frozen CSVs remain authoritative.

**Modified (path/metadata only):** machine-absolute paths scrubbed to `<project-root>` in PROJECT_STATUS.md, 00_PHASE1_AUDIT_AND_DESIGN.md, source_log.md (legacy-notebook defect descriptions of `D:\PLI_Export_Project` kept — historical facts); CLEANUP_AUDIT_PROPOSAL.md date corrected to 8 Sep 2026 and figure count corrected 42→44 (QA-discovered miscount; also fixed in README).

**Final QA (A–L): ALL PASS.** 12 results CSVs present; all report-referenced figures exist (44 PNGs); no code or report references deleted files; all pipeline files in place; zero machine-absolute paths in the three publication-facing docs; 99_legacy untouched (14 files); frozen numerical results byte-unchanged; F-1 byte-identical; README/.gitignore present; final structure matches the approved tree.

**Status: local cleanup complete. READY FOR GITHUB PREPARATION. GitHub publication/push NOT started, per instruction.**

---

## 9. REPRODUCIBILITY + PRESENTATION PACKAGE EXECUTED (8 September 2026, user-approved)

**Four writer gaps closed with ORIGINAL code recovered verbatim from the session transcript** (not reverse-engineered): (1) `EDA_summary.csv` writer inserted as a cell in `01_EDA.ipynb`; (2) `ITS_arma_aic_scan.csv` — `03_robustness_ITS.ipynb` now retains each basket's AIC scan and saves it, and its save cell also applies the recovered `se_type` column insertion so the matrix reproduces exactly; (3) `forecast_validation.csv` — save added to nb 04's validation cell; (4) `forecast_counterfactual.csv` — nb 04's counterfactual cell replaced with the recovered final writer (selection/selection_note columns, raw-winner rows). The `vol_01_rolling_sd_windows.png` generator (also recovered) added to `05_volatility_R12.py` as `make_rolling_vol_figure`.

**Notebook format defect discovered and repaired:** all four notebooks had been saved with source lines missing newline separators — every code cell was one syntactically invalid line (they could never have executed or rendered correctly). Normalized (format-only), cell ids added.

**All four notebooks executed top-to-bottom, zero errors**, committed WITH outputs: 01_EDA 13/13 cells, 22 inline figures; 02_ITS 11/11, 8; 03_robustness 10/10, 4; 04_forecasting 4/4, 4. Inline display uses the same PNGs saved to 07_figures (no duplicates). No absolute paths anywhere in notebooks.

**FROZEN-RESULT VERIFICATION: all 12 CSVs in 06_results/ regenerated by the executed pipeline BYTE-IDENTICAL to the frozen snapshot** (including the ARMA matrix with se_type and both forecast files). `05_volatility_R12.py` re-verified byte-identical after the figure addition. All 44 figures present, same filenames; all report references resolve; 99_legacy untouched (14 files).

**Created:** `requirements.txt` (genuine deps only; statsmodels pinned 0.15.0). **Modified:** `.gitignore` (+4 local-only process ledgers incl. this file), README reproducibility section (executed-notebook note, per-notebook output map).

**Status: READY FOR GITHUB REVIEW. Push not started, per instruction.**

---

## 10. FINAL CLEAN-ROOM VERIFICATION (9 September 2026, user-directed proof pass)

Entire pipeline copied to an isolated scratch location, notebook outputs stripped, executed from clean kernels; repo untouched throughout (12/12 repo CSVs unchanged vs pre-verification snapshot). Results: all four notebooks executed without error (13/13, 11/11, 10/10, 4/4 cells); **all 12 result CSVs reproduced BYTE-IDENTICAL from the clean room**; all 43 regenerated figures byte-identical to the repo copies (fully deterministic figure generation); report figure/result references resolve; no absolute paths in notebooks (one grep false-positive from JSON-escaped "D:\n" text); 99_legacy untouched (14 files). **One documented retained diagnostic:** `its_01_B1_MOBILE_fitwithTransition.png` is the only figure not generated by committed code (generator `its_core.plot_fit(tag=...)` exists; the call was session code; one-line fix available on request) — README wording adjusted accordingly. Three README wording changes applied: the two user-specified corrections (forecast-selection sentence; "B2 and B4 show no robust evidence of a post-implementation trajectory change") plus precision fix to the inline-charts claim. **READY FOR GITHUB REVIEW.**

---

## 7. CONTROL RULES IN FORCE

1. `99_legacy/` — never modified, overwritten, renamed or deleted. Immutable reference.
2. `01_raw_data/` — raw downloads never overwritten. New vintages saved as new versions with a retrieval date.
3. No deletions for tidiness without explicit authorisation. Items flagged in §6 instead.
4. `02_policy_sources/` — source documents kept unchanged.
5. Audit trail maintained in `docs/` and the source log.
6. **Any methodological change affecting the research design is documented here and stopped on — never silently implemented.**
7. No final modelling until the Phase 2 memo is signed off and the blocking issues in §4 are resolved.
8. This file is updated whenever work is done.
