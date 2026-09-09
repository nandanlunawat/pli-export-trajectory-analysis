# Research Design Memo — LOCKED SPECIFICATION

**Project:** PLI Scheme — Export Trajectory, Counterfactual and Volatility Analysis
**Version:** 1.0 (locked)
**Date:** 28 August 2026
**Status:** Design locked. No trade data downloaded. No models estimated. Stop condition in §10 governs.

**Companion files**

| File | Contents |
|---|---|
| `03_mapping/hs_mapping_master.csv` | Every basket: old code → new code → continuity rationale → source |
| `02_policy_sources/pli_intervention_dates.csv` | Five-way date decomposition per scheme, primary D_s and sensitivities |
| `03_mapping/control_sector_mapping.csv` | Pre-registered control baskets with justification |
| `02_policy_sources/source_log.csv` | 34 sourced claims with confidence grades |
| `08_report/data_quality_report.md` | Data provenance, known defects, open risks |
| `04_clean_data/master_monthly_exports.csv` | Schema only — population blocked by §10 |

---

## §1 — HS CLASSIFICATION CONTINUITY: RESOLVED

### 1.1 What was actually done

Continuity was established from **Indian government classification instruments**, not from WCO correlation tables and not from commercial HS websites. Three primary documents carry the result:

1. **DGCI&S ITC(HS)-2017, Chapter 85** — the schedule "implemented at DGCI&S from April 2017". Gives the *old* Indian 8-digit structure.
2. **DGFT Notification No. 54/2015-20 dated 09.02.2022**, Annexure-II — the official 8-digit list of every ITC(HS) code **DELETED** and every code **created** at the HS2017 → HS2022 transition, across Chapters 1–97. This is the decisive document.
3. **DGFT Notification No. 08/2023 dated 29.05.2023**, Annexure-I — the same for the Finance Act 2023 changes (w.e.f. 01.05.2023), which is what the **April 2024** DGCI&S code directory contains.

Plus Budget TRU letters for 2025-26 and 2026-27 to close out the April 2026 directory.

**A documented gap, stated plainly.** CBIC's *"Correlation of Customs Tariff between 2021 and 2022"* was located and authenticated — its Annexure-I correlation-code scheme (SF / DF / NF / DP / NP) was read in full. Its Annexure-II 8-digit table could not be read past Chapter 28–29 on any mirror because PDF text extraction truncates, and CBIC's canonical URL is JavaScript-gated. **The SF/DF/NF letter codes for our chapters are therefore NOT VERIFIED.** DGFT Notification 54 was substituted: it records additions and deletions rather than correlation letters, which answers the substantive question — did the codes change, and is the basket closed — without the letter grades.

### 1.2 The design principle

> **An analytical basket is the union of every code that carried the product in any vintage, defined at whatever digit level makes that union closed. The basket, not the code, is the analytical variable.**

This is what makes the series economically consistent rather than merely code-stable, and it is why the mobile-phone series survives a split that would destroy any single-code series.

### 1.3 Verified continuity — the four baskets

| Basket | Old codes | New codes | Union used | Verdict |
|---|---|---|---|---|
| **B1 Telephone sets** | `851711`, `851712`, `851718` | `851711`, `851713` Smartphones, `851714` Other cellular telephones, `851718` | **851711 + 851712 + 851713 + 851714 + 851718** | **Continuous — empirically confirmed** |
| **B2 Pharmaceuticals** | `3003` + `3004` | unchanged | **3003 + 3004** | **Fully continuous — zero changes** |
| **B3 Air conditioners** | `8415` | unchanged | **8415** | **Fully continuous — cleanest series in the design** |
| **B4 MMF fabrics** | 14 codes named in the PLI notification | unchanged | **the 14 codes** | **Fully continuous — zero changes** |

### B1 — TWO transitions, not one *(amended 29 Aug 2026 under approved Change Proposal 001)*

The original design assumed a single classification transition at April 2022 and a three-code union. **Direct observation of MEIDB falsified both.** Values are US$ million, HS-6, retrieved 29 Aug 2026 (`01_raw_data/raw_trade_data/meidb_continuity_probe_2026-08-29.csv`).

| HS-6 | Dec-2021 | **Jan-2022** | Mar-2022 | **Apr-2022** | Mar-2024 |
|---|---|---|---|---|---|
| 851711 | 0.32 | **33.06** | 3.08 | 4.87 | 0.23 |
| 851712 | **775.78** | **230.90** | 503.82 | 153.52 | 0.00 |
| 851713 Smartphones | — | — | — | **498.26** | 1,988.42 |
| 851714 | — | — | — | **2.06** | 1.23 |
| 851718 | 1.39 | **272.16** | 306.77 | 33.13 | 0.45 |
| 851770 Parts | 26.26 | 27.20 | 31.33 `*` | **0.00** `*` | — |
| 851771 / 851779 | — | — | — | **6.45 / 23.33** | 8.99 / 35.54 |

**Transition 1 — January 2022.** `851712` halves while `851718` rises **196-fold** and `851711` **103-fold**, with no new codes appearing. This is the date the Customs Tariff moved to HS2022 (Fifth Schedule to the Finance Act 2021, w.e.f. 01.01.2022) while the DGCI&S statistical directory still offered only the HS2017 code set — so HS2022 declarations were mapped onto the nearest legacy codes and cellular handsets landed in the residual lines. A 196-fold jump in "other telephone sets" is not an economic event.

**Transition 2 — April 2022.** `851713`/`851714` first appear, `851770` falls to exactly **0.00** and is replaced by `851771`/`851779`, and heading `8524` appears. This is the DGCI&S directory switch, consistent with the ITC(HS)-2022 title page *"(EFFECTIVE FROM 1ST APRIL, 2022)"*.

**Jan–Mar 2022 is a contamination window** in which the flow splits across `851711`, `851712` and `851718`.

**Consequence.** The originally locked three-code union showed a **70% collapse** into January 2022 and understated March 2022 by **38%** — pure artefact. Both transitions fall **inside B1's post-intervention window** (D_s = Aug 2020), so this would have biased β₃ directly. The five-code union — the complete **8517.1x telephone-sets group** — is closed under both transitions and is economically coherent: *telephone sets of all kinds*. The non-cellular content it adds is immaterial in undisturbed months: December 2021 `851711 + 851718` = **1.71** against `851712` at **775.78**, i.e. **0.22%**.

### What B1 is, and what it is not

> **B1 is an HS-based export proxy for the mobile-phone segment of the PLI-LSEM scheme. It is not a measure of PLI-covered output.**

Three gaps between the basket and the policy, all of which must be stated in the report rather than left implied:

1. **The basket is broader than the scheme's target.** PLI-LSEM's target segment is *"mobile phones and specified electronic components"*, with invoice-value tiers. The 8517.1x group additionally contains line telephone sets with cordless handsets (`851711`) and other telephone sets (`851718`). These are immaterial in undisturbed months (0.22% at Dec-2021) but they are **included by construction** — they are the price of a series that survives the Jan-2022 reclassification, not an assertion that they are PLI goods.
2. **The basket contains non-beneficiary output.** It captures *all* Indian exports of telephone sets, by every exporter, whether or not that exporter is an approved PLI applicant. Firm-level beneficiary data is not public, so the treated unit is a **product group**, not a set of treated firms. This attenuates β₃ toward zero, which makes the estimate conservative — a property worth stating explicitly rather than a defect to conceal.
3. **The basket is gross export value.** DGCI&S exports include re-exports, and assembly-heavy handset exports carry high import content, so the series measures gross trade value rather than domestic value added or PLI-incentivised incremental sales.

**Correct phrasing throughout the project:** *"exports of telephone sets (HS 8517.1x), the closest continuous HS proxy for the mobile-phone segment targeted by PLI-LSEM"*. **Never** *"PLI mobile-phone exports"* or *"exports covered by the PLI scheme"*.

