# Hostile Methodological Audit — Phases 1–6

**Date:** 2 September 2026
**Basis:** the actual files — code (`its_core.py`, `robustness_core.py`, `eda_core.py`), notebooks, `master_monthly_exports.csv`, the locked memo, the decision log, and every Phase 4–6 output CSV. Mechanical claims below were **re-verified by re-execution**, including a by-hand reproduction of the Newey–West covariance and a synthetic-data identity test of the growth companion. Nothing was modified; no new model was run. This document is the only file created.

---

## 1. FULL IMPLEMENTATION AUDIT

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | Data sample & monthly continuity | **NO ISSUE** | Re-checked: 672 rows, 96 months × 7 baskets, no gaps, no duplicates. |
| 2 | Basket construction & HS mapping | **NO ISSUE** | B1 `codes_summed` = the five locked codes; C1/C2/C3 = 20/25/70 codes matching `control_hs6_codes.csv`; prefix logic cannot leak across chapters at HS-6. |
| 3 | Intervention dates | **NO ISSUE** | `its_core.D_S` re-checked against `pli_intervention_dates.csv` programmatically: identical. |
| 4 | TimeAfter definition | **NO ISSUE** | `max(0, T − T_Ds)`; re-verified TimeAfter = 0 at D_s, 1 at D_s+1. |
| 5 | Post indicator | **NO ISSUE** | 0 at D_s−1, 1 at D_s. |
| 6 | Month FE / omitted month | **NO ISSUE** | 11 dummies, `M04` absent (April reference), as locked. |
| 7 | COVID treatment | **NO ISSUE** | Levels: Apr–Jun 2020 block (3 months). Growth: four month-specific dummies incl. Jul 2020. Robustness drop: Mar–Sep 2020 (n = 89). All as locked. |
| 8 | B1 Transition_t | **NO ISSUE** | Jan–Apr 2022, 4 months, B1 only; carried into 6B unchanged. |
| 9 | Log-level specification | **NO ISSUE** | `ln(export_usd_mn)`; all inputs strictly positive (min 0.86). |
| 10 | Stationary growth companion | **NO ISSUE** | **Verified by synthetic-data identity test**: on a constructed piecewise-linear log series with β₃ = 1.5 lgp/mo and β₂ = 0.5, the companion returns α₁ = 1.500000 exactly, with `Break` absorbing the T_Ds jump. The specification is algebraically correct, not merely plausible. |
| 11 | HAC(3) and HAC(12) | **NO ISSUE** | `cov_type="HAC"`, Bartlett kernel, `use_correction=True`. **Reproduced by hand**: manual Newey–West(12) SE on B2's β₃ matches statsmodels to <1e-6. |
| 12 | ARMA-error specifications | **NO ISSUE** | Same exog matrix, d = D = 0 (deterministics carry trend/season), `trend="c"` with no duplicated constant, stationarity/invertibility enforced. |
| 13 | ARMA AIC selection | **MINOR REPORTING ISSUE** | Selection rule (lowest AIC among **converged** models) worked as designed, but for **B4 the lowest-AIC model overall — MA(1), AIC −51.8 — failed to converge** and selection correctly fell to AR(1)×SAR(1) (AIC −48.9). This is only visible in `ITS_arma_aic_scan.csv`; the findings doc does not disclose it. Disclose it. Also: the 9-model grid was fixed *after* Phase-5 baseline results were known (though before any ARMA result existed). AIC is blind to β₃ and the fixed-AR(1) comparator limits the risk, but the sequencing should be stated. |
| 14 | Alternative-date tests | **MINOR REPORTING ISSUE** | All 19 dates verified verbatim against the registry; none added or dropped post hoc. **But** the findings doc calls this battery a "placebo test". Strictly it is not: every alternative date is a *plausible policy-adjacent date*, not a pre-policy placebo. The **true placebo leads the Phase-1 design specified (R4: longest feasible lead, e.g. 2019-08 for B1) were never run** — partly because for B2/B3 a −24-month lead lands on COVID. The *curvature* inference (§3.2 of the findings) does not depend on the placebo label and survives; the label should be corrected. |
| 15 | Structural-break diagnostics | **MATERIAL METHODOLOGICAL ISSUE** *(as evidence — correctly not leaned on)* | Three defects: (i) `drop_covid` leaves a **7-month calendar gap**, and both supF and Binseg treat the spliced series as contiguous — break-location estimates near the gap are unreliable; (ii) Binseg **forces** `n_bkps=2`, so "breaks" at 2018-09/2025-07 are largely artefacts of forcing breaks onto near-trendless residuals; (iii) supF statistics (11.8–21.6) are reported **without Andrews critical values**, so they support no formal inference. The findings doc already treats these as "corroboration that failed to arrive," which is the right weight — but the mechanical weaknesses mean they could not have corroborated much even if the dates had matched. Classify the *diagnostics* as weak; the *use made of them* as acceptable. |
| 16 | Control-basket regressions | **NO ISSUE** | 9 rows (3 controls × 3 dates), identical specification, labelled descriptive-only. |
| 17 | Sample sizes after exclusions | **NO ISSUE** | 96 (full), 95 (growth), 89 (COVID-dropped) — all as expected. |
| 18 | Missing values / zeros | **NO ISSUE** | No nulls; minimum 0.86 > 0; `851712`'s post-2022 zeros live inside a positive union. |
| 19 | SE / p-value computation | **MINOR REPORTING ISSUE** | OLS+HAC rows: verified correct. **ARMA rows store ML z-based SEs and p-values in columns named `*_se_hac12` / `*_p_hac12`** in `ITS_robustness_matrix.csv`. The values are correct; the column names are wrong for those rows. Anyone reading the CSV cold would mislabel the ARMA inference. Rename or footnote. |
| 20 | Inadvertent outcome-driven choices | **MINOR REPORTING ISSUE** (two disclosures; one overstatement to correct) | (a) ARMA grid reduced 36→9 after a timeout; the timed-out run printed no coefficients, so the reduction was β-blind, but Phase-5 results were known — disclose. (b) The Phase-6 scope (6A–6C) leaves pre-specified robustness items **R4 (placebo leads), R7 (HS-4 aggregation), R8 (INR), R10 (outlier influence), R11 (drop last 3 months), R12 (quadratic pre-trend)** unexecuted. Since the verdict is already null, the unrun items could only stress it further — no positive was manufactured — but the final report must list them as not run, and R12 bears directly on the curvature diagnosis. (c) **One overstatement in my own Phase-6 findings**: "the method is over-rejecting" from 2-of-9 significant controls. Exact binomial: P(≥2 of 9 at α=0.05) = **0.071** under independence — elevated, not damning. The correct wording: *more nominal significance than expected, short of demonstrating over-rejection.* |

