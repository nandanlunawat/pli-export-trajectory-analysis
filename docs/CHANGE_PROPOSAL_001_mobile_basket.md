# CHANGE PROPOSAL 001 — Mobile-phone basket definition

**Raised:** 29 August 2026
**Status:** **PROPOSED — NOT IMPLEMENTED.** Raised under control rule 8 (document a design-affecting change; do not implement silently).
**Affects:** basket **B1_MOBILE** in `03_mapping/hs_mapping_master.csv` and §1.3, §2.3 and the specification box of `08_report/research_design_memo.md`.
**Evidence:** `01_raw_data/raw_trade_data/meidb_continuity_probe_2026-08-29.csv` (MEIDB, retrieved 29 Aug 2026).

---

## 1. What the locked design assumes

Two things, both now falsified by observation:

1. **One transition.** That the published monthly series switches from ITC(HS)-2017 to ITC(HS)-2022 at a single point, most likely **April 2022** (the DGCI&S statistical adoption date), with January 2022 relevant only to the customs tariff.
2. **A three-code union suffices.** That `851712 ∪ 851713 ∪ 851714` is closed, because `851712` was deleted and `851713`/`851714` created inside heading 8517.

Both rested on classification documents. Neither survives contact with the data.

---

## 2. What the data shows

Monthly exports, US$ million, HS-6, MEIDB, retrieved 29 Aug 2026. "—" = no row returned.

| HS-6 | Dec-2021 | **Jan-2022** | Mar-2022 | **Apr-2022** | Mar-2024 | Apr-2024 |
|---|---|---|---|---|---|---|
| 851711 line telephone sets | 0.32 | **33.06** | 3.08 | 4.87 | 0.23 | 0.02 |
| 851712 telephones for cellular networks | **775.78** | **230.90** | 503.82 | 153.52 | 0.00 | 0.00 |
| 851713 Smartphones | — | — | — | **498.26** | 1,988.42 | 1,511.38 |
| 851714 Other cellular telephones | — | — | — | **2.06** | 1.23 | 1.80 |
| 851718 Other telephone sets | 1.39 | **272.16** | 306.77 | 33.13 | 0.45 | 0.41 |
| 851770 Parts | 26.26 | 27.20 | 31.33 `*` | **0.00** `*` | — | — |
| 851771 Aerials | — | — | — | **6.45** | 8.99 | 8.03 |
| 851779 Other parts | — | — | — | **23.33** | 35.54 | 19.15 |
| 8524 (three HS-6 lines) | — | — | — | **0.95** | 6.25 | 3.68 |

`*` = description displayed with an asterisk prefix, MEIDB's marker for a code dropped from the current directory.

### Finding 1 — there are TWO transitions, not one

**January 2022.** `851712` halves (775.78 → 230.90) while `851718` rises **196-fold** (1.39 → 272.16) and `851711` **103-fold** (0.32 → 33.06). No new codes appear. This coincides exactly with the Customs Tariff moving to HS2022 on **01.01.2022** (Fifth Schedule to the Finance Act 2021), while the DGCI&S statistical directory still offered only the HS2017 code set — so HS2022 declarations were mapped onto the nearest available legacy codes, and cellular handsets landed in the residual lines `851711` and `851718`.

A 196-fold jump in "other telephone sets" is not an economic event. It is a classification artefact.

**April 2022.** `851713` and `851714` appear for the first time; `851770` goes to exactly **0.00** and is replaced by `851771`/`851779`; heading `8524` appears. This is the DGCI&S directory switch, consistent with the ITC(HS)-2022 title page *"(EFFECTIVE FROM 1ST APRIL, 2022)"*.

**Jan–Mar 2022 is therefore a contamination window** in which the mobile-phone flow is split across `851711`, `851712` and `851718`.

### Finding 2 — the specified union fails

| Basket | Dec-2021 | Jan-2022 | Mar-2022 | Apr-2022 |
|---|---|---|---|---|
| **As locked** `851712+851713+851714` | 775.78 | **230.90** | 503.82 | 653.84 |
| **Proposed** `+ 851711 + 851718` | 777.49 | **536.12** | 813.67 | 691.84 |