**Pre-specified robustness:** a `Transition_t` dummy for **Jan 2022 – Apr 2022** in the B1 segmented regression, β₃ reported with and without. Declared before estimation.

**Residual issue.** Even on the wider basket, January 2022 sits **31%** below December 2021 where the same month a year earlier fell only **4%**. The dip survives at HS-4, so it is *not* within-8517 leakage — it is either genuine or leakage into another heading. Four months cannot distinguish; assess on the full series.

**B1 — electronics, March 2024 → April 2024.** Within heading 8517 the April 2024 directory dropped only `85176240` (HDSL) and `85176950` (Subscriber end equipment), with description substitutions at `85176230`, `85176270`, `85176960`. **None of `85171300`, `85171400`, `85177100`, `85177910`, `85177990` changed.** The mobile basket is untouched. April 2026: no change to 8517 at all.

**A third break point, flagged.** The 2017 schedule shows `85171210` / `85171290`; the codes deleted in 2022 were `85171211` / `85171219` / `85171290`. An **undated intermediate national 8-digit change** occurred between April 2017 and December 2021. This is a third reason never to build this series at 8-digit — and it is exactly the kind of thing that would have silently corrupted an 8-digit panel.

**B3 — air conditioners.** The string `8415` **does not occur anywhere** in DGFT Notification 54 Annexure-II, which enumerates every deleted and every new 8-digit code across all 97 chapters. Finance Act 2023's Chapter 84 amendments were confined to headings 8414 and 8419. Finance Acts 2025 and 2026 touch `8415 90 00` on rate only. Nothing entered, nothing left, nothing renumbered, at any point.

**B2 — pharmaceuticals.** Zero rows for `3003` or `3004` in DGFT Notification 54 Annexure-II. Chapter 30 absent from the Finance Act 2023 amended-chapter list. Budget 2025-26 TRU letter: *"Chapters 30 to 32: No change"*.

**B4 — MMF fabrics.** None of the 14 Annexure-II codes appears in any change instrument. Chapters 54 and 60 have **zero rows** in DGFT Notification 54. Chapter 55's only HS2022 change was the `5501.10` aramid split; Chapter 58's only change was heading `5802` (terry towelling), and code `580632` sits in heading 5806. April 2024: the only Chapter 54 change was heading `5402`. April 2026: *"Chapters 42 to 59: No change"*, *"Chapter 57-65: No Change"*.

### 1.4 What was ruled OUT — and why this matters

Three candidate series were tested and **rejected on continuity grounds**. Each rejection is a finding, and each is a trap avoided.

| Rejected | Reason |
|---|---|
| **Any Chapter-85 aggregate** | New heading `8524` was created at HS2022 fed partly from `90138010`/`90138090` — **Chapter 90, outside Chapter 85**. Goods entered the chapter from outside it. A Chapter-85 total has a genuine upward break in 2022. `8524` was then *completely renumbered* in April 2024 (6 codes → 24). |
| **Heading 3002 (biologicals)** | `30021100` (Malaria diagnostic test kits) was deleted from Chapter 30 outright with no successor inside 3002. Heading 3006 has the same problem via `30062000`. Genuine downward breaks. |
| **MMF apparel (PLI Annexure-I)** | HS2022 collapsed headings 6201/6202 from an article-based structure (overcoats `..11/..12/..13/..19`, anoraks `..91/..92/..93/..99`) into a fibre-based one (`..20` wool, `..30` cotton, `..40` MMF, `..90` other). ~24 codes deleted, ~16 created. A union is constructible but merges two article headings the post-2022 data cannot separate — not like-for-like. |

**Conditional, not load-bearing:** heading `2941` (antibiotics) is continuous through HS2022 and April 2024, but the Finance Act 2025 created or modified 18 tariff items in Chapter 29 w.e.f. 01.05.2025 *without the government TRU letter itemising the headings*. Whether 2941 is among them is **NOT VERIFIED**. Do not build a headline result on 2941.

### 1.5 The one thing not done, and the protocol to close it

**No MEIDB query was executed.** MEIDB is a client-rendered application — a plain HTTP GET returns the form shell and the string `Loading…`, with no data — and no browser was available to this session. Every continuity finding above therefore rests on **classification documents**, not on observed values.

This matters because of one specific fact. MEIDB's help page states:

> *"ITC HS Code of the Commodity is from latest HS Code Directory provided by DGCIS Kolkata on April 2024."*

MEIDB serves the **entire 2018-onward series under a single current code directory**, not under the vintage in force at the time of each observation. Whether historical values were genuinely re-mapped, or simply relabelled with dropped codes flagged by `*`, cannot be settled from documents.

**Verification protocol — run before building the panel. Four queries, ten minutes.**

| # | Query | Pass criterion | Fail meaning |
|---|---|---|---|
| V1 | Commodity-wise, HS-6, **March 2022** and **April 2022**, US$ mn. Read `851712`, `851713`, `851714`. | Union total (`851712+851713+851714`) shows no discontinuity; individual codes may switch | If the union jumps, the re-mapping is lossy — stop and re-scope |
| V2 | Same for **December 2021** and **January 2022** | Establishes whether the series break is **Jan-2022** (customs tariff date) or **Apr-2022** (DGCI&S statistical date) | Either answer is fine for B1 — the union is invariant. Record which, for the data quality report |
| V3 | Specific HSCode `8517`, HS-6, **March 2024** and **April 2024** | HS-4 8517 total continuous; `851713`/`851714` unchanged | If broken, the April-2024 directory did more than DGFT Notification 08/2023 records |
| V4 | Specific HSCode `8415` and `3004`, HS-6, **March 2022 / April 2022** and **March 2024 / April 2024** | No structural discontinuity | Contradicts the documentary finding — investigate before proceeding |

Also record verbatim: the coverage banner, the `Data last updated on` date, and whether any description in the baskets is prefixed with `*` (a dropped code).

**Gate:** V1 and V3 must pass before `master_monthly_exports.csv` is populated.

---

## §2 — FINAL SECTOR SELECTION

### 2.1 Scoring, 1–5, on the eight stated criteria

| # | Criterion | Electronics | Pharma | White Goods | Textiles | Telecom |
|---|---|---|---|---|---|---|
| 1 | Quality of official PLI definition | **5** | 4 | 4 | **5** | 4 |
| 2 | Quality of HS-code mapping | **5** | 4 | 3 | **5** | 2 |
| 3 | Continuity through HS revisions | **5** | **5** | **5** | **5** | 3 |
| 4 | Length of pre-policy history | **1** | 4 | 4 | **5** | 3 |
| 5 | Length of post-policy history | **5** | 4 | 4 | **1** | 4 |
| 6 | Economic relevance of export response | **5** | 3 | 2 | 3 | 3 |
| 7 | Forecasting feasibility | **1** | 4 | 4 | **5** | 2 |
| 8 | Interview defensibility | 4 | 4 | 4 | 4 | 2 |
| | **Total /40** | **31** | **32** | **30** | **33** | **23** |

**Scoring notes that carry weight.**

- *Criterion 1, Textiles = 5:* the Textiles PLI is the **only** scheme of the fourteen whose notification publishes HS annexures. The Ministry of Textiles tells you the codes. Every other sector requires analyst judgement.
- *Criterion 2, White Goods = 3:* heading 8415 is dominated by finished units, while the scheme targets **components** and states *"Mere assembly of finished goods shall not be incentivized."* A real mismatch, declared up front.
- *Criterion 4, Electronics = 1:* 28 pre-policy months, with COVID inside them. Binding constraint on everything. **Irreducible** — January 2018 is the start of official Indian monthly HS-level dissemination (verified 2 Sep 2026; `08_report/backward_extension_feasibility.md`), not a window this project chose.
- *Criterion 6, White Goods = 2:* AC exports are small and the scheme is component/import-substitution oriented. An export response is not the primary expected channel.
- *Criterion 7:* computed, not judged — see §4.3. Electronics supports **zero** validation origins at any usable horizon.
- *Criterion 8, Telecom = 2:* the basket is defined by analyst judgement rather than by the scheme, which is the first thing an interviewer will attack.

