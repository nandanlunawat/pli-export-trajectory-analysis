# PLI Scheme: Export Competitiveness and Export Trajectory Analysis

### An Interrupted Time-Series Study of PLI-Linked Sector Exports, 2018–2026

**Author:** Nandan Lunawat
**Date:** September 2026
**Data:** DGCI&S Monthly Export Import Data Bank (MEIDB), monthly HS-6 exports, April 2018 – March 2026, US$ million (retrieved 29 August 2026)
**Code and full outputs:** see repository README; all numerical results in this report are transcribed from the frozen results files in `06_results/` via `08_report/FINAL_EVIDENCE_TABLE.md`.

---

## Abstract

India's Production Linked Incentive (PLI) schemes — fourteen sectoral programmes linking incentives to incremental sales of goods manufactured in India — are the country's flagship effort to raise domestic manufacturing output, with export competitiveness among their stated objectives. This study asks how the export trajectories and volatility of four PLI-linked product groups — mobile handsets, pharmaceutical formulations, air conditioners, and man-made-fibre textiles — evolved around the implementation of the relevant schemes. Using monthly Government of India trade data at the HS-6 level and a pre-specified segmented interrupted time-series design with autocorrelation-robust inference, the analysis estimates pre-policy trends, immediate level changes, and changes in post-implementation trajectory, then subjects each estimate to a locked robustness framework: ARMA-error re-estimation, a differenced-space companion regression, alternative intervention dates, COVID-window exclusion, quadratic pre-trend curvature, structural-break diagnostics, and descriptive control sectors. Across four PLI-linked product groups, the analysis finds no robust evidence of a trajectory change specifically timed to PLI implementation over the study period; the results therefore do not establish either a positive or negative causal effect of the schemes on sector-level exports. Air-conditioner exports display the largest positive estimated trajectory change and the largest descriptive volatility change among the four baskets, but the trajectory acceleration is smooth rather than dated and the volatility decline reverses when COVID months are excluded. The null is an informative finding: the pre-specified framework did not identify a trajectory change that remained robust across alternative error structures, differenced-space inference, alternative dates and curvature specifications.

---

## 1. Research question and economic motivation

The Production Linked Incentive schemes are the largest industrial-policy initiative India has undertaken since liberalisation: fourteen sectoral programmes paying manufacturers a percentage of incremental sales, explicitly designed to build scale in sectors where India imports much of what it consumes and exports little of what it makes. Whether such subsidies change export behaviour is a first-order economic question. Export performance is where scale, cost competitiveness and integration into global value chains become observable; if PLI is building internationally competitive capacity rather than merely subsidising sales into a protected home market, the change should eventually be visible in the trade data.

This study asks a deliberately bounded version of that question: **how did the export trajectories and volatility of selected PLI-linked product groups evolve around the implementation of the relevant PLI schemes?** The design is observational. A single country's sectoral export series around a policy date cannot, by itself, separate the policy's contribution from the global demand cycle, supply-chain reorientation away from China, input prices, or the exchange rate — all of which moved substantially over the same years. The analysis therefore estimates and stress-tests *changes in trajectory around implementation dates*, and reports them as associations. Where the data cannot distinguish a policy-timed change from other patterns, the report says so. The strongest claims made anywhere below are of the form "the post-implementation trajectory changed" or "no robust change is detectable" — never "PLI caused" or "PLI failed to cause."

Figure 1 (`eda_00_overview_log_all_baskets.png`) orients the reader: log monthly exports for the four product groups over the full 96-month sample, with each scheme's implementation date marked. Two features visible in this figure organise everything that follows: mobile-handset exports increase by roughly two orders of magnitude across the sample, beginning well before the marked date; and air-conditioner exports accelerate visibly, but along a curve rather than at a kink.

## 2. PLI institutional context and intervention-date logic

Four schemes and four export baskets are studied. In each case the basket is an HS-code proxy for the scheme's product scope — a point developed in Section 3 — and the intervention date is the month from which the scheme could plausibly begin affecting production decisions that show up in exports.

**B1 — Large-Scale Electronics Manufacturing (mobile handsets).** Notified April 2020; incentives are linked to incremental sales of goods manufactured in India, applicable from 1 August 2020 under the notification itself. August 2020 (2020-08) is the primary intervention date. The scheme's notification date, the elected first year of some participants (August 2021), and mechanical ±3-month and 6-month-lag shifts are retained as alternative dates.

**B2 — Pharmaceuticals.** Notified March 2021, with participant selection and gestation delaying the first performance year to FY 2022-23. April 2022 (2022-04) is the primary date; the notification month and a fermentation-route sensitivity date (April 2023) are alternatives.

**B3 — White Goods (air conditioners).** Notified April 2021 with an explicit investment gestation period; incentives apply to incremental sales from FY 2022-23. April 2022 (2022-04) is the primary date; the notification month and a two-year-gestation date (April 2023) are alternatives.

