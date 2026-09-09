# Data Quality Report

**Project:** PLI Scheme — Export Trajectory, Counterfactual and Volatility Analysis
**Version:** 1.0 — pre-extraction
**Date:** 28 August 2026
**Status:** No trade data has been downloaded. This report documents provenance, known defects and open risks *before* extraction, and is to be updated after every pull.

---

## 1. Primary data source

| Attribute | Value |
|---|---|
| Source | **MEIDB** — Monthly Export Import Data Bank, DGCI&S / Department of Commerce |
| URL | https://tradestat.commerce.gov.in/meidb/commoditywise_export |
| Compiling agency | Directorate General of Commercial Intelligence and Statistics, Kolkata |
| Granularity | HS 2 / 4 / 6 / 8 digit, monthly |
| Units | US$ million (primary) and ₹ crore; quantity at 8-digit only |
| Coverage banner, verbatim, as at 28 Aug 2026 | *"Data available:Jan 2018 to Jun 2026 ((R) Revised Final upto Mar 2026, (F) Final upto Jun 2026)"* |
| Last updated (portal) | 13/08/2026 |
| Access | No login, no captcha. **Client-rendered** — a plain HTTP GET returns the form shell and `Loading…` with no data. No API, no bulk download. |
| Valuation | Exports FOB |
| Currency derivation | INR is the compilation currency; USD derived monthly at the RBI average rate (NMDS §2.6) |

**Study window:** April 2018 – March 2026, 96 months, eight complete Indian fiscal years.
**Binding constraint:** monthly HS data begins **January 2018**. January–March 2018 is discarded to obtain whole fiscal years and exact 12-month seasonal cycles.

---

## 2. Known characteristics that must be carried into the report

| # | Characteristic | Source | Consequence for this project |
|---|---|---|---|
| D1 | **Dynamic Data Revision Policy** (since 2009-10): on every monthly release, prior months of the current financial year are restated. | DGCI&S revision policy document | The pipeline must **re-pull the entire series**, never append. Every extract carries a `retrieval_date`. Two extracts taken weeks apart are not the same dataset. |
| D2 | **Exports include re-exports.** Verbatim: *"India's Imports/Exports include re-imports/re-exports also."* | MEIDB help page | Gross trade value, not domestic value added. Material for mobile phones, where assembly has high import content. Must be a stated limitation; plot the matching import series so the reader can see the gross-vs-net gap. |
| D3 | **MEIDB serves the whole series under ONE code directory.** *"ITC HS Code of the Commodity is from latest HS Code Directory provided by DGCIS Kolkata on April 2024."* Old codes *"may be either dropped or re-allocated"*; dropped ones are flagged with `*`. | MEIDB help page | Whether historical values were genuinely re-mapped or merely relabelled cannot be settled from documents. **This is the reason for verification protocol V1–V4.** |
| D4 | **Help page and front page disagree on the directory vintage.** Help says April 2024; the portal front page carries the same warning with respect to **April 2026**. | MEIDB help page vs front page | The help page appears to lag. Record which vintage is actually in force at retrieval time. |
| D5 | **Units of measure may change** at directory revisions, and exist only at 8-digit. | MEIDB help page | Quantity series are for descriptive price/volume cross-check only. Never model on them. |
| D6 | **Provisional vs revised.** `(R)` Revised Final to Mar 2026; `(F)` Final to Jun 2026. | MEIDB coverage banner | The study window ends March 2026 precisely because it sits inside the Revised-Final range. Apr–Jun 2026 is excluded as exposed to restatement. |
| D7 | **DGCI&S itself flags the comparability problem.** *"Change in ITC(HS) Coding system, especially cases for many to many changes poses challenge for maintaining comparability over time."* | DGCI&S NMDS §7.2 | The compiling agency agrees this project's core methodological concern is real. Worth citing in the report. |
| D8 | **No official QE-group → HS concordance is published.** The official concordance covers the 168 Principal Commodity groups, not the 30-group Quick Estimate taxonomy used in the legacy annual dataset. | DGCI&S PC composition PDFs | This is why the legacy annual data cannot be tied to any HS-level PLI definition, and the formal justification for rebuilding from HS. |

---

## 3. Classification continuity — status by basket