### 2.2 Verdict on the stated preference

> **Your preference — Electronics, Pharmaceuticals, White Goods as core, Textiles optional — remains appropriate. Adopt it, with two amendments.**

**Amendment 1 — Textiles is promoted from "optional" to a defined-role robustness sector.** It scores highest on the criteria as stated, and it is the only sector that can carry the forecasting-methodology validation. Its role is specific: *(a)* the forecast-protocol showcase (31 validation origins at h=12 against 7 for the core sectors); *(b)* the only scheme with official HS annexures, so it demonstrates what a gold-standard mapping looks like; *(c)* a late-intervention sector where a large export response would be **surprising** — which makes it a useful check on whether the method finds effects everywhere.

**Amendment 2 — Telecom is dropped.** Lowest total (23/40), weakest mapping, not forecast-validatable at the primary horizon, and — decisively — its basket is *heading 8517 minus the phone lines*, which **overlaps B1 in the same HS-4 heading**. Two treated series carved from one heading with different intervention dates is an unforced methodological problem.

**Note on the scoring, honestly.** Textiles topping the table is an artefact of criteria 1–3 and 7 rewarding data quality, while criterion 5 (post-policy history) is where it fails badly with 24 months. The CV claims are about *post-policy* trend and volatility change, so post-policy history deserves more weight than a flat 1–5 average gives it. **The scoring informs the decision; it does not make it.** That is why Textiles is the robustness sector and not a core one.

### 2.3 Locked selection

| Basket | Sector | Role | HS basis | N_pre | N_post |
|---|---|---|---|---|---|
| **B1_MOBILE** | Electronics — telephone sets | **CORE** (primary endpoint) | 851711 + 851712 + 851713 + 851714 + 851718 | 28 | 68 |
| **B2_PHARMA** | Pharmaceuticals — formulations | **CORE** | 3003 + 3004 | 48 | 48 |
| **B3_AC** | White Goods — air conditioners | **CORE** | 8415 | 48 | 48 |
| **B4_TEXTILE** | Textiles — MMF fabrics | **ROBUSTNESS** | the 14 Annexure-II codes | 72 | 24 |
| C1, C2, C3 | Controls — see §8 | robustness layer | see mapping file | — | — |

**On the pharmaceuticals basket — a correction to Phase 1.** Phase 1 proposed a bulk-drugs/API basket. That is now **rejected**: the bulk-drugs PLI is greenfield-only and explicitly import-substituting, and the API codes sit in the parts of Chapter 29 that HS2022 *did* churn. The 2021 **Pharmaceuticals PLI** is the better target — its Category 1 (biopharmaceuticals, complex generics, patented/near-patent-expiry, cell and gene therapy, orphan drugs) and Category 3 (repurposed, autoimmune, anti-cancer, anti-diabetic, anti-infective, cardiovascular, psychotropic, anti-retroviral drugs) are **formulations**, which map to headings 3003 + 3004. Those headings have perfect verified continuity. Better mapping, better continuity, clearer mechanism.

---

## §3 — INTERVENTION DATES

### 3.1 Five-way decomposition

| | **Electronics** | **Pharmaceuticals** | **White Goods** | **Textiles** |
|---|---|---|---|---|
| Cabinet approval | 2020-03-20 † | 2021-02-24 | 2021-04-07 | NOT VERIFIED ‡ |
| Notification | 2020-04-01 | 2021-03-03 | 2021-04-16 | 2021-09-24 |
| Guidelines | 2020-06-01 | 2021-06-01 | 2021-06-04 | 2021-12-28 |
| Application window | R1 closed 2020-07-31; R2 2021-03-11→31 | not verified | 2021-06-15 → 2021-09-15 | not verified |
| Operational / effective | **2020-08-01** | duration from FY2020-21; gestation FY2021-22 | first *investment* year FY2021-22 | in force from issuance; gestation FY2022-23→FY2023-24 |
| First incremental-sales year | FY2020-21 | **FY2022-23** | **FY2022-23** | **FY2024-25** |
| **PRIMARY D_s** | **2020-08** | **2022-04** | **2022-04** | **2024-04** |

† MeitY's 23.09.2021 notification states *"approved by Union Cabinet on 20.03.2020"*; the corresponding PIB release carries a **posting date** of 21 MAR 2020. A next-day posting of a 20 March decision is the ordinary reading — cite 20.03.2020 and note the posting date; do **not** present this as two official sources disagreeing.
‡ Neither the PIB release nor the notification states a calendar approval date. Only the PIB posting date of 08 SEP 2021 is verifiable.

### 3.2 Selection rule and why the dates are not equated

**Rule: D_s is the start of the first period in which incremental sales accrue toward a claim.**

The justification is economic, not administrative. PLI pays on *incremental sales*. Cabinet approval and gazette notification are **announcement** events — they may trigger anticipatory investment, but they do not change the marginal return on producing one more exported unit. That return changes when the first performance period opens. Choosing the notification date for Pharmaceuticals would place the break **thirteen months** before any incremental sale could be claimed.

**Electronics is the one case where the dates genuinely coincide, and the scheme says so.** Gazette para 10.5, in the *original* 1 April 2020 notification: *"Incentives under the Scheme will be applicable from 01.08.2020."* That is not the notification date and not the Cabinet date — it is the operational date, and it is the first incentive date. D_s = August 2020 is read off the instrument, not inferred.

**White Goods states the distinction explicitly**, which is why it is unambiguous — notification para 4.2: *"The first year of investment will be FY 2021-22 and the first year of incremental sale will be FY 2022-23."*

### 3.3 Sensitivity analysis on dates — pre-specified

Three families, all run in R1, all reported whatever they show:

1. **Alternative institutional dates.** Electronics: 2020-04 (notification), **2021-08** (elected Year 1 under the 23.09.2021 amendment — note this is an *applicant election*, not a blanket shift). Pharma: 2021-03 (notification), 2021-04 (gestation start). White Goods: 2021-04 (notification / first investment year), 2023-04 (2-year gestation option). Textiles: 2021-09 (notification), 2022-04 (gestation start).
2. **Symmetric perturbation.** D_s ± 3 months, all sectors. Tests whether the result is knife-edge on the exact month.
3. **Implementation lag.** D_s + 3 and D_s + 6 months. Rationale: capacity installation, qualification and export order cycles mean a production incentive cannot move shipments instantaneously. If β₃ is materially larger at D_s + 6 than at D_s, that is *informative about the response lag* — report it as such, do not adopt it as the headline.

**Rule: the primary D_s is fixed now and does not move.** Any lag specification is reported alongside, never in place of, the primary.

---

## §4 — FORECASTING DESIGN (COUNTERFACTUAL)

### 4.1 Structure

```
[------------ TRAINING (pre-policy only) ------------][-- FORECAST --]
 Apr-2018 .................................. D_s − 1  D_s ... D_s+h−1
                                                       ↑
                                     counterfactual vs actual compared here
```

Model selection happens **entirely inside the pre-policy window** by rolling-origin validation. **Post-policy data is never touched until a single model has been selected and frozen.** This is the whole point of the design and it must be enforced in code, not by discipline: the panel is split at D_s and the post-policy slice is not loaded during the selection step.

### 4.2 Candidate models

| # | Model | Role |
|---|---|---|
| 1 | **Seasonal naïve** — ŷ(t+h) = y(t+h−12) | Mandatory benchmark. Any model that cannot beat it is discarded. |
| 2 | **ETS** — automatic error/trend/season selection over additive and multiplicative forms, damped and undamped | Primary candidate |
| 3 | **SARIMA** | **Conditional only.** Admitted if and only if the pre-policy residual diagnostics justify it — specifically, if ETS residuals fail Ljung-Box at lag 12 or 24, or if the ACF/PACF of the seasonally differenced series shows structure ETS cannot represent. If ETS residuals are clean, SARIMA is not fitted. |