The locked basket shows a **70% collapse** into January 2022 that is pure artefact. At March 2022 it understates the flow by **38%** (503.82 against 813.67). For basket B1 both transitions fall **inside the post-intervention window** (D_s = Aug 2020), so this contaminates β₃ directly — the coefficient the whole project exists to estimate.

### Finding 3 — MEIDB does not re-map history

`851712` returns values for months long before HS2022 and `851713` returns none, while `851770` is displayed as `*PARTS:`. So MEIDB **retains the codes as originally filed** and merely stars those absent from the current directory. It does not restate history onto one classification. **This resolves open item U3.**

### Finding 4 — the other three baskets are clean

- **B3 `8415`:** all six HS-6 codes present with plausible values at every boundary tested. No additions, no deletions, no starring. **V4 passes.**
- **B2 `3003`+`3004`:** the same code set at every boundary. Two codes (`300342`, `300443`) return no row in some months — these are **zero-trade months, not deletions**; both appear in other months. **V4 passes.**
- **April 2024:** no HS-6 change anywhere in 8517, 8524, 8415, 3003 or 3004. The documented April-2024 changes (`85176240`, `85176950` deleted; `8524` renumbered) are **8-digit only** and invisible at HS-6. **V3 passes — and this vindicates working at HS-6 rather than HS-8.**

---

## 3. Proposed change

> **Redefine B1_MOBILE as `851711 + 851712 + 851713 + 851714 + 851718`** — the complete **8517.1x "telephone sets"** group.

**Why this basket.** It is economically coherent — *telephone sets of all kinds* — rather than an arbitrary union. It is closed under **both** transitions. And the non-cellular content it adds is immaterial in undisturbed months: in December 2021, `851711 + 851718` totals **1.71** against `851712` at **775.78**, i.e. **0.22%** of the basket. The design trades 0.2% of contamination in normal months for the removal of a 38–70% artefact in the transition window.

**Why not HS-4 8517.** That would fold in base stations, transmission apparatus, routers and parts — the dropped Telecom sector — roughly 12% of the heading and a different product with a different intervention date. Retain HS-4 8517 as the continuity cross-check it already is (`B1R_8517`), not as the basket.

---

## 4. Residual issue requiring a check, not a decision

Even on the proposed basket, January 2022 falls **31%** below December 2021 (536.12 against 777.49), where the same month a year earlier fell only **4%** (Dec-2020 418.51 → Jan-2021 400.65). The HS-4 8517 total behaves similarly (−28%).

Because the dip survives at HS-4, it is **not** explained by leakage within heading 8517. It is either genuine (a real January contraction) or leakage into a heading outside 8517. **Four months cannot distinguish these.** Assess once the full 96-month series exists, using the seasonal profile.

**Pre-specified robustness, to be added if this proposal is accepted:** a `Transition_t` dummy for **Jan 2022 – Apr 2022** in the B1 segmented regression, with β₃ reported with and without it. This is declared now, before estimation, so it cannot be chosen on results.

---

## 5. Impact if accepted

| Item | Effect |
|---|---|
| B1 basket definition | Two codes added. `hs_mapping_master.csv` row B1_MOBILE rewritten. |
| B1 intervention date | **Unchanged** — D_s = Aug 2020 |
| B2, B3, B4 | **Unchanged** — all verified clean |
| Study window | **Unchanged** — Apr 2018 – Mar 2026 |
| Sector selection | **Unchanged** |
| Volatility windows | **Unchanged** |
| Forecast design | **Unchanged** |
| New robustness item | `Transition_t` dummy for Jan–Apr 2022 on B1 |
| Documents to update | `03_mapping/hs_mapping_master.csv`; memo §1.3, §2.3, specification box; `data_quality_report.md` §3 and §5 (U2 and U3 now resolved) |

**This does not alter any research question, any intervention date, or any conclusion. It corrects the measurement of one series.**

---

## 6. Decision required

- [ ] **Accept** — B1 becomes `851711+851712+851713+851714+851718`; `Transition_t` robustness added; documents updated.
- [ ] **Accept with variation** — e.g. exclude `851711` (smaller artefact, cleaner product definition).
- [ ] **Reject** — keep the three-code union. *Not recommended: the January 2022 artefact would sit inside B1's post-intervention window and bias β₃.*

**Implemented only after the decision was recorded in `DECISION_LOG.md` (D-001).**
