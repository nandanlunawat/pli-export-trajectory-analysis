# DECISION LOG

Chronological record of design-affecting decisions, maintained under control rule 8.
Every entry records what was proposed, who approved it, when, and what changed as a result.
**No design-affecting change is implemented until it appears here as APPROVED.**

---

## D-001 — Change Proposal 001: mobile-phone basket definition

| | |
|---|---|
| **Proposal** | `docs/CHANGE_PROPOSAL_001_mobile_basket.md` |
| **Raised** | 29 August 2026, following the MEIDB continuity probe (D2) |
| **Decision** | **APPROVED** |
| **Approved by** | Project owner |
| **Approved on** | 29 August 2026 |
| **Option selected** | *Accept* — the full option as proposed, without variation |

**Evidence base.** `01_raw_data/raw_trade_data/meidb_continuity_probe_2026-08-29.csv`. Two classification transitions were observed where the design assumed one: January 2022 (Customs Tariff HS2022, `851712` halves while `851718` rises 196-fold and `851711` 103-fold with no new codes) and April 2022 (DGCI&S directory, `851713`/`851714`/`851771`/`851779`/`8524` appear and `851770` falls to exactly 0.00).

**What changes**

| Item | From | To |
|---|---|---|
| B1_MOBILE basket | `851712 ∪ 851713 ∪ 851714` | **`851711 + 851712 + 851713 + 851714 + 851718`** (the complete 8517.1x telephone-sets group) |
| B1 robustness | — | New pre-specified `Transition_t` dummy for **Jan 2022 – Apr 2022**; β₃ reported with and without |

**What does NOT change.** Intervention date (D_s = Aug 2020); baskets B2, B3, B4; study window; sector selection; volatility windows; forecast design; every research question and hypothesis. This corrects the measurement of one series and nothing else.

**Files amended under this decision**
- `03_mapping/hs_mapping_master.csv` — row `B1_MOBILE` rewritten
- `08_report/research_design_memo.md` — §1.3, §2.3, §C.12 robustness table, specification box
- `08_report/data_quality_report.md` — §3 and §5 (U2, U3 resolved)

**Implemented:** 29 August 2026, after this approval was recorded.

---

## D-002 — Change Proposal 002: replacement of control basket C2

| | |
|---|---|
| **Proposal** | `docs/CHANGE_PROPOSAL_002_control_basket.md` |
| **Raised** | 29 August 2026, following the D3 control-chapter continuity check |
| **Decision** | **APPROVED — replacement pre-registered here** |
| **Direction given** | Project owner, 29 August 2026: *replace* ceramics/glassware with a new non-PLI control basket rather than modifying it post hoc; pre-register and justify on HS-6 continuity, economic comparability and common exposure to export shocks; do not look at treatment results when choosing |

**Why C2 had to go.** Chapters 69 and 70 both fail HS-6 continuity at the HS2022 transition — heading `6903` restructured (`69031010`, `69031090` deleted; `69031000` created) and heading `7019` heavily restructured (`70194000`, `70199010`, `70199090` deleted, with a large block of new `7019xx` codes). Carving the broken headings out of the existing basket would be exactly the post-hoc modification ruled out.

**Selected replacement: C2 = Footwear, Chapter 64.** Full justification and the rejected alternatives are in the proposal document.

**Consequential change.** C1 was originally defined as *"Chapter 42 manufactures of leather + heading 6403/6405 (leather footwear)"*. Adopting Chapter 64 as C2 would have overlapped C1. **C1 is therefore narrowed to Chapter 42 only.** This is a de-overlap forced by the C2 decision, not a results-driven adjustment; no treatment result has been computed or seen.

**Files amended under this decision**
- `03_mapping/control_sector_mapping.csv` — C2 replaced, C1 narrowed
- `08_report/research_design_memo.md` — §8

**Status:** implemented in the mapping and the amended memo.

---

## D-003 — Change Proposal 003: composition of control basket C3

| | |
|---|---|
| **Proposal** | `docs/CHANGE_PROPOSAL_003_C3_composition.md` |
| **Raised** | 29 August 2026, during the O5 code enumeration |
| **Decision** | **APPROVED** |
| **Approved by** | Project owner |
| **Approved on** | 29 August 2026 |
| **Option selected** | **Option 1** — C3 = HS headings **5208–5212** (cotton woven fabrics) only |

**Evidence base.** MEIDB HS-6 code inventory read at two vintages (Mar-2019 on the ITC(HS)-2017 basis, Apr-2024 on the ITC(HS)-2022 basis) plus DGFT Notification 08/2023 Annexures I–III. Two problems drove the proposal:

1. **C3 was not fibre-matched to B4.** B4 is MMF *fabrics*; C3 as specified spanned four value-chain stages — raw cotton (5201–5203), yarn (5204–5207), fabrics (5208–5212) and apparel (Ch 61/62). Raw cotton is an agricultural commodity driven by crop cycles, MSP and India's periodic export restrictions, none of which touch MMF fabric production.
2. **The Chapter 62 cotton lines were discontinuous** — `620112`, `620192`, `620212`, `620292` exist only before April 2022; `620130`, `620230` only after (the 6201/6202 article-to-fibre merger). A control with a mid-panel break is worse than no control, because it would appear to corroborate a treated-series break.

**What changes**

| Item | From | To |
|---|---|---|
| C3 definition | Chapter 52 (all 124 HS-6 codes) + cotton lines of Ch 61/62 | **Headings 5208–5212 only** (cotton woven fabrics) |
| C3 role | Sector-matched control for B4 | **Unchanged in role, strengthened in construction** — now a fibre-only contrast |
| Raw cotton 5201–5203 | Included | **Excluded** — agricultural commodity |
| Cotton yarn 5204–5207 | Included | **Excluded** — one stage upstream |
| Cotton apparel Ch 61/62 | Included | **Excluded** — different value-chain stage; also removes the Ch 62 discontinuity |

**What does NOT change.** C1 (Ch 42) and C2 (Ch 64); baskets B1, B2, B3, B4; every intervention date; study window; volatility windows; forecast design; COVID treatment; every research question and hypothesis.

**Files amended under this decision**
- `03_mapping/control_hs6_codes.csv` — C3 rows replaced with the enumerated 5208–5212 lines
- `03_mapping/control_sector_mapping.csv` — C3 row rewritten
- `08_report/research_design_memo.md` — §8.2, §8.3, §8.6, specification box
- `08_report/DATASET_VALIDATION_REPORT.md` — created

**Implemented:** 29 August 2026, after this approval was recorded.

---

## Standing rule

An entry may be added here only after the project owner has given an explicit decision. Recording an approval that was not given, or implementing ahead of the record, breaks the audit trail that this project depends on.