Nothing else. No Prophet, no LSTM, no XGBoost, no ensembling. The reason to exclude them is not that they are bad; it is that their assumptions cannot be explained in an interview in one sentence, and they buy nothing here.

### 4.3 Which sectors can actually support this — the decisive arithmetic

Rolling-origin (expanding-window) validation with minimum training length **m = 30 months** (2.5 seasonal cycles — an ETS with 12 seasonal states plus level, trend and smoothing parameters needs at least two full cycles plus residual degrees of freedom):

> **number of validation origins at horizon h  =  N_pre − h − m + 1**

| Sector | N_pre | h = 6 | h = 12 | h = 18 |
|---|---|---|---|---|
| **B1 Electronics** | 28 | **−7 → infeasible** | **−13 → infeasible** | infeasible |
| **B2 Pharmaceuticals** | 48 | 13 | **7** | **1** |
| **B3 White Goods** | 48 | 13 | **7** | **1** |
| **B4 Textiles** | 72 | 37 | **31** | **25** |
| *Telecom (dropped)* | *36* | *1* | *−5 → infeasible* | *infeasible* |

**This table is the single most important finding for the forecasting request, and it is bad news for the headline sector.**

**Electronics cannot support a validated forecast counterfactual.** With 28 pre-policy months there is no horizon at which even one validation origin exists. Relaxing m to 24 does not fix it (h=6 gives −1). Only by dropping to m = 12 — which admits *seasonal naïve alone*, since ETS and SARIMA cannot be fitted on 12–24 months of seasonal data — do origins appear (11 at h=6, 5 at h=12). But then **model selection is impossible**: you would be reporting seasonal naïve because it is the only thing that fits, not because validation chose it.

**Decision, and it is a real constraint you should not paper over:**

- **Primary forecasting deliverable: B2, B3, B4 only.** Full protocol, full model selection, full metrics.
- **B1 Electronics: EXCLUDED from model-selected forecasting.** It receives the **explicitly defined seasonal-naïve benchmark only** — `ŷ(t+h) = y(t+h−12)` — at h = 6 and h = 12, reported in a clearly separated subsection headed *"no model selection was possible"*. ETS and SARIMA are **not fitted** for B1. The output must be labelled **"seasonal-naïve benchmark, not model-selected"** everywhere it appears: in the results table, in every figure caption, and in the report text. It is an honest benchmark, not a chosen model. Say so in the report and say so in the interview.
- ~~**Optional route to a validated electronics counterfactual via FTPA long history**~~ — **CLOSED AS NOT VIABLE, 2 September 2026.** The gate was to confirm FTPA's group list before relying on it. Confirmed directly: FTPA reaches back to January 2010 but is **neither HS-level nor truly monthly** — its Detailed Report returns 191 Principal Commodity groups with **cumulative fiscal-year-to-date** value columns. Worse, the nearest group to B1 is **P4 TELECOM INSTRUMENTS**, which merges handsets with base stations and transmission equipment — i.e. it fuses B1 with the **Telecom sector deliberately dropped in Phase 2**. The Phase-1 assumption of a usable "electronics group" was wrong. Full assessment in `08_report/backward_extension_feasibility.md`; open item O3 is closed.

### 4.4 Is 12 months the best primary horizon? — Yes. Four reasons.

1. **Seasonal completeness.** Twelve months is one full cycle, so the cumulative counterfactual gap is not contaminated by *which* part of the year the window happens to cover. A 6-month gap starting in April is not comparable to one starting in October; a 12-month gap always is.
2. **It is the longest horizon that can be validated.** At h = 18 the core sectors yield **exactly 1 origin** — a single error observation, from which no distribution, no mean absolute error and no interval coverage can be computed. A horizon you cannot validate is a horizon you cannot defend.
3. **Interval width.** Forecast intervals widen roughly with √h. At 18 months on a 48-month training set the counterfactual band is wide enough to contain almost any outcome, so the comparison stops discriminating.
4. **Post-policy coverage.** All four sectors have ≥ 24 post-policy months, so h = 12 is comfortably covered everywhere — including Textiles, whose 24 post-months are exactly 2 × 12.

**Locked:**

- **h = 12 — PRIMARY.**
- **h = 6 — secondary**, reported for all sectors as a short-run check (13 origins in the core sectors — the most reliably validated horizon).
- **h = 18 — reported for B4 Textiles ONLY** (25 origins), labelled exploratory. **Not reported for B2 or B3**, because one validation origin is not validation.

### 4.5 Metrics

Validation (pre-policy, per horizon, averaged across origins): **MAE**, **RMSE**, **MAPE**, and **empirical coverage of the 80% and 95% prediction intervals**.

> **MANDATORY DISCLOSURE, to appear alongside every forecasting result.** At the primary horizon **h = 12, B2 and B3 have only 7 rolling-origin validation origins each**. Seven origins is a thin basis on which to choose between candidate models: the mean RMSE differences between seasonal naïve, ETS and SARIMA will carry wide sampling uncertainty, and interval coverage estimated from 7 origins × 12 horizons is itself imprecise. **Model selection for B2 and B3 is therefore weakly identified and must be reported as such** — not as a confident determination that the selected model is best. B4 is the only basket with a comfortable margin (31 origins at h = 12). Where the RMSE gap between the winner and the seasonal-naïve benchmark is small relative to its spread across origins, say so explicitly and prefer the simpler model.

- MAPE is reported because these are strictly positive trade series with no near-zero months, so it is well-defined and scale-free — useful for comparing across sectors of very different size.
- **Interval coverage is the criterion that matters most here** and is usually the one omitted. A counterfactual whose 95% interval only contains the truth 60% of the time in validation will manufacture a spurious "gap" in the post period. If nominal coverage fails badly in validation, the counterfactual gap must be reported without significance language at all.
- **Model selection rule, fixed in advance:** lowest mean RMSE at h = 12 across validation origins, subject to 95% interval coverage falling in [0.85, 1.00]. If no candidate meets the coverage condition, seasonal naïve is used and the coverage failure is reported.

Counterfactual reporting (post-policy): actual, point forecast, 80% and 95% bands, and the **gap** in level, in per cent, and cumulatively over the horizon.

### 4.6 Language discipline — non-negotiable

The gap is **"the difference between observed exports and a pre-policy time-series counterfactual"**. It is **not** a PLI effect, not an impact, not an attributable increase.

It embeds every non-PLI thing that happened after D_s: global demand, the China+1 reallocation, the rupee, freight, tariffs under the Phased Manufacturing Programme, and — for the sectors with D_s in 2022 — the energy and geopolitical shock. The correct sentence is: *"Actual exports exceeded the counterfactual by X% over the 12 months following implementation; this is consistent with, but does not establish, a policy effect."*

---

## §5 — LONG-RUN TRAJECTORY ANALYSIS (SEGMENTED / INTERRUPTED TIME SERIES)

### 5.1 The specification

For each basket s, monthly, t = 1 … 96 (April 2018 = 1):

```
ln(Y_st) = β₀ + β₁·T_t + β₂·Post_st + β₃·TimeAfter_st
                + Σ_{m=2}^{12} γ_m·Month_mt
                + δ·Covid_t
                + ε_st

    T_t          = 1, 2, …, 96
    Post_st      = 1{ T_t ≥ T_Ds }
    TimeAfter_st = max(0, T_t − T_Ds)          ← note: NOT +1
    Covid_t      = 1{ t ∈ Apr, May, Jun 2020 }
    Month        = 11 dummies, April omitted as reference
```

Estimated by **OLS with Newey–West HAC standard errors**, reported at lag **3** (the rule-of-thumb ⌊4(96/100)^(2/9)⌋ = ⌊3.96⌋ = 3 — the rule floors, it does not round) **and** at lag 12 (one seasonal cycle).