**B4 — Textiles (man-made-fibre fabrics and technical textiles).** Notified September 2021; the scheme's first performance year is FY 2024-25. April 2024 (2024-04) is the primary date. Because the scheme's incentive structure rewards output measured from that year, earlier dates (notification, gestation start) are treated as alternatives.

The choice among notification, effective, and performance-year dates involves judgement — schemes announce long before they pay, and firms may respond to announcement, to selection, or to the start of the measurement period. Rather than defending a single date, the design commits to one primary date per scheme on the operational logic above and then re-estimates every model at every registered alternative date (Section 8). One documented gap is recorded: the gazette notification for the electronics scheme does not state the Round-1 application-window opening date; the August 2020 production-period start is taken from the scheme guidelines. Table 1 summarises; the full date registry with sources is Appendix A.

**Table 1. Schemes, baskets, and intervention dates**

| Basket | PLI scheme | Primary date D_s | Date logic | Alternative dates tested |
|---|---|---|---|---|
| B1 Mobile handsets | Large-Scale Electronics Manufacturing | 2020-08 | incentives applicable from 01.08.2020 (notification) | 2020-04, 2021-08, ±3m, +6m |
| B2 Pharma formulations | Pharmaceuticals | 2022-04 | first performance year | 2021-03, 2023-04, ±3m, +6m |
| B3 Air conditioners | White Goods | 2022-04 | first incremental-sales year (FY 2022-23) | 2021-04, 2023-04, ±3m, +6m |
| B4 MMF textiles | Textiles | 2024-04 | first performance year | 2021-09, 2022-04, ±3m |

## 3. Data, HS-code construction, and classification continuity

The dataset is built from the DGCI&S Monthly Export Import Data Bank (MEIDB), the official monthly commodity-level trade source for India, at the HS-6 level in US$ million. The sample runs April 2018 through March 2026 — 96 months — for seven series: the four treated baskets and three comparison sectors. The final panel contains 672 basket-month observations with no missing values; all figures carry the MEIDB's revised (R) vintage as of retrieval on 29 August 2026. Raw downloads are preserved unmodified with retrieval dates; a scripted, resumable extraction routine (`fetch_meidb.py`) reproduces the panel from the source.

Basket construction is where most of the project's data work lies, because HS classifications changed mid-sample. Two transitions matter: the WCO HS-2022 revision entered the Indian Customs Tariff in January 2022, and the DGCI&S commodity directory was realigned in April 2022. MEIDB does not re-map history — discontinued codes simply stop, and successor codes start — so a basket defined naively on either the old or the new codes would contain a spurious level break in early 2022.

For mobile handsets this is not a hypothetical. The pre-2022 smartphone code (851712) loses roughly two-thirds of its value between December 2021 and January 2022, exactly when the new code 851718 begins reporting; a second reallocation (851713 appearing, 851770 ceasing) follows in April 2022. The B1 basket is therefore defined as the union of five codes — 851711, 851712, 851713, 851714, 851718 — which is continuous across both transitions. The transition-month values documenting this reallocation are reproduced in Appendix B; because some compositional noise may remain in the handover months, the B1 model additionally carries a January–April 2022 transition indicator (Section 5), which turns out to be immaterial (Section 7).

For the remaining baskets — B2, headings 3003+3004 (formulations); B3, heading 8415 (air conditioners); B4, the fourteen HS codes listed in the Textiles scheme's own product annexure — continuity was established as follows: B2 and B3 were checked against the relevant official classification/correlation material, while B4 is defined directly from the Textile PLI scheme's own HS-code annexure; a subset of CBIC letter-code correlation evidence for B4 remains unverified and is documented as such in the appendix. The comparison sectors — chosen before any treated-basket estimate was seen, on continuity, economic comparability, and common exposure to export shocks — are C1, leather goods (Chapter 42, 20 codes); C2, footwear (Chapter 64, 25 codes); and C3, cotton woven fabrics (headings 5208–5212, 70 codes). Full code lists are in Appendix B.

Two validation layers support the panel. A parser spot-check reconciles scripted extraction against MEIDB's own displayed totals to within 0.002%, and fifteen hard assertions (row counts, date coverage, non-negativity, aggregate reconciliation, transition-month continuity) all pass; the validation report is cited in Appendix B.

One definitional caution governs the whole report: **these baskets are HS-based export proxies for scheme scope, not measures of PLI beneficiary output.** B1 in particular is a telephone-set export proxy aligned to the mobile-phone scheme's product space — the trade data cannot distinguish exports by scheme participants from exports by non-participants, and scheme coverage does not map one-to-one onto HS lines. Everything estimated below is therefore a sector-level association, even before the identification issues of Section 11.

## 4. Why monthly time-series data

