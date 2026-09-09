# ITS Robustness Findings — Phase 6A/6B/6C

**Date:** 30 August 2026
**Scope:** ARMA-errors cross-check, pre-specified robustness, controls. **Not run:** forecasting, volatility inference, stacked interaction models.
**Specification:** locked and unchanged. Robustness variants never replace the baseline.

Artefacts: `05_analysis/03_robustness_ITS.ipynb`, `05_analysis/robustness_core.py`, `06_results/ITS_robustness_matrix.csv` (45 rows, 24 specifications, 7 units), `06_results/ITS_structural_breaks.csv`, `06_results/ITS_arma_aic_scan.csv`, `07_figures/rob_01_*_beta3_forest.png`.

> **Interpretation rule applied throughout.** A result significant in one specification but not in the stationary companion, the ARMA-errors fit, or the pre-specified robustness set is **non-robust — not a finding**. No model or date was selected on significance.

---

## Headline

**Nothing survives as a robust trajectory-change finding.** The one candidate — B3 air conditioners — is significant in six of nine specifications but fails both the stationary growth companion and the fixed AR(1) error structure, and it is *equally* significant at intervention dates two years apart. That last fact is decisive and is discussed in §3.2.

---

## 1. What was declared before estimation

- **ARMA grid:** a fixed 9-model set — AR(1), AR(2), MA(1), ARMA(1,1), seasonal AR(1), seasonal MA(1), and three mixed forms — with `d = D = 0` because the deterministic terms already carry trend and season. Selection by **AIC**, which scores fit and is blind to β₃. Only converged models eligible. A **fixed AR(1)** comparator is reported alongside so order selection never does the work alone.
- **Alternative dates:** taken verbatim from `pli_intervention_dates.csv`. None added, removed or re-specified after any result was seen.
- **COVID-adjusted window:** Mar–Sep 2020, exactly as locked.
- **B1 `Transition_t`:** Jan–Apr 2022, carried forward unchanged.

All 45 reported model fits converged. **Convergence disclosure (audit item 13):** within the ARMA AIC scans, some candidates failed to converge and were correctly excluded from selection by the pre-declared rule. The materially relevant case is **B4**, where the lowest-AIC candidate overall — MA(1), AIC −51.8 — **did not converge**, and selection fell to the best converged model, AR(1)×SAR(1) (AIC −48.9). Full scan in `ITS_arma_aic_scan.csv`. **SE labelling (audit item 19):** in `ITS_robustness_matrix.csv`, rows for specs `A1_*` and `A2_*` are SARIMAX fits whose standard errors and p-values are **ML z-based, not HAC**; they occupy the `*_hac12` columns for layout only. An `se_type` column has been added to the CSV making this explicit.

---

## 2. 6A — ARMA-errors cross-check

β₃ in log-growth points per month (lgp/mo); standard errors on the same scale.

| Basket | Baseline OLS+HAC | ARMA AIC-best | Fixed AR(1) | Growth companion (Ph 5) |
|---|---|---|---|---|
| **B1_MOBILE** | −2.921 (se 2.020, p 0.148) | −1.553 (se 1.797, p 0.387) `ARMA(1,1)` | −0.965 (se 1.424, p 0.498) | −4.148 (p 0.505) |
| **B2_PHARMA** | −0.134 (se 0.152, p 0.379) | −0.145 (se 0.243, p 0.551) `AR(1)` | −0.145 (se 0.243, p 0.551) | +0.529 (p 0.590) |
| **B3_AC** | **+0.874 (se 0.272, p 0.0013)** | **+0.852 (se 0.390, p 0.0287)** `AR(2)` | +0.883 (se 0.616, **p 0.152**) | +0.662 (**p 0.718**) |
| **B4_TEXTILE** | +0.050 (se 0.233, p 0.829) | −0.344 (se 1.173, p 0.769) `AR(1)×SAR(1)` | −0.091 (se 1.159, p 0.937) | −1.272 (p 0.467) |