**No DESIGN CHANGE REQUIRED items.** The locked design was implemented faithfully; every mechanical spot-check reproduced.

---

## 2. SAMPLE-SIZE ASSESSMENT — FOR THIS DESIGN, NOT A RULE OF THUMB

Serial dependence in the baseline residuals, measured directly (AR(1) coefficient ρ₁), with a **heuristic** indication of how much it erodes information. *(Corrected per review: the n_eff figures below are the standard n(1−ρ)/(1+ρ) heuristic for the variance of a mean under AR(1) dependence — an* **indication that serial dependence reduces effective information relative to the nominal 96 observations**, *not an actual sample size, and not exact for trend-change estimands.)*

| Basket | n | residual ρ₁ | Dependence erosion (heuristic) | Pre-segment length |
|---|---|---|---|---|
| B1 | 96 | +0.448 | severe (~⅓ of nominal, heuristically) | 28 months (2.3 years) |
| B2 | 96 | +0.287 | moderate | 48 months (4.0 years) |
| B3 | 96 | +0.107 | mild | 48 months (4.0 years) |
| B4 | 96 | +0.253 | moderate | 72 months (6.0 years) |

**A. Is 96 months adequate for ITS?** Yes, for this design — argued from the segments themselves rather than from any citation-free universal threshold. *(Corrected per review: the earlier "≥12/≥24 points per segment" phrasing implied an academic standard without a verified source; it is withdrawn.)* The concrete facts are: the shortest segment (B4 post) holds 24 observations — two complete seasonal cycles — against 16 parameters, most of which (the 11 month effects and the pre-trend) are identified primarily from the other, longer segment; every fitted model is well-conditioned and converged; and the resulting confidence intervals are wide but usable. Adequacy for *fitting* is not adequacy for *powered inference*: with this much seasonality and dependence, the design detects only large trajectory changes, which is consistent with the wide CIs observed (B1's β₃ CI spans ±4 lgp/mo).

**B. B1's 28-month pre-period: BORDERLINE, leaning weak — usable for description, weak for inference.** The argument is the segment arithmetic, not a threshold: net of month fixed effects, a trend is identified from across-year contrasts, and B1's pre-segment contains barely more than two annual cycles — roughly two observations per calendar month — with three of its 28 months being the COVID block (so δ rests on 3 observations). Nothing about the estimate is invalid; its precision is simply low, and that is visible in the output rather than hidden. Two things keep it acceptable: the design *declared* the weakness in advance, and the post-segment (68 months) is strong, so the fitted post-trend is well identified even if the pre/post *contrast* is not.

**C. B2/B3 at 48/48: yes, reasonably informative.** Four full seasonal cycles per segment is a genuinely balanced monthly ITS. B3's clean residuals (ρ₁ = 0.11, n_eff ≈ 77) make it the best-conditioned series in the panel — which sharpens, rather than blunts, the §5 conclusion that its result still fails robustness.

**D. Does seasonality reduce effective information? Materially, yes.** Eleven of ~16 parameters are month effects. The trend within a segment is identified from across-year variation only: B1's pre-segment effectively compares ~2 observations per calendar month. For B2/B3 (4 per month) the cost is real but tolerable. This is the price of the (correct) decision not to pre-filter seasonally.

**E. Does serial dependence reduce effective information? Materially, yes, and unevenly.** The direct evidence is the residual dependence itself (ρ₁ from +0.11 for B3 to +0.45 for B1) and its consequence for inference: B1's HAC(12) SE is 2.2× its OLS SE. Heuristically the dependence erosion is severe for B1 and mild for B3, but no single number should be quoted as "the" effective sample size. This is exactly why HAC and ARMA-errors were pre-specified — the design pays for dependence honestly instead of ignoring it.

**F. Is the design appropriately cautious given these constraints? Yes.** Two-lag HAC, a stationary companion with an exact algebraic identity to β₃, ARMA cross-checks with a fixed comparator, pre-registered dates, and a binding non-robustness rule — the caution is structural, not rhetorical. If anything the caution is *asymmetric in the right direction*: every discretionary call (companion adjudication, AR(1) vs AR(2), curvature reading) was resolved against finding an effect.

**Is the short sample a legitimate data limitation?** Yes, and it is now *documented as irreducible*: MEIDB begins January 2018 (verified directly), EIDB is annual, FTPA is PC-group cumulative. January 2018 is where official Indian monthly HS dissemination starts. That is a property of the dissemination system, established by direct query of all three portals, not a window this project chose.

---

## 3. AUDIT OF THE CENTRAL ECONOMETRIC LOGIC

**Is ITS the correct central framework?** Yes. The research question is literally "did the trajectory change around a known date" for a single treated aggregate with no credible donor pool — the setting ITS exists for. DiD lacks a defensible parallel-trends control (§7C); synthetic control lacks donors; event-study needs many events. The framework was also effectively dictated by the frozen CV wording. Correct choice, correctly implemented.

**Is the growth companion legitimate adjudication?** Yes — and this audit hardened that claim: on synthetic piecewise-linear data the companion recovers β₃ *exactly* (α₁ = 1.500000 against a true 1.5). It is the same estimand in differenced space, not a different model that happens to disagree. When levels-inference and companion-inference diverge, the divergence is informative about the levels SEs, not about the estimand. One honest caveat the report should carry: differencing when the truth is trend-stationary *over*-differences, inflating the companion's SEs (DW ≈ 2.4–2.8) — so the companion is a **conservative** adjudicator. Treating "significant in levels, insignificant in companion" as non-robust is therefore a deliberately strict standard. Strict is the right direction for this project, but call it strict.

**Is treating B3 as non-robust appropriate?** Yes — see §5. The rule was declared before Phase 6 ran; applying it to B3 is the rule working, not discretion.

**Does the alternative-date profile indicate curvature?** Yes, and this is the strongest single inference in Phase 6. β₃ ∈ [+0.85, +1.11], all p < 0.002 at six dates spanning 24 months, is the signature of a smooth convexity being approximated by a hinge placed anywhere in the bend. Supporting evidence: the memo's own §5.2 warning that a large β₂ signals mis-dating/mis-specification (B1's β₂ = −43%); and R12 (quadratic pre-trend), which would test curvature directly, is *unrun* — the one genuinely useful unrun robustness item. The label "placebo test" should be dropped (item 14) but the inference stands on the flatness of the profile itself.

