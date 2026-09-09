# DATASET VALIDATION REPORT

**Project:** PLI Scheme — Export Trajectory, Counterfactual and Volatility Analysis
**Version:** 2.0 — **POST-EXTRACTION, COMPLETE**
**Date:** 30 August 2026
**Verdict:** **ALL HARD ASSERTIONS PASS (15/15).** The panel is cleared for modelling.

---

## 1. Final sector definitions

| ID | Basket | Role | HS-6 definition | D_s | N_pre | N_post |
|---|---|---|---|---|---|---|
| **B1_MOBILE** | Telephone sets — HS proxy for the PLI-LSEM mobile-phone segment | CORE (primary endpoint) | `851711+851712+851713+851714+851718` | **2020-08** | 28 | 68 |
| **B2_PHARMA** | Pharmaceutical formulations | CORE | all HS-6 under `3003`+`3004` | **2022-04** | 48 | 48 |
| **B3_AC** | Air conditioners | CORE | all HS-6 under `8415` | **2022-04** | 48 | 48 |
| **B4_TEXTILE** | MMF fabrics | ROBUSTNESS | the 14 PLI Annexure-II codes | **2024-04** | 72 | 24 |
| **C1_LEATHER** | Leather goods | CONTROL | Chapter `42` | placebo | — | — |
| **C2_FOOTWEAR** | Footwear | CONTROL | Chapter `64` | placebo | — | — |
| **C3_COTTON** | Cotton woven fabrics | CONTROL (matched to B4) | headings `5208`–`5212` | placebo | — | — |

Controls carry no intrinsic D_s; each is estimated once per treated date (2020-08, 2022-04, 2024-04) — memo §8.5.

---

## 2. HS-6 codes per basket

| Basket | Codes in definition | Codes observed per month | Note |
|---|---|---|---|
| B1_MOBILE | 5 | **3** to 2022-03, **5** from 2022-04 | Expected: `851713`/`851714` did not exist before the HS2022 transition. The union is what makes the series continuous. |
| B2_PHARMA | all `3003`/`3004` | 20–22 | Variation is **zero-trade months**, not code deletions — every code reappears in other months |
| B3_AC | 6 | **6** every month | Perfectly stable |
| B4_TEXTILE | 14 | **14** every month | Perfectly stable |
| C1_LEATHER | 20 | **20** every month | Perfectly stable |
| C2_FOOTWEAR | 25 | **25** every month | Perfectly stable |
| C3_COTTON | 70 | **70** every month | Perfectly stable |

Mutual exclusivity (verified programmatically): C1∩C2, C1∩C3, C2∩C3, (C1∪C2∪C3)∩B1, (C1∪C2∪C3)∩B4 — **all empty**. No duplicates. Controls total **115** HS-6 codes.

---

## 3. Classification continuity

| Boundary | B1 | B2 | B3 | B4 | C1 | C2 | C3 |
|---|---|---|---|---|---|---|---|
| Jan-2022 (Customs Tariff HS2022) | transition, union closed | — | — | — | — | — | — |
| Apr-2022 (DGCI&S directory) | transition, union closed | no change | no change | no change | no change | no change | no change |
| Apr-2024 (directory refresh) | no HS-6 change | no change | no change | no change | no change | no change | no change |
| Apr-2026 (directory refresh) | no change | no change | no change | no change | no change | no change | no change |

The extracted data confirms the documentary finding directly. B1 component detail (`b1_code_detail.csv`):

| | Dec-2021 | Jan-2022 | Mar-2022 | Apr-2022 | Mar-2024 |
|---|---|---|---|---|---|
| `851711` | 0.32 | **33.06** | 3.08 | 4.87 | 0.23 |
| `851712` | **775.78** | **230.90** | 503.82 | 153.52 | 0.00 |
| `851713` | — | — | — | **498.26** | 1988.42 |
| `851714` | — | — | — | **2.06** | 1.23 |
| `851718` | 1.39 | **272.16** | 306.77 | 33.13 | 0.45 |
| **B1 union** | **777.49** | **536.12** | **813.67** | **691.84** | **1990.33** |

---

## 4. Date coverage

| Item | Specification | Observed | Result |
|---|---|---|---|
| Panel window | 2018-04 to 2026-03 | 2018-04 to 2026-03 | **PASS** |
| Months per basket | 96 | 96 for all 7 | **PASS** |
| Total rows | 672 | 672 | **PASS** |
| Duplicate (month, basket) | none | none | **PASS** |
| Source vintage | inside the (R) Revised Final range | **all 96 months flagged (R)** | **PASS** |

---

## 5. Missing observations and monthly continuity

| Check | Result |
|---|---|
| Calendar gaps | **PASS** — every month present exactly once per basket |
| Nulls | **PASS** — none |
| Negatives | **PASS** — none |
| Strictly positive (log-transform valid) | **PASS** — minimum across the whole panel is **0.86** (B3_AC, Apr-2020) |
| Dropped-code (`*`) flag | **PASS** — no basket code returned starred in any month |
| Structural zeros | **PASS** — no basket is zero in any month. `851712` reaches 0.00 from May-2022, which is the retired code behaving correctly inside a union that stays positive |

**Apr–Jun 2020 is a genuine collapse, not missing data.** B3_AC falls to 0.86, C1 to 8.68, B4 to 9.23, C3 to 12.31. All positive, all continuous, consistent with the national lockdown. B2_PHARMA *rises* over the same window — the essential-goods exemption already documented in memo §7.1.

