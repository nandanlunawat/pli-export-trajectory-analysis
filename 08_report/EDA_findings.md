# EDA Findings — Phase 4

**Date:** 30 August 2026
**Scope:** Diagnosis only. No ITS, forecasting, volatility inference, control or robustness model has been estimated.
**Binding constraint:** nothing here has altered — or may alter — a locked specification. Every finding below is recorded as a diagnostic or an interpretation caveat, never as grounds to re-specify.

Artefacts: `05_analysis/01_EDA.ipynb`, `05_analysis/eda_core.py`, `06_results/EDA_summary.csv` (244 rows, 9 blocks), `07_figures/` (22 figures).

---

## 1. What each series looks like

| | B1 Telephone sets | B2 Pharma formulations | B3 Air conditioners | B4 MMF fabrics |
|---|---|---|---|---|
| Range (US$ mn) | 26.65 → 3,166.91 | 990 → 2,735 | 0.86 → 53.79 | 9.23 → 119.97 |
| Max ÷ min | **118.8×** | 2.8× | 62.5× | 13.0× |
| Mean | 985.20 | 1,524.26 | 24.48 | 82.76 |
| SD of monthly log growth | 40.25 lgp | 11.43 lgp | 41.22 lgp | 29.75 lgp |
| Log-growth extremes | −206.5 / +101.8 lgp | −39.1 / +40.3 lgp | −275.8 / +222.2 lgp | −220.7 / +105.2 lgp |
| …as simple % change | −87.3% / +176.7% | −32.3% / +49.6% | −93.7% / +822.1% | −89.0% / +186.5% |

> **Notation.** `g_t = 100 × [ln(Y_t) − ln(Y_{t−1})]` is measured in **log-growth points (lgp)**, i.e. percentage points of log change. It is *not* a percentage growth rate. The two coincide only for small moves; for large ones they diverge sharply — B3's April-2020 value of **−275.8 lgp** corresponds to a simple change of **−93.7%**, and May-2020's **+222.2 lgp** to **+822%**. Throughout this document and all downstream analysis, "lgp" denotes log-growth points and percentage-growth language is reserved for actual percentage changes.
| STL trend strength | **0.925** | 0.860 | 0.634 | **0.249** |

**B1** is the dramatic series: a two-order-of-magnitude climb with the strongest trend in the panel (F_trend = 0.93). It is also the noisiest of the large series, and its early years are small enough that ordinary monthly lumpiness reads as large percentage moves.

**B2** is the calm one — a large, mature series moving in a 2.8× band with the lowest growth dispersion (11.4 lgp). It is the only basket that *rose* through the lockdown (May-2020: +22.6 lgp, a simple increase of about 25%), consistent with the essential-goods exemption already documented in memo §7.1.

**B3** is small in absolute terms and dominated by a single episode: April 2020 at 0.86 (**−275.8 lgp**, a simple fall of **−93.7%**) followed by **+222.2 lgp** in May (a simple rise of about **+822%**). Outside that, it trends up steadily.

**B4** is the flattest — trend strength 0.249, meaning most of its variation is not trend at all. It sits in a 60–120 band for almost the whole window, with the April 2020 collapse the only large excursion.

**Every series has its extreme log-growth months in April–May 2020**, except B2 whose largest moves are March/April 2025. That is the locked COVID block behaving exactly as anticipated.

---

## 2. Is seasonality evident? — Yes, and it is strong

| Basket | STL seasonal strength | March | April | Nov–Dec |
|---|---|---|---|---|
| B1 | **0.549** | +13.6 | **−64.7** | +48.1 / +41.0 |
| B2 | 0.323 | +9.1 | −4.8 | −4.8 / +7.4 |
| B3 | 0.015 | +15.3 | **−38.4** | +0.2 / +14.1 |
| B4 | 0.144 | +15.7 | **−25.8** | −10.4 / +10.6 |

*Log points ×100, deviation from own-year mean.*