**Are the structural-break tests over-interpreted?** They are correctly *weighted* in the findings ("corroboration that failed to arrive") but the mechanics are weaker than the write-up lets on: gapped series, forced break count, no critical values (§1.15). The honest final-report sentence is: *"break diagnostics, run under acknowledged limitations, provided no support for a break at the policy dates."* Nothing stronger, in either direction.

**Are the controls useful?** Yes, as designed — descriptive placebos at the treated dates, never a causal contrast. They did their job: they show the specification generating nominal significance in never-treated series.

**Is "2 of 9 significant → over-rejection" too strong? Yes.** Exact binomial p ≈ 0.071, and the nine tests are not independent (shared macro shocks). The defensible statement: *nominal significance appeared in control series more often than expected, which counsels treating all nominal p-values in this design with suspicion* — a caution, not a demonstrated property.

---

## 4. WHAT THE STUDY CAN CLAIM

### CAN CLAIM
- Constructed and validated a 96-month official monthly HS-level export panel (Apr 2018–Mar 2026) for four PLI-linked baskets and three non-PLI controls, with verified classification continuity across two ITC(HS) transitions.
- Applied segmented (interrupted) time-series analysis in log levels with month fixed effects, a COVID control, HAC inference at two lags, a stationary growth-rate companion, ARMA-error cross-checks, pre-registered alternative dates, and descriptive control comparisons.
- **Found no trajectory change, in any basket, that is robust across the pre-specified specification set.**
- A descriptive **ranking** of estimated post-policy trend changes: B3 largest positive (+0.87 lgp/mo), B4 ≈ 0, B2 small negative, B1 largest negative (−2.9 lgp/mo) — each with its (wide) confidence interval.
- Sector-specific descriptive facts: telephone-set exports grew ~119%/yr pre-D_s and ~54%/yr post; AC exports accelerated from ~2021 onward; documented HS-reclassification artefacts and their repair.