The research question concerns changes in behaviour *around a dated event within the sample*. Annual data cannot answer it. Over 2018–2026 an annual design would have eight observations per basket, of which at most four are post-policy for the later schemes and two for textiles; no trend change, seasonal pattern, or volatility comparison can be estimated credibly from that. Monthly data provide 96 observations per basket, allow each intervention to be placed in its correct month rather than attributed to a fiscal year, expose the pronounced within-year seasonality of trade flows (which annual totals average away and which, unmodelled, would masquerade as noise or trend), and generate enough residual degrees of freedom to treat serial correlation seriously rather than assume it away.

The sample boundaries are external constraints, not choices. The MEIDB monthly series begins in January 2018; an investigation into extending the sample backward (summarised in Appendix C) found no defensible route — the alternative official sources are annual or cumulative within fiscal years, and neither preserves comparable monthly product definitions. The April 2018 start aligns the panel to complete fiscal years. **In consequence, B1's pre-policy window is 28 months — the distance from the start of the official monthly series to the scheme date — and its final five months overlap the COVID disruption. This is a data-availability constraint imposed by the source, not a truncation chosen by the analyst**, and it limits what the B1 estimates can support throughout the report. The pre/post splits are: B1 28/68, B2 48/48, B3 48/48, B4 72/24. B4's short 24-month post-window is the mirror-image constraint at the sample's end. The relevant issue is therefore not whether 96 is a universal minimum for time-series analysis, but whether the available pre- and post-intervention segments contain enough information for the specific intervention question being estimated; that information is substantially weaker for B1 than for B2 and B3.

## 5. Research design and the primary ITS specification

The core design is a segmented (interrupted) time-series regression, chosen because it answers the research question directly with three interpretable quantities. Intuitively: fit the log export series with a straight trend line plus seasonal terms up to the intervention month; allow the series to jump and to change slope at that month; and ask whether the jump or the slope change is distinguishable from zero once the series' own persistence is accounted for. The pre-policy slope (β₁) measures how fast exports were already growing; the level term (β₂) measures any immediate shift at implementation; and the trajectory term (β₃) — the coefficient this project's central claim rests on — measures whether the *growth path itself* steepened or flattened after implementation.

Formally, for each basket:

ln(Y_t) = β₀ + β₁ T_t + β₂ Post_t + β₃ TimeAfter_t + Σₘ γₘ Month_{m,t} + δ Covid_t + ε_t

where T_t is a monthly time index (April 2018 = 1), Post_t indicates months from the intervention date onward, TimeAfter_t = max(0, T_t − T_{D_s}) counts post-intervention months, eleven month indicators absorb seasonality (April is the reference month), and Covid_t marks April–June 2020, the months of acute pandemic disruption. The B1 equation additionally carries the January–April 2022 classification-transition indicator described in Section 3.

Month fixed effects are necessary because trade seasonality is large relative to the effects of interest — for some baskets, calendar-month swings exceed anything a policy could plausibly produce in a year. Autocorrelation-aware inference is necessary because monthly export series are strongly persistent; conventional OLS standard errors can therefore understate uncertainty and overstate precision. All levels-equation inference uses Newey–West HAC standard errors at lags 3 and 12, with lag 12 reported as primary; and because HAC correction is itself an approximation, Section 8 re-estimates every equation with explicitly modelled ARMA error structures and, separately, in differenced space.

The specification, the intervention dates, the COVID definitions, the robustness set, and the interpretation rules were locked in a design memo before estimation. The binding interpretation rule is quoted here because it decides the report's central result: *a result significant in one specification but not in the stationary companion, the ARMA-errors fit, or the pre-specified robustness set is non-robust — not a finding; specifications and dates are never selected on significance.*

The three comparison sectors are estimated with the identical equation at each treated date. They serve as **descriptive comparators only**: they show how similar untreated export sectors behaved around the same calendar dates. This is explicitly not a difference-in-differences design — no treated-versus-control contrast is estimated, and the controls provide no causal identification. A stacked DiD was considered and deliberately not run, because with one series per sector and common national shocks the parallel-trends assumption could not be defended.

## 6. Exploratory analysis: what the series demand of the model

The exploratory phase exists to justify specification choices, and four of its findings matter downstream.

*Logs are the right scale.* The levels series span up to two orders of magnitude within-sample (B1 most dramatically), and their fluctuations scale with their level. Log transformation renders trends comparable across baskets and turns trajectory changes into growth-rate changes, which is the economically meaningful unit. Monthly growth is reported throughout as g = 100·Δln(Y), in **log-growth points (lgp)** — approximately percentage growth for small changes, but not identical, and never annualised unless labelled.