**B1 only — pre-specified additional term (Change Proposal 001).** Add `Transition_t = 1{ t ∈ Jan 2022 … Apr 2022 }` to absorb the two-stage HS2022 reclassification, which falls *inside* B1's post-intervention window. **Report β₃ both with and without it.** Declared before estimation; it does not apply to B2, B3 or B4, whose codes did not change.

### 5.2 Coefficients

| Coefficient | Meaning | Reported as |
|---|---|---|
| **β₀** | Log exports in April (the omitted month) at T = 0 — an extrapolation one month before the sample. Not economically interesting. | — |
| **β₁** | **Pre-implementation trend.** Average monthly change in log exports before D_s. This is the counterfactual trend. | ×100 = % per month; ×1200 ≈ % per year |
| **β₂** | **Immediate level shift** at D_s. Because TimeAfter = 0 at the break month, β₂ is a clean level jump. Interpret cautiously — trade flows rarely jump discretely, so a large β₂ usually signals a mis-dated break or a one-off shock rather than a policy response. | ×100 = % level change |
| **β₃** | **Change in trajectory.** The difference between the post- and pre-implementation trend. **Post-period trend = β₁ + β₃.** This coefficient is the analysis. | pp per month, HAC SE, 95% CI |
| **γ_m** | Month-m deviation from April. Expect a large positive March coefficient (Indian fiscal year-end). | — |
| **δ** | COVID block deviation. **For Electronics this is identified off three observations, all in the pre-window** — state that number. | — |

**On the TimeAfter convention.** With `max(0, T − T_Ds)`, TimeAfter = 0 at the break month, so β₂ reads as the level shift. Under `max(0, T − T_Ds + 1)` the fitted jump becomes β₂ + β₃ and β₂ alone no longer reads as a level shift. β₃ is the slope change under either convention. State the convention in the report — it gets probed.

### 5.3 Why log exports

1. **Coefficients become percentages**, which makes β₁ and β₃ directly comparable across sectors spanning three orders of magnitude — from AC exports to pharmaceutical formulations.
2. **Multiplicative seasonality becomes additive**, so month fixed effects are the correct functional form rather than an approximation. Trade seasonality is proportional, not absolute: March is *x per cent* above average, not *x million dollars* above.
3. **Variance stabilisation.** Export series are heteroskedastic in levels — dispersion scales with the level. Logs largely remove that.
4. **First differences of logs are growth rates**, which is exactly the volatility input in §6, so one transform serves both analyses.

### 5.4 Why month fixed effects are required

Indian monthly export data has strong, stable seasonality — a pronounced fiscal-year-end surge in March, plus festival and shipping-cycle effects. Omitting it does three separate kinds of damage:

1. **Omitted-variable bias in β₃.** If the pre- and post-windows contain different numbers of high-season months — which they generally will, since D_s falls mid-year for Electronics — the seasonal pattern loads onto the trend terms.
2. **Grossly inflated and serially correlated residuals**, which corrupts every standard error in the model.
3. **It contaminates the volatility measure.** Seasonal swings would be counted as volatility, and any change in the pre/post seasonal composition would show up as a spurious Δσ.

**Why estimated jointly rather than by pre-filtering.** Do not seasonally adjust first and then regress. The decisive reason is **break-smearing**: a two-sided filter spreads a genuine break across the months either side of it, strongly attenuating β₂ and locally distorting β₃. This is precisely why X-13 carries LS/AO outlier regressors for known breaks. Estimating month FE inside the equation keeps the adjustment auditable in one table and keeps the break sharp.

STL is used for two purposes only: a descriptive trend/seasonal/remainder exhibit, and a robustness re-estimation. That robustness variant **inherits the break-smearing problem**, so its β₂ is a lower bound — say so.

### 5.5 Autocorrelation — four layers

1. **Diagnose.** ACF and PACF of residuals; Ljung–Box at lags 12 and 24; Durbin–Watson; Breusch–Godfrey.
2. **Baseline inference: Newey–West HAC** at lags 3 and 12. Report both; if they disagree materially, say so.
3. **Cross-check: regression with ARMA errors** (SARIMAX with exogenous regressors). If HAC-OLS and ARMA-errors agree in sign and rough magnitude, the result is not an inference artefact. If they disagree, ARMA-errors is the more credible number.
4. **Stationarity — the spurious-regression defence.** ln(Y) is plausibly I(1) with drift, and a segmented regression on a trending non-stationary series is exposed to spurious inference. Four parts:
   - ADF **and** KPSS on ln(Y) and on g_t — they test opposite nulls, report both.
   - **Zivot–Andrews or Perron break-augmented** unit-root tests. Perron (1989): a standard ADF on a series with a trend break is biased *toward* non-rejection of the unit root, so the premise "ln(Y) is I(1)" may itself be a break artefact. You cannot invoke a structural break for the model and then use a break-blind unit-root test on the same series.
   - ADF on fitted residuals, **using Engle–Granger critical values** — standard ADF critical values are invalid on residuals containing estimated parameters. Treat as suggestive.
   - **The growth-rate companion, reported next to β₃ in the main table:**
     ```
     g_st = α₀ + α₁·Post_st + α₂·Break_st + Σ φ_m·Month_mt + Σ_k δ_k·CovidMonth_kt + u_st
            g_st     = 100 × [ ln(Y_st) − ln(Y_s,t−1) ]
            Break_st = 1{ t = T_Ds }
            CovidMonth = separate dummies for Apr, May, Jun AND Jul 2020
     ```
     α₁ is the change in average monthly growth after D_s, estimated entirely in stationary space. **Two details the naive version gets wrong:** differencing the level model turns the β₂ level jump into a **one-month spike at t = T_Ds** (hence `Break_t`), and turns a level *block* COVID dummy into a spike at April 2020 **plus a reversal at July 2020** (hence month-specific dummies including July). If β₃ and α₁ agree in sign, the trajectory finding survives the spurious-regression attack.

---

## §6 — VOLATILITY

### 6.1 Definition

```
g_t     = 100 × [ ln(Y_t) − ln(Y_{t−1} ) ]         monthly log growth, LOG-GROWTH POINTS (lgp)
σ_pre   = SD(g_t | t ∈ pre-window)                  lgp
σ_post  = SD(g_t | t ∈ post-window)                 lgp
Δσ      = σ_post − σ_pre                            absolute change, lgp
%Δσ     = 100 × Δσ / σ_pre                          relative change in the SD, per cent
rolling = 6-month rolling SD of g_t, plotted with D_s marked
```

> **Notation, binding on all downstream reporting.** `g_t` is measured in **log-growth points (lgp)** — percentage points of log change — **not** in percentage growth. The two coincide only for small moves and diverge sharply otherwise: −275.8 lgp is a simple change of −93.7%, and +222.2 lgp is +822%. Never write a log-growth figure with a "%" growth label. Where a simple percentage change is genuinely meant, compute `100 × (exp(g/100) − 1)` and label it as such. `%Δσ` is exempt: it is a ratio of two standard deviations and is a genuine percentage.

**Standard deviation of export levels is not used anywhere in this project.** It is a scale measure, not a volatility measure: it rises mechanically with sector size and with trend strength, so it ranks the largest sectors as the most volatile regardless of their actual variability. σ here is computed on **log differences** and is therefore scale-free **by construction** — the old defect cannot recur, and that is an analytic property, not something a correlation needs to demonstrate.

**Report σ in log-growth points per month, not √12-annualised.** Annualising by √12 assumes serially independent growth — the very assumption §5.5 spends its length rejecting. If an annualised figure is wanted for readability, give it alongside the monthly figure and state the assumption.

### 6.2 Comparison windows — FIXED NOW, BEFORE ANY DATA IS SEEN

**Primary: symmetric ±24 months around D_s.** Equal sample sizes remove the unequal-n objection, and 24 months is exactly two seasonal cycles on each side. Feasible for all four baskets — verified against the actual window lengths.

