# Phase 1 — Forensic Audit and Proposed Research Design

**Project:** PLI Scheme — Export Trajectory and Volatility Analysis
**Date of audit:** 26 August 2026
**Status:** Design proposal. No new code written. Requires sign-off before Phase 2.

**Evidence tiers used throughout:**

- **[V]** Verified directly from the uploaded project files or from a primary/authoritative source cited inline.
- **[I]** Methodological inference — my reading of the code/report, not something the files state explicitly.
- **[R]** Requires external research or verification you have not yet done.

---

# PART A — AUDIT OF THE EXISTING PROJECT

## A.1 Files inspected

| File | Size | Modified | Note |
|---|---|---|---|
| `data/india_exports_commodities.xlsx` | 16.8 KB | 19 Feb 2026 | Single sheet, 31 rows × 7 cols |
| `export_analysis.ipynb.ipynb` (root) | 207.6 KB | 1 May 2026 | 22 cells; exec counts 3–23, 17 stored outputs |
| `analysis/export_analysis.ipynb.ipynb` | 72.4 KB | 19 Feb 2026 | 22 cells; exec counts 23–42, 6 stored outputs |
| `report/PLI_Export_Structural_Analysis_Report.pdf` | 347.6 KB | 15 Feb 2026 | |
| `report/PLI_Export_Structural_Analysis_Report.docx` | 369.6 KB | 20 Feb 2026 | |
| `report/README.md` | 2.3 KB | 15 Feb 2026 | |
| `figures/` | 8 files | 1 May 2026 | 4 PNG, 4 XLSX |

**[V] The two notebooks are not divergent versions.** Their 22 cell sources are byte-identical; they differ only in stored outputs and execution counts. The root copy is a later re-run of the same code, not a fork. (Corrected during verification — the MD5 difference alone did not support the stronger claim.)

**[V] Chronology problem — confirmed by direct evidence.** The report PDF/DOCX are dated 15–20 Feb 2026; the figures were regenerated 1 May 2026. The report's embedded `word/media/image3.png` is a real chart of 69,736 bytes, whereas the current `figures/pli_share_no_petroleum.png` is a blank white image (see A.5). **The report's figures are therefore demonstrably not the current figure files.** Until resolved, you cannot claim the report and the repository agree.

**Cell references** throughout this document are **0-based JSON indices** (`nb['cells'][n]`). Counting from 1 in a notebook UI shifts every reference by one.

---

## A.2 What data you currently use — [V]

**Content:** 31 commodity rows, 6 fiscal-year columns (`2019-20` … `2024-25`), integer values in ₹ crore. No nulls, all `int64`, no metadata sheet, no source cell, no download date.

**Total exports by year (₹ crore), from the notebook output:**

| FY | 2019-20 | 2020-21 | 2021-22 | 2022-23 | 2023-24 | 2024-25 |
|---|---|---|---|---|---|---|
| Total | 22,19,854 | 21,59,044 | 31,47,021 | 36,21,550 | 36,18,954 | 37,01,070 |

Sanity check passes: FY2019-20 ≈ ₹22.2 lakh crore ≈ US$313bn at ~₹71/US$, consistent with published Indian merchandise exports.

**What the data actually are — [V] with [I] on provenance.**
The 31 row labels are an *exact* match for the **DGCI&S "Quick Estimates for Selected Major Commodities"** taxonomy: 30 named commodity groups plus a residual "Other Commodities". Row names like `Cotton Yarn/Fabs./made-ups Handloom Products etc.`, `Mica Coal & Other Ores Minerals including processed minerals`, and `Plastic & Linoleum` are verbatim DGCI&S QE group labels.