*Seasonality is strong and heterogeneous.* STL decompositions and month-of-year profiles show pronounced seasonal structure in all baskets — March fiscal-year-end effects most visibly — confirming that month fixed effects are essential. For B3 the STL seasonal-strength statistic is low, but this reflects a large irregular component rather than an absence of seasonality; the month-profile evidence still supports seasonal terms. Figure 2 shows the representative level/log/growth panel; Figure 3 shows the B3 STL decomposition, whose trend panel already displays the feature that dominates Section 8 — a smooth upward bend beginning around late 2021 rather than a kink at any single month.

*Autocorrelation is pervasive.* Log levels show slowly decaying ACFs; monthly growth shows negative low-order autocorrelation and seasonal structure. This motivates the three-layer inference strategy (HAC, ARMA errors, differenced-space companion) and, for forecasting, justifies admitting a seasonal ARIMA candidate.

*Stationarity evidence supports a differenced companion.* ADF and KPSS diagnostics provide evidence consistent with non-stationary log levels and broadly stationary monthly growth, although the evidence differs across baskets and should not be interpreted as establishing a common integration order. This licenses the growth-rate companion regression used in Section 8 — an independent check whose inference does not lean on HAC corrections in a trending series.

The exploratory phase also raised the concern that becomes the crux of the B3 analysis: several series, B3 most visibly, curve smoothly over the sample. A segmented-trend model confronted with smooth curvature will happily place a "trend break" wherever the segmentation says to look. The quadratic pre-trend check (R12) in Section 8 was pre-specified for exactly this reason. Remaining EDA panels and the full diagnostic table are in Appendix D.

## 7. Main ITS findings

Table 5 reports the baseline trajectory estimates; Figure 4 overlays the fitted segments on the actual series. The purpose of the table is to answer the central question in one row per basket: did the growth path change at the scheme date?

**Table 5. Baseline segmented ITS: change in post-implementation trajectory (β₃)**

| Basket | D_s | β₃ (lgp/month) | HAC(12) p | 95% CI (lgp/mo) | Immediate level shift β₂ (log points), p |
|---|---|---|---|---|---|
| B2 Pharma | 2022-04 | −0.13 | 0.379 | [−0.43, +0.16] | −7.5, p = 0.081 |
| B4 Textiles | 2024-04 | +0.05 | 0.829 | [−0.41, +0.51] | −0.5, p = 0.928 |
| B1 Mobile | 2020-08 | −2.92 | 0.148 | [−6.88, +1.04] | −56.2, p = 0.092 |
| B3 Air conditioners | 2022-04 | +0.87 | 0.0013 | [+0.34, +1.41] | +4.3, p = 0.424 |

For **pharmaceutical formulations and MMF textiles** the answer is plainly no: the estimated trajectory changes are economically negligible and statistically indistinguishable from zero. For B2 and B4, the overall verdict is unchanged by the robustness analysis: although some alternative specifications produce nominal significance (Sections 8.4–8.5), the evidence does not remain stable across the pre-specified checks. For B4 the short 24-month post-window limits power, so its null is read as "no detectable change" rather than "demonstrated absence of change."

For **mobile handsets** the point estimate suggests deceleration — growth was extraordinarily rapid before the scheme date and slower after — but the estimate is imprecise and not significant. Every B1 number carries the Section 4 caveat: 28 pre-policy months ending inside the COVID disruption leave the pre-trend, against which any change is measured, poorly determined. The classification-transition indicator barely moves the estimate (β₃ shifts by 0.65%), so the 2022 HS reallocation is not driving the B1 results. No substantive claim about B1's trajectory is made in this report, in either direction.

**Air conditioners** produce the sample's one tempting result: an estimated post-implementation steepening of +0.87 lgp per month — roughly ten log points a year added to the growth path (0.87 × 12) — with a HAC(12) p-value of 0.0013. Taken alone, this row would appear to be exactly what the study was looking for. It is not accepted as a finding, for reasons the next section documents in full: the estimate loses significance in the differenced-space companion regression and under a fixed AR(1) error structure; it is equally "significant" at every one of six candidate dates spanning two years, which is the opposite of evidence for a change timed to April 2022; and a quadratic pre-trend absorbs it entirely. AC exports exhibit a substantial acceleration in the observed series; its attribution to a dated trajectory break at the scheme's start does not survive scrutiny.

The section's conclusion is the report's central one. **Across four PLI-linked product groups, the analysis finds no robust evidence of a trajectory change specifically timed to PLI implementation over the study period; the results therefore do not establish either a positive or negative causal effect of the schemes on sector-level exports.** Full regression output, including all seasonal coefficients and both HAC lag choices, is in Appendix E.

## 8. Robustness and model diagnostics

This section is the evidentiary core of the report. The baseline estimates of Section 7 are only as credible as their error assumptions and their timing assumptions, and the pre-specified framework probes both. The progression runs: alternative error structures (8.1), differenced-space inference (8.2), COVID-window sensitivity (8.3), alternative dates (8.4), curvature (8.5), break diagnostics (8.6), comparison sectors (8.7), and residual diagnostics (8.8). Figure 5 — the B3 forest plot of β₃ across all specifications — compresses the section's message into one picture: the interval crosses zero in the specifications designed to be hardest to fool. Table 6 condenses the full 45-row robustness matrix (Appendix F).

