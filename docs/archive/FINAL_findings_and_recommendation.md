# Final Findings Memo — R12, Volatility, and the Forecasting Recommendation

**Date:** 2 September 2026
**Scope:** R12 quadratic pre-trend robustness (§1), the pre-registered volatility analysis (§2), the forecasting assessment (§3), updated methodology/limitations wording (§4), and the exact defensible interview interpretation (§5).
**Not run:** forecasting (awaits approval), DiD/stacked interactions, GARCH, any new specification. All locked components unchanged.

Artefacts this phase: `06_results/ITS_R12_quadratic_pretrend.csv`, `06_results/volatility_results.csv`, `07_figures/vol_01_rolling_sd_windows.png`, plus the reporting corrections applied to `ITS_robustness_findings.md`, `ITS_robustness_matrix.csv` (new `se_type` column) and `HOSTILE_METHODOLOGICAL_AUDIT.md` (n_eff and threshold language).

---

## §1 — R12: Quadratic pre-trend robustness

### 1.1 Specification

Exactly the locked baseline plus **one** term:

```
ln(Y_t) = b0 + b1·T + b1q·T² + b2·Post + b3·TimeAfter + Σ γ_m·Month_m + δ·Covid + ε
```

with T² = (T/100)² for conditioning. Same D_s, same COVID block, same month FE (April omitted), same HAC(3)/HAC(12). No other nonlinear specification was introduced. The question R12 was pre-specified to answer: *does β₃ survive when a smooth quadratic trend is allowed to compete with the piecewise-linear break?*

### 1.2 Results — β₃ in lgp/month, HAC(12) inference

| Basket | Baseline β₃ (p) | R12 β₃ (p) | R12 T² coefficient (p) | β₃ change |
|---|---|---|---|---|
| **B1** | −2.921 (0.148) | **+1.266 (0.430)** | −4.203 (**<0.0001**) | sign flips |
| **B2** | −0.134 (0.379) | +1.321 (0.0002) | −1.518 (**<0.0001**) | sign flips |
| **B3** | **+0.874 (0.0013)** | **−1.126 (0.215)** | +2.086 (**0.026**) | **sign flips; significance vanishes** |
| **B4** | +0.050 (0.829) | −0.896 (0.303) | +0.971 (0.230) | sign flips |

### 1.3 Reading

**The B3 curvature interpretation is decisively strengthened.** Allowing one smooth curvature term takes B3's β₃ from +0.874 (p = 0.0013) to −1.126 (p = 0.215): the significance does not merely weaken — the *sign reverses*, and the significance migrates to T² (+2.086, p = 0.026). The quadratic absorbs the acceleration entirely. Combined with the flat alternative-date profile and the companion's p = 0.718, three independent pre-specified checks now point at the same object: **a smooth trend acceleration, not a dated break.**

**The result generalises beyond B3.** β₃'s sign flips under the quadratic in all four baskets, and T² is strongly significant for B1 and B2 as well (B1's log series is smoothly *concave* — decelerating — which the quadratic captures where the hinge could not). The mechanical reason is measurable: the partial correlation between T² and TimeAfter, conditioning on all other regressors, is **0.970** for B3. On this window, a hinge at any plausible date and a gentle parabola are close to observationally equivalent. **β₃ and smooth curvature are not separately identified in this data.**

**Two disciplined notes.** First, B2's newly "significant" R12 β₃ (p = 0.0002) is **not a finding** — the interpretation rule applies symmetrically: significant in one specification, absent in the baseline, companion and ARMA set, atop a 0.97 collinearity, is non-robust by construction. Second, R12 does not *replace* the baseline; the locked levels ITS remains the primary specification. R12's role is diagnostic, and its diagnosis is that the dated-break parameter cannot be distinguished from curvature — which is a statement about what the data can identify, not about which model is "true".

**Consequence for the headline conclusion:** unchanged in direction, strengthened in confidence. No basket shows a robust policy-timed trajectory change, and for B3 the reason is now positively established rather than inferred.

---

## §2 — Pre-registered volatility analysis

### 2.1 What was run — the locked design, nothing else

`g_t = 100·Δln(Y_t)` in **log-growth points (lgp), not annualised**; symmetric **±24-month windows** around each D_s (primary) and full windows (secondary); σ_pre, σ_post, Δσ, %Δσ; 6-month rolling SD for visualisation (`vol_01_rolling_sd_windows.png`, windows shaded); **moving-block bootstrap** as the primary uncertainty procedure (block length 6, matching the rolling convention; 4,000 replications; fixed seed 20260902 — all declared); the pre-specified **COVID-excluded variant** (Mar–Sep 2020 removed); and the **break-straddling observation** g(D_s) identified and reported separately in every variant because it contains the β₂ level shift. No GARCH, no other volatility model, no significance search.

Break-straddling values: B1 **+55.1** lgp, B2 −13.2, B3 −26.3, B4 −25.5. Results below exclude it (the locked treatment); including it changes nothing material (`volatility_results.csv` holds all variants).