| Basket | D_s | Pre-window (24 obs) | Post-window (24 obs) |
|---|---|---|---|
| **B1 Electronics** | 2020-08 | **Aug 2018 – Jul 2020** | **Aug 2020 – Jul 2022** |
| **B2 Pharmaceuticals** | 2022-04 | **Apr 2020 – Mar 2022** | **Apr 2022 – Mar 2024** |
| **B3 White Goods** | 2022-04 | **Apr 2020 – Mar 2022** | **Apr 2022 – Mar 2024** |
| **B4 Textiles** | 2024-04 | **Apr 2022 – Mar 2024** | **Apr 2024 – Mar 2026** |

**Secondary: full available windows** — B1 27/68, B2 47/48, B3 47/48, B4 71/24 growth observations (one fewer than the level count on the pre side, since g_t is undefined at t = 1).

**Tertiary: full windows excluding March–September 2020.**

*Note the asymmetry the symmetric windows create, and do not hide it:* B1's pre-window contains COVID at its **end**, while B2's and B3's pre-windows contain COVID at their **start**. That is what the tertiary windows are for.

**The symmetric windows are for the volatility comparison only. The ITS in §5 uses the full 96-month window** — restricting it to ±24 would discard 44 months of post-policy data for Electronics and destroy the trajectory estimate.

### 6.3 Inference on Δσ

1. **Levene / Brown–Forsythe** equality-of-variance test. Robust to non-normality; **not** robust to serial correlation — say so.
2. **MAD-shift regression on regime- and season-demeaned residuals.** Do *not* regress |g_t − ḡ| on Post using a full-sample mean: if mean growth shifts at D_s — which is the trajectory hypothesis — a full-sample demeaning makes the coefficient pick up the **mean** shift, conflating the two hypotheses by construction.
   ```
   û_t   from  the §5.5 growth equation
   |û_t| = θ₀ + θ₁·Post_t + Σ λ_m·Month_m + v_t        HAC SEs
   ```
   θ₁ is a shift in **mean absolute deviation**, not in σ (under normality σ = √(π/2)·MAD ≈ 1.2533·MAD). Report it as a MAD shift. Note û is an estimated regressand, so HAC SEs understate uncertainty here.
3. **Moving-block bootstrap CI on Δσ — the primary inference.** It is the only layer that handles both serial dependence and the generated-regressand problem.

**Also report:** the **break-straddling observation.** The first post-window growth observation is ln Y(T_Ds) − ln Y(T_Ds − 1), which spans the break and contains the entire β₂ level jump. If β₂ ≠ 0 it inflates σ_post. Report Δσ with and without it.

### 6.4 Ranking

Sectors ranked by Δσ and by %Δσ, each with bootstrap CIs and n_pre / n_post shown alongside. A ranking without intervals is a ranking of noise.

---

## §7 — COVID TREATMENT

### 7.1 The principled definition, fixed in advance

**`Covid_t = 1` for April, May and June 2020.**

Chosen on the **policy and epidemiological event**, not on model fit: India's national lockdown was imposed from 25 March 2020, with phased unlocking beginning June 2020. The merchandise export collapse and its sharpest rebound fall in these three months. This definition is set here, before estimation, and **does not move regardless of what it does to any coefficient.**

**A caveat that must be in the report:** the collapse was **not universal**. Pharmaceutical exports rose through the lockdown under the essential-goods exemption — the legacy annual data shows Drugs & Pharmaceuticals up **23.5%** in FY2020-21 while Man-made Yarn fell **17.7%**. Do not describe April–June 2020 as a uniform export collapse.

### 7.2 The two models

**Baseline:** as specified in §5.1, with `Covid_t` included.

**COVID-adjusted robustness:** March 2020 – September 2020 **dropped from estimation entirely**. This is the strongest test — it removes the disruption rather than modelling it, at the cost of 7 observations.

Both are reported side by side in the main results table for every sector. Two further variants (widening the block to Mar–Sep 2020 as a dummy; month-specific dummies rather than a block) go in the robustness matrix.

### 7.3 How conclusions could change — stated in advance

**Electronics is where this bites, and the bias has two channels, not one.** With D_s = August 2020, the April–June 2020 collapse sits in the **pre**-window and the July 2020 – March 2021 rebound sits in the **post**-window. The collapse depresses β̂₁; the rebound steepens the post segment. **Both push β₃ upward.** The block `Covid_t` dummy absorbs the collapse but **not the rebound** — and widening it to September 2020 still leaves October 2020 – March 2021 of rebound inside the post segment. **A residual upward bias in β₃ survives the baseline specification.** Name this yourself before an interviewer does.

The sign of the bias in **Δσ is ambiguous**, because the rebound inflates σ_post as well as σ_pre.

**For B2, B3 and B4 the COVID window sits well inside the pre-period**, so it affects the level of β₁ and the training data for the forecast, but not the break itself.

**For the forecasting counterfactual:** the training windows for B2, B3 and B4 all contain COVID. Fit on the **full pre-policy window including COVID** — so nothing is cherry-picked — and report a robustness fit treating April–June 2020 as outlier-adjusted. If the two counterfactuals differ materially, report both bands.

**Decision rule:** if the sign of β₃ flips between the baseline and the COVID-adjusted model for any sector, **that is the headline finding for that sector** and must be reported as such, not buried.

---

## §8 — CONTROL GROUP

### 8.1 Status

A control group is a **robustness layer**. It is not there to manufacture a causal claim, and the design does not make one. Full detail in `03_mapping/control_sector_mapping.csv`.

### 8.2 Pre-registered basket *(C2 replaced 29 Aug 2026 under approved Change Proposal 002)*

| ID | Control | HS basis | Matched to | HS-6 continuity | Why |
|---|---|---|---|---|---|
| **C1** | Leather goods | **Chapter 42 only** | General | **Clean — 0 rows** | Manufactured, labour-intensive, discretionary consumer end-use, same OECD buyer base, same rupee/freight/COVID exposure. Slow secular growth, no policy break. |
| **C2** | **Footwear** | **Chapter 64** | General; consumer-durable comparator for **B1** and **B3** | **Clean — 0 rows** | A finished, manufactured, **discretionary consumer durable sold into OECD retail** — the closest available structural analogue among non-PLI categories to air conditioners and consumer electronics. Large, long-established export line. Shares the treated sectors' exposure to global retail demand, freight rates, the rupee, and the COVID collapse and rebound. |
| **C3** | **Cotton woven fabrics** | **Headings 5208–5212** (70 HS-6 codes) | **B4 Textiles** | **Clean — 70 codes identical at both vintages** | **The strongest control in the design.** Same *product* (woven fabric), same industry, often the same mills, same buyers, same logistics — differing **only in fibre**, which is precisely the boundary the PLI Scheme for Textiles itself draws: the scheme covers **only** MMF apparel, MMF fabrics and technical textiles. |

**C3 narrowed 29 Aug 2026 under approved Change Proposal 003, Option 1.** It previously spanned all of Chapter 52 plus the cotton lines of Chapters 61/62 — four different value-chain stages. Two problems: (i) B4 is MMF *fabrics*, so a control mixing raw cotton, yarn, fabric and apparel was not stage-matched, and raw cotton (5201–5203) is an **agricultural commodity** driven by crop cycles, MSP and India's periodic export restrictions — drivers wholly absent from the treated series; (ii) the Chapter 62 cotton lines were **discontinuous** (`620112`/`620192`/`620212`/`620292` pre-April-2022 only; `620130`/`620230` after — the 6201/6202 article-to-fibre merger). Narrowing to woven fabrics restores the fibre-only contrast **and removes the only discontinuity in the control set**.

**Full code lists for all three controls are enumerated in `03_mapping/control_hs6_codes.csv`** — C1 = 20, C2 = 25, C3 = 70, total 115 HS-6 codes, every one verified present at both the Mar-2019 and Apr-2024 vintages, with zero overlap between controls and zero overlap with any treated basket.