### CAN SAY WITH QUALIFICATION
- *"For air conditioners, point estimates consistently suggest trend acceleration of ~0.9 lgp/month, but the timing cannot be tied to the PLI incentive date — the same estimate appears at every candidate date over two years — and its statistical significance does not survive the stationary companion."*
- *"Evidence is consistent with no detectable policy-timed trajectory change at the sector-aggregate level over this window"* — qualified by limited power (§2), 24–48 post-months for the later schemes, and the fact that the treated units are product-group proxies containing non-beneficiary output (attenuation toward zero is built in).
- *"B1's trajectory decelerated after Aug 2020 in point-estimate terms"* — only with the CI (spanning zero) attached and the 119%/yr base-effect arithmetic stated.

### CANNOT CLAIM
- **"Effect of PLI" / "impact of PLI" / "PLI caused export growth"** — nothing in the design identifies causation, and the results would not support it even if it did.
- **"Trajectory changed after PLI"** as an unqualified statement — no robust β₃ exists.
- That the null proves PLI *failed* — absence of a detectable sector-aggregate trajectory change is not evidence of scheme ineffectiveness (power, aggregation, proxy dilution, and the 2–4-year horizon all cap what this design can see).
- Any statistically significant policy-timed result. B3's baseline p = 0.0013 is, by the binding rule, non-robust — not a finding.
- Any volatility claim **yet** — volatility inference has not been run (§8.5).

