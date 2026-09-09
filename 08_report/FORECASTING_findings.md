# Forecasting Findings — Limited Exploratory Phase

**Date:** 2 September 2026
**Scope:** the pre-planned counterfactual component only, executed under the locked protocol. Descriptive/exploratory throughout.
**Standing conclusion, not subject to revision here:** *no basket shows a trajectory change that survives the pre-specified robustness framework.*

Artefacts: `05_analysis/04_forecasting.ipynb`, `05_analysis/forecast_core.py`, `06_results/forecast_validation.csv`, `06_results/forecast_counterfactual.csv` (FINAL + raw-winner variants), `07_figures/fc_01_*_counterfactual.png` (4).

> **Binding label.** Every gap in this memo is **"actual minus pre-policy time-series counterfactual."** It is never a PLI effect, impact, treatment effect, or causal estimate. No significance test was performed on any gap.

---

## 1. Validation results (pre-policy data only)

Expanding-origin validation, minimum training window m = 30; candidates: seasonal naïve, ETS (additive, damped/undamped), and the single pre-declared SARIMA(0,1,1)(0,1,1)[12] airline model (admitted on the Phase-4 seasonal-autocorrelation diagnostics; no order search). RMSE/MAE on ln(Y); MAPE in %; coverage pooled over steps 1–12 across origins.

> **Mandatory disclosure: B2 and B3 have only 7 validation origins at h = 12.** Their model selection is weakly identified and their counterfactuals are exploratory. **B4, with 31 origins, is the only well-validated case** and the only basket where this exercise is a genuinely useful methodological demonstration.

| Basket | Model | Origins (h=12) | RMSE | MAE | MAPE | 95% coverage |
|---|---|---|---|---|---|---|
| **B2_PHARMA** | **snaive** | 7 | **0.0706** | 0.0565 | 0.78 | **0.953** |
| | ets_damped | 7 | 0.1094 | 0.0949 | 1.31 | 0.779 ✗ |
| | sarima_airline | 7 | 0.1725 | 0.1630 | 2.25 | 0.839 |
| | ets | 7 | 0.1673 | 0.1581 | 2.18 | 0.483 ✗ |
| **B3_AC** | sarima_airline | 7 | **0.2646** | 0.2374 | 7.88 | 0.953 |
| | **snaive** | 7 | 0.2715 | 0.2481 | 8.17 | 0.953 |
| | ets_damped | 7 | 0.4073 | 0.4041 | 13.28 | 0.953 |
| | ets | 7 | 0.6230 | 0.6207 | 20.47 | 0.953 |
| **B4_TEXTILE** | ets_damped | 31 | **0.1521** | 0.1320 | 2.94 | 0.982 |
| | **snaive** | 31 | 0.1550 | 0.1323 | 2.95 | 0.984 |
| | sarima_airline | 31 | 0.3185 | 0.2531 | 5.66 | 0.998 |
| | ets | 31 | 0.3987 | 0.3116 | 6.99 | 0.970 |

✗ = fails the locked coverage condition [0.85, 1.00].

## 2. Selected models

**Raw RMSE winners:** B2 → seasonal naïve (outright, by a wide margin); B3 → SARIMA-airline (by 2.5%); B4 → ETS-damped (by 1.9%).

**The locked tie-break clause then applies** (memo §4.5: where the winner's RMSE gap over seasonal naïve is small relative to its spread across origins, say so and **prefer the simpler model**). Operationalised mechanically — paired per-origin |12-step error| differences, prefer naïve if paired t < 1:

| Basket | Paired diff (naïve − winner) | t | Outcome |
|---|---|---|---|
| B3 | +0.0107 (SE 0.0238) | **0.45** | prefer seasonal naïve |
| B4 | +0.0002 (SE 0.0084) | **0.03** | prefer seasonal naïve |

> **FINAL SELECTION: seasonal naïve for all four baskets** — B1 by lock (benchmark only, **not model-selected**), B2 outright, B3 and B4 by tie-break. Post-policy data played no role at any point. Raw-winner counterfactuals for B3/B4 are retained in the CSV, flagged as superseded.

This is itself the most instructive validation result: **on these series, nothing in the candidate set detectably beats last-year's-same-month.** The fancier models either overfit the short windows (B2's ETS variants fail coverage badly) or match naïve within noise.