**Why C2 changed.** The former C2 — ceramic products and glassware, Chapters 69 and 70 — **failed HS-6 continuity**: heading `6903` was restructured (`69031010`, `69031090` deleted; `69031000` created) and heading `7019` heavily restructured (`70194000`, `70199010`, `70199090` deleted, with a large block of new `7019xx` codes). It was **replaced outright rather than trimmed**, because excising the broken headings after their data properties are known would be a post-hoc modification of a control — which is not a control.

**Candidate screen.** Continuity was applied as a hard first filter against DGFT Notification 54/2015-20 Annexure-II. **Passed:** Chapters 41, 42, 52, 63, 64. **Failed:** Ch 39 (`3907`, `3911`), Ch 68 (`6812`, `6815`), Ch 69 (`6903`), Ch 70 (`7019`), Ch 94 (`9401`, `9403`, `9404`, `9405`), Ch 95 (`9508`). Chapter 63 passed continuity but was rejected on role grounds — it duplicates C3's textile coverage. Chapter 41 was rejected as a semi-processed *intermediate* rather than a finished consumer good. Full screen in `docs/CHANGE_PROPOSAL_002_control_basket.md`.

**Consequential narrowing of C1.** C1 previously included headings `6403`/`6405` (leather footwear). Adopting Chapter 64 as C2 would have overlapped it, so **C1 is narrowed to Chapter 42 only**. This is a de-overlap forced by the C2 decision, not a results-driven adjustment — no treatment result had been computed or observed. The three controls now share no codes.

**Pre-registration statement.** C2 was selected on 29 August 2026 against HS-6 continuity, economic comparability and common export-shock exposure. **No treatment result of any kind had been computed or observed** — no regression, no growth rate, no volatility figure. The only trade values seen in this project are the 100 classification-probe observations covering six boundary months, read solely to establish code continuity.

**Verified absent from PLI:** leather, footwear and cotton are not among the official 14 sectors. Note that *food products* **is** a PLI sector, so marine and processed-food categories are unusable as controls.

### 8.3 Declared idiosyncratic risks

Stated now, not discovered later.

- **C2 footwear — China+1 sourcing reallocation.** Footwear is among the categories most affected by the global shift away from Chinese sourcing. This cuts both ways: it is a *shared* shock that a control should absorb, but it also means footwear is partially "treated" by the same reallocation the design is trying to net out. **This is the most important limitation of C2 and must be stated in the report.**
- **C2 footwear — growth regime and labour intensity.** Footwear grows slowly while mobile assembly scaled rapidly; the control matches shock *exposure*, not growth *rate*. It is also more labour-intensive, so more exposed to lockdown labour disruption than, say, pharmaceutical formulations.
- **C2 footwear — Quality Control Orders.** India has introduced QCOs covering footwear. Primarily import-facing standards, but they may have affected domestic producers. **Dates and scope NOT VERIFIED** — flagged as a check, not asserted.
- **C3 cotton fabrics** carry cotton-specific input-price shocks not shared with MMF: the 2021-22 global cotton price spike and India's April 2022 cotton import-duty exemption. Note these reach C3 through the *input* channel only — raw cotton itself is excluded from the basket, so the direct agricultural-policy channel (export bans, MSP) does not enter.
- **Rejected earlier and still rejected:** gems & jewellery (dominated by re-export routing — the same structural defect flagged for the treated series — plus the 2022 Russian rough-diamond sanctions) and marine products (US antidumping actions).

### 8.4 The limitation that must be stated

**There is no within-industry control for mobile phones.** Every adjacent electronics assembly category is either directly PLI-covered (mobile components, IT hardware, telecom equipment) or PLI-adjacent through the same component ecosystem and the same Phased Manufacturing Programme tariff changes. C1, C2 and C3 are general comparators, **not industry matches**, and the B1 comparison is weaker for it. This is a real weakness of the headline sector and belongs in the limitations section, unprompted.

### 8.5 How the comparison is reported

**Which D_s is applied to a control.** A control basket has no intervention of its own, so it has no intrinsic D_s. Each control is therefore estimated **once per treated sector, using that treated sector's own primary D_s as a placebo break date**:

| Control run | D_s applied | Compared against |
|---|---|---|
| C1 / C2 / C3 with D_s = **2020-08** | B1's date | β₃ for **B1** |
| C1 / C2 / C3 with D_s = **2022-04** | B2's date | β₃ for **B2** |
| C1 / C2 / C3 with D_s = **2022-04** | B3's date | β₃ for **B3** |
| C1 / C2 / C3 with D_s = **2024-04** | B4's date | β₃ for **B4** |

Because B2 and B3 share D_s = 2022-04, that control run is estimated once and serves both. This yields **three distinct control estimations per control basket** (2020-08, 2022-04, 2024-04) — nine control regressions in total.

Every other element of the specification is held identical to the treated run at that date: the same 96-month window, the same month fixed effects, the same `Covid_t` definition, the same `TimeAfter = max(0, T − T_Ds)` convention, and the same Newey–West HAC lags. The **only** thing that differs between a treated run and its matched control run is the series.

`Transition_t` (the Jan–Apr 2022 reclassification dummy) is **B1-specific and is not applied to any control**, since no control basket's codes changed at that boundary.

Estimate the identical model on each control and report β₃^control **alongside** β₃^treated at the matching date.

**State the caveat rather than implying a test exists:** two separately estimated coefficients have no standard error on their difference, so "β₃^control ≈ β₃^treated" has no decision rule. Two honest options — *(a)* declare the comparison **descriptive**, which is the baseline choice here; or *(b)* stack treated and control with a `Treated × TimeAfter` interaction, which yields the contrast and its SE directly. Option (b) **is** a difference-in-differences whatever it is called; if taken, own the label and defend parallel trends. **Baseline = (a); (b) offered as a named extension.**

### 8.6 Gate — mostly cleared

**CLEARED 29 August 2026. Both blocking checks are done.**

1. **DGFT Notification 08/2023 (the April 2024 directory) read end to end.** Chapters **42 and 64 have zero entries** anywhere — not in Annexure-I (codes and policy conditions), not in Annexure-II (description revisions), not in Annexure-III. The chapters that do appear are 03, 04, 09, 10, 12, 13, 19, 27, 29, 31, 38, 39, 48, 52, 54, 57, 61, 62, 63, 69, 71, 84, 85, 87, 98. Chapter 52's only entry is at heading **5201** (8-digit split of raw cotton by staple length) — outside the C3 basket entirely.
2. **HS-6 line lists enumerated** in `03_mapping/control_hs6_codes.csv`: C1 = 20, C2 = 25, C3 = 70. Every code verified present at **both** the Mar-2019 (ITC(HS)-2017) and Apr-2024 (ITC(HS)-2022) vintages. Mutual exclusivity verified programmatically: zero overlap between controls, zero overlap with any treated basket, no duplicates.

**One non-blocking item remains:** verify the footwear Quality Control Order dates and scope, for the limitations section.

---

## §9 — DATA ARCHITECTURE

Created and in place:

```
PLI_Export_Project/
├── 01_raw_data/
│   ├── raw_trade_data/              ← MEIDB cached responses, one file per (month × HS level), never overwritten
│   └── legacy_annual_data/          ← copy of the original annual xlsx, preserved
├── 02_policy_sources/
│   ├── pli_intervention_dates.csv   ← five-way date decomposition + primary D_s + sensitivities
│   └── source_log.csv               ← 34 sourced claims, confidence-graded
├── 03_mapping/
│   ├── hs_mapping_master.csv        ← old code → new code → rationale → source, per basket
│   └── control_sector_mapping.csv   ← pre-registered controls
├── 04_clean_data/
│   └── master_monthly_exports.csv   ← SCHEMA ONLY, population blocked by §10
├── 05_analysis/                     ← notebooks and src
├── 06_results/                      ← regression and volatility tables, robustness matrix
├── 07_figures/
├── 08_report/
│   ├── research_design_memo.md      ← this file
│   └── data_quality_report.md
├── 99_legacy/                       ← original notebook, figures, report — preserved, not deleted
└── docs/                            ← Phase 1 forensic audit
```