**The Indian fiscal-year pattern is unmistakable: March high, April collapse.** All four baskets show a positive March and a negative April, and for B1 the April deficit is 65 log points. This is the fiscal-year-end loading the memo predicted in §5.4 — and it is the single strongest reason month fixed effects are not optional. B1's second-largest log-growth outlier is **April 2021 at −102.0 lgp** (a simple fall of about 64%), a pure seasonal event with no policy content.

**Two caveats on reading the seasonal profile.** First, for a fast-growing basket the deviation-from-own-year-mean measure mixes within-year *trend* into the seasonal estimate, which inflates B1's apparent late-year strength; STL's F_seasonal = 0.549 is the cleaner number.

**Second — and this must not be misread — B3's STL seasonal strength of 0.015 does NOT mean B3 has no seasonality.** The strength measure is a *ratio*: `F_seasonal = 1 − Var(remainder) / Var(seasonal + remainder)`. B3's remainder standard deviation is **33.4 lgp**, by far the largest in the panel, because the April-2020 shock and its May rebound dominate the decomposition even under robust STL. A large denominator drives the ratio toward zero regardless of how regular the seasonal component is.

**The recurring month-of-year pattern in B3 is plainly visible and consistent with the other baskets:** March **+15.3**, December **+14.1**, September **+9.2** against April **−38.4** and January **−13.0** log points. That is the same fiscal-year signature seen in B1, B2 and B4. The correct reading is *"seasonality is present and follows the fiscal-year pattern, but is small relative to B3's exceptionally large idiosyncratic variance"* — not *"B3 is non-seasonal"*. Month fixed effects remain fully justified for B3.

---

## 3. Is the log transformation appropriate? — Yes, with one honest qualification

| Basket | CV of levels | corr(annual SD, annual mean) of **levels** | corr(\|g\|, ln Y) |
|---|---|---|---|
| B1 | 0.887 | **+0.589** | −0.416 |
| B2 | 0.184 | +0.468 | +0.173 |
| B3 | 0.471 | **+0.826** | −0.568 |
| B4 | 0.206 | −0.470 | −0.826 |

**Supporting the log transform:** for B1, B2 and B3 the annual dispersion of the *level* rises with the annual mean (+0.47 to +0.83) — textbook proportional heteroskedasticity, which is exactly what logs are for. Add the 119× and 62× dynamic ranges of B1 and B3, the multiplicative seasonality in §2, and the fact that the analysis is about *rates* of change, and the case is straightforward.

**The qualification:** after logging, `|g|` is *negatively* correlated with the level for B1, B3 and B4. The log transform does not merely stabilise the variance — for these series it slightly over-corrects, leaving the small-scale early period proportionally **more** volatile. That is a property to carry into interpretation (§7 below), not a reason to abandon logs. Levels would be far worse.

---

## 4. Is autocorrelation present? — Yes in three of four baskets, and it is seasonal

**Log levels** are strongly persistent everywhere: ACF(1) of 0.53–0.89, ACF(12) of 0.14–0.58. Expected for trending monthly trade data.

**Monthly growth** — Ljung–Box p-values:

| Basket | ACF(1) of g | ACF(12) of g | LB(6) | LB(12) | LB(24) |
|---|---|---|---|---|---|
| B1 | −0.152 | **+0.512** | 0.537 | **0.0001** | **0.0001** |
| B2 | **−0.430** | **+0.300** | **0.0000** | **0.0000** | **0.0000** |
| B3 | **−0.351** | +0.139 | **0.0153** | **0.0356** | 0.234 |
| B4 | −0.218 | 0.161 | 0.134 | 0.164 | 0.314 |

*95% band ≈ ±0.201 on n = 95.*

Three patterns, all consequential:

1. **B1's autocorrelation is almost entirely at the seasonal horizon.** LB(6) is insignificant (p = 0.54) while LB(12) and LB(24) are p = 0.0001, and ACF(12) = +0.51. Short-lag dependence is negligible; twelve-month dependence is very strong.
2. **B2 has both**, with a large negative ACF(1) of −0.43 (month-to-month reversion) and significant seasonal structure.
3. **B4 shows no significant autocorrelation in growth at any horizon** — every Ljung–Box p exceeds 0.13.