**Safest wording for the main conclusion:**

> *"Using segmented time-series analysis of official monthly HS-level export data over April 2018–March 2026, I evaluated whether the export trajectories of four PLI-linked product groups changed around each scheme's first incentive period. Point estimates identify air conditioners as the strongest candidate for post-policy trend acceleration and telephone sets as the strongest deceleration, but no estimated trajectory change is robust across the pre-specified stationary, ARMA-error and alternative-date checks. The evidence is consistent with no detectable policy-timed trajectory change at the sector-aggregate level over this horizon; it does not establish that the schemes had no effect."*

---

## 5. THE B3 RESULT — WHAT IT ACTUALLY MEANS

Assembling all six pieces of evidence: a stable point estimate (+0.85 to +1.11 lgp/mo, always positive); baseline significance (p = 0.0013); significance under AR(2) (p = 0.029) but not AR(1) (p = 0.152); companion insignificance (p = 0.718); uniform significance at six dates spanning 2021-04 to 2023-04; and break diagnostics that place nothing at 2022-04.

**What a serious applied econometrician concludes:**

1. **The phenomenon is real; the attribution is not.** Indian AC exports genuinely accelerated — the trend roughly doubled (≈12%/yr to ≈24%/yr) somewhere in 2021–2023. That is a fact about the series, visible to the eye and stable across every specification.
2. **The acceleration is smooth, not dated.** A discontinuity at the incentive date would produce a peaked β₃-vs-date profile. The observed profile is flat across 24 months. The hinge fits equally well anywhere in the bend, which is what a gradual steepening looks like through the lens of a piecewise-linear model. supF's argmax at 2021-07 — nine months *before* the incentive date — points the same way.
3. **The inference instability is a symptom of the same thing.** When the mean function is mis-specified as piecewise-linear around a smooth bend, residual dependence structure absorbs the discrepancy differently under different error models, and "significance" becomes an artefact of which error model you pick. That is exactly the observed AR(1)-vs-AR(2) flip.
4. **Attribution is additionally over-determined.** The acceleration window admits at least three stories on equal footing: the PLI *investment* year (FY2021-22), the post-COVID global durables boom, and the China+1 sourcing shift. Monthly aggregate trade data cannot separate them. It is also fair to note the White-Goods scheme's design (components, not finished units) made a strong finished-AC export response the *less* expected outcome ex ante.
5. **The correct scientific statement:** *"AC exports show a robustly estimated but smoothly emerging trend acceleration beginning around 2021–22, whose timing cannot be attributed to the PLI incentive date and whose statistical significance is specification-dependent. It is a lead worth noting, not a finding."* Anything stronger — in either direction, including "there is nothing here" — misreads the evidence. The point estimate is informative; the p-value is not.

---

## 6. THE B1 RESULT AND ITS SHORT PRE-PERIOD

**Recommendation: RETAIN as a core case — as the descriptive centrepiece and the pre-registered primary endpoint — while explicitly removing it from any claim of inferential precision.**

Reasons, in order:

1. **Demoting it now would be outcome-driven.** B1 was pre-registered as the primary endpoint (memo §C.2, before extraction). Reclassifying the primary endpoint after seeing an inconclusive result is the mirror image of promoting a significant one. The registration is only worth having if it binds both ways.
2. **Its descriptive story is the strongest single product of the project**: a 119%→54%/yr trajectory across the biggest industrial-policy episode in recent Indian history, measured on a basket that survives two classification transitions *because this project rebuilt it* — plus the honest arithmetic point that 119%/yr growth decelerates by necessity.
3. **Its inferential weakness is structural and now documented as irreducible** (28 pre-months; official monthly HS data starts Jan 2018). A limitation you can prove is external is presentable; one that looks chosen is not.
4. **Presentation formula:** *primary endpoint, descriptive centrepiece, inferentially inconclusive by design constraint* — with the CI (−6.9 to +1.0 lgp/mo) always shown, and the deceleration never framed as a policy disappointment (base effects guarantee deceleration at that growth rate).