The Phase 1 notebook, figures and report have been **moved to `99_legacy/`, not deleted**. The two exported tables identified as methodologically wrong (`volatility_analysis.xlsx`, `growth_comparison.xlsx`) are preserved there for the audit trail but must not be cited.

---

## §10 — STOP CONDITION

### 10.1 Resolved — design is locked on these

| Item | Status |
|---|---|
| Final sectors | **LOCKED** — B1 Electronics, B2 Pharmaceuticals, B3 White Goods (core); B4 Textiles (robustness). Telecom dropped. |
| Exact HS/product baskets | **LOCKED as amended** — §1.3 and `hs_mapping_master.csv`. B1 widened to the 8517.1x group under approved Change Proposal 001. |
| Classification continuity | **RESOLVED** from Indian government primary sources **and confirmed by direct observation of MEIDB** — §1.3, §1.4 |
| Intervention dates | **LOCKED** — §3, `pli_intervention_dates.csv` |
| Study window | **LOCKED** — April 2018 – March 2026, 96 months |
| Forecast horizon | **LOCKED** — h = 12 primary, h = 6 secondary, h = 18 for B4 only |
| Forecasting candidates | **LOCKED** — seasonal naïve, ETS, SARIMA conditional on diagnostics |
| Control basket | **PRE-REGISTERED as amended** — C1 leather (Ch 42, narrowed), **C2 footwear (Ch 64, replacing ceramics/glassware)**, C3 cotton (§8), subject to the two residual checks in §8.6 |
| Volatility windows | **FIXED** — symmetric ±24 months, §6.2 |
| COVID treatment | **FIXED** — Apr–Jun 2020, §7.1 |

### 10.2 Open — must clear before the panel is built

| # | Open item | Blocking? |
|---|---|---|
| ~~O1~~ | ~~MEIDB empirical continuity confirmation~~ | **CLEARED 29 Aug 2026.** V1–V4 run. Two transitions found, not one; B1 basket amended under CP-001; B2/B3 confirmed clean; no HS-6 change at April 2024. |
| ~~O2~~ | ~~Continuity check on control chapters~~ | **CLEARED 29 Aug 2026.** Ch 41, 42, 52, 63, 64 clean; Ch 69, 70 failed → C2 replaced under CP-002. |
| **O2b** | Confirm Chapter 64 has no rows in DGFT Notification 08/2023 Annexure-I (April 2024 directory) | **YES**, before controls are used |
| **O5** | Fix the exact HS-6 line lists for C1, C2, C3 | **YES**, before controls are used |
| **O6** | On the amended B1 basket, Jan-2022 still sits 31% below Dec-2021 against a 4% seasonal fall a year earlier, and the dip survives at HS-4 | No — assess on the full series; `Transition_t` already pre-specified |
| **O3** | Confirm FTPA group list, start date and units, if the long-history electronics forecast route is wanted | No — only if §4.3 option is taken |
| **O4** | Finance Act 2025 Third Schedule — whether heading 2941 gained new tariff items w.e.f. 01.05.2025 | No — only if 2941 is ever used |
| **O7** | Footwear Quality Control Order dates and scope | No — for the limitations section |

### 10.3 Next actions, in order

1. ~~Run V1–V4 against MEIDB~~ — **DONE 29 Aug 2026.** Raw observations in `01_raw_data/raw_trade_data/meidb_continuity_probe_2026-08-29.csv`.
2. ~~Clear control-chapter continuity~~ — **DONE 29 Aug 2026.**
3. **SIGN OFF THIS MEMO** as amended by Change Proposals 001 and 002 (see `docs/DECISION_LOG.md`). Then and only then:
4. Clear O2b and O5 — the two residual control checks.
5. Write `05_analysis/fetch_meidb.py` — resumable, rate-limited, one cached raw file per request, retrieval-date stamped, **re-pull never append**. *(Method note: use the All Commodities → 6 digit Level route; the Specific HSCode route 404s without the modal picker. The results grid is a DataTables table holding all ~5,150 rows client-side, so the full set can be read without paging. A query for month M, year Y returns both M-(Y−1) and M-Y, halving the request count.)*
6. Build `master_monthly_exports.csv` against the schema, with hard validation assertions (96 rows per basket, no gaps, basket ≤ HS-4 parent, monthly totals reconcile to the published DGCI&S headline within tolerance).
7. EDA → ITS → forecasting → volatility → robustness → write-up → CV claim audit.

---

## THE ONE RECOMMENDED SPECIFICATION

> **Outcome.** y = ln(monthly exports, US$ million FOB), DGCI&S/MEIDB, April 2018 – March 2026, 96 months.
>
> **Units of analysis.** Four baskets, each a *closed union* of HS codes verified continuous against Indian government classification instruments **and confirmed by direct observation of the published series**: **B1** 851711+851712+851713+851714+851718 (telephone sets — an HS-based **proxy** for the PLI-LSEM mobile-phone segment, not a measure of PLI-covered output; D_s = **Aug 2020**); **B2** 3003+3004 (pharmaceutical formulations, D_s = **Apr 2022**); **B3** 8415 (air conditioners, D_s = **Apr 2022**); **B4** the 14 PLI Annexure-II MMF fabric codes (D_s = **Apr 2024**, robustness role).
>
> **Intervention date rule.** D_s = start of the first period in which incremental sales accrue toward a claim — not the Cabinet date, not the notification date.
>
> **Trajectory.** Segmented regression `ln Y = β₀ + β₁T + β₂Post + β₃TimeAfter + month FE + δCovid + ε`, with `TimeAfter = max(0, T − T_Ds)`, OLS with Newey–West HAC at lags 3 and 12, cross-checked against ARMA errors, and reported alongside the stationary growth-rate companion `g = α₀ + α₁Post + α₂Break + month FE + COVID month dummies`. **β₃ is the estimand.**
>
> **Counterfactual.** Rolling-origin validation inside the pre-policy window only (m = 30 months minimum training); candidates seasonal naïve, ETS, and SARIMA only if diagnostics justify; selected on mean RMSE at **h = 12** subject to 95% interval coverage ∈ [0.85, 1.00]; then frozen and projected 12 months past D_s. **B2, B3, B4 only** — B1 gets a seasonal-naïve-only counterfactual, explicitly labelled as not model-selected. The gap is *not* a causal effect.
>
> **Volatility.** g = 100·Δln Y; σ_pre and σ_post over **symmetric ±24-month windows**; Δσ and %Δσ with moving-block bootstrap CIs; 6-month rolling SD; never the SD of levels.
>
> **COVID.** `Covid_t` = Apr–Jun 2020, fixed on the lockdown event. Baseline with the dummy; robustness dropping Mar–Sep 2020. For B1, the residual upward bias in β₃ from the post-window rebound is declared, not hidden.
>
> **Controls.** C1 leather goods (Ch 42, 20 codes), C2 footwear (Ch 64, 25 codes), C3 cotton woven fabrics (headings 5208–5212, 70 codes, matched to B4 on fibre *and* value-chain stage) — 115 HS-6 codes in total, every one present at both classification vintages, mutually exclusive, and pre-registered before any result was computed. Reported descriptively alongside; no causal contrast claimed.
>
> **Claim language.** Post-implementation change, trajectory change, level shift, volatility change, evidence consistent with, association around implementation. Never *caused*, never *impact*, never *attributable*.

---

**Locked elements:** the four baskets and their D_s; h = 12 as primary; the decision to exclude Electronics from the validated forecast; dropping Telecom; the C1/C2/C3 control basket; the ±24-month volatility windows; the Apr–Jun 2020 COVID definition.

**Nothing below §10.3 step 3 proceeds without it.**