**This directly validates the locked inference plan.** HAC standard errors are necessary, not decorative, and reporting at **both** lag 3 and lag 12 — which memo §5.5 pre-specifies — is exactly right: for B1 a lag-3 HAC would miss the entire dependence structure, which lives at lag 12. The ARMA-errors cross-check is likewise justified. Month fixed effects should absorb much of the ACF(12); whether they do is a residual diagnostic for the ITS phase, not something to pre-judge here.

---

## 5. Do stationarity results support the planned approach? — Yes

**Log levels** (ADF with constant+trend; KPSS matching; Zivot–Andrews break-aware):

| Basket | ADF p | KPSS p | ZA stat vs 5% crit −5.073 | ZA break | Reading |
|---|---|---|---|---|---|
| B1 | 0.285 | 0.100 | −4.252 | 2020-02 | evidence consistent with **I(1)-type behaviour** |
| B2 | 0.010 | 0.057 | −4.900 (p = 0.082) | 2021-03 | mixed; ADF leans trend-stationary, KPSS marginal |
| B3 | 0.000 | 0.079 | −8.461 | 2020-05 | evidence consistent with **trend-stationarity** |
| B4 | 0.000 | 0.100 | −6.775 | 2020-02 | evidence consistent with **trend-stationarity** |

**Growth** is consistent with stationarity essentially everywhere: ADF rejects the unit-root null for all four (p ≤ 0.016) and KPSS fails to reject the stationarity null for three of four.

**The single exception, and it is COVID.** B3's KPSS on growth rejects at p = 0.0417. Removing Mar–Sep 2020 moves it to **p = 0.100** — consistent with the rejection being driven by the April-2020 outlier rather than by genuine non-stationarity. The same test on B1 goes 0.100 → 0.052 (marginal); B2 and B4 stay at 0.100.

**A note on how strongly any of this can be claimed.** ADF, KPSS and Zivot–Andrews are tests with limited power on 96 observations, and no one of them establishes an integration order. Failing to reject a unit root is not proof of one; rejecting stationarity is not proof of integration. Everything below is phrased as *evidence consistent with* a characterisation, and the design's response is the same either way — report the levels ITS and the stationary growth companion side by side, and let their agreement or disagreement carry the weight.

**Three things follow, all of which the locked design already anticipated.**

*First, B1 is the one basket whose evidence is consistent with I(1)-type behaviour in levels* — ADF fails to reject at p = 0.28, and Zivot–Andrews still fails to reject even when a break in intercept and trend is allowed (−4.252 against a 5% critical value of −5.073). Two tests pointing the same way is suggestive, not decisive. But it is precisely the case memo §5.5 was written for: for B1 the growth-rate companion is not an optional extra, it is the specification carrying the inference. For B2, B3 and B4 the evidence is more consistent with trend-stationarity, so the levels ITS rests on firmer ground and the growth equation corroborates.

*Second, the Zivot–Andrews break dates land on COVID, not on policy.* B1 → 2020-02, B3 → 2020-05, B4 → 2020-02; only B2 → 2021-03 is elsewhere. **Not one coincides with its D_s** (2020-08, 2022-04, 2022-04, 2024-04). Memo §C.12 predicted exactly this — *"R9 will find COVID first"* — and pre-specified running Bai–Perron on the COVID-adjusted series and interpreting the second break. That prediction is now confirmed, before any structural-break test has been run for inference.

*Third, nothing here contradicts the planned approach.* Logs are appropriate, growth is stationary, month FE are required, HAC at two lags is justified, and the growth companion is essential for B1.

---

## 6. Data-integrity observations

- **No new data problems.** No gaps, no nulls, no non-positive values, no unexplained zeros. The validation report's 15/15 pass stands.
- **B1 Jan–May 2022 turbulence is visible in the data**, as the design anticipated: Dec-2021 777.5 → Jan-2022 536.1 (**−37.2 lgp**, −31.0% simple) → Feb 603.5 → Mar 813.7 (**+29.9 lgp**, +34.8%) → Apr 691.8 → May 448.4 (**−43.4 lgp**, −35.2%). The pre-specified `Transition_t` covers Jan–Apr 2022.
- **B3's April-2020 value of 0.86** is the panel minimum and the source of a **−275.8 / +222.2 lgp** pair (simple changes of −93.7% and +822%). It is genuine — air-conditioner exports effectively stopped during the lockdown — and it is positive, so the log specification is safe.