Full detail in `03_mapping/hs_mapping_master.csv`. Summary:

| Basket | Apr-2022 (HS2022) | Apr-2024 directory | Apr-2026 directory | Overall |
|---|---|---|---|---|
| **B1** 851711+851712+851713+851714+851718 | **TWO transitions** — Jan-2022 (tariff) and Apr-2022 (directory); union closed under both | No HS-6 change to the basket codes | No change | **CONTINUOUS — EMPIRICALLY CONFIRMED** |
| **B2** 3003+3004 | No change | No change | No change | **FULLY CONTINUOUS** |
| **B3** 8415 | No change | No change | Rate-only | **FULLY CONTINUOUS** |
| **B4** 14 MMF fabric codes | No change | No change | No change | **FULLY CONTINUOUS** |
| C1/C2/C3 controls | **NOT YET CHECKED** | not checked | not checked | **GATE O2** |

**Third break point flagged:** the DGCI&S ITC(HS)-2017 schedule shows `85171210`/`85171290` under subheading 851712, but the codes deleted at HS2022 were `85171211`/`85171219`/`85171290`. An **undated intermediate national 8-digit change** occurred between April 2017 and December 2021. The date is NOT VERIFIED. This is a third independent reason the mobile series must not be built at 8-digit.

**Series explicitly ruled out on continuity grounds:** any Chapter-85 aggregate (heading 8524 imported goods from Chapter 90, then was completely renumbered in 2024); heading 3002 and heading 3006 (codes deleted out of Chapter 30 with no successor); MMF apparel under 6201/6202 (article-based structure collapsed into fibre-based).

---

## 4. Verification status — what rests on what

| Evidence class | Status |
|---|---|
| PLI scheme names, dates, covered products | **VERIFIED** from gazette notifications, PIB releases and ministry guidelines |
| HS code additions/deletions at HS2022 | **VERIFIED** from DGFT Notification No. 54/2015-20 dated 09.02.2022, Annexure-II |
| HS code changes in the April 2024 directory | **VERIFIED** from DGFT Notification No. 08/2023 dated 29.05.2023, Annexure-I |
| HS code changes in the April 2026 directory | **VERIFIED** from Budget 2025-26 and 2026-27 TRU letters |
| ITC(HS)-2017 Indian 8-digit structure | **VERIFIED** from the DGCI&S Chapter 85 schedule |
| CBIC SF/DF/NF/DP/NP correlation letter codes | **NOT VERIFIED** — see §5 |
| Observed MEIDB values across any break | **NOT VERIFIED** — see §5 |
| Date DGCI&S statistics switched to HS2022 | **PARTIALLY VERIFIED** — see §5 |

---

## 5. Documented gaps — stated plainly

### G1 — CBIC correlation letter codes could not be read (non-blocking)

CBIC's *"Correlation of Customs Tariff between 2021 and 2022"* was located and authenticated; its Annexure-I correlation-code scheme (SF / DF / NF / DP / NP) was read in full. **Annexure-II, the 8-digit table, truncates at Chapter 28–29 on every mirror** because PDF text extraction hits a size cap, and CBIC's canonical URL is JavaScript-gated. Mirrors attempted: `gst.kar.nic.in`, `ipga.co.in`, `texprocil.org`, `cbic.gov.in`, `old.cbic.gov.in`, `beta.cbic.gov.in`.

**Substituted:** DGFT Notification 54 Annexure-II, which records additions and deletions rather than correlation letters. **Impact: none on the design.** The substantive question — did the codes change, and is the basket closed — is fully answered. What is missing is only CBIC's letter grade for each row.