**8.1 ARMA error structures.** Each baseline equation is re-estimated with the identical regressors but explicitly modelled ARMA errors, using a nine-model ARMA candidate set that was fixed before any ARMA result was inspected, after the originally broader computational grid proved impractical; model order was then selected by AIC, with a fixed AR(1) variant always reported alongside so that order selection never carries the result alone. (These p-values are maximum-likelihood z-based rather than HAC.) B2 and B4 remain null (p = 0.551, 0.769; B4's lowest-AIC candidate, an MA(1), failed to converge and was passed over for the converged next-best — disclosed rather than hidden). B1's deceleration estimate falls by roughly half and remains insignificant (−1.55, p = 0.387). B3 splits: the AIC-selected AR(2) keeps nominal significance (+0.85, p = 0.029), but the fixed AR(1) comparator does not (+0.88, p = 0.152). A result that depends on which stationary error structure absorbs the persistence is already fragile.

**8.2 The stationary growth companion.** The sharpest check re-poses the question in differenced space, where the trending-regressor inference problem disappears: regress monthly growth on a post-period shift, month effects, and COVID month dummies. Algebraically, the post-shift coefficient in this equation recovers the trajectory-change parameter — a correspondence verified exactly on synthetic data before use. In growth space, no basket shows a significant post-implementation shift; for B3 the estimate is +0.66 lgp with p = 0.61. The levels significance of B3 does not survive translation into differenced space, where inference no longer rests on HAC corrections applied to a trending regression.

**8.3 COVID window.** Dropping March–September 2020 leaves B2, B3 and B4 essentially unchanged (B3: +0.90, p = 0.0008 — its fragility lies elsewhere). B1's estimate becomes strongly negative and significant (−5.60, p < 0.001). Under the locked interpretation rule this variant result is reported but not promoted: it is one specification's verdict on a basket whose baseline is null and whose pre-window is the sample's weakest. The exclusion materially alters a relatively short B1 pre-period because the COVID episode overlaps its final months.

**8.4 Alternative intervention dates.** Every equation is re-estimated at every pre-registered alternative date. This is a robustness exercise on timing, not a formal placebo test — the dates are institutionally motivated candidates, not draws from a known null. For B2 and B4 the locked-date nulls stand, with isolated nominal significance at the notification dates only. For B1 the pattern is mixed — early dates produce significant deceleration, later dates nothing — which reinforces reading B1 as undetermined. The B3 result is the decisive one. At the locked April 2022 date, β₃ is positive and significant (p = 0.0013), while the five alternative dates spanning April 2021 to April 2023 also produce positive significant estimates (all p ≤ 0.0007; estimates +0.87 to +1.11 across the six dates). If AC exports had genuinely changed trajectory in April 2022, moving the assumed date a year in either direction should weaken the estimate; instead it is indifferent to timing. Date-invariance of this kind is what smooth acceleration looks like through a segmented-trend lens.

**8.5 Quadratic pre-trend (R12).** Adding a single quadratic term in time asks whether gentle curvature, present throughout the sample, explains what the segmented model attributes to a dated break. For B3 it does: β₃ flips to −1.13 (p = 0.215) while the curvature term is positive and significant (p = 0.026). The reason is structural rather than subtle — within this sample and specification, the dated trajectory-change parameter is highly collinear with smooth curvature (partial correlation 0.970 between the quadratic and TimeAfter terms), limiting the ability to distinguish the two. The same instability appears for B1 and B2, whose β₃ estimates also change sign under the quadratic. Under the quadratic specification, B2's β₃ changes sign and becomes nominally significant (+1.32, p = 0.0002); because this result is specification-dependent and reverses the baseline sign, it is treated as evidence of specification instability rather than as a substantive finding. B4 remains null with an insignificant curvature term. R12 does not prove the acceleration is smooth; it demonstrates that, within this sample, the data have very limited ability to distinguish a smooth path from a dated break, which suffices to withhold the break interpretation.

**8.6 Structural-break diagnostics.** Unknown-date break statistics (a sup-F scan and a two-break Bai–Perron segmentation) were run as corroborative diagnostics only. Their limitations are material: unknown-date tests on short, trending, seasonal series with many regressors are sensitive to trimming and candidate-set choices, and a detected break near a policy date would not establish a policy link any more than an absent one refutes it. Read at that weight, they corroborate Section 8.4-8.5: for B2, B3 and B4, neither method locates a break at the scheme date (B3's candidates fall in mid-2021 (supF) and 2018/late-2024 (segmentation), not April 2022). For B1 the sup-F scan peaks at October 2020, near the scheme date — noted, and given no more weight than the method can bear.

**8.7 Comparison sectors.** The three untreated sectors, estimated identically at each treated date, provide descriptive context. Their trajectory estimates are generally null, as expected. Two of nine descriptive control regressions were nominally significant at the 5% level, illustrating that individual nominal p-values should be interpreted cautiously in this design. That caution applies with particular force to the one headline p-value in this report, B3's 0.0013.

**8.8 Residual diagnostics.** Residual diagnostics (Ljung–Box and Breusch–Godfrey statistics on the baseline OLS residuals, with plots in Appendix E) confirm the serial dependence motivating the HAC and ARMA specifications; these diagnostics are treated as justification for the inference architecture rather than as evidence of a particular policy effect.

**The B3 diagnosis, stated once and plainly.** Air-conditioner exports accelerated — that is visible in the raw series and no part of the analysis disputes it. What the evidence does not support is the claim that the acceleration is a trajectory break dated to the scheme's implementation. The estimate fails the differenced-space companion (p = 0.61) and the fixed-AR(1) check (p = 0.152); it is indistinguishable across candidate dates spanning two years; and it is absorbed by smooth curvature that the sample cannot separate from a dated break. The acceleration appears to begin around late 2021 — before the scheme's first incremental-sales year — and to build gradually. Whether PLI contributed to it is a question this design cannot answer; what the design can and does show is that the evidence does not support a dated break at D_s.

## 9. Volatility analysis

The second half of the research question concerns volatility. Volatility here is defined on monthly log growth — the standard deviation of g = 100·Δln(Y), in lgp — compared across symmetric ±24-month windows around each scheme date, with the single growth observation that straddles the break date excluded from both windows. Statistical uncertainty is assessed with a moving-block bootstrap, which respects the serial dependence in monthly growth; a variant excluding the COVID months (March–September 2020) separates pandemic disruption from everything else. Table 8 reports the results; Figure 6 shows six-month rolling volatility across the sample with scheme dates marked.

**Table 8. Volatility of monthly log growth, ±24-month windows (lgp)**

| Basket | σ pre | σ post | Δσ | %Δσ | Δσ, COVID excluded | MBB 95% CI excludes 0? |
|---|---|---|---|---|---|---|
| B3 Air conditioners | 76.0 | 23.3 | **−52.7** | −69.3% | **+6.2** (+36.2%) | No |
| B1 Mobile | 61.1 | 37.0 | **−24.0** | −39.4% | **+1.1** (+2.9%) | No |
| B4 Textiles | 13.5 | 16.7 | +3.2 | +23.6% | +3.2 (unchanged) | No |
| B2 Pharma | 11.0 | 10.5 | −0.5 | −4.2% | −0.5 (−4.6%) | No |

Descriptively, the ranking is clear: air conditioners show by far the largest volatility change, mobile handsets the second largest, while pharmaceuticals and textiles barely move. Combined with Section 7, this identifies B3 as the basket with the largest positive estimated trajectory change and the largest descriptive volatility change; B1 carries the largest negative trajectory point estimate (−2.92 lgp/month, not significant) and the second-largest descriptive volatility change.

The two large declines do not survive inspection. Both B3's and B1's pre-windows contain the COVID months, when monthly growth swung violently; remove those months and B3's decline of 52.7 lgp becomes an *increase* of 6.2, while B1's decline of 24.0 becomes +1.1. The headline declines measure the passing of the pandemic out of the comparison window, not a post-policy stabilisation of exports. Consistent with this, no moving-block-bootstrap confidence interval excludes zero for any basket in any variant — baseline or COVID-excluded, straddle included or excluded, symmetric or full windows (full 32-row grid in Appendix G).

The section's conclusion: there is **no robust volatility finding**. The descriptive ranking answers the descriptive question of where volatility changed most; it does not show that any scheme stabilised — or destabilised — its sector's exports.

## 10. Exploratory historical counterfactual forecasting

A final, deliberately secondary exercise asks what each basket's exports would have looked like had the pre-policy pattern simply continued, and how far actual exports departed from that path. Its outputs are labelled throughout as **actual minus pre-policy time-series counterfactual** — univariate extrapolations that embed no economic structure, inherit every confounder the ITS could not separate, and carry no causal content. Nothing in this section can revise the conclusions of Sections 7–9.

The candidate set and primary model-selection framework were pre-specified in advance; the quantitative operationalisation of the simplicity tie-break was fixed after the raw RMSE comparison, and this sequencing is disclosed below. Candidate models — seasonal naïve, additive Holt-Winters ETS (damped and undamped), and a single pre-declared SARIMA(0,1,1)(0,1,1)[12] admitted on the seasonal-autocorrelation diagnostics, with no order search — were compared by expanding-origin validation entirely inside each pre-policy window (minimum training length 30 months). Selection required the lowest 12-step RMSE **subject to a hard eligibility condition**: pooled 95%-interval coverage within [0.85, 1.00]. Post-policy data played no role in selection, validation, or tuning.

**Table 9. Validation at h = 12 (RMSE on ln Y; ✗ = fails the coverage eligibility bound [0.85, 1.00])**

| Basket | Origins | snaive | ETS | ETS damped | SARIMA airline |
|---|---|---|---|---|---|
| B2 Pharma | 7 | **0.071** (0.953) | 0.167 (0.483 ✗) | 0.109 (0.779 ✗) | 0.173 (**0.839 ✗**) |
| B3 AC | 7 | 0.272 (0.953) | 0.623 (0.953) | 0.407 (0.953) | **0.265** (0.953) |
| B4 Textiles | 31 | 0.155 (0.984) | 0.399 (0.970) | **0.152** (0.982) | 0.319 (0.998) |

*Coverage figures (in parentheses) are pooled over forecast steps 1–12, not coverage specifically at h = 12.*

Seasonal naïve was selected for all four baskets, by three distinct routes. For **B1** it was imposed by the locked protocol: with 28 pre-policy months ending in the COVID period, validation is not meaningful, so B1 receives a benchmark-only counterfactual that is explicitly **not model-selected** and supports no claim. For **B2** seasonal naïve was the only candidate satisfying the coverage condition — all three alternatives fail it, SARIMA at 0.839 — and it also had the lowest RMSE outright. For **B3 and B4** the nominal RMSE winners (SARIMA and damped ETS, by 2.5% and 1.9%) triggered the design memo's pre-specified simplicity clause: where the winner's advantage over seasonal naïve is small relative to its spread across origins, prefer the simpler model. Operationalised as paired per-origin error comparisons, the winners' advantages are statistically indistinguishable from zero (paired t = 0.45 and 0.03), and seasonal naïve was retained. One disclosure belongs here rather than in a footnote: the simplicity **clause** was pre-specified, but its quantitative operationalisation (the t < 1 rule) was fixed only after the raw RMSE table had been seen. The rule can only ever move selection toward the benchmark, never toward a more flexible model, and the superseded raw-winner counterfactuals are retained in the results file (B3's, for instance, gives +21.4% rather than +23.2% at h = 12 — the same qualitative picture).

Two validation caveats bound the exercise. B2 and B3 have only **7** validation origins at the primary horizon — far too few to identify the best model with confidence, so their counterfactuals are exploratory by construction. **B4, with 31 origins, is the only well-validated case** and carries the exercise's real weight.

**Table 10. Cumulative gaps: actual minus pre-policy time-series counterfactual**

| Basket | h = 6 | h = 12 | h = 18 | Months outside 95% interval |
|---|---|---|---|---|
| B1 Mobile (benchmark only) | −2.6% | +23.2% | — | 0 of 12 |
| B2 Pharma | +2.6% | +2.6% | — | 0 of 12 |
| B3 AC | +37.4% | +23.2% | — | 0 of 12 |
| B4 Textiles | −7.1% | −2.2% | −1.9% | 0 of 18 |

The single most consequential row-level fact: **every actual observation lies inside the 95% counterfactual interval, in every basket, at every horizon.** No departure from the pre-policy pattern exceeds pre-policy forecast uncertainty. Reading the gaps individually: B2's actuals track their counterfactual almost exactly, consistent with its null throughout. B3's +23.2% was anticipated in writing before any gap was computed — its counterfactual extrapolates the pre-April-2022 trend, so the gap mechanically restates the smooth acceleration documented in Section 8.5 and adds no independent information. B1's +23.2% is reported for completeness and interpreted not at all: an unselected benchmark projected from a COVID-contaminated 28-month window, with intervals to match. B4 — the well-validated case, shown in Figure 7 — runs slightly *below* its counterfactual at both horizons, consistent with its ITS null. No significance test was performed on any gap, by design; large gaps here are not evidence of policy success, and small ones are not evidence of policy failure. Full validation grids and the remaining counterfactual figures are in Appendix H.

## 11. Limitations and identification boundaries

Each limitation below is stated in terms of what it prevents the analysis from concluding.

**No causal identification.** The design compares each sector's post-implementation path with its own pre-implementation pattern. Anything that changed around the same time — the global demand cycle, supply-chain reorientation toward India, input prices, the rupee — is absorbed into the same coefficients. The analysis therefore cannot attribute any observed change to PLI, and equally cannot attribute the absence of robust change to policy ineffectiveness: a genuine policy contribution offset by adverse global conditions, or one materialising with a lag beyond the sample, would look identical. The comparison sectors describe context; with one series per sector and common national shocks, they cannot carry a parallel-trends assumption, which is why no difference-in-differences contrast was estimated.

**Proxy measurement.** The baskets are HS-code aggregates, not beneficiary output. If scheme participants' exports moved sharply while non-participants' moved oppositely, sector-level series would show little — so the null constrains sector-level trajectories only, not firm-level responses.

**The B1 pre-period.** Twenty-eight pre-policy months, ending inside the pandemic, are imposed by the start of the official monthly series. They are too few, and too contaminated, to pin down the extraordinary pre-scheme growth trend against which any change must be measured. The honest statement about mobile handsets is that this design, on this data, cannot deliver a determination in either direction.

**The B3 curvature boundary.** Within this sample and specification, the dated trajectory-change parameter is highly collinear with smooth curvature (partial correlation 0.970), limiting the ability to distinguish the two. This is a boundary of the data, not of effort: no re-specification within a single-series design resolves a partial correlation of 0.97 between the competing terms. The report accordingly does not interpret B3's acceleration as evidence of a dated break at the scheme's implementation date — which is not a claim that it is unrelated to the policy environment.

**COVID and the volatility comparison.** The pandemic sits inside B1's and B3's pre-windows, and Section 9 shows it accounts for the entirety of their headline volatility declines. Any volatility comparison spanning 2020 measures the pandemic first and everything else second.

**Power at the sample's edge.** B4's 24 post-policy months limit the detectable effect size; its null is best read as "nothing detectable yet."

**Inference caveats.** Nominal p-values should be interpreted cautiously in this design (Section 8.7); the structural-break diagnostics carry the limitations stated in Section 8.6; and the forecasting exercise carries its origin-count and tie-break disclosures (Section 10).

**What a stronger design would require.** Causal identification would need firm-level data distinguishing scheme participants from non-participants within the same HS lines, or credible comparison units exposed to the same global shocks but not to the scheme — for instance, the same products exported by comparable countries. Both were outside this project's data perimeter. The single-series ITS deployed here is the appropriate tool for the question actually posed — whether trajectories changed around implementation — and the report claims nothing beyond it.

## 12. Conclusion

This project asked how the export trajectories and volatility of four PLI-linked product groups evolved around the implementation of their schemes, using 96 months of official trade data and a pre-specified segmented time-series design. The answer: **across four PLI-linked product groups, the analysis finds no robust evidence of a trajectory change specifically timed to PLI implementation over the study period; the results therefore do not establish either a positive or negative causal effect of the schemes on sector-level exports.**

Descriptively, B3 shows the largest positive estimated trajectory change and the largest descriptive volatility change among the four baskets, but neither change is attributable to PLI: the trajectory acceleration is smooth rather than dated, and the volatility decline reverses when COVID months are excluded. B1 carries the sample's largest negative trajectory point estimate, but it is imprecise and no directional reading is supported. Pharmaceuticals and textiles show essentially no post-implementation change on any measure; mobile handsets cannot be adjudicated on a pre-period constrained to 28 months by the start of the official monthly series and overlapped by COVID. This descriptive ranking identifies where the largest changes occurred; it is not a ranking of policy effects.

The project's durable contributions are methodological: a continuity-verified monthly HS-6 panel spanning two classification regimes, including the empirical detection and repair of the 2022 mobile-handset code reallocation; and a locked, pre-specified robustness framework — alternative error structures, differenced-space inference, alternative dates, curvature, and COVID sensitivity — applied without exception. That framework is what separates this report's conclusion from the one a single regression would have suggested: a naive reading of the baseline output would headline a highly significant AC-export acceleration at the scheme date; the framework shows that reading to be unsupported.

The null is an informative finding: the pre-specified framework did not identify a trajectory change that remained robust across alternative error structures, differenced-space inference, alternative dates and curvature specifications. Establishing whether the schemes are causally changing India's export performance will require firm-level beneficiary data or credible cross-country comparisons; at the sector level, over this period, the trade data do not yet tell that story.

---

## Appendices (separate from main text)

| Appendix | Contents |
|---|---|
| A | Full intervention-date registry with sources; source-log index (S01–S42) |
| B | Complete HS-6 code lists (B4, C1–C3); B1 transition-month evidence table; extraction protocol; dataset validation summary |
| C | Backward-extension feasibility investigation |
| D | Full EDA figure set and diagnostic table (levels/seasonality/STL/ACF-PACF per basket) |
| E | Full baseline regression output (all coefficients, OLS/HAC(3)/HAC(12) SEs); residual diagnostics |
| F | Full 45-row robustness matrix; ARMA AIC scan; grid-reduction disclosure (the Phase-5 baseline results were already known when the originally broader computational grid was reduced to the nine ARMA candidates, although no ARMA result had been inspected); forest plots for all baskets |
| G | Full volatility grid (32 rows: window schemes × COVID variants × straddle treatment) |
| H | Full forecast validation grid (all models × horizons); B1/B2 counterfactual figures |

*All appendix content exists as files in the project repository (`06_results/`, `07_figures/`, `02_policy_sources/`, `03_mapping/`, `08_report/`); the README maps each appendix to its files.*