---

## 7. Issues that could weaken interpretation — none invalidates the locked design

Listed so they are on record **before** any estimation.

**7.1 — Volatility comparison is exposed to a level effect, over and above COVID.** SD of log growth (lgp) in the lowest third of levels versus the highest third:

| Basket | ratio (low ÷ high) | ratio excluding Mar–Sep 2020 |
|---|---|---|
| B1 | 2.31 | **1.52** |
| B2 | 0.75 | 0.76 |
| B3 | 3.90 | **0.91** |
| B4 | 4.54 | **1.36** |

For B3 the level effect is *entirely* COVID (3.90 → 0.91) and for B4 mostly so. **For B1 a residual 1.52× survives**: its low-level early years are about 50% more volatile in log terms than its high-level later years, for reasons unrelated to policy. Since B1's pre-period *is* its low-level era, σ_pre will be inflated relative to σ_post by a scale effect masquerading as a volatility change.

The locked design already mitigates this — symmetric ±24-month windows, Δσ reported with and without COVID, moving-block bootstrap CIs. **The mitigation is not complete**, and the residual must be stated in the final report as a limitation on the B1 volatility result specifically. It is not grounds to change the windows.

**7.2 — B4's trend strength is only 0.249.** Most of B4's variation is not trend. A trajectory-change coefficient estimated on a series with little trend to change will be imprecise. Compounded by B4 having just 24 post-intervention months, this reinforces its designated role as the **robustness** sector rather than a headline result — which is what the design already says.

**7.3 — B4 shows no significant autocorrelation in growth** (all Ljung–Box p > 0.13). Not a problem; it simply means the HAC correction will do little work for B4. Worth noting so that a near-identical HAC and OLS standard error for B4 is not later mistaken for an error.

**7.4 — B1's dependence is at lag 12, not at short lags.** Any inference on B1 that used only a short HAC lag would understate uncertainty badly. The pre-specified lag-12 report is essential here, not merely a robustness gesture.

**7.5 — Observation on the `Transition_t` window, recorded and deliberately not acted on.** May-2022 shows −43.4 lgp for B1, just outside the pre-specified Jan–Apr 2022 window. April is also B1's weakest month seasonally (−65 log points), so month FE should absorb much of both the April and May moves. **Extending the window because the data suggests it would be exactly the outcome-driven re-specification the design forbids.** The window stays as pre-registered. Recorded here so the decision is auditable.

---

## 8. Verdict

| Question | Answer |
|---|---|
| Seasonality evident? | **Yes — strong and fiscal-year driven.** March high, April collapse in all four baskets, B3 included. Month FE are essential. B3's low STL seasonal *strength* reflects its large idiosyncratic remainder, not an absence of seasonality. |
| Log transformation appropriate? | **Yes.** Proportional heteroskedasticity in levels for B1/B2/B3, 119× and 62× dynamic ranges, multiplicative seasonality. One qualification: logs slightly over-correct for B1/B3/B4, leaving early periods proportionally more volatile. |
| Autocorrelation present? | **Yes in B1, B2, B3; not detected in B4.** B1's is almost purely at lag 12. HAC at both lag 3 and lag 12 is justified; ARMA-errors cross-check is warranted. |
| Stationarity supports the plan? | **Yes.** Growth is consistent with stationarity throughout (the one exception is COVID-driven and resolves when Mar–Sep 2020 is removed). For B1 the evidence is consistent with I(1)-type behaviour in levels even when a break is allowed, which makes the growth companion essential for the primary endpoint. No single test establishes an integration order, and none is relied on alone. |
| Anything that invalidates the locked design? | **No.** Two interpretation caveats to carry forward: the residual level-dependence of B1's volatility (§7.1) and B4's weak trend (§7.2). Neither is a specification problem. |

**No specification has been altered. No model has been estimated.**

*End of Phase 4. The ITS estimation follows in `02_ITS_diagnostics.ipynb`.*