### 2.2 Primary results — symmetric ±24, straddle excluded

| Rank by \|Δσ\| | Basket | σ_pre | σ_post | **Δσ** | %Δσ | MBB 95% CI | CI excludes 0? |
|---|---|---|---|---|---|---|---|
| 1 | **B3_AC** | 75.98 | 23.31 | **−52.67** | −69.3% | [−66.0, +14.1] | no |
| 2 | **B1_MOBILE** | 61.09 | 37.04 | **−24.04** | −39.4% | [−47.4, +12.7] | no |
| 3 | **B4_TEXTILE** | 13.48 | 16.67 | **+3.19** | +23.6% | [−1.9, +8.7] | no |
| 4 | **B2_PHARMA** | 10.95 | 10.49 | **−0.46** | −4.2% | [−2.7, +2.9] | no |

*(n = 24 pre / 23 post per basket; units lgp per month.)*

### 2.3 The COVID-excluded variant is decisive for interpretation

| Basket | Δσ (baseline) | Δσ (ex Mar–Sep 2020) |
|---|---|---|
| B3 | −52.67 | **+6.20** |
| B1 | −24.04 | **+1.08** |
| B4 | +3.19 | +3.19 (COVID outside both windows) |
| B2 | −0.46 | −0.51 |

**The two large apparent volatility declines are entirely the COVID episode sitting inside the pre-windows.** B2/B3's symmetric pre-window *begins* in April 2020; B1's *ends* in July 2020. Remove Mar–Sep 2020 and B3's −69% becomes +36% (CI still spanning zero) and B1's −39% becomes +3%. The design predicted precisely this (memo §7.3; EDA §7.1), and the pre-registered variant exists precisely so the headline number cannot be quoted without its cause.

### 2.4 Honest summary of the volatility component