Your README and report cite **"RBI Handbook of Statistics on Indian Economy"**. That is at best imprecise. The RBI Handbook reproduces Commerce Ministry commodity-group data; it is not the compiling agency. The originating source is **DGCI&S / Ministry of Commerce**. *(DGCI&S Quick Estimates archive: https://www.dgciskol.gov.in/Quick_Estimate.aspx)*

**Undocumented items you must record before this dataset can be called final:**

- Exact source table and URL — [R]
- Download date — [R]
- Whether the figures are provisional or revised. **[V] DGCI&S operates a Dynamic Data Revision Policy since 2009-10 under which prior months/years are restated on every release** (https://www.dgciskol.gov.in/Writereaddata/Downloads/Dynamic_Data_Revision.pdf). Your snapshot has no vintage stamp, so it is not reproducible.
- **[V] DGCI&S note on the QE table: "Exports include Re-Exports."** Never stated in your report. Material for electronics.

### Fatal characteristic: frequency

**[V] The data are annual (fiscal-year). Six observations per sector.**

This single fact is what breaks both CV bullets. Everything in A.5 below follows from it.

---

## A.3 Time frequency — [V]

Annual, Indian fiscal year (April–March). Six periods, FY2019-20 to FY2024-25.

**[V] Labelling error propagated through the whole project.** The README title, the report title, the report abstract and the report body all say **"2019–2024"**. The data run April 2019 to **March 2025**. The report says *"increased from ₹82,936 crore in 2019 to ₹3,27,173 crore in 2024"* — both years are wrong; they are FY2019-20 and FY2024-25. An interviewer who knows Indian data will spot this in the first thirty seconds and will then distrust everything downstream.

---

## A.4 Sectors currently classified as PLI-linked

**[V] Three mutually inconsistent lists exist inside your own project:**

| Source | Sectors listed |
|---|---|
| README + report §2.2 + notebook cell 3 | Electronic Goods; Drugs & Pharmaceuticals; Engineering Goods; Organic & Inorganic Chemicals; Plastic & Linoleum |
| Notebook **cell 14** (redefines `pli_sectors`) | the above **plus** `Man-made Yarn/Fabs./made-ups etc.` |
| Notebook **cell 19** (volatility) | reloads the **entire 31-row file**, including Petroleum Products and Other Commodities, into a variable still named `pli_df` |

So the volatility table you exported to `figures/volatility_analysis.xlsx` is not a PLI table at all — it ranks all 31 commodity groups, and its top entry is Petroleum Products, which is not a PLI sector under any reading.

**[V] Against the official list, the classification does not survive.** PIB (Release ID 1945155, 02 Aug 2023) states the 14 PLI sectors verbatim: *"(i) Mobile Manufacturing and Specified Electronic Components, (ii) Critical Key Starting Materials/Drug Intermediaries & Active Pharmaceutical Ingredients, (iii) Manufacturing of Medical Devices (iv) Automobiles and Auto Components, (v) Pharmaceuticals Drugs, (vi) Specialty Steel, (vii) Telecom & Networking Products, (viii) Electronic/Technology Products, (ix) White Goods (ACs and LEDs), (x) Food Products, (xi) Textile Products: MMF segment and technical textiles, (xii) High efficiency solar PV modules, (xiii) Advanced Chemistry Cell (ACC) Battery, and (xiv) Drones and Drone Components."*

| Your sector | Verdict | Basis |
|---|---|---|
| **Plastic & Linoleum** | **Not a PLI sector.** No plastics PLI exists. | [V] PIB 14-sector list |
| **Engineering Goods** | **Not a PLI sector.** A ~₹9.9 lakh crore residual aggregate spanning most of HS 72–90. PLI-covered items (AAT auto components, telecom hardware, AC/LED components, specialty steel) are a small minority of it. Indefensible as a treatment unit. | [V] + [I] |
| **Organic & Inorganic Chemicals** | **Not a PLI sector as a group.** There is *partial* overlap: bulk-drug PLI APIs/KSMs sit in HS Ch. 29. But the group as a whole is not PLI-targeted. | [V] + [I] |
| **Drugs & Pharmaceuticals** | **Partially defensible.** Two real schemes exist (Bulk Drugs 2020; Pharmaceuticals 2021). But the QE group is dominated by *formulations*, whereas the bulk-drugs PLI targets *APIs/KSMs* — near-opposite ends of the value chain. | [V] |
| **Electronic Goods** | **Defensible in direction, too broad in practice.** LSEM's target segment is *mobile phones and specified electronic components*, not all electronic goods. | [V] |
| `Man-made Yarn/…` (cell 14 only) | Closest to a real scheme (Textiles PLI = MMF apparel/fabrics/technical textiles) — and it is the one you dropped from the README. | [V] |

**Bottom line: of the five sectors you present as PLI-linked, one is directionally right but too broad, two are partial overlaps whose group definitions are wrong, and two are not PLI sectors at all.** This is the most serious substantive finding in the audit.

---

## A.5 What analyses are actually implemented — [V] with defect assessment

| # | Cell(s) | What it does | Correct? |
|---|---|---|---|
| 1 | 4 | CAGR, `years=5` over 6 points | **Arithmetic correct** (5 intervals between 6 points) |
| 2 | 5, 9 | Sector share of total; PLI aggregate share | Arithmetic correct |
| 3 | 6 | HHI across the 31 groups | Arithmetic correct, **conceptually invalid** (see below) |
| 4 | 11–12 | Petroleum-adjusted share | Arithmetic correct; good instinct |
| 5 | 17 | "Growth acceleration" pre vs post | **Invalid** |
| 6 | 19 | "Export volatility" | **Invalid** |

### Defect 5 — "Growth acceleration" is arithmetically meaningless

```python
pre_growth  = (pli_df["2020-21"] - pli_df["2019-20"]) / pli_df["2019-20"] * 100   # 1-year growth
post_growth = (pli_df["2024-25"] - pli_df["2021-22"]) / pli_df["2021-22"] * 100   # 3-year growth
growth_compare["Growth_Acceleration"] = post_growth - pre_growth
```

Two problems, either of which is disqualifying:

1. **Incomparable horizons.** `pre` is a one-year change; `post` is a three-year cumulative change. Subtracting one from the other is a category error. The reported "Electronic Goods acceleration = 181.07" is a 3-year cumulative growth minus a 1-year growth. It is not an acceleration and has no units.
2. **The pre-window straddles COVID asymmetrically.** FY2020-21 is the *endpoint* of the pre-window, so COVID enters by deflating `pre_growth`, mechanically inflating the difference. The effect is sector-specific, not universal — the project's own exported table shows Drugs & Pharmaceuticals **+23.5%** through FY2020-21 while Man-made Yarn fell **−17.7%**, and total exports fell only 2.7% (₹22,19,854 → ₹21,59,044 crore), so at annual frequency FY2020-21 is not a uniform "collapse". That heterogeneity is by itself enough to make the cross-sector ranking of "acceleration" uninterpretable.

### Defect 6 — the volatility measure is the single most damaging item

```python
volatility = pli_df.std(axis=1)   # SD of levels in ₹ crore across 6 fiscal years
```

This is **not volatility**. It is the standard deviation of the *level* of a trending series, in currency units. Consequences:

- It scales with sector size. Petroleum (₹2.27 lakh crore SD) and Engineering Goods (₹1.80 lakh crore SD) rank 1–2 *because they are the largest sectors*, not because they are the most volatile.
- It is increasing in trend strength. A sector that grew perfectly smoothly and fourfold would score as "highly volatile".
- It is computed over the whole sample. **There is no pre/post comparison anywhere in the project** — so the CV phrase "volatility changes" has no computation behind it at all.
- It is computed on all 31 commodities including Petroleum and "Other Commodities", despite the variable name.

This is a first-course econometrics error and it is directly load-bearing for CV bullet 2.

### Defect 3 — HHI is not interpretable as specified

The 31 rows are heterogeneous in width (one row is "Rice", another is "Engineering Goods"), and one row is a residual **"Other Commodities"** bucket (₹1.3–2.1 lakh crore over the period). An HHI over an arbitrary, unequal, partly-residual partition is not a concentration index in any standard sense. It also has no reported numeric output — only a plot — so the report's claim that concentration is "stable" is unquantified.

### Code-quality defects — [V]

- **Blank figure bug.** Cell 13 is a stray `plt.savefig(...pli_share_no_petroleum.png...)` executed on an empty figure, **overwriting** the chart from cell 12. Verified by pixel inspection, not inferred from size: the file is a valid 1920×1440 PNG containing **a single uniform white field, zero non-white pixels**. Because cell 13 runs on every execution, the file has *never* held the good chart.
- **Hardcoded Windows paths** `D:\PLI_Export_Project\...` in **twelve cells (0, 4, 5, 6, 7, 9, 12, 13, 14, 18, 19, 20)**. Not reproducible on any other machine, including yours after a folder move (the project now lives at `<project-root>`, so **the notebook as saved fails at cell 0**).
- **Non-raw string literals** — `"D:\PLI_Export_Project\data\..."`. Works only by luck (`\P`, `\d` are not escape sequences). `\t`, `\n`, `\f`, `\b`, `\r`, `\v`, `\a`, `\x` would silently corrupt the path.
- **`df.fillna(0)` after `to_numeric(errors='coerce')`** — silently converts any unparsable cell to zero. No validation, no assertion, no row/column count check.
- **Two copies of the notebook** with identical code but different stored outputs and execution counts. Not a fork, but still ambiguous provenance — one must be designated canonical.
- **Filename** `export_analysis.ipynb.ipynb` — double extension.
- No `requirements.txt`, no library versions, no data dictionary, no raw/clean separation (`data/` holds a single already-cleaned file; the raw download is gone).

### Report-internal inconsistencies — [V]

**First.** Report §3.1 body text: *"Engineering Goods recorded a CAGR of approximately **12.9%**"*. The code, the exported table, and the report's own table say **12.09%**.

**Second.** Report §3.2: *"PLI-linked sectors accounted for 44% of total exports in 2019. By 2024, this share increased to 51%, indicating a **7-percentage-point** rise over five years."* The computed shares are **44.92% → 51.07%**, a rise of **6.15 pp**, not 7. The "7 pp" is an artefact of the report's own truncation. Separately, 44.92% rounds to **45%**, not 44% — the README and report abstract both truncate rather than round.

Two independent transcription errors in a four-page report. Fix both in the rewrite and check every remaining number against the code.

---

## A.6 What the current analysis genuinely supports

| Claim | Status |
|---|---|
| Electronic Goods nominal ₹ CAGR = 31.59%, FY2019-20 → FY2024-25 | **Supported as arithmetic.** Not supported as a *real* or USD growth rate. |
| Selected-sector share of total exports rose 44.9% → 51.1% | **Supported as arithmetic.** The "PLI-linked" label is unvalidated. |
| Ex-petroleum share rose 51.7% → 59.7% | **Supported as arithmetic.** Same labelling caveat. |
| Export concentration "stable" | **Weak.** No numbers reported; index not well-defined over this partition. |
| "Growth acceleration" by sector | **Not supported.** Incomparable windows. |
| Volatility ranking | **Not supported.** Wrong estimator; no pre/post comparison exists. |
| Any statement about PLI implementation | **Not supported.** No implementation date appears anywhere in the project. |

**[I] The implicit break date.** Cell 17's `post` window starts at FY2021-22, so the code implicitly places the break between FY2020-21 and FY2021-22. This is never stated and never justified. It coincides with exactly one scheme date in the whole programme — the Telecom PLI, effective 1 April 2021 — which the project never cites and almost certainly did not intend, since Telecom is not among its five sectors.

---

## A.7 CV bullet audit

### Bullet 1 — "Analyzed GoI trade data using time-series analysis to assess PLI-linked sector exports"

| Component | Status |
|---|---|
| "GoI trade data" | **Partial.** The data are DGCI&S-origin, but you cite RBI, with no table reference, URL, download date or vintage. Documentation-fixable. |
| "time-series analysis" | **Unsupported.** Six annual points, CAGR and share ratios. No time index in any model, no seasonality, no autocorrelation, no decomposition, no dynamics, no stationarity treatment. A growth rate is a two-point comparison, not time-series analysis. **This is the single most exposed word on your CV.** |
| "PLI-linked sector" | **Unsupported and partly false.** Three of five sectors are not PLI sectors. |

### Bullet 2 — "Evaluated changes in export trajectories around PLI implementation and identified sectors with the strongest post-policy trend and volatility changes"

| Component | Status |
|---|---|
| "around PLI implementation" | **Unsupported.** No implementation date exists in the project. |
| "changes in export trajectories" | **Unsupported.** No trajectory (trend) is ever estimated. |
| "strongest post-policy trend change" | **Unsupported.** The only candidate computation (cell 17) is arithmetically invalid. |
| "volatility changes" | **Unsupported.** Wrong estimator; no pre/post split. |

**Blunt summary: bullet 1 is largely unsupported — only the loosest reading of "GoI trade data" survives. Bullet 2 is wholly unsupported — not one of its four components has a valid computation behind it.** Neither is currently defensible under questioning. Both are recoverable — see Parts B–E.

---

## A.8 What an econometrics interviewer will attack

Ranked by how quickly it ends the conversation.

1. **"How many observations?"** — Six. Nothing in the project can be inferential. Immediate.
2. **"std of levels is your volatility measure?"** — Textbook error, and it is in an exported deliverable.
3. **"Your acceleration compares a one-year change to a three-year change."**
4. **"Plastic & Linoleum is a PLI sector?"** — It isn't. Nor is Engineering Goods, nor Chemicals broadly.
5. **"Real or nominal?"** — Nominal ₹. The 31.59% CAGR embeds ~5% annual inflation *and* rupee depreciation. In USD it is materially lower; you have not computed it.
6. **"What's your base year?"** — FY2019-20, and the second observation is the COVID trough. Growth off a collapsed base.
7. **"What's the intervention date?"** — Not stated anywhere. And there is no single PLI date: LSEM incentives run from 01.08.2020; Telecom from 01.04.2021; White Goods, Pharma and Auto from FY2022-23; Textiles from FY2024-25 — all **[V]**, each with its source in the mapping file.
8. **"Aggregation."** — LSEM covers *mobile phones and specified components*; you use the whole "Electronic Goods" group. The bulk-drug PLI covers *APIs/KSMs*; the QE group is dominated by formulations.
9. **"Where's your counterfactual?"** — None. Single-series before/after with no control, no placebo, no comparison group.
10. **"Re-exports."** — DGCI&S QE data include re-exports. Never mentioned.
11. **"Can you separate PLI from the post-COVID global demand rebound, the China+1 supply-chain shift and rupee depreciation?"** — Currently, no. Nothing in the design attempts it.
12. **"Reproducibility."** — Two ambiguous notebook copies, hardcoded `D:\PLI_Export_Project` paths that no longer resolve (the notebook fails at cell 0), one silently blanked figure, no library versions, no raw data.
13. **"Your report says 12.9%, your table says 12.09%; your report says a 7 pp share rise where the arithmetic gives 6.15 pp; and your title says 2019–2024 for FY2019-20 to FY2024-25."**
14. **"HHI over a partition that contains a residual 'Other Commodities' bucket."**

---

## A.9 What is worth preserving

Do not discard these — they become the **structural / context layer** of the new project:

- Sectoral export shares and the petroleum-adjusted variant. Excluding petroleum was a genuinely good instinct and is worth keeping as motivation.
- The annual commodity-group series as macro context: *"PLI-adjacent groups' share of the non-petroleum basket rose from X to Y over FY2019-20 to FY2024-25"* — an honest, correctly-labelled descriptive framing.
- CAGR, once recomputed in USD alongside ₹ and correctly labelled by fiscal year.
- The report's Section 4 caution against causal attribution. That instinct is right and should carry into the new report.

HHI should be dropped or completely respecified. The volatility table and the growth-acceleration table must be deleted, not repaired.

---

# PART B — WHAT THE PROJECT SHOULD BECOME

## B.1 Is interrupted/segmented time series the right main framework?

**Yes — and it is the *only* framework that maps one-to-one onto your CV wording.** Read the bullet literally:

> "changes in export **trajectories** around PLI implementation" → a **slope change at a known date** = β₃ in a segmented regression.
> "sectors with the **strongest** post-policy **trend and volatility changes**" → a **ranking** over estimated β₃ and Δσ.

There is no other standard method whose output *is* those two objects. DiD needs a credible untreated control at the same aggregation (weak here); synthetic control needs a donor pool of comparable units (you have one country); event study needs many events. ITS needs one series, one known date, and enough observations — which is achievable.

**Recommendation: segmented (interrupted) time-series regression on monthly data is the main framework. Confirmed.**

## B.2 Why the time-series *structure* is genuinely necessary — not decoration

Three independent reasons. You must be able to give all three.

1. **The estimand is a slope, and slopes need points.** "Trajectory change" is defined as the difference between two trend rates. Six annual points against four parameters (β₀, β₁, β₂, β₃) leaves **2 residual degrees of freedom** — enough to fit, nowhere near enough to infer, and that is before any seasonal or COVID term. Monthly data over Apr 2018–Mar 2026 gives 96 observations.

2. **The data-generating process has structure that invalidates naive inference.** Monthly Indian export series are strongly seasonal (a pronounced fiscal-year-end March effect, plus festival and shipping-cycle effects) and strongly serially correlated. If you ignore this, OLS standard errors are badly understated and you will find "significance" that isn't there. Handling it — month fixed effects, ACF/Ljung-Box diagnostics, HAC or ARMA-error inference — *is* the time-series analysis.

3. **Volatility is only defined at a sampling frequency.** A second moment needs a sample. Six annual levels give you one number that is mostly a scale artefact (that is exactly the bug in A.5). Monthly log growth gives **27–47 pre and 48–68 post observations** depending on the sector — one fewer than the level counts, since g_t is undefined at t = 1 — from which σ_pre and σ_post are estimable and comparable.

## B.3 What "time-series analysis" means in this project — the exact defensible claim

When asked "what time-series analysis did you do?", the answer is:

1. Constructed a monthly, seasonally-structured, HS-level export panel and validated it against published totals.
2. Log transform; first differences for growth; ADF and KPSS stationarity testing on both.
3. Seasonality modelled via month fixed effects inside the estimating equation; STL decomposition as a diagnostic exhibit.
4. Segmented regression on the time index with a known, externally-dated break — separate pre-trend, level-shift and trend-change parameters.
5. Residual diagnostics: ACF/PACF, Ljung-Box at lags 12 and 24, Durbin-Watson, heteroskedasticity tests.
6. Inference corrected for serial correlation: Newey-West HAC, cross-checked against regression-with-ARMA-errors.
7. Second-moment analysis: SD of monthly log growth pre/post, 6-month rolling SD, and an inference-valid volatility-shift test.
8. Structural-break testing (Chow at the known date; Bai–Perron for an unknown break) as corroboration, not proof.

That is applied time-series econometrics in the standard sense. It is not inflated, and every item answers a stated question.

## B.4 Why forecasting is not necessary — and when it would be a mistake

Both CV bullets are **retrospective**. Neither claims a prediction. A SARIMA forecast answers "what happens next", which nothing on your CV asserts, and it would import a set of assumptions (order selection, invertibility, forecast-interval coverage) you would then have to defend for zero return on the claims.

The one legitimate use would be a **counterfactual**: fit an ARIMA on pre-period data only, project forward, and compare actual to projection. Assess honestly:

- It requires a long, clean pre-period. For mobile phones the pre-period is 28 months and ends with the COVID collapse. The projection would be built on the worst possible base.
- Forecast intervals widen fast; at a 60-month horizon they would be too wide to discriminate anything.
- It adds a second identification story you must defend alongside the first.

**Recommendation: do not include forecasting.** If you later want it, include it only as a clearly-labelled appendix sensitivity for a sector with a ≥48-month clean pre-period, never as evidence for a CV bullet.

## B.5 Exact quantities required to support each bullet

### Bullet 1 — a *process* claim

Supported by the existence and correctness of: a documented DGCI&S monthly HS-level dataset with vintage and revision notes; STL/seasonality exhibits; ACF/PACF plots; ADF/KPSS results; HAC-corrected inference. Deliverables: the master monthly dataset, the diagnostics section, the source log.

### Bullet 2 — two named numbers per sector, plus two rankings

| Quantity | Symbol | Definition | Reported as |
|---|---|---|---|
| Pre-implementation trend | β₁ | Mean monthly log-growth before D_s | % per month, HAC SE |
| Immediate level shift | β₂ | Discrete jump in ln(exports) at D_s | %, HAC SE |
| **Trajectory change** | **β₃** | Change in monthly trend after D_s | **pp per month, HAC SE, 95% CI** |
| Pre volatility | σ_pre | SD of monthly log growth, t < D_s | **% per month** (see note) |
| Post volatility | σ_post | SD of monthly log growth, t ≥ D_s | **% per month** |
| **Volatility change** | **Δσ** | σ_post − σ_pre | Absolute and %, with a test |

**Note on annualisation.** Report σ in **raw % per month**. Scaling a monthly SD by √12 assumes serially independent growth — the very assumption Section C.11 spends its length rejecting. If an annualised figure is wanted for readability, give it *alongside* the monthly figure and state the independence assumption explicitly.

Then **two ranking tables**: sectors ordered by β₃ (with CIs), sectors ordered by Δσ (with tests). The word "identified" in your CV is satisfied by producing these two tables — regardless of which way the numbers come out.

---

# PART C — RESEARCH DESIGN

## C.1 Final research question

> **Did the monthly export trajectory and the monthly export volatility of narrowly PLI-targeted product groups change around the start of their respective schemes' first incentive periods, relative to their own pre-scheme trend and to comparable non-PLI product groups, over April 2018 – March 2026?**

Observational. The design supports statements about *association around implementation*, not causation.

## C.2 Testable hypotheses

**H1 — Trajectory.** For at least one narrowly-mapped PLI product group, β₃ > 0: post-implementation monthly trend growth exceeds pre-implementation trend growth, conditional on month fixed effects and a COVID control, with HAC-corrected inference.
*Rejected if* β₃ is indistinguishable from zero or flips sign across the robustness set.

**H2 — Specificity.** β₃ is larger where the HS mapping is tighter to the scheme's stated target segment, and is indistinguishable from zero for matched non-PLI control groups and for placebo break dates.
*Rejected if* control groups show β₃ of similar magnitude — which would identify the post-COVID export rebound, not policy.

**H3 — Volatility.** Δσ ≠ 0 for PLI groups.
Stated two-sided. Prior: rising volatility in rapidly scaling groups (lumpy capacity additions, order concentration), roughly unchanged in mature groups.
*Note on the A.5 repair:* σ here is the SD of **log differences**, which is scale-free **by construction** — the old bug (SD of levels in ₹ crore) cannot recur, and that is an analytic fact, not something a correlation demonstrates. A Δσ-vs-mean-size scatter is still worth reporting as visual confirmation, but with n = 4 sectors it has no power and must not be presented as a test.

**Pre-specified primary endpoint.** The deliverable is a ranking over 4 sectors × 2 statistics, cross-checked against 12 robustness specifications. Claiming "strongest" or "distinguishable from zero" across that grid without a pre-registered primary endpoint invites the standard multiplicity objection. **Mobile phones is the single pre-specified primary endpoint; the other three sectors are secondary and are reported as such.** Fix this now, in writing, before any estimation.

## C.3 Study period

**April 2018 – March 2026. 96 months. Eight complete fiscal years.**

Justification:
- **[V] Hard lower bound at HS granularity:** the free MEIDB monthly HS portal carries data from **January 2018** only (banner as at 26 Aug 2026: *"Data available: Jan 2018 to Jun 2026"*). Jan–Mar 2018 is discarded to obtain whole fiscal years and exact 12-month seasonal cycles.
- **Upper bound:** end at March 2026 — a fiscal year-end, and **[V]** within the "(R) Revised Final upto Mar 2026" window. **[I]** Apr–Jun 2026 is labelled "(F) Final" but falls outside the Revised-Final window and is therefore exposed to restatement under the Dynamic Data Revision Policy; excluding it is the conservative call.
- Fixed *ex ante*, applied identically to every sector. Do not tune it.

**[R] Extension option.** DGCI&S FTPA carries monthly data back to Jan 2010, but only at ~21 broad commodity-group level, not HS. Usable as a long-pre-period robustness check on coarse aggregates for the mobile-phone case, where 28 pre-months is the binding weakness. Verify feasibility in Phase 2.

## C.4 Sectors — 4 treated + 1 control

Selected for **mapping tightness to the scheme's own stated target segment** first, with demonstrative value and pre/post balance as secondary tie-breakers. Never for size or for likely result. **Only mobile phones is rated HIGH confidence; the other three are MEDIUM** (see D.4) — that is a property of the PLI notifications, which mostly do not publish HS codes, not of the selection process.

| # | Series | Scheme | D_s | Pre / post months |
|---|---|---|---|---|
| 1 | **Mobile phones** | PLI-LSEM (mobile phone segment) | **Aug 2020** | 28 / 68 |
| 2 | **Telecom & networking equipment** | PLI Telecom & Networking Products | **Apr 2021** | 36 / 60 |
| 3 | **Bulk drugs / APIs & drug intermediates** | PLI Pharmaceuticals (chem-synthesis route) | **Apr 2022** | 48 / 48 |
| 4 | **Air conditioners** | PLI White Goods (AC segment) | **Apr 2022** | 48 / 48 |
| C | **Non-PLI control basket** | — | placebo dates as above | — |

**Why these four.** Mobile phones is the cleanest mapping in the entire PLI programme and is the headline case. Telecom equipment is explicitly product-listed in the notification. Bulk drugs/APIs is a *balanced* 48/48 split, the strongest statistical case, and it directly corrects your existing pharma misclassification. Air conditioners has a very clean HS mapping and a strong seasonal signal — good for demonstrating that your seasonality handling works.

**Why the control matters more than a fifth treated sector.** Every sector above rebounded post-COVID. Without a control, β₃ cannot be distinguished from the common recovery. The control basket is your primary answer to the hardest interview question.

**[R] Selection criteria — pre-commit in writing before estimating anything.** Comparable global-demand exposure **and** a comparable secular growth regime. The second criterion is the one usually forgotten and is the real analogue of parallel trends here: none of the obvious candidates scales like assembly electronics, and that mismatch must be stated as a limitation whichever is chosen. Candidates with their known problems:

- *Gems & jewellery* — dominated by re-export routing (India imports rough, exports polished), which is the same structural defect flagged as V7 for the treated series, plus an idiosyncratic hit from 2022 Russian rough-diamond sanctions.
- *Marine products* — US antidumping actions and shrimp-specific shocks.
- *Leather goods, ceramic products* — smaller and less shock-prone, but slower-growing.

**Excluded deliberately, with reasons to state:**
- *Textiles PLI* — first performance year FY2024-25 [V]. Only ~24 post-months. Too early. Say so.
- *Automobiles* — the notification defers the eligible-component list to guidelines and contains no HS annexure [V]. AAT components cannot be mapped to trade codes with confidence.
- *IT Hardware* — laptops/tablets/servers. **[I]** India's exports in these lines are believed small relative to imports, giving a weak signal. **Verify against MEIDB before citing this reason in the report** — it is currently a prior, not a checked fact, and no IT Hardware row exists in the mapping file.
- *Medical devices, food, solar, ACC, steel, drones* — mapping or scale problems; excluded for parsimony.

## C.5 Outcome variable

**y_t = ln(monthly export value, US$ million, FOB).**

- **Why USD.** Removes rupee depreciation from the estimated trend. **[V]** USD is the DGCI&S headline presentation currency, derived monthly from INR using the RBI monthly average rate (DGCI&S NMDS §2.6).
- **Why logs.** β coefficients read as percentage changes; multiplicative seasonality becomes additive; variance is stabilised.
- **Robustness:** re-run in ₹ crore. If β₃ differs materially, the difference is exchange-rate driven and must be reported as such.
- **Deflation — be honest about this.** No freely-available monthly export unit-value index exists at this HS granularity for India. **[R]** Check whether RBI/DGCI&S publish a usable monthly export UVI. If not, the correct position is: *the series is nominal USD; global price inflation is common to treated and control groups and is therefore partly differenced out by the control comparison, but a price/volume decomposition is not attempted and this is a stated limitation.* Do not claim a real series you do not have.
- **Quantity cross-check:** MEIDB exposes quantity at HS-8 [V]. Where units are consistent, plot volume alongside value as a descriptive price/volume sanity check. Do not build the model on it — **[V]** MEIDB warns that units of measure **may** change at the Apr-2022/2024/2026 HS revisions.

## C.6 Intervention variable

**Post_t = 1{t ≥ D_s}**, with D_s **sector-specific** and set to **the start of the scheme's first incentive/performance period** — not the Cabinet date, not the notification date.

**Justification you must be able to give:** PLI pays on *incremental sales* measured within defined performance years. The economic incentive to raise output binds when the first performance year begins and incremental sales start accruing toward a claim. Cabinet approval and gazette notification are announcement events; they may generate anticipatory investment but do not switch on the incentive. Choosing the performance-year start is a substantive, pre-committed decision.

**[V] All alternative dates are documented in `docs/archive/pli_sector_mapping_PROPOSED.csv`, and will be re-estimated in robustness R1.** If β₃ is highly sensitive to which of these dates you use, that is itself a finding and must be reported.

## C.7 Trend specification

Time index T_t = 1, 2, …, 96 (Apr 2018 = 1).
**TimeAfter_t = max(0, T_t − T_{D_s})** — note **not** `+1`.

This definition matters and will be probed. With `max(0, T − T_D)`, TimeAfter = 0 at the break month, so **β₂ is a clean level shift at D_s**. Under `max(0, T − T_D + 1)` the fitted jump at D_s becomes β₂ + β₃, so β₂ alone no longer reads as the level shift. (β₃ remains the slope change under either convention — do not overstate this.) State the convention explicitly in the report.

## C.8 Seasonality treatment

**Eleven month dummies, estimated inside the equation.**

**Do not seasonally adjust first and then regress.** The decisive reason is **break-smearing**: a two-sided filter spreads a genuine break across the months either side of it, strongly attenuating β₂ and mildly, locally distorting β₃. (This is precisely why X-13 carries LS/AO outlier regressors for known breaks.) Pre-filtering also induces serial dependence in the residuals with no clean interpretation, which the HAC correction is then asked to clean up after. Estimating month FE jointly keeps the seasonal adjustment inside the model and auditable in one table.

*Do not overstate the standard-error argument.* Filter-induced dependence is not sign-definite — X-11-family filters induce **negative** autocorrelation at seasonal lags — and this design uses HAC anyway. Break-smearing, not SE bias, is the argument to make.

**STL** is used for two legitimate purposes only: (i) a descriptive exhibit showing trend/seasonal/remainder per sector; (ii) a robustness check re-estimating on the STL trend + remainder. Report as robustness, never as the baseline — **and note that variant (ii) inherits the break-smearing problem, so its β₂ should be read as a lower bound.**

**[I] Expect a strong March effect** in Indian monthly export data (fiscal-year-end). This is a prior, not a sourced fact. Verify it appears in the estimated month coefficients — if it doesn't, suspect a data-assembly error.

## C.9 Volatility measure

```
g_t   = 100 × [ ln(Y_t) − ln(Y_{t−1}) ]
σ_pre  = SD(g_t | t < D_s)      σ_post = SD(g_t | t ≥ D_s)
Δσ = σ_post − σ_pre             %Δσ = Δσ / σ_pre × 100
```
Plus a **6-month rolling SD of g_t**, plotted with D_s marked.

**Inference on Δσ — three layers.**

1. **Levene / Brown–Forsythe** equality-of-variance test. Robust to non-normality; **not** robust to serial correlation — say so.
2. **Residual-based volatility-shift regression.** *Do not regress |g_t − ḡ| on Post with a full-sample mean.* If mean growth shifts at D_s — which is H1, the very thing being tested — a full-sample demeaning makes θ₁ pick up the **mean** shift, not a variance shift, and H1 and H3 become conflated by construction. Demean **within regime and net of seasonality** instead:
   ```
   û_t   from   g_t = α₀ + α₁·Post_t + Σ γ_m·Month_m + δ·Covid_t + u_t
   |û_t| = θ₀ + θ₁·Post_t + Σ λ_m·Month_m + v_t          # HAC SEs
   ```
   θ₁ is a shift in **mean absolute deviation**, not in σ (under normality σ = √(π/2)·MAD ≈ 1.2533·MAD). Report it as a MAD shift; do not call it "the inference-valid version of Δσ" — it is a related but distinct estimand. Note also that û is an estimated regressand, so HAC SEs here understate uncertainty.
3. **Moving-block bootstrap CI on Δσ.** This is the only layer that handles both serial dependence *and* the generated-regressand problem, so treat it as the primary inference on Δσ rather than an afterthought.

**Two checks to report:**

- **Scale-freeness.** σ is computed on log differences and is therefore scale-free **by construction** — the A.5 bug cannot recur. Report a Δσ-vs-mean-size scatter as visual confirmation, but with n = 4 sectors it has no power and must not be presented as a test.
- **COVID asymmetry — the biggest threat to the mobile-phone result.** With D_s = Aug 2020 the Apr–Jun 2020 collapse falls in the **pre**-period and the Jul 2020 – Mar 2021 rebound falls in the **post**-period. In a specification without `Covid_t` this both depresses β̂₁ and steepens the post segment, pushing β₃ **upward** through two channels. The block `Covid_t` dummy absorbs the collapse but **not the rebound**, so a residual upward bias survives the baseline — and RC1 (widening to Sep 2020) still leaves Oct 2020 – Mar 2021 of rebound inside the post segment. The sign of the bias in **Δσ is ambiguous**, since the rebound inflates σ_post as well as σ_pre. And the sign may **reverse** for bulk drugs: Indian pharmaceutical exports rose through the lockdown under the essential-goods exemption — the project's own annual table shows Drugs & Pharmaceuticals **+23.5%** in FY2020-21. Report Δσ and β₃ both with and without Mar–Sep 2020, for every sector, in the main results table — not buried in an appendix.
- **Break-month growth observation.** Under `σ_post = SD(g_t | t ≥ D_s)` the first post observation is `ln Y_{T_D} − ln Y_{T_D−1}`, which straddles the break and contains the entire β₂ level jump. If β₂ ≠ 0 this single observation inflates σ_post and biases Δσ upward. State the convention and report Δσ with that observation dropped.

## C.10 COVID treatment

Baseline: `Covid_t = 1` for **Apr, May, Jun 2020** (India's hard lockdown). Note that the *collapse* is concentrated in these months but the *rebound* runs well beyond them, and that the collapse was **not universal** — pharmaceutical exports rose through the lockdown under the essential-goods exemption. Do not describe Apr–Jun 2020 as a uniform export collapse.

Robustness ladder:
- **RC1** widen to Mar 2020 – Sep 2020
- **RC2** drop those months from estimation entirely
- **RC3** month-specific dummies for Apr/May/Jun 2020 rather than one block dummy
- **RC4** — **the strongest defence** — estimate the identical model on the non-PLI control basket and report β₃^treated alongside β₃^control. If the control shows the same slope change, you have measured the recovery, not the policy.

  **Caveat you must state, or estimate your way out of.** Reporting two *separately estimated* coefficients side by side is not a test of their difference — there is no standard error on β₃^t − β₃^c, so "β₃^control ≈ β₃^treated" has no decision rule. Two honest options: (a) declare the comparison **descriptive** and say plainly that no test of the contrast is available; or (b) **stack treated and control and interact**, `Treated × TimeAfter`, which yields the contrast and its SE directly. Option (b) is a difference-in-differences whatever it is called — if you take it, own the label and defend the parallel-trends assumption rather than smuggling it in. **Recommendation: take option (a) for the baseline report and option (b) as a named extension**, so the design stays honest about what it does and does not identify.

Report β₃ under all of these in one table. If the sign of β₃ flips anywhere, that is the headline finding and it must be reported as such.

**Other confounders to address in the report (narratively, with the control comparison as the empirical handle):** global demand recovery; China+1 supply-chain reorientation; rupee depreciation (addressed by the USD outcome); semiconductor and commodity price cycles 2021–23; the 2022 energy/geopolitical shock; and — for electronics specifically — the interaction with tariff policy on components, which moved over the same period and is not separable from PLI in trade data. Say this plainly rather than waiting to be asked.

## C.11 Autocorrelation treatment

1. **Diagnose:** ACF/PACF of residuals; Ljung–Box at lags 12 and 24; Durbin–Watson; Breusch–Godfrey.
2. **Baseline inference:** **Newey–West HAC**. Report at the Newey–West rule-of-thumb lag ⌊4(T/100)^(2/9)⌋ = ⌊3.96⌋ = **3** for T = 96 (Stock–Watson 0.75·T^(1/3) = 3.43 → 3 also), **and** at lag 12 (a full seasonal cycle). If they disagree materially, report both and say so. **Use 3, not 4 — the rule floors, it does not round.**
3. **Cross-check:** regression with ARMA errors (`statsmodels` SARIMAX with exogenous regressors). If β₃ from HAC-OLS and from ARMA-errors agree, the result is not an inference artefact. If they disagree, ARMA-errors is the more credible number.
4. **Stationarity — the spurious-regression defence.** ln(Y_t) is plausibly I(1) with drift. A segmented regression on a trending non-stationary series is exposed to spurious inference. Four parts:

   - **ADF and KPSS** on ln(Y_t) and on g_t; report both (they test opposite nulls).
   - **Break-augmented unit-root tests — Zivot–Andrews or Perron.** Perron (1989): a standard ADF on a series with a trend break is biased *toward* non-rejection of the unit root. So the premise "ln(Y_t) is I(1)" may itself be a break artefact. You cannot cite Bai–Perron for the break and then use a break-blind unit-root test on the same series.
   - **ADF on the fitted residuals**, with the caveat that **standard ADF critical values are invalid** on residuals containing estimated parameters — use Engle–Granger / Phillips–Ouliaris critical values, and note that the presence of break regressors degrades even those. Treat this as suggestive, not decisive.
   - **Estimate the growth-rate specification as a parallel headline:**
     ```
     g_t = α₀ + α₁·Post_t + α₂·Break_t + Σ φ_m·Month_m + Σ_{k} δ_k·CovidMonth_kt + u_t
         where  Break_t = 1{ t = T_D }
     ```
     α₁ is the change in *average monthly growth* after D_s, estimated entirely in stationary space — the direct, stationarity-robust version of the trajectory claim. **Report it next to β₃ in the main results table.**

     **Two specification details the naive version gets wrong.** Differencing the level model gives `g_t = β₁ + β₃·Post_t + β₂·1{t = T_D} + Δ(seasonals) + Δ(Covid)`. So (i) the β₂ level jump becomes a **one-month spike at t = T_D** — without `Break_t` that single observation contaminates α₁; and (ii) a level *block* dummy for Apr–Jun 2020 becomes, in differences, a spike at Apr 2020 and a **reversal at Jul 2020** — so carrying `Covid_t` across unchanged does not absorb what it absorbs in levels. Use month-specific dummies for Apr/May/Jun/**Jul** 2020 in the growth equation. Note also that φ, δ and the seasonal coefficients here are **different objects** from the γ, δ of the level equation despite similar roles — letter them distinctly in the code and tables.

     With those two dummies in place, if β₃ and α₁ agree in sign, the trajectory finding survives the spurious-regression attack. This costs a handful of lines and closes the hardest methodological hole in the design.

## C.12 Robustness checks — the full pre-committed set

| ID | Check | Guards against |
|---|---|---|
| R1 | Alternative break dates: Cabinet, notification, guidelines, performance-year start, D_s ± 3 months | Break-date cherry-picking |
| R2 | COVID window variants RC1–RC3 | COVID confounding |
| R3 | Non-PLI control basket, same model | Post-COVID recovery as the true driver |
| R4 | **Placebo break** at the longest feasible lead before true D_s | Model detecting smooth trends as breaks |
| R5 | Growth-rate specification (C.11.4) | Spurious regression / non-stationarity |
| R6 | ARMA-errors vs HAC-OLS | Inference method artefacts |
| R7 | HS-4 vs HS-6 vs HS-8 aggregation | HS-2022 reallocation breaking the series |
| R8 | ₹ crore instead of US$ mn | Exchange-rate-driven trend |
| R9 | Bai–Perron / supF unknown-break test | Does the *data-detected* break coincide with D_s? |
| R10 | Cook's distance / DFBETA; trim the March spike | Single-month outlier leverage |
| R11 | Drop the final 3 months | End-of-sample leverage on the post-segment slope |
| R12 | Log-linear vs quadratic pre-trend | Piecewise-linear mis-specification |

**R4 and R9 are the two most persuasive** and are usually the two candidates skip. Do not skip them. Both need care:

**R4 feasibility.** A 24-month lead is *not* available for the headline sector: for mobile phones D_s = Aug 2020, so a placebo at Aug 2018 leaves **4 pre-months** against 11 month dummies and a trend — the pre-segment slope is not estimable. Use the longest feasible lead (**D_s − 12**, giving 16 pre-months) and state the reduced power, or run R4 only on the three sectors where a 24-month lead is estimable. Do not quietly drop it.

**R9 will find COVID first.** An unknown-break search over 96 months containing a three-month multi-sigma shock at T = 25–27 will locate that shock before anything else. A detected break at Apr–Jun 2020 is the **expected first result and is not evidence against D_s**. Either estimate Bai–Perron on the COVID-dummied residual series, or report the full break set and interpret the *second* break. R9 also requires a declared partial-structural-change partition: **allow only the intercept and trend to break; hold the month fixed effects constant.**

**R11 note.** C.3 ends the sample at Mar 2026 precisely because it sits inside the "(R) Revised Final" window, so R11 is *not* about provisional data — it guards against end-of-sample leverage on the post-segment slope.

---

# PART D — SECTOR MAPPING RESEARCH

Full table with sources, confidence ratings and every alternative date: **`docs/archive/pli_sector_mapping_PROPOSED.csv`**. Source log: **`docs/source_log.md`**.

## D.1 Verified scheme facts for the four proposed sectors

All dates below are **[V]** from primary GoI documents (gazette notifications, PIB releases, ministry guidelines).

### 1. PLI for Large Scale Electronics Manufacturing — mobile phones

- Cabinet approval: the MeitY notification of 23.09.2021 states *"approved by Union Cabinet on **20.03.2020**"*; the corresponding PIB release (PRID 1607487) carries a **posting date of 21 MAR 2020**. A next-day posting of a 20 March decision is the ordinary reading, so this is most likely not a factual conflict. **Cite the 20.03.2020 gazette/MeitY date and note the PIB posting date — do not present it as two official sources disagreeing.**
- Gazette notification: **1 April 2020**, No. 84, CG-DL-E-01042020-218990, F. No. W-28/1/2019-IPHW-MeitY
- Guidelines: 1 June 2020
- **Effective date (para 10.5, in the original gazette): *"Incentives under the Scheme will be applicable from 01.08.2020."*** Base year: FY2019-20.
- Target segment (para 4): *"mobile phones and specified electronic components"*
- 23.09.2021 amendment: approved companies may elect any 5 consecutive years in FY2020-21…FY2025-26; *"Incentives for Year 1 will be applicable from 01.08.2020 or 01.08.2021 depending on the choice of Year 1."* **This is an applicant election, not a blanket shift** — a common misreading.
- **→ D_s = August 2020.** Alternatives for R1: 2020-03-20 (Cabinet), 2020-04-01 (notification), 2021-08-01 (elected Year 1).

### 2. PLI for Telecom and Networking Products

- Cabinet approval: **17 February 2021** (PIB PRID 1698686)
- Gazette notification: **24 February 2021**, No. 68, CG-DL-E-24022021-225442, F. No. 13-01/2020-IC
- Guidelines: 3 June 2021. Application window **4 June – 3 July 2021** (PIB PRID 1724121). *Note: the widely-repeated "1 April – 3 May 2021" window is wrong — 1 April 2021 is the effective date, not the window.*
- **Notification para 6: *"The scheme will be effective from 1st April, 2021."*** Sales base year FY2019-20; investment baseline as on 31.03.2021.
- Annexure-1 product list: core transmission equipment (DWDM, OTN, MSPP, SDH, PTN/MPLS, GPON/NG-PON OLT, digital microwave radio); 4G/5G radio access and wireless equipment; access & CPE, IoT access devices; enterprise switches and routers. Eleven products added by OM of 20 June 2022.
- **→ D_s = April 2021.**

### 3. PLI for Pharmaceuticals — bulk drugs / APIs route

Two distinct schemes exist. **Do not conflate them.**

*Bulk Drugs PLI (KSMs/DIs/APIs):* gazette text says *"approved by the Government of India on 20th March, 2020"* — note this is **Government** approval wording, not explicitly "Cabinet"; the corresponding PIB release was posted 21 Mar 2020. Notified **21 July 2020**, No. 172, CG-DL-E-21072020-220616; revised guidelines 29 Oct 2020; base year FY2019-20; **first incentive year FY2022-23 for chemical-synthesis products, FY2023-24 for fermentation products**; covers 41 named products spanning 53 identified APIs. **Greenfield projects only** — an important limitation for a trade-flow study.

*Pharmaceuticals PLI (2021):* Cabinet **24 Feb 2021**; notified **3 March 2021**, No. 76, CG-DL-E-03032021-225603; operational guidelines 1 June 2021; base year FY2019-20; **incentives on incremental sales from FY2022-23**; Categories 1 (biopharma, complex generics, patented/near-patent, cell & gene, orphan, special capsules, complex excipients, phyto-pharma), 2 (APIs/KSMs/DIs), 3 (repurposed, autoimmune, anti-cancer, anti-diabetic, anti-infective, cardiovascular, psychotropic, anti-retroviral, IVDs, drugs not manufactured in India).

- **→ D_s = April 2022** (start of FY2022-23) for both the API route and the Pharmaceuticals PLI. Convenient: a single, well-documented date, and a balanced 48/48 split.
- **Interview vulnerability to pre-empt:** the bulk-drugs PLI is greenfield-only and small in outlay relative to the sector, and it is *import-substituting* by design — its stated purpose is reducing API import dependence, not raising exports. State this explicitly and treat a null β₃ here as the *expected* result, not a failure. That framing is far stronger than pretending an export effect should exist.

### 4. PLI for White Goods — air conditioners

- Cabinet approval: **7 April 2021** (PIB PRID 1710116)
- Gazette notification: **16 April 2021**, No. 129, CG-DL-E-16042021-226671, F. No. P-29014/101/2020-LEI. Administered by **DPIIT** (not MeitY).
- Guidelines 4 June 2021; Round 1 window 15 Jun – 15 Sep 2021.
- **Para 4.2: *"The first year of investment will be FY 2021-22 and the first year of incremental sale will be FY 2022-23."*** Base year FY2019-20 (**not** FY2020-21 — a common error; the 16.08.2021 corrigendum only lets pre-qualified applicants use the higher of FY2019-20/FY2020-21 as the sales comparator).
- AC target segment: ACs and components — high-value intermediates (copper tubes, aluminium foil, compressors) and low-value intermediates (controller PCB assemblies, BLDC motors, service valves, cross-flow fans). Para 8.1: *"Mere assembly of finished goods shall not be incentivized."*
- **→ D_s = April 2022.**
- **Vulnerability:** the scheme targets *components*, and explicitly excludes mere assembly, while HS 8415 is dominated by finished units. Mapping confidence is therefore MEDIUM, and you should say so before the interviewer does.

## D.2 Data source — verified

**[V] Primary source: DGCI&S / Ministry of Commerce MEIDB (Monthly Export Import Data Bank)**, https://tradestat.commerce.gov.in/meidb/commoditywise_export

- Monthly, **HS 2/4/6/8 digit**, exports and imports, **US$ million or ₹ crore**, calendar or fiscal year framing.
- Coverage banner as at 26 Aug 2026: *"Data available: Jan 2018 to Jun 2026 ((R) Revised Final upto Mar 2026, (F) Final upto Jun 2026)."*
- **No login, no captcha.** But **no API and no bulk download** — Laravel/Livewire, server-rendered HTML tables, one POST per month per HS level (CSRF token + session cookie; fields `ddMonth`, `ddYear`, `ddCommodityLevel`, `ddReportVal`, `ddReportYear`). **Budget ~300 requests**: 96 months × three HS levels (HS-4, HS-6 and HS-8 are all required — by R7 and by the D.3 verification), plus the principal-commodity-wise pulls for the bulk-drugs mapping. At ~7.8 MB per HS-8 month the raw cache is roughly **1 GB**. Rate-limit politely, cache raw responses, make the loop resumable.
- **[V] Dynamic Data Revision Policy:** every release restates prior months of the current fiscal year. **The pipeline must re-pull, never append.** Stamp every extract with a retrieval date.
- **[V] Concordance:** an official "Composition of Principal Commodity Groups" PDF exists on an HS-2017 basis (https://ftddp.dgciskol.gov.in/dgcis/resources/pdfs/PC_composition_HSN2017.pdf). **No HS-2022-basis composition table is published** — the link labelled HS2022 actually serves the full 739-page ITC(HS)-2022 tariff schedule. Better route: MEIDB's live *Principal commodity wise all HSCode* report, which returns every HS-8 line inside a chosen principal commodity for any month — an effectively current, machine-readable concordance.
- **[V] Gap to flag:** the official concordance covers the **168 Principal Commodity groups**, not the **31 Quick-Estimate rows (30 named groups + "Other Commodities")** your current dataset uses. **No official QE-group → HS mapping is published.** This is precisely why your existing annual dataset cannot be tied to any HS-level PLI definition, and it is a clean, honest justification for rebuilding from HS.

## D.3 Classification breaks you must handle — [V] and [R]

- **[V] ITC(HS)-2017 applies to 31 Mar 2022; ITC(HS)-2022 from 1 April 2022** (India adopted one quarter after the WCO's 1 Jan 2022 date).
- **[V] Further national 8-digit reallocations from April 2024 and April 2026** — MEIDB help text warns codes may be *"dropped or re-allocated"* and units of measure changed at both points.
- **→ Three break points in any HS-8 series: Apr 2022, Apr 2024, Apr 2026.** With the study period ending Mar 2026, only **Apr 2022 and Apr 2024** bind.

**[R] — MUST VERIFY BEFORE BUILDING THE PANEL.**
HS 2022 is understood to have split heading **8517.12** (telephones for cellular networks) into **8517.13** (smartphones) and **8517.14** (other telephones for cellular networks), and to have created new heading **85.24** (flat panel display modules) with a new Chapter 85 Note 7 transferring goods in from other headings. **My confidence is high but this is not verified against India's own ITC(HS)-2022 schedule, and only India's schedule governs the MEIDB series.**

**Verification procedure (Phase 2, Step 2):**
1. Pull the same month at HS-6 and HS-8 for Mar 2022 and Apr 2022.
2. Confirm 851712 goes to zero and 851713/851714 appear.
3. Confirm the **HS-4 total for 8517** is continuous across the boundary.
4. Cross-check against the ITC(HS)-2022 schedule at https://www.dgciskol.gov.in/Itchs.aspx.

**Mitigation, decided in advance:** build the mobile-phone series as **851712 + 851713 + 851714**, i.e. summed across both vintages, so the aggregate is continuous by construction. Run R7 (HS-4 total for 8517) as the confirming robustness check. If a discontinuity survives at HS-4, add a `HS2022_t` dummy from Apr 2022 and report β₃ with and without it.

## D.4 Proposed mapping — summary

Full detail, confidence ratings and sources in `docs/archive/pli_sector_mapping_PROPOSED.csv`.

| Sector | Proposed HS basis | D_s | Mapping confidence |
|---|---|---|---|
| Mobile phones | 851712 (to Mar-22) + 851713 + 851714; HS-4 8517 as robustness | 2020-08 | **HIGH** — scheme names the product; HS lines are specific. Codes need [R] verification per D.3. |
| Telecom & networking equipment | HS-4 8517 **minus** the phone lines; plus 851762/851769-family enterprise switching/routing lines | 2021-04 | **MEDIUM** — the notification lists products, not HS codes. HS-8 line selection is analyst judgement and must be documented line by line. |
| Bulk drugs / APIs & intermediates | Ch. 29 API/intermediate lines + 2941; anchored to the DGCI&S principal-commodity group for bulk drugs rather than hand-built | 2022-04 | **MEDIUM** — 41 named products do not map one-to-one to HS-8. Using the official PC group is more defensible than a hand list. |
| Air conditioners | HS-4 8415 | 2022-04 | **MEDIUM** — scheme targets components and excludes mere assembly; 8415 is dominated by finished units. Flag openly. |
| Non-PLI control basket | **[R] to be pre-committed** | placebo | — |

**No mapping above is rated HIGH-CONFIDENCE-FINAL.** Every one requires the Phase 2 Step 2 verification pass before a single regression is run. **Flag rather than invent** — where a scheme's product list cannot be resolved to HS-8, record the ambiguity in the mapping file and carry it into the limitations section.

---

# PART E — RECOMMENDED BASELINE METHODOLOGY

One design. Not five.

## E.1 The equation

For each series s, monthly, t = 1 … 96 (Apr 2018 = 1):

```
ln(Y_st) = β₀ + β₁·T_t + β₂·Post_st + β₃·TimeAfter_st
                + Σ_{m=2}^{12} γ_m·Month_mt
                + δ·Covid_t
                + ε_st

    Post_st      = 1{ T_t ≥ T_{D_s} }
    TimeAfter_st = max(0, T_t − T_{D_s})            # note: NOT +1
    Covid_t      = 1{ t ∈ Apr–Jun 2020 }
```

Estimated by **OLS with Newey–West HAC standard errors** (lags **3** and 12 both reported).

Reported alongside it, always, as the stationarity-robust companion:

```
g_st = α₀ + α₁·Post_st + α₂·Break_st + Σ φ_m·Month_mt + Σ_k δ_k·CovidMonth_kt + u_st

    g_st         = 100 × [ ln(Y_st) − ln(Y_s,t−1) ]
    Break_st     = 1{ t = T_{D_s} }                       # absorbs the differenced β₂ spike
    CovidMonth_k = separate dummies for Apr, May, Jun AND Jul 2020
```
(φ and δ here are distinct objects from the γ and δ of the level equation — a level block dummy differences into a spike *and a reversal*. See C.11.4.)

And the volatility block:

```
σ_pre = SD(g_st | t < T_D)     σ_post = SD(g_st | t ≥ T_D)     Δσ = σ_post − σ_pre
   → also report Δσ excluding the break-month observation g_{T_D}, which straddles the break

û_st  = residuals from the growth equation above          # regime- and season-demeaned
|û_st| = θ₀ + θ₁·Post_st + Σ λ_m·Month_mt + v_st          # HAC SEs; θ₁ = MAD shift, NOT Δσ
   → primary inference on Δσ is the moving-block bootstrap CI (see C.9)
```

## E.2 Meaning of every coefficient

| Coef. | Reads as | Interpretation |
|---|---|---|
| **β₀** | Intercept | Log exports in the reference month (**April**, the omitted dummy) at T = 0 — an extrapolation one month before the sample starts. Not economically interesting. |
| **β₁** | Pre-implementation trend | Average monthly change in log exports **before** D_s. ×100 → % per month; ×1200 → approx. % per year. **The counterfactual trend.** |
| **β₂** | Immediate level shift | Discrete jump in ln(exports) at D_s. ×100 → % level change. Interpret cautiously: policies rarely produce instantaneous level jumps in trade flows; a large β₂ more often signals a mis-dated break or a one-off shock. |
| **β₃** | **Trajectory change** | Change in the monthly trend after D_s. **Post-period trend = β₁ + β₃.** This coefficient *is* CV bullet 2. |
| **γ_m** | Seasonality | Month-m deviation from **April** (the omitted month). Expect a large positive March coefficient. |
| **δ** | COVID | Log deviation during the lockdown block. **For mobile phones this is identified off three observations, all in the pre-window.** |
| **α₁** | Growth-rate shift | Change in *average monthly growth* after D_s, in stationary space. The stationarity-robust analogue of β₃ — equal to β₃ in expectation once `Break_t` absorbs the differenced level jump. |
| **θ₁** | MAD shift | Change in mean absolute deviation of the *residualised* monthly growth after D_s, HAC SEs. **A related but distinct estimand from Δσ** (under normality σ ≈ 1.2533·MAD) — report it as a MAD shift, not as "the volatility change". |

## E.3 Assumptions

1. **Correct break date.** D_s is the true switch point. Untestable directly; addressed by R1 (alternative dates) and R9 (Bai–Perron detects the break from the data).
2. **Piecewise-linear log trend.** The trend is linear in logs within each segment. If the true trend is smoothly curved, a spurious β₃ appears. Addressed by R4 (placebo break) and R12 (quadratic pre-trend). **This is the assumption most likely to be attacked and the one you must be most fluent on.**
3. **Stable, additive seasonality.** Month effects are constant across the sample. If seasonality changed post-COVID (plausible for consumer electronics), month FE mis-specify it. Check by estimating separate pre/post month effects and testing equality.
4. **No other coincident shock at D_s.** The core threat. Addressed by R3 (control basket) and by narrative treatment of tariffs, China+1 and demand recovery. **Never fully satisfied — say so.**
5. **Residuals stationary and dependence correctly handled.** Addressed by ADF on residuals, Ljung–Box, HAC, and the ARMA-errors cross-check.
6. **Exports respond to a production incentive.** PLI rewards incremental sales, domestic and export. The export series responds only insofar as the incremental capacity is export-oriented. Strong for mobile phones (export-led assembly); weak for bulk drugs (import-substituting by design). **State the mechanism per sector.**
7. **Measurement.** Trade values include re-exports [V]; nominal USD; provisional data revised.

## E.4 Limitations to state in the report, unprompted

- **Observational, single-unit design. No causal identification.** Language throughout: *post-implementation change, trajectory change, level shift, volatility change, evidence consistent with, association around implementation.*
- Only **28 pre-months** for mobile phones, and COVID sits inside them. Concretely: β₁ is estimated off 28 months net of 11 seasonal dummies, and δ off just **three** observations. Name these numbers in the report rather than waiting to be asked.
- No firm-level data; you cannot see which exporters are PLI beneficiaries. The treated group is a *product* group, not a set of treated firms — so it contains non-beneficiary output. This attenuates β₃ toward zero, meaning your estimate is conservative. **Say this — it converts a weakness into a defensible property.**
- Nominal USD; no price/volume decomposition.
- Re-exports included; assembly-heavy electronics exports embed high import content, so export value overstates domestic value added.
- HS reclassification at Apr 2022 and Apr 2024.
- Multiple overlapping policies (tariffs, FTAs, RoDTEP, scheme interactions) over the same window.
- Provisional data subject to revision.

## E.5 What would SUPPORT the CV claims

- **Bullet 1** is supported by *doing the work correctly*: a documented DGCI&S monthly HS panel, seasonality and stationarity treatment, diagnostics, HAC inference. It does not depend on any result.
- **Bullet 2** is supported by producing **two defensible ranking tables** — sectors ordered by β₃ with CIs, and by Δσ with bootstrap CIs. Strongest form: β₃ distinguishable from zero for the **pre-specified primary endpoint (mobile phones)**, sign stable across R1/R2/R5/R6, β₃^control near zero, placebo β₃ near zero, and Bai–Perron placing a break near D_s once COVID is accounted for.

## E.6 What would WEAKEN or CONTRADICT the claims

- β₃ ≈ 0 everywhere, or sign-flipping across specifications
- β₃^control of similar magnitude to β₃^treated → you have measured the post-COVID rebound. (Note the decision rule is weak by construction — see RC4; state that limitation rather than implying a test exists.)
- Placebo break (R4) yields a similar β₃ → the model is fitting curvature, not a break
- Bai–Perron (R9) places no break near D_s *after* COVID is accounted for
- Results vanish when COVID months are dropped
- HAC-OLS and ARMA-errors disagree in sign
- β₃ and α₁ disagree in sign → the level result is a non-stationarity artefact

## E.7 The reassurance that matters

**Read your CV bullets literally: neither asserts a direction, a magnitude, or statistical significance.**

> "Evaluated changes in export trajectories around PLI implementation and identified sectors with the strongest post-policy trend and volatility changes."

"Evaluated" and "identified sectors with the strongest" are satisfied by a correctly-estimated ranking **whatever the numbers turn out to be**. If β₃ is negative for two sectors and near zero for two others, the bullet still holds — you evaluated the changes and you identified which sectors moved most. A null result is a finding, and a candidate who explains why a null was the expected outcome for an import-substituting scheme is more impressive than one who found a large effect and can't defend it.

**Therefore: never adjust a window, a break date, a COVID definition or a sector list to improve a coefficient.** Your CV is safe under any result provided the method is right. It is not safe if the method is tuned — that is the one failure mode that cannot be recovered.

---

# PART F — INTERVIEW TEST

Ten hardest questions, and the specific evidence the finished project must contain to answer each.

**1. "Your dependent variable is log exports with a linear trend. That's almost certainly I(1). Why isn't your segmented regression spurious?"**
*Evidence needed:* ADF and KPSS on ln(Y) and on g_t; **Zivot–Andrews or Perron break-augmented** unit-root tests; residual ADF with Engle–Granger critical values; and the growth-rate specification (α₁) next to β₃ in the main table. *Answer:* "It tests I(1) in levels — though a standard ADF is biased toward non-rejection when there's a trend break, so I also run Zivot–Andrews. The deterministic terms absorb the trend and the residuals test stationary, using Engle–Granger critical values since ADF's own are invalid on estimated residuals. But I don't rest on any of that — I estimate the same hypothesis in first differences, entirely in stationary space, and α₁ agrees with β₃ in sign."

**2. "COVID starts five months before your mobile-phone break. How do you know β₃ isn't the recovery from the lockdown trough?"**
*Evidence needed:* β₃ under RC1/RC2/RC3, β₃^control from the same model, and Δσ with and without Mar–Sep 2020, all in the main table. *Answer:* name the direction of the bias yourself, and name **both** channels: "The collapse sits in my pre-period, depressing β₁, and the rebound sits in my post-period, steepening the post segment. Both push β₃ **upward**. My block COVID dummy absorbs the collapse but not the rebound, so a residual upward bias survives the baseline — which is why I also report the estimate with Mar–Sep 2020 dropped entirely, and the control basket's β₃."

**3. "How do you distinguish a genuine break from a smooth nonlinear trend you've mis-specified as piecewise linear?"**
*Evidence needed:* R4 placebo break at the longest feasible lead; R12 quadratic pre-trend; R9 Bai–Perron on the COVID-adjusted series. *Answer:* "The placebo break gives β₃ near zero. Bai–Perron finds COVID first, as you'd expect from a three-month multi-sigma shock — so I run it on the COVID-dummied residual series and report the full break set, and the second break is at [month]." **Do not scripted-answer this as "Bai–Perron independently locates the break" — it will find Apr–Jun 2020 first, and claiming otherwise will be caught.**

**4. "You picked HS 851713 for mobile phones. India assembles with high import content and some of that is re-exported. Are you measuring domestic production or trade routing?"**
*Evidence needed:* explicit statement that DGCI&S exports include re-exports; the import series for the same HS lines plotted alongside exports; a stated import-content caveat. *Answer:* "Gross export value, not value added. I plot the matching import series so the reader can see the gross-versus-net gap. I can't net it out with trade data alone — that needs input-output or firm-level data, and I say so."

**5. "Newey–West at 12 lags on 96 observations — how many effective degrees of freedom do you have, and what does that do to your t-stats?"**
*Evidence needed:* HAC results at lags **3** (the rule-of-thumb value for T = 96) and 12 side by side; Ljung–Box justifying the lag choice. *Answer:* "HAC doesn't cost degrees of freedom directly, but at lag 12 on T = 96 the long-run variance estimate is noisy and finite-sample coverage is poor. That's why I report both lag lengths and cross-check against ARMA errors. If they disagreed I'd trust the ARMA-error result."

**6. "Your volatility is the SD of monthly log growth, and your pre and post samples differ in length. How do you know Δσ isn't a small-sample artefact?"**
*Evidence needed:* n_pre and n_post reported next to every σ; **moving-block bootstrap CIs on Δσ** as the primary inference; the MAD-shift regression on regime- and season-demeaned residuals; Δσ with the break-straddling observation dropped. *Answer:* give the sample sizes unprompted (27 and 68 for mobile phones), then the bootstrap CI. If asked why not a simple F-test of variances: "It assumes normality and independence, and I have neither."

**7. "PLI incentivises incremental sales — domestic and export. Why should exports respond at all?"**
*Evidence needed:* a per-sector mechanism paragraph, and honest differentiation. *Answer:* "For LSEM the incentive is calibrated to global-champion assembly that is overwhelmingly export-oriented, so exports are the natural margin. For the bulk-drugs PLI the stated purpose is reducing API import dependence — I expected a null on exports and I got one, which is consistent with the scheme's design rather than a failure of it."

**8. "If I handed you the same code and a random non-PLI sector, would you find a break?"**
*Evidence needed:* R3 control basket and R4 placebo, both in the main results table — not an appendix. *Answer:* "I ran exactly that. Here are the control-basket coefficients — and I'll flag that comparing two separately-estimated β₃s gives me no standard error on the difference, so I read it descriptively. If you want a test of the contrast I'd stack the series with a Treated × TimeAfter interaction, which is a difference-in-differences and would need me to defend parallel trends."

**9. "Nominal USD. Semiconductor and commodity prices moved violently 2021–23. How much of your trend is price and how much is volume?"**
*Evidence needed:* quantity series plotted alongside value where units are consistent; explicit statement that no monthly export UVI is available at this granularity; the control comparison as the partial handle. *Answer:* "I can't decompose it — India doesn't publish a monthly export unit-value index at this HS granularity. I show quantity alongside value where the unit is stable, and the control group shares the same global price environment, so the treated-minus-control comparison partly differences prices out. It's a stated limitation, not something I've papered over."

**10. "One treated unit per sector, no counterfactual. What's your identifying assumption, and what would falsify it?"**
*Evidence needed:* an explicit assumptions section; R3, R4, R9; the limitations section. *Answer:* "The assumption is that absent PLI the pre-trend would have continued, conditional on seasonality and the COVID control. It's falsified if a comparable untreated group shows the same slope change, if a placebo date reproduces the coefficient, or if the data-detected break is far from the policy date. I test all three, and I don't claim causation — I claim a documented trajectory change around implementation."

**Three more likely to come up:**
- *"You're ranking four sectors on two statistics across twelve specifications. What's your multiple-comparisons correction?"* — "I pre-specified mobile phones as the single primary endpoint before estimating anything; the other three are secondary and I report them as such. The robustness matrix is a sign-stability check, not twelve independent tests."
- *"Why not difference-in-differences?"* — "No credible untreated control at the same aggregation; parallel trends is not defensible when the treated group is defined by product rather than by geography or firm — and none of my candidate controls has a comparable secular growth regime. I use a control basket as a descriptive comparison rather than dressing it up as identification."
- *"Why not forecast a counterfactual with ARIMA?"* — "It answers a question my analysis doesn't claim to answer, and for the mobile-phone case it would be fitted on a 28-month pre-period ending in the COVID collapse. The intervals would be too wide to discriminate anything."

**A note on how to handle these.** Do not deliver any of the above as a memorised script. The pattern that works is: name the weakness before the interviewer does, give the number, then say what you did about it. Every answer above follows that shape deliberately.

---

# PHASE 2 — IMPLEMENTATION PLAN

**Gate: nothing below begins until Parts C, D and E are signed off and the control basket is pre-committed in writing.**

### Step 0 — Housekeeping (0.5 day)
Restructure to `data/raw/` (never overwritten), `data/interim/`, `data/processed/`, `src/`, `notebooks/`, `outputs/figures/`, `outputs/tables/`, `docs/`. Resolve the two notebook copies (identical code, different stored outputs): keep the root copy as `legacy/`, delete the duplicate. Replace all `D:\PLI_Export_Project\...` paths with `pathlib` relative paths. Add `requirements.txt` with pinned versions. Delete `volatility_analysis.xlsx` and `growth_comparison.xlsx` — they are wrong and must not survive into the final repo.

### Step 1 — Freeze the mapping (1 day) — **BLOCKING**
Finalise `pli_sector_mapping.csv`: sector, scheme, ministry, Cabinet date, notification date, guidelines date, D_s, all alternative dates, HS codes, confidence rating, source URL per row. **Pre-commit, in writing: (a) the control basket, with justification against both criteria in C.4; (b) mobile phones as the single primary endpoint.** Anything unresolvable is flagged in the file, not guessed. Add a CSV-parse assertion (every row must yield the same field count as the header) to the pipeline's validation step — this file has already had one silent field-shift bug.

### Step 2 — Verify HS continuity (0.5 day) — **BLOCKING**
Execute the D.3 verification procedure against MEIDB. Confirm the 851712 → 851713/851714 transition empirically. Confirm HS-4 continuity across Apr 2022 and Apr 2024. Record findings in `docs/source_log.md`. **If the mobile-phone series is not continuous at HS-4, stop and re-scope before proceeding.**

### Step 3 — Build the pipeline (2 days)
`src/fetch_meidb.py` — CSRF-token POST loop, one request per month per HS level (~300 requests, ~1 GB cached), raw HTML written to `data/raw/` with retrieval timestamp, polite rate limiting, resumable. `src/build_panel.py` — parse, map to sectors, assemble the 96-month panel in both US$ mn and ₹ crore. **Provision disk for the raw cache before starting.**
**Validation gates (hard assertions, pipeline fails if breached):** 96 rows per sector, no gaps; sector sums ≤ HS-4 parent totals; monthly totals reconcile to the published PIB/DGCI&S headline within tolerance; no negatives; no zeros in a series that should be continuous; every extract carries a retrieval date.
Outputs: `data/processed/monthly_panel.csv` + a data dictionary.

### Step 4 — Exploratory time-series analysis (1 day)
Per sector: level and log plots with D_s marked; STL decomposition; ACF/PACF; ADF and KPSS; seasonal sub-series plot; monthly growth distribution; 6-month rolling SD. Output: `outputs/figures/`, plus a written EDA note. **Read these before running any regression** — this is where data errors surface.

### Step 5 — Segmented regression (1.5 days)
Baseline E.1 per sector, plus the growth-rate companion **including `Break_t` and the four COVID month dummies**. Full residual diagnostics: ACF, Ljung–Box (12, 24), Durbin–Watson, Breusch–Godfrey, heteroskedasticity, ADF on residuals (Engle–Granger critical values), ADF/KPSS and Zivot–Andrews on the series. HAC at lags **3** and 12; ARMA-errors cross-check. Output: `outputs/tables/its_results.csv` and a formatted regression table with β₁, β₂, β₃, α₁, all SEs and CIs.

### Step 6 — Volatility analysis (1 day)
σ_pre, σ_post, Δσ, %Δσ, with n_pre/n_post, reported in **% per month** (not √12-annualised). 6-month rolling SD charts. Levene; MAD-shift regression on **regime- and season-demeaned residuals** (not full-sample-demeaned |g − ḡ|); moving-block bootstrap CIs as primary inference. Δσ **with and without the break-straddling observation**. COVID-excluded variants for every sector. Δσ-vs-mean-size scatter as visual confirmation only. Output: `outputs/tables/volatility_results.csv` + the ranking table.

### Step 7 — Robustness (2 days)
R1–R12 in full. R4 and R9 are mandatory, not optional — subject to the feasibility notes in C.12 (R4 needs a shortened lead for mobile phones; R9 must be run COVID-adjusted with a declared break partition). Output: `outputs/tables/robustness_matrix.csv` — one row per (sector × specification), one column per coefficient, so sign stability is visible at a glance. This single table is the most persuasive artefact in the project.

### Step 8 — Structural break corroboration (0.5 day)
Chow at D_s; Bai–Perron / supF for unknown breaks, on the COVID-adjusted series, allowing only intercept and trend to break. Report the **full break set** against D_s, not just the first break. **Frame as corroboration only** — a detected break does not establish that PLI caused it, and a break at Apr–Jun 2020 is expected and is not evidence against D_s.

### Step 9 — Write-up (2 days)
Rebuild the report: research question, data with full provenance and vintage, methodology with justification per method, results, robustness, limitations, conclusion. Correct every labelling and arithmetic error from A.3 and A.5 (the "2019–2024" labelling, the 12.9 vs 12.09 CAGR, and the "7 pp" share rise that is actually 6.15 pp) and re-check every remaining number in the old report against the code. Preserve the annual descriptive layer (correctly labelled) as context. Rewrite the README to the structure in your project instructions. Build the interview-prep sheet from Parts B, E and F of this document.

### Step 10 — CV claim audit (0.5 day) — **MANDATORY FINAL GATE**
Line-by-line: each CV phrase → the exact file, table and cell that supports it. Anything unsupported gets fixed or the claim gets narrowed. Output: `docs/cv_claim_audit.md`. **Do not skip this. It is the step that makes the project safe to talk about.**

**Estimated effort: ~12–13 working days.** Steps 1 and 2 are blocking and must be signed off before Step 3.

---

## Standing interview-vulnerability register

Carry these forward and add to them as you go.

| # | Vulnerability | Mitigation | Status |
|---|---|---|---|
| V1 | Mobile-phone pre-period is only 28 months and contains COVID; the rebound sits in the post-period and is **not** absorbed by the block COVID dummy, leaving a residual upward bias in β₃ | RC1–RC3, control basket, FTPA long-history check; name the bias direction unprompted | Open |
| V2 | HS-2022 reallocation could break the electronics series | Sum across vintages; HS-4 robustness; empirical verification in Step 2 | **Blocking** |
| V3 | Bulk-drugs PLI is import-substituting and greenfield-only — an export effect is not the expected outcome | State the mechanism per sector; frame a null as expected | Open |
| V4 | AC PLI targets components and excludes assembly; HS 8415 is finished units | Declare mapping confidence MEDIUM up front | Open |
| V5 | Telecom HS-8 line selection is analyst judgement | Document line by line; HS-4 robustness | Open |
| V6 | No price/volume decomposition | Quantity cross-check; control comparison; stated limitation | Open |
| V7 | Re-exports and import content in electronics | Plot matching imports; stated limitation | Open |
| V8 | Product-level treatment contains non-beneficiary output | Frame as attenuation → conservative estimate | Open |
| V9 | Existing report/README contain two arithmetic errors and a period-labelling error | Full rewrite in Step 9; re-check every number against code | Open |
| V10 | Existing exported tables (volatility, growth acceleration) are wrong | Delete in Step 0 | Open |
| V11 | R4 placebo is not estimable at a 24-month lead for the headline sector | Use D_s − 12 for mobile phones; state reduced power | Open |
| V12 | R9 Bai–Perron will detect COVID before D_s | Run COVID-adjusted; report the full break set; declare the break partition | Open |
| V13 | Control comparison has no standard error on β₃^t − β₃^c | Declare descriptive in the baseline; offer the stacked interaction as a named extension | Open |
| V14 | Multiplicity across 4 sectors × 2 statistics × 12 specifications | Pre-specify mobile phones as the single primary endpoint, in writing, before estimating | Open |
| V15 | Unit-root pre-test is itself break-contaminated (Perron 1989) | Zivot–Andrews / Perron break-augmented tests; Engle–Granger critical values on residuals | Open |