---

## 6. Unit consistency

| Check | Result |
|---|---|
| Single unit throughout | **PASS** — US$ million, FOB, every row |
| No unit mixing | **PASS** — `export_inr_cr` empty for all rows in this extract |
| HS level | **PASS** — 6-digit for every row |
| Quantity | **PASS** — not extracted, not modelled (units change at directory revisions) |
| Currency derivation | Documented: USD derived by DGCI&S at the RBI monthly average rate (NMDS §2.6) |

**₹ crore is not yet extracted.** Robustness check R8 requires a second pass with `ddReportVal=3`; `fetch_meidb.py --currency 3` performs it. Not blocking — R8 is a robustness check, not a baseline requirement.

---

## 7. Reconciliation checks

| # | Check | Result |
|---|---|---|
| **R-1** | B1 ≤ HS-4 `8517` total, every month | **PASS** |
| **R-2** | B3 == HS-4 `8415` total, every month | **PASS** — equal within 0.02 |
| **R-3** | C3 ≤ Chapter `52` total, every month | **PASS** |
| **R-4** | Parsed HS-6 rows == MEIDB's own "India's Total Export" | **PASS** — 4-month spot-check spanning both vintages: −0.001%, 0.000%, −0.002%, −0.001%. Confirms no rows dropped by the parser |
| **R-7** | B1 == sum of its five component codes | **PASS** — within 0.02 every month |
| **R-8** | Every row carries `retrieval_date` and `vintage_flag` | **PASS** |
| R-5 | Reconcile to the published PIB headline | Superseded by R-4, which tests the same property against the portal's own total |
| R-6 | Re-pull stability | Not applicable to a first extraction. Baseline for future pulls under the Dynamic Data Revision Policy |

---

## 8. Descriptive completeness (validation only — no EDA performed)

| Basket | n | min | max | mean | first (2018-04) | last (2026-03) |
|---|---|---|---|---|---|---|
| B1_MOBILE | 96 | 26.65 | 3166.91 | 985.20 | 26.65 | 2792.22 |
| B2_PHARMA | 96 | 990.19 | 2735.13 | 1524.26 | 990.19 | 1972.06 |
| B3_AC | 96 | 0.86 | 53.79 | 24.48 | 13.83 | 39.78 |
| B4_TEXTILE | 96 | 9.23 | 119.97 | 82.76 | 71.22 | 78.89 |
| C1_LEATHER | 96 | 8.68 | 256.11 | 205.17 | 172.42 | 200.74 |
| C2_FOOTWEAR | 96 | 15.16 | 297.68 | 211.82 | 209.55 | 167.92 |
| C3_COTTON | 96 | 12.31 | 239.01 | 164.66 | 153.56 | 169.90 |

US$ million. Range and endpoint figures only, to demonstrate the series are populated and plausibly scaled. **No trends, growth rates, breaks or volatility have been computed or examined.**

---

## 9. Provenance

| Item | Value |
|---|---|
| Source | MEIDB, DGCI&S / Department of Commerce |
| Retrieval date | **2026-08-29** |
| Coverage banner (verbatim) | *"Data available:Jan 2018 to Jun 2026 ((R) Revised Final upto Mar 2026, (F) Final upto Jun 2026)"* |
| Portal last updated (verbatim) | *"Data last updated on: 13/08/2026"* |
| Query settings | EXPORTS · Commodity-wise · All Commodities 6-digit · US$ Million · Calendar Year |
| Requests | 48 (each returns two months) |
| HS-6 rows parsed per month | 5,121–5,491 |
| Raw artefacts | `01_raw_data/raw_trade_data/meidb_hs6_extract_2026-08-29/` — `panel_compact.csv`, `b1_code_detail.csv`, `reconciliation_aggregates.csv`, `extraction_manifest.json` |

**On raw preservation — stated plainly.** The in-session extraction preserved the **parsed HS-6 values** for every basket code, plus reconciliation aggregates and B1 component detail, all retrieval-date stamped and never overwritten. It did **not** archive the ~48 full HTML responses (~250 MB), because that volume cannot pass through this session. `05_analysis/fetch_meidb.py` performs full gzipped raw-response archiving when run locally, and refuses to overwrite an existing raw file. Anyone re-running it reproduces both the archive and this panel.

---

## 10. Gate

| Section | Status |
|---|---|
| 1 Sector definitions | **PASS** |
| 2 HS-6 counts and mutual exclusivity | **PASS** |
| 3 Classification continuity | **PASS** |
| 4 Date coverage | **PASS** |
| 5 Missing observations / continuity | **PASS** |
| 6 Unit consistency | **PASS** |
| 7 Reconciliation | **PASS** |

**15 of 15 hard assertions PASS. Zero failures.**

> **STOPPED FOR REVIEW.** No EDA, no regression, no forecasting, no volatility analysis has been performed. Modelling begins only on your instruction.

**Carried forward into the final report (properties, not failures):** exports include re-exports; nominal USD with no price/volume decomposition; B1 is a product-group proxy containing non-beneficiary output; the residual Jan-2022 dip in B1 that survives at HS-4 (`Transition_t` is pre-specified); C2's China+1 exposure; and the unread CBIC correlation letter codes, which leave a pure scope-change at an unchanged code not fully excluded.