- **The pre-registered descriptive deliverable is complete**: a Δσ ranking with uncertainty — B3 largest absolute change, then B1, B4, B2 — which is what the frozen CV wording requires (§5).
- **No Δσ is distinguishable from zero** by the MBB CIs, in any window, any variant. There is no volatility *finding*, and none is claimed.
- **Sign fragility must travel with the ranking**: B1's and B3's Δσ flip sign under the COVID exclusion, so the ranking is of *magnitudes shaped substantially by where COVID falls relative to each scheme's date*. The EDA's level-dependence caveat (B1's low-level early months are ~1.5× more volatile ex-COVID) applies on top.
- Full windows (secondary) tell the same story with the same caveats.

---

## §3 — Forecasting: assessment and recommendation (NOT run)

### 3.1 The pre-policy facts, basket by basket

| Basket | N_pre | Validation origins at h=12 (m=30) | h=6 | h=18 | What is actually possible |
|---|---|---|---|---|---|
| B1 | 28 | 0 (−13) | 0 | 0 | **Seasonal-naïve benchmark only**, as locked — no model selection is possible; training window ends in the COVID collapse |
| B2 | 48 | **7** | 13 | 1 | Full protocol, weakly identified selection — 7-origin disclosure mandatory |
| B3 | 48 | **7** | 13 | 1 | Same — and its training window ends exactly where R12 shows the curvature beginning |
| B4 | 72 | **31** | 37 | 25 | The only well-validated case; h=18 pre-specified for B4 only |

### 3.2 Would it provide meaningful descriptive information?

**Modest, and uneven — with eyes open:**

- **B4 — yes.** 31 origins make model selection genuinely credible; the counterfactual (Apr 2024 onward) is a clean demonstration of the full rolling-origin protocol. This is the one basket where the exercise works as designed.
- **B2 — marginal.** Selection rests on 7 origins; the pharma series is calm, so the counterfactual band will likely contain the actuals and the gap will be small — an unspectacular but honest exhibit.
- **B3 — marginal, with a known hazard.** Any pre-policy model trains on data ending March 2022 — just where the smooth acceleration R12 identified takes hold. A large actual-minus-counterfactual gap is therefore *expected* and would restate the curvature finding in forecast form, not add evidence. If run, the write-up must say this in advance.
- **B1 — minimal.** A seasonal-naïve projection off a 28-month window ending in COVID will produce an enormous gap that invites exactly the over-reading the project has spent five phases preventing.

The gaps add no identification — they inherit every confounder the ITS already could not separate. What the exercise adds is (i) completion of a pre-registered component (dropping it *because* results are null would be outcome-driven in mirror image), and (ii) a demonstrated validation protocol, which has interview value under CV bullet 1.

### 3.3 Recommendation

**RUN ONLY AS EXPLORATORY**, exactly as locked: B2/B3/B4 through the full protocol (pre-policy-only selection; seasonal-naïve, ETS, SARIMA-if-justified; h=12 primary, h=6 secondary, h=18 for B4 only; the **7-origin disclosure attached to every B2/B3 output**); B1 as the **seasonal-naïve benchmark only, labelled "not model-selected"** everywhere it appears; every gap labelled *actual minus pre-policy time-series counterfactual* with **no causal interpretation**; and a pre-stated note that a large B3 gap is the expected signature of the already-documented curvature. If you prefer to skip it entirely, the defensible minimum is **B4 alone** (the only well-validated case) — but running the locked scope with the locked labels is the cleaner execution of the pre-registration. **Awaiting your approval either way; nothing has been run.**

---

## §4 — Updated methodology / limitations wording (for the final report)

**Methodology paragraph (drop-in):**

> Trajectories were analysed by segmented (interrupted) time-series regression on log monthly exports over April 2018–March 2026, with sector-specific intervention dates set ex ante at each scheme's first incentive period, month fixed effects, and a fixed April–June 2020 COVID control. Inference used Newey–West HAC standard errors at lags 3 and 12, cross-checked against SARIMAX error structures selected by AIC from a pre-declared nine-model grid. Identification of the trajectory-change parameter was stress-tested four pre-specified ways: a stationary log-growth companion that recovers the same estimand in differenced space; alternative intervention dates fixed in the design registry; a quadratic pre-trend alternative (R12); and structural-break diagnostics. Volatility was measured as the standard deviation of monthly log growth (log-growth points) over symmetric ±24-month windows, with moving-block bootstrap intervals, a COVID-excluded variant, and separate treatment of the break-straddling observation. Controls (leather goods, footwear, cotton woven fabrics) were estimated under the identical specification at each treated date as descriptive placebos; no causal contrast was computed.

**Limitations paragraph (drop-in):**

> Five limitations bound what this analysis can show. (1) The treated units are HS product-group proxies containing non-beneficiary output, which attenuates any policy effect toward zero; exports are gross values including re-exports, in nominal US dollars. (2) The panel begins in January 2018 because no official Indian source disseminates monthly HS-level data earlier — an external constraint that leaves the telephone-sets series 28 pre-policy months, three of them the COVID block. (3) Strong fiscal-year seasonality and serial dependence (residual AR(1) up to 0.45) substantially reduce the information available from the nominal 96 observations, so only large, sharply-timed trajectory changes were detectable. (4) The trajectory-change parameter is not separately identified from smooth trend curvature on this window (partial correlation with a quadratic term ≈ 0.97): the design can date a sharp break but cannot attribute a gradual acceleration. (5) COVID-19 overlaps the study period asymmetrically across intervention dates; every headline volatility change reverses or vanishes when March–September 2020 is excluded, and nominal significance arose in never-treated control series more often than expected, warranting caution about all nominal p-values. Pre-specified checks not run: true pre-policy placebo leads (largely infeasible around COVID), HS-4 re-aggregation, rupee-denominated, outlier-influence, and end-of-sample trims — none of which could plausibly rescue a positive finding from the observed nulls, but which remain undone.

---

## §5 — Exact defensible interview interpretation

**The one-paragraph answer to "what did you find?":**

> "Three things. First, the measurement result: official monthly HS-level series for PLI sectors break twice at the 2022 classification transition — the naive mobile-phone series shows a 70% artefact — and I built code-union baskets, verified against DGFT notifications and the data itself, that are continuous through it. Second, the descriptive result: telephone-set exports grew about 119% a year before the scheme's incentive date and 54% after — deceleration from an extreme base, as arithmetic requires; air-conditioner exports roughly doubled their trend growth, from about 12% to 24% a year, emerging smoothly through 2021–23. Third, the econometric result: no sector's trajectory change survives the pre-specified robustness set. The air-conditioner estimate is significant in the baseline, but it's equally significant at candidate dates two years apart, it disappears in stationary space, and when I allow a quadratic trend the significance migrates entirely to the curvature term — the break parameter and smooth curvature are 97% collinear here. For volatility, the largest swings — air conditioners at −69%, phones at −39% — reverse sign once COVID months are excluded, and no change is distinguishable from zero by block bootstrap. So I report a disciplined null with a defensible ranking, rather than a fragile positive."

**On the frozen CV bullets.** Bullet 1 is fully supported. Bullet 2 is now fully covered: trajectories were *evaluated* (Phases 5–6 + R12); the **trend ranking** is B3 strongest positive point estimate, B1 strongest negative, with CIs; the **volatility ranking** now exists — B3 largest |Δσ|, then B1, B4, B2 — with bootstrap intervals. Both rankings are descriptive: "strongest" means largest estimated change, never statistically significant policy effect.

**Never say:** "PLI effect/impact," "PLI caused," "trajectory changed after PLI" unqualified, "significant volatility change," or any sentence quoting B3's p = 0.0013 or the −69% volatility figure without, respectively, the curvature result and the COVID-exclusion reversal in the same breath.

---

## §6 — Status

R12: **run, reported** — curvature interpretation decisively strengthened. Volatility: **run, reported** — pre-registered descriptive component complete; CV volatility clause now covered; no significance claimed or found. Reporting corrections from the audit: **all six applied.** Forecasting: **assessed, not run — awaiting your decision** on the RUN-ONLY-AS-EXPLORATORY recommendation (full locked scope, or the B4-only minimum).

**Stopped.**