## 3. Counterfactual forecasts and descriptive gaps

Selected model frozen, trained on the full pre-policy window, projected past D_s. Gaps are **actual minus pre-policy time-series counterfactual**.

| Basket | Model | h=6 cum. gap | h=12 cum. gap | h=18 cum. gap | Months outside 95% PI |
|---|---|---|---|---|---|
| **B1_MOBILE** | snaive (**not model-selected**) | −2.6% | +23.2% | — | **0** of 12 |
| **B2_PHARMA** | snaive | +2.6% | +2.6% | — | **0** of 12 |
| **B3_AC** | snaive | +37.4% | +23.2% | — | **0** of 12 |
| **B4_TEXTILE** | snaive | −7.1% | −2.2% | −1.9% | **0** of 18 |

*(Raw winners, for transparency: B3 SARIMA +21.4% at h=12; B4 ETS-damped +8.9% — same qualitative picture, all months inside 95% PIs.)*

**The single most important row-level fact: every actual observation lies inside the 95% counterfactual interval, in every basket, at every horizon.** No gap anywhere exceeds pre-policy forecast uncertainty.

**Per basket:**

- **B1 (+23.2% at h=12).** Reported for completeness only. The benchmark projects a 28-month window that **ends inside the COVID-distorted period**, its intervals are correspondingly enormous, and the model was **not selected by validation**. **No substantive counterfactual claim is made for B1.**
- **B2 (+2.6%).** Pharmaceutical actuals hug the counterfactual — consistent with everything else known about B2.
- **B3 (+37.4% at h=6, +23.2% at h=12).** **As pre-stated before any gap was computed:** B3's training window ends March 2022, exactly where R12 locates the onset of smooth trend acceleration. This gap is therefore the *forecast-space restatement of the curvature already identified* — the counterfactual extrapolates the pre-2022 trend, the actuals follow the acceleration, and the difference is the acceleration itself. **It must not be treated as evidence of PLI impact**, and it is additionally inside the 95% interval throughout.
- **B4 (−2.2% at h=12, −1.9% at h=18).** The best-validated case shows actuals slightly **below** the counterfactual — MMF fabric exports ran a touch under their pre-policy seasonal pattern in the two years after the scheme's first performance year. Descriptive; within interval; consistent with the ITS null.

## 4. Limitations

1. **Weak selection for B2/B3** (7 origins) — disclosed above; their counterfactuals are exploratory by construction.
2. **B1 is excluded from inference entirely**: not model-selected, 28 pre-months, COVID-contaminated training tail.
3. **Seasonal-naïve intervals are wide** (they carry the full year-over-year variance, including COVID for B1), so "inside the 95% PI" is a weak test for B1 in particular — the statement cuts against over-reading gaps, not in favour of precision.
4. **The counterfactual inherits every confounder** the ITS could not separate: global demand, China+1, prices, the rupee. A gap of either sign bundles all of them with any policy contribution.
5. **B3's gap is mechanically entangled with the documented curvature** — see §3.
6. No gap was significance-tested, by design; interval non-exceedance is reported as description, not as a test result.

## 5. No causal identification — explicit statement

**This forecasting exercise provides no causal identification of any policy effect.** A large actual-minus-counterfactual gap (B3, B1) does not establish a PLI effect; a small or negative gap (B2, B4) does not prove PLI had no effect. The counterfactual is a univariate extrapolation of each series' own pre-policy pattern and embeds no economic structure. The standing conclusion of the project — **no basket shows a trajectory change that survives the pre-specified robustness framework** — is unchanged by, and cannot be overridden by, anything in this memo.

---

*End of the forecasting phase.*