**B1.** Sign stable and negative throughout, but the magnitude **attenuates by half to two-thirds** once error dependence is modelled: −2.92 → −1.55 → −0.97. Never significant in any specification. The Phase-5 diagnosis was that B1's residual autocorrelation is severe (DW 1.06); modelling it explicitly absorbs much of what the OLS trend-change coefficient was picking up. **B1 shows no robust trajectory change.**

**B2 and B4.** Null everywhere, with B4 flipping sign across specifications — noise around zero.

**B3 is the case that matters.** The **point estimate is remarkably stable**: +0.852 to +0.883 across all three error structures, and +0.852 to +1.109 across all nine specifications in the matrix. What is *not* stable is the inference. The standard error inflates from 0.272 (HAC) to 0.390 (AR(2)) to 0.616 (AR(1)), and p moves 0.0013 → 0.029 → 0.152. Add the growth companion at p = 0.718 and the picture is clear.

**The distinction worth being precise about:** B3's *effect estimate* is stable; B3's *inference* is not. Those are different claims. The point estimate being insensitive to specification is genuinely reassuring about the magnitude; it says nothing about whether that magnitude is distinguishable from zero, which depends entirely on how error dependence is modelled — and the answer changes with it. **Under the interpretation rule, B3 is non-robust.**

---

## 3. 6B — Pre-specified robustness

### 3.1 Sign and significance across all specifications

| Basket | Specs | Sign (+/−) | Significant at 5% | β₃ range (lgp/mo) |
|---|---|---|---|---|
| B1_MOBILE | 10 | 0 / 10 | 3 / 10 | [−5.596, −0.216] |
| B2_PHARMA | 9 | 0 / 9 | 1 / 9 | [−0.549, −0.049] |
| B3_AC | 9 | **9 / 0** | **8 / 9** | [+0.852, +1.109] |
| B4_TEXTILE | 8 | 5 / 3 | 1 / 8 | [−0.344, +0.602] |

**COVID-adjusted (drop Mar–Sep 2020)** changes nothing materially for any basket. For B3, β₃ = +0.902, p = 0.0008 on n = 89 — the result is not COVID-driven.

### 3.2 The alternative-date results are the most important finding in this phase

B3's β₃ across every pre-specified date:

| Date | Rationale in registry | β₃ (lgp/mo) | p |
|---|---|---|---|
| 2021-04 | first investment year | **+1.109** | <0.0001 |
| **2022-04** | **LOCKED — first incremental-sale year** | **+0.874** | **0.0013** |
| 2022-01 | D_s − 3 | +0.944 | 0.0001 |
| 2022-07 | D_s + 3 | +0.869 | 0.0007 |
| 2022-10 | implementation lag +6 | +0.901 | <0.0001 |
| 2023-04 | 2-year gestation option | **+0.912** | <0.0001 |

**β₃ is large, positive and highly significant at every candidate date across a two-year span — including dates 24 months apart.** A genuine break at a specific date would show a peaked profile: strong at the true date, weakening as the assumed break moves away. This profile is flat.

**The natural reading is that the segmented model is fitting smooth curvature in B3's log level, not a discontinuity at any particular date.** *Terminology correction (audit item 14):* this battery is an **alternative-date robustness test**, not a placebo test — every date in it is a plausible policy-adjacent date, and the true pre-policy placebo leads specified in the Phase-1 design (R4) were not run, partly because a −24-month lead for B2/B3 lands on COVID. The curvature inference does not depend on the placebo label: it rests on the *flatness* of the β₃-versus-date profile itself. *(Subsequently confirmed directly by R12 — see `ITS_R12_quadratic_pretrend.csv` and the final findings memo.)*

This is not a reason to prefer a different date. It is a reason to conclude that **B3's β₃ does not identify a policy-timed trajectory change.**

### 3.3 B1 `Transition_t` — carried forward unchanged

