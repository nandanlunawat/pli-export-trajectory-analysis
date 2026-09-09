# ITS Preliminary Findings — Phase 5

**Date:** 30 August 2026
**Status:** **PRELIMINARY.** Baseline ITS, residual diagnostics, growth companion and the pre-specified B1 `Transition_t` robustness only.
**Not run:** forecasting, volatility inference, controls, the full robustness matrix, alternative break dates, Bai–Perron, ARMA-errors.
**Specification:** locked and unchanged. This phase implemented it; it did not revise it.

Artefacts: `05_analysis/02_ITS_diagnostics.ipynb`, `05_analysis/its_core.py`, `06_results/ITS_prelim_*.csv` (4 files), `07_figures/its_*.png` (13 figures).

**Units:** β coefficients are in log units per month; ×100 gives **log-growth points per month (lgp/mo)**. Simple percentage equivalents are given where useful and labelled as such.

---

## 1. Design matrix — verified against the lock before fitting

All four baskets pass every assertion: `Post` switches at D_s and not before; `TimeAfter = 0` at D_s and 1 the month after (the locked `max(0, T − T_Ds)` convention, **not** `+1`); `Break` fires once; `Covid` covers exactly 3 months; April is the omitted reference; n = 96.

| Basket | T_Ds | D_s |
|---|---|---|
| B1_MOBILE | 29 | 2020-08 |
| B2_PHARMA | 49 | 2022-04 |
| B3_AC | 49 | 2022-04 |
| B4_TEXTILE | 73 | 2024-04 |

---

## 2. Baseline ITS results

| Basket | β₁ (lgp/mo) | pre-trend %/yr | **β₃ (lgp/mo)** | post-trend %/yr | HAC(3) se | HAC(12) se | p (HAC12) | 95% CI (HAC12) |
|---|---|---|---|---|---|---|---|---|
| **B1_MOBILE** | +6.538 | +119.1 | **−2.921** | +54.3 | 1.944 | 2.020 | 0.148 | [−6.88, +1.04] |
| **B2_PHARMA** | +0.765 | +9.6 | **−0.134** | +7.9 | 0.127 | 0.152 | 0.379 | [−0.43, +0.16] |
| **B3_AC** | +0.934 | +11.9 | **+0.874** | +24.2 | 0.305 | 0.272 | **0.0013** | [+0.34, +1.41] |
| **B4_TEXTILE** | +0.170 | +2.1 | **+0.050** | +2.7 | 0.337 | 0.233 | 0.829 | [−0.41, +0.51] |

β₂ (immediate level shift): B1 −43.0% (p = 0.092), B2 −7.2% (p = 0.081), B3 +4.4% (p = 0.424), B4 −0.5% (p = 0.928). None significant at 5%.

**Read the point estimates before the p-values.** B1's pre-intervention trend is extraordinary — **+119% a year**. Its post-intervention trend is +54% a year. The point estimate says the trajectory **decelerated** by about 2.9 lgp/month, but the confidence interval spans zero comfortably. A sector growing at 119% annually was always going to decelerate; that is arithmetic, not policy.

B3 is the only β₃ that is significant in levels, roughly doubling the trend from +11.9%/yr to +24.2%/yr. **Section 4 shows this does not survive the stationary cross-check.**

---

## 3. Residual diagnostics — autocorrelation survives the month fixed effects

**Levels models:**

| Basket | LB(6) | LB(12) | LB(24) | BG(6) | BG(12) | Durbin–Watson | resid SD (log) |
|---|---|---|---|---|---|---|---|
| B1 | **0.0000** | **0.0003** | **0.0000** | **0.0003** | **0.0007** | 1.057 | 0.298 |
| B2 | 0.082 | 0.167 | 0.377 | 0.188 | 0.440 | 1.402 | 0.072 |
| B3 | **0.016** | **0.007** | 0.079 | **0.003** | **0.014** | 1.744 | 0.224 |
| B4 | **0.0007** | **0.0020** | **0.0001** | **0.0010** | **0.0025** | 1.471 | 0.164 |

**Residual autocorrelation is present in three of four baskets after month FE.** B1 is severe — Durbin–Watson 1.06 and every Ljung–Box and Breusch–Godfrey p below 0.001. Only B2's residuals look clean.

**This vindicates the locked inference plan and shows HAC is doing real work — in both directions:**

| Basket | OLS se on β₃ | HAC(3) | HAC(12) | HAC12 ÷ OLS |
|---|---|---|---|---|
| B1 | 0.00920 | 0.01944 | 0.02020 | **2.20×** |
| B2 | 0.00115 | 0.00127 | 0.00152 | 1.32× |
| B3 | 0.00360 | 0.00305 | 0.00272 | **0.76×** |
| B4 | 0.00552 | 0.00337 | 0.00233 | **0.42×** |

For B1, OLS would have **understated** the standard error by a factor of 2.2 — reporting OLS inference there would have been indefensible. For B3 and B4 HAC is *smaller* than OLS, a consequence of negative autocorrelation at some lags. Either way, OLS standard errors would have been wrong, which is exactly why the design pre-specified HAC at two lag lengths.