**Residual risk:** DGFT Annexure-II captures *code* additions and deletions. A pure **scope change at an unchanged code** (CBIC's "DF") would not appear. That risk is not fully excluded for B2, B3 and B4, though it is low for headings with zero rows across all three change instruments.

### G2 — No MEIDB query was executed (BLOCKING, gate O1)

MEIDB is client-rendered and no browser was connected to this session. **Every continuity finding in this project rests on classification documents, not on observed values.** Protocol V1–V4 in `research_design_memo.md` §1.5 must be run before the panel is built. It is four queries and about ten minutes.

### G3 — HS2022 statistical adoption date (mitigated by design)

Three dates exist and they are genuinely different:

| Date | What it is | Source |
|---|---|---|
| **01.01.2022** | Customs Tariff First Schedule aligned to HS2022 by the Fifth Schedule to the Finance Act 2021 | CBIC guidance document |
| **09.02.2022** | DGFT notifies ITC(HS) 2022 Schedules | DGFT Notification 54/2015-20 |
| **01.04.2022** | DGCI&S statistical adoption | DGCI&S ITC(HS)-2022 title page: *"(EFFECTIVE FROM 1ST APRIL, 2022)"* |

April 2022 is the operative date for the published series, supported by the title page and by precedent — DGCI&S adopted HS2017 in **April 2017** despite the tariff changing on 01.01.2017 (*"Implemented at DGCI&S from April. 2017"*). **But no DGCI&S circular saying so in terms was found**, and customs declarations for Jan–Mar 2022 were already filed against the HS2022-aligned tariff.

**RESOLVED 29 August 2026 — and the assumption was wrong.** Protocol V2 was run. **There are TWO transitions, not one.**

- **January 2022** (Customs Tariff HS2022): `851712` halves 775.78 → 230.90 while `851718` rises **196-fold** (1.39 → 272.16) and `851711` **103-fold** (0.32 → 33.06), with no new codes. The statistical directory still offered only HS2017 codes, so HS2022 declarations were mapped onto the nearest legacy lines.
- **April 2022** (DGCI&S directory): `851713`/`851714`/`851771`/`851779`/`8524` first appear; `851770` falls to exactly 0.00.

The original three-code union was therefore **not** invariant — it showed a 70% collapse into January 2022 and understated March 2022 by 38%. B1 was widened to the full 8517.1x group under approved Change Proposal 001. B2, B3 and B4 remain unaffected: no code change at all, confirmed by observation.

### G4 — Heading 2941 after May 2025 (non-blocking, conditional)

Finance Act 2025 created or modified 18 supplementary notes and tariff items in Chapter 29 w.e.f. 01.05.2025, and the government TRU letter does **not** itemise the headings. Whether 2941 is affected is **NOT VERIFIED**. Not blocking, because 2941 is not used in the locked design — but it must be cleared if any API basket is ever added.

---

## 6. Validation gates for the extraction pipeline

Hard assertions. The pipeline fails, loudly, if any is breached.

| # | Assertion |
|---|---|
| A1 | Exactly 96 monthly observations per basket, April 2018 – March 2026, no gaps |
| A2 | Every basket total ≤ its HS-4 parent total, every month |
| A3 | For B1: `851711 + 851712 + 851713 + 851714 + 851718` ≤ heading `8517` total, every month |
| A4 | Monthly all-India export totals reconcile to the published DGCI&S/PIB headline within a stated tolerance |
| A5 | No negative values; no zero months in a series that should be continuous |
| A6 | Every row carries a `retrieval_date` and a `vintage_flag` |
| A7 | No basket code appears with a `*`-prefixed description (dropped code) without an explicit note |
| A8 | `hs_mapping_master.csv` and `control_sector_mapping.csv` parse to a constant field count per row — this file family has already had one silent field-shift bug |
| A9 | Re-pull, never append: a fresh extract must fully replace the prior one, and any month whose value changed by more than a stated tolerance is logged |

---

## 7. Legacy data

`01_raw_data/legacy_annual_data/india_exports_commodities.xlsx` — 31 rows × 6 fiscal years (FY2019-20 … FY2024-25), ₹ crore, matching the DGCI&S Quick Estimates 30-group taxonomy plus a residual "Other Commodities".

**Retained for the descriptive/context layer only.** Known defects, all documented in `docs/00_PHASE1_AUDIT_AND_DESIGN.md`: no source table reference, no download date, no vintage stamp, annual frequency, and no published concordance to HS (see D8). The original notebook, figures and report are preserved in `99_legacy/` — including two exported tables (`volatility_analysis.xlsx`, `growth_comparison.xlsx`) identified as methodologically invalid, which are kept for the audit trail and **must not be cited**.

---

## 8. Update protocol

This file is re-generated after every extraction run and must record: retrieval date, coverage banner verbatim, directory vintage in force, rows extracted per basket, every assertion result, any month whose value changed against the previous pull, and any newly starred or dropped code.