Do not exclude it; do not headline its point estimate as if precise.

---

## 7. WHAT ELSE, IF ANYTHING

### A. Historical counterfactual forecasting — **RUN ONLY AS EXPLORATORY**
It was pre-planned (dropping a pre-registered component *because* results are null would itself be outcome-driven), and B4 can validate it properly (31 origins). But its evidential yield is now known to be low: B1 admits only the seasonal-naïve benchmark (excluded from model selection by prior decision — a large B1 "gap" would be an over-claiming hazard, not information); B2/B3 carry the mandatory 7-origin disclosure, so model selection is weakly identified; and any counterfactual gap inherits every confounder the ITS already could not separate. Run it as pre-specified, label every output descriptive, and expect it to add texture, not evidence.

### B. Volatility analysis — **RUN**
Unambiguous, for one decisive reason: **the frozen CV bullet claims "volatility changes," and no volatility computation currently exists.** Bullet 2 is unsupported on that clause until this runs (§8.5). It is also fully pre-registered (symmetric ±24-month windows, MBB CIs as primary inference, COVID-excluded variants, break-straddling-observation treatment), so running it is executing the plan, not adding a model. The known hazards — serial dependence, COVID, B1's level-dependent early volatility (EDA §7.1: residual 1.52× after removing COVID) — are all pre-documented with pre-assigned mitigations; the EDA caveat must sit beside the B1 result, and expectations should be set now that Δσ will likely be descriptive rather than significant. That outcome still completes the ranking the CV requires.