**Residual ADF** rejects a unit root in residuals for all four (p ≤ 0.039), consistent with the deterministic terms having absorbed the trend — but Engle–Granger critical values apply to residuals containing estimated parameters, so this is suggestive only, as the memo states.

---

## 4. The cross-check that matters — β₃ against α₁

The growth companion estimates the same quantity in stationary space. `Break` absorbs the differenced level jump, so α₁ is identified off `t ≥ T_Ds + 1`.

| Basket | β₃ (lgp/mo) | se | p | α₁ (lgp/mo) | se | p | Same sign? | se ratio |
|---|---|---|---|---|---|---|---|---|
| B1 | −2.921 | 2.020 | 0.148 | −4.148 | 6.226 | 0.505 | **YES** | 3.08× |
| B2 | −0.134 | 0.152 | 0.379 | +0.529 | 0.982 | 0.590 | no | 6.46× |
| B3 | **+0.874** | 0.272 | **0.0013** | +0.662 | 1.832 | 0.718 | **YES** | 6.73× |
| B4 | +0.050 | 0.233 | 0.829 | −1.272 | 1.748 | 0.467 | no | 7.50× |

**This is the single most important preliminary result, and it is a caution, not a finding.**

**B3's significance does not survive.** In levels, β₃ = +0.874 lgp/mo with p = 0.0013. In stationary space the point estimate is similar in sign and magnitude (+0.662 lgp/mo) but the standard error is **6.7× larger**, and p = 0.718. The two specifications agree about the *direction and rough size* of the effect and disagree completely about whether it can be distinguished from noise.

The levels specification produces standard errors 3–7.5× tighter than the growth specification for the same underlying quantity across all four baskets. That gap is the classic signature of a trending regressor delivering artificially precise inference. **On the evidence so far, no basket shows a trajectory change that is distinguishable from zero once inference is done in stationary space.**

Where β₃ and α₁ differ in sign (B2, B4), both are far from significant in both specifications, so the sign disagreement carries no information — it is noise around zero.

**Growth-model residuals** still show autocorrelation at seasonal lags for B1 (LB12 p = 0.0006), and Durbin–Watson values of 2.4–2.8 across the four indicate negative residual autocorrelation, the usual signature of differencing a series that is not a pure random walk. The pre-specified ARMA-errors cross-check in Phase 6 is therefore necessary, not optional.

---

## 5. B1 `Transition_t` robustness — pre-specified, and it passes cleanly

| Model | β₃ | HAC(12) se | p | β₂ | adj R² |
|---|---|---|---|---|---|
| Without `Transition_t` | −0.02921 | 0.02020 | 0.148 | −0.5623 | 0.9199 |
| With `Transition_t` | −0.02902 | 0.02023 | 0.152 | −0.5821 | 0.9194 |

`Transition_t` coefficient **+0.1268**, HAC(12) se 0.1167, **p = 0.278** — not distinguishable from zero.

**β₃ moves by +0.00019, which is 0.65% of the coefficient.** The Jan–Apr 2022 reclassification window has essentially no influence on B1's trajectory estimate. The union basket construction adopted under Change Proposal 001 has done its job: the two-stage HS2022 transition, which would have produced a 38–70% artefact in the original three-code basket, leaves no detectable trace in the fitted model.

This is a genuine vindication of the Phase-2 decision to widen the basket — and the robustness was declared before any estimate existed.

---

## 6. Issues for review before Phase 6

**6.1 — The levels/growth divergence is the headline methodological issue.** B3's only significant result vanishes in stationary space. Before any conclusion is drawn about B3, the pre-specified ARMA-errors cross-check must adjudicate. Do **not** report B3's β₃ as a finding on the strength of the levels model alone.

**6.2 — B1's residual autocorrelation is severe** (DW 1.06, all diagnostics p < 0.001). HAC handles the inference, but the ARMA-errors specification is likely to be the more credible number for B1, exactly as memo §5.5 anticipated.

**6.3 — β₂ is not cleanly interpretable for B1.** A −43% instantaneous level shift at D_s is not economically plausible for a trade flow. It most likely reflects the piecewise-linear form absorbing curvature in a series growing at 119%/yr, rather than a genuine discontinuity. The memo already warns that a large β₂ usually signals mis-specification or mis-dating rather than a policy response; that warning applies here.

**6.4 — No CV claim is yet supported.** These are preliminary estimates on one specification. The trajectory-change claim requires the robustness matrix, the controls and the stationary cross-check to agree. On present evidence the honest summary is: *point estimates suggest deceleration for B1 and acceleration for B3, neither distinguishable from zero once inference is done in stationary space.*

**6.5 — Nothing here justifies changing the design.** The locked specification produced exactly the diagnostics it was built to produce. The divergence between levels and growth inference is a *result*, not a defect, and the design anticipated it by requiring both.

---

*End of Phase 5. The robustness framework follows in `03_robustness_ITS.ipynb`.*
> No forecasting, no volatility inference, no controls, no full robustness matrix has been run.