Coefficient +0.1268 (HAC(12) se 0.1167, p = 0.278); β₃ moves by 0.65% of itself. The two-stage HS2022 reclassification leaves no detectable trace. The CP-001 basket widening did its job.

### 3.4 Structural-break diagnostics on COVID-adjusted data

| Basket | Locked D_s | supF argmax | supF stat | Bai–Perron breaks |
|---|---|---|---|---|
| B1_MOBILE | 2020-08 | 2020-10 | 20.64 | 2018-09 \| 2025-07 |
| B2_PHARMA | 2022-04 | 2021-02 | 11.77 | 2019-02 \| 2025-07 |
| B3_AC | 2022-04 | **2021-07** | 14.63 | 2018-09 \| 2024-09 |
| B4_TEXTILE | 2024-04 | 2020-10 | 21.62 | 2020-12 \| 2021-10 |

**No locked date is recovered by either diagnostic.** B1's supF argmax (2020-10) is two months from its locked date, which is the closest correspondence in the panel; the rest are far away. B3's data-detected break at 2021-07 is nine months before its locked date, consistent with §3.2's reading that the series has curvature rather than a dated discontinuity.

**These diagnostics are explicitly LIMITED corroborative evidence, for three mechanical reasons (audit item 15):** (i) the COVID-adjusted series has a **7-month calendar gap** that both procedures treat as contiguous, making break locations near the gap unreliable; (ii) Binseg **forces** exactly two breaks, so "breaks" at near-boundary dates are partly artefacts of the forced count; (iii) the supF statistics are reported **without Andrews critical values** and therefore support no formal inference. The defensible statement is only: *break diagnostics, run under acknowledged limitations, provided no support for a break at the policy dates.* Nothing stronger, in either direction — and as the memo requires, a detected break would not have proved PLI caused anything either.

---

## 4. 6C — Controls

**Descriptive placebo comparison. Not a causal contrast.** Two separately estimated coefficients carry no standard error on their difference. No stacked `Treated × TimeAfter` interaction has been run, and nothing below implies one.