### C. Stacked treated × TimeAfter / DiD — **DO NOT RUN**
It would upgrade a comparison the design explicitly classified as descriptive into an identification claim resting on parallel trends — indefensible here: no within-industry control exists for B1 (declared limitation), control growth regimes differ by construction (declared at C2's selection), and C2 itself moved "significantly" at B1's date. It would not improve identification; it would manufacture the appearance of it. Adding it now, after nulls, is precisely the move rule 8 and the interpretation rule exist to prevent. The memo's option-(a)/(b) fork was decided in favour of (a); keep it.

---

## 8. THE FROZEN CV BULLETS

**Bullet 1 — "Analyzed GoI trade data using time-series analysis to assess PLI-linked sector exports."**
**Fully supported.** Official DGCI&S/MEIDB monthly data with documented provenance; the analysis is time-series econometrics in the standard sense (STL, unit-root and break-aware diagnostics, segmented regression, HAC, ARMA errors, Ljung–Box/Breusch–Godfrey); baskets mapped to PLI schemes from gazette notifications. This bullet was ~unsupported in the legacy project; it is now the project's firmest ground.

**Bullet 2 — "Evaluated changes in export trajectories around PLI implementation and identified sectors with the strongest post-policy trend and volatility changes."**
- *"Evaluated changes in export trajectories around PLI implementation"* — **supported.** That is exactly Phases 5–6. Evaluation does not require a positive verdict.
- *"identified sectors with the strongest post-policy **trend** changes"* — **supported as a descriptive ranking**, which is the honest reading of "identified … strongest": B3 strongest positive, B1 strongest negative, with CIs. It is NOT a claim of significant policy effects and must never be presented as one.
- *"and **volatility** changes"* — **NOT YET SUPPORTED.** No volatility computation exists. This clause is the outstanding obligation of the frozen wording and is the decisive argument for §7B. Until then, this half of the sentence has nothing behind it.

**2. What you can defend when asked "what did you actually find?"** —
> *"Three main things. First, the data work: official monthly HS-level series for PLI-linked sectors break twice at the 2022 classification change, and I built code-union baskets that survive it — the naive series shows a 70% artefact. Second, the trajectories: mobile-phone exports grew about 119% a year before the scheme's incentive date and about 54% after — still extraordinary, decelerating from an extreme base; air conditioners roughly doubled their trend growth, but that acceleration appears smoothly through 2021–23 rather than at the incentive date. Third, the econometrics: no sector's trajectory change survives my pre-specified robustness set — stationary-space estimation, ARMA errors, alternative dates. The estimate that looks significant in the baseline is equally 'significant' at dates two years apart, which tells you the model is tracing a curve, not detecting a policy break. I'd rather report a disciplined null than a fragile positive."*

**3. What you must NOT imply:** that PLI caused or measurably changed exports; that B3 is a robust effect; that the deceleration in B1 reflects policy failure; that any nominal p-value in this design is reliable at face value; that "strongest" means "significant"; that volatility results exist (until they do).

**4. Does "identified sectors with the strongest post-policy trend" mean a ranking?** Yes — and only a ranking. The design memo established this reading before any data existed (§E.7: "evaluated" and "identified the strongest" are satisfied by a correctly-estimated ranking whatever the numbers show). The completed analysis delivers that ranking with uncertainty attached. Present it as "largest estimated change," never "largest effect."

**5. Is the volatility wording currently supported?** **No.** It becomes supported the day the pre-registered volatility analysis produces the Δσ ranking — significant or not. This is a gap in *coverage of the frozen wording*, not in the science, and it has one remedy: §7B.

---

## 9. FINAL VERDICT

### PROJECT STATUS: **COMPLETE ONLY A LIMITED FINAL DESCRIPTIVE/EXPLORATORY PHASE**

Specifically, in order: **(1)** the pre-registered volatility analysis — required by the frozen CV wording (RUN); **(2)** the forecasting counterfactual as pre-specified, labelled exploratory (optional but pre-planned); **(3)** the low-cost unrun robustness items that bear on stated conclusions — above all **R12 (quadratic pre-trend)**, which directly tests the curvature reading, plus R7/R8/R10/R11 as cheap stress checks; **(4)** the three MINOR reporting corrections from §1 (ARMA column labels; B4 convergence disclosure; "placebo"→"alternative-date"; soften "over-rejecting"); **(5)** final report and the line-by-line CV claim audit. **No stacked DiD. No new specifications. No further inference-seeking.**

- **Strongest methodological feature:** the pre-registration discipline — dates, windows, grids, and the non-robustness rule all fixed before estimation, then *enforced against the project's own most promising result*. The B3 verdict is the system working. Close second: the HS-transition forensics, without which every downstream number would be wrong by construction.
- **Biggest methodological weakness:** low inferential power dressed in exact machinery — strong seasonality and serial dependence (residual ρ₁ up to +0.45) against 16 parameters mean only large, sharp breaks were ever detectable, and the piecewise-linear form is poorly matched to the smooth accelerations the data actually contains (the unrun R12 is the loose thread). The structural-break diagnostics as implemented (gapped series, forced breaks, no critical values) are the weakest concrete component.
- **Biggest remaining risk:** presentation risk — that the B3 point estimate or a large B1 counterfactual gap gets voiced as a policy effect, in the report or in an interview, undoing the discipline. Secondary: the volatility clause of the CV staying uncovered if §7B is skipped.
- **Sample size acceptable?** Yes for the design as scoped: adequate for fitting and description everywhere; adequate for inference on large effects in B2/B3; borderline for B1 (irreducibly — Jan 2018 is where official monthly HS data begins); B4's post-segment thin and correctly quarantined as robustness.
- **Central ITS design defensible?** Yes — it is the right framework, faithfully implemented, mechanically verified in this audit, and honest about what it cannot see. Its null-with-caveats output is a defensible result, not a failure.
- **Next action:** authorise the limited final phase above; then reporting and the CV audit. Nothing else.

*Audit complete. No files modified, no models run. Awaiting review.*