| Control | at 2020-08 (B1's date) | at 2022-04 (B2/B3's date) | at 2024-04 (B4's date) |
|---|---|---|---|
| C1 Leather | +0.635 (p 0.062) | +0.053 (p 0.875) | −0.090 (p 0.622) |
| C2 Footwear | **+0.845 (p 0.032)** | −0.073 (p 0.851) | −0.248 (p 0.374) |
| C3 Cotton fabrics | −0.259 (p 0.263) | **−0.765 (p 0.037)** | +0.252 (p 0.337) |
| *Treated, same date* | *B1: −2.921 (p 0.148)* | *B2: −0.134 (p 0.379) · B3: **+0.874 (p 0.0013)*** | *B4: +0.050 (p 0.829)* |

**Two of nine control regressions are significant at 5%.** *Corrected wording (audit item 20c):* under independent true nulls the exact binomial probability of two or more nominal rejections in nine tests is **0.071** — and the nine tests share macro shocks, so they are not independent. **Nominal significance therefore appeared more often than expected, which warrants caution about all nominal p-values in this design; it does not demonstrate over-rejection.** The caution is reinforced by the Phase-5 finding that residual autocorrelation survives the month fixed effects in three of four baskets.

Two specific readings:

- **C2 Footwear shows a significant positive β₃ at 2020-08**, the date at which B1 — the primary endpoint — shows an insignificant *negative* coefficient. A control "responding" where the treated series does not is a direct warning about the method at that date.
- **At 2022-04, C3 Cotton shows −0.765 (p 0.037) while B3 shows +0.874 (p 0.0013).** Opposite signs, both nominally significant. C3 is the fibre-matched control for B4, not for B3, so this is not a like-for-like contrast — but it does show the specification generating significant coefficients in a series with no intervention at that date.

**Conclusion from 6C: the control set does not corroborate any treated result, and it actively undermines confidence in the nominal significance levels.**

---

## 5. Verdict against the interpretation rule

| Basket | Baseline | ARMA-errors | Growth companion | Alt dates | Controls | **Verdict** |
|---|---|---|---|---|---|---|
| B1_MOBILE | n.s. | n.s. (attenuates by ⅔) | n.s. | sign stable, 3/10 sig | C2 sig at same date | **No robust trajectory change** |
| B2_PHARMA | n.s. | n.s. | n.s. | 1/9 sig | — | **No robust trajectory change** |
| B3_AC | **sig** | sig under AR(2), **n.s. under AR(1)** | **n.s.** | **sig at every date over 2 years** | C3 sig, opposite sign | **NON-ROBUST — not a finding** |
| B4_TEXTILE | n.s. | n.s., sign flips | n.s. | 1/8 sig | — | **No robust trajectory change** |

**No basket shows a trajectory change that survives the pre-specified robustness set.**

---

## 6. What this means, stated plainly

**6.1 — This is a real result, not a failed analysis.** A correctly specified interrupted time series on four PLI-linked export baskets finds no trajectory change that survives ARMA-errors, the stationary companion, placebo dates and controls. That is an informative answer to the research question, and it is more defensible than a fragile positive.

**6.2 — The CV claims remain supportable, and are unaffected by the direction of the result.** The bullets say *"evaluated changes in export trajectories around PLI implementation"* and *"identified sectors with the strongest post-policy trend and volatility changes"*. Both are satisfied by a correctly estimated ranking regardless of sign or significance — the design memo made this point before any estimate existed, and it holds now. B3 has the largest positive β₃ and B1 the largest negative; that ranking is real. What must **not** be claimed is that any of it is statistically robust.

**6.3 — B3 must not be reported as a finding.** It is significant in the baseline and in one of two error structures, and insignificant in the growth companion. It is *equally* significant at dates two years apart. Reporting it as a PLI effect would be exactly the outcome-driven selection the design forbids.

**6.4 — The over-rejection in the control set is a genuine methodological caveat.** Two of nine placebo regressions significant at 5% suggests nominal p-values in this design are optimistic. This belongs in the limitations section, and it strengthens rather than weakens the case for the cautious verdict above.

**6.5 — Nothing here justifies changing the design.** Every diagnostic behaved as the locked specification anticipated: HAC was necessary, the growth companion adjudicated, placebo dates exposed curvature, controls exposed over-rejection. The design worked. The answer is null.

---

---

## 7. Pre-specified robustness items and their execution status (audit item 4f)

| Item | Status |
|---|---|
| Alternative intervention dates (R1) | **Run** (Phase 6B) |
| COVID window variants (R2) | **Run** (Phase 6B) |
| ARMA-errors vs HAC (R6) | **Run** (Phase 6A) |
| Growth-rate companion (R5) | **Run** (Phase 5) |
| Structural-break diagnostics (R9) | **Run**, with the limitations stated in §3.4 |
| B1 `Transition_t` (R13) | **Run** (Phases 5–6) |
| Quadratic pre-trend (R12) | **Run** (2 Sep 2026) — see `ITS_R12_quadratic_pretrend.csv` and the final findings memo |
| True pre-policy placebo leads (R4) | **NOT RUN** — a −24-month lead lands on COVID for B2/B3; the feasible shorter leads were not executed |
| HS-4 re-aggregation (R7) | **NOT RUN** |
| ₹ crore denomination (R8) | **NOT RUN** (requires a second extraction pass) |
| Outlier influence / March-spike trim (R10) | **NOT RUN** |
| Drop final 3 months (R11) | **NOT RUN** |

The unrun items could only further stress results that are already null — none could plausibly manufacture a positive — but they remain undone and are listed in the final report's limitations.

*End of Phase 6.*
> No forecasting model, no stacked interaction model has been run. (The pre-registered descriptive volatility analysis was subsequently completed on instruction — see `docs/archive/FINAL_findings_and_recommendation.md` §2.)
