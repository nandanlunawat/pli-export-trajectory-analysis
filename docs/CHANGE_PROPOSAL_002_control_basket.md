# CHANGE PROPOSAL 002 — Replacement of control basket C2

**Raised:** 29 August 2026
**Status:** **PRE-REGISTERED — adopted with the amended memo (D-002).**
**Affects:** `03_mapping/control_sector_mapping.csv` and §8 of `08_report/research_design_memo.md`.
**Decision record:** `docs/DECISION_LOG.md` entry D-002.

> **Pre-registration statement.** This basket was selected on 29 August 2026. At the time of selection **no treatment result of any kind had been computed or observed** — no regression, no growth rate, no volatility figure, no chart. The only trade values seen anywhere in this project are the 100 classification-probe observations in `01_raw_data/raw_trade_data/meidb_continuity_probe_2026-08-29.csv`, which cover six boundary months and were read solely to establish HS-code continuity. Selection was made against the three stated criteria applied to *classification documents and prior structural knowledge*, not to outcome data.

---

## 1. Why C2 had to be replaced rather than repaired

The original C2 was *Ceramic products and glassware, Chapters 69 and 70*. The D3 continuity check found **both chapters fail at HS-6**:

| Chapter | Failure | Evidence |
|---|---|---|
| **69** | Heading `6903` restructured — `69031010` and `69031090` **DELETED**, `69031000` created | DGFT Notification 54/2015-20 (09.02.2022), Annexure-II |
| **70** | Heading `7019` heavily restructured — `70194000`, `70199010`, `70199090` **DELETED**, with a large block of new `7019xx` codes (`70191300`–`70197300`) | same |

Excising `6903` and `7019` and keeping the remainder would be a **post-hoc modification of a control basket**, which is precisely what the project owner ruled out. A control chosen or trimmed after its data properties are known is no longer a control. The basket is therefore replaced outright.

---

## 2. Candidate screen — criterion 1, HS-6 continuity (applied first, as a hard filter)

Every candidate was screened against DGFT Notification 54/2015-20 Annexure-II, which enumerates every 8-digit ITC(HS) code added and deleted at the HS2022 transition across Chapters 1–97. **Zero rows for a chapter means no code in it was created, deleted or renumbered.**

| Chapter | Candidate | Rows in Annexure-II | Verdict |
|---|---|---|---|
| **41** | Raw hides, skins, leather | **0** | **PASS** |
| **42** | Articles of leather | **0** | **PASS** |
| **52** | Cotton | **0** | **PASS** |
| **63** | Made-up textile articles | **0** | **PASS** |
| **64** | **Footwear** | **0** | **PASS** |
| 39 | Plastics | `3907` restructured (`39072010`, `39072090` deleted; `39072100`, `39072910`, `39072990` created), `3911` changed | **FAIL** |
| 68 | Stone, plaster, asbestos articles | `6812` and `6815` restructured (`68151010`, `68151090` deleted; `68151100`–`68151900` created) | **FAIL** |
| 69 | Ceramic products | `6903` restructured | **FAIL** (incumbent) |
| 70 | Glass and glassware | `7019` heavily restructured | **FAIL** (incumbent) |
| 94 | Furniture and lighting | `9401`, `9403`, `9404`, `9405` all restructured (`94013000`, `94014000`, `94019000`, `94039000` deleted) | **FAIL** |
| 95 | Toys, games, sports goods | `9508` restructured (`95089000` deleted, `95082100`–`95084000` created) | **FAIL** |

Five chapters survive the hard filter: **41, 42, 52, 63, 64.**

Chapters 42 and 52 are already committed to C1 and C3. That leaves **41, 63 and 64** as genuine replacement candidates.

---

## 3. Criteria 2 and 3 — economic comparability and common shock exposure

| | **Ch 64 Footwear** | **Ch 63 Made-up textiles** | **Ch 41 Raw hides & leather** |
|---|---|---|---|
| Manufactured good | Yes — finished consumer product | Yes — finished consumer product | **No — semi-processed intermediate** |
| Demand type | Discretionary consumer durable | Household consumer, semi-durable | Industrial input |
| Buyer base | OECD retail, same as treated consumer sectors | OECD retail | Tanneries and manufacturers |
| Export scale | Large, long stable history | Large | Moderate |
| Common exposure: global retail demand | **High** | High | Indirect |
| Common exposure: container freight, rupee | **High** | High | High |
| Common exposure: COVID collapse and rebound | **High** — discretionary, retail-channel | High | Moderate |
| Overlap with C1 (Ch 42) or C3 (Ch 52/61/62) | **None** — different chapter, no shared codes | **Conceptual overlap with C3** — both textile, both largely cotton | None |
| Distinct analytical role | Consumer-durable comparator for **B1** and **B3** | Duplicates C3's textile role | Weak — different position in the value chain |

**Selected: C2 = Footwear, Chapter 64.**

**Why it is the right replacement, criterion by criterion.**

1. **HS-6 continuity (hard requirement).** Chapter 64 has **zero rows** in DGFT Notification 54 Annexure-II — no code created, deleted or renumbered at the HS2022 transition. Budget 2026-27 TRU letter states *"Chapter 57-65: No Change"*, covering the April 2026 directory. This is the same standard of evidence that qualified baskets B2, B3 and B4.

2. **Economic comparability.** Footwear is a **finished, manufactured, discretionary consumer durable sold into OECD retail** — the closest available structural analogue to air conditioners (B3) and to consumer electronics (B1) among non-PLI categories. It is a large, long-established Indian export line, so the series is thick enough to model and has a pre-2018 history if the long-window route is ever needed.

3. **Common exposure to export shocks.** Footwear shares the treated sectors' exposure to global retail demand, container freight rates and the rupee, and it took a comparable COVID collapse and rebound as a discretionary retail-channel good. That shared exposure is the entire point of the control: it absorbs the post-COVID recovery that would otherwise be mistaken for a policy effect.

4. **Analytical distinctness.** Chapter 64 shares **no codes** with C1 (Chapter 42) or C3 (Chapters 52/61/62). The three controls remain genuinely separate series rather than three views of the same trade.

5. **Definitively non-PLI.** Footwear appears nowhere in the official 14 PLI sectors (PIB Release ID 1945155).

---

## 4. Consequential change to C1 — declared, not concealed

C1 was originally *"Chapter 42 manufactures of leather **+ heading 6403/6405 (leather footwear)**"*. Adopting Chapter 64 as C2 would have made C1 and C2 overlap on the footwear headings.

> **C1 is narrowed to Chapter 42 only** — articles of leather (bags, cases, gloves, apparel).

This is a **de-overlap forced by the C2 decision**, not a results-driven adjustment. It makes C1 a cleaner construct in its own right (leather goods, not leather goods plus some footwear), and it keeps every control basket mutually exclusive. Recorded here so the change is auditable rather than silent.

---

## 5. Known idiosyncratic risks — declared in advance

A control is not required to be shock-free. It is required that its shocks be **named before estimation**, so they cannot be discovered afterwards to explain an inconvenient result.

| Risk | Assessment |
|---|---|
| **China+1 sourcing reallocation** | Footwear is one of the categories most affected by the global shift away from Chinese sourcing. This cuts both ways: it is a *shared* shock with electronics assembly, which is what a control should absorb — but it also means footwear is partially "treated" by the same global reallocation the design is trying to net out. **This is the most important limitation of C2 and must be stated in the report.** |
| **Different secular growth regime** | Footwear grows slowly; mobile-phone assembly scaled rapidly over the window. The control cannot match the treated group's growth *rate*, only its *shock exposure*. No control available in Indian trade data matches a fast-scaling assembly sector — the same limitation already declared for B1 in §8.4 of the memo. |
| **Domestic quality-control orders on footwear** | India has introduced Quality Control Orders covering footwear in recent years. These are primarily import-facing standards, but they may have affected domestic producers. **Dates and scope NOT VERIFIED** — flagged as a check to run before the control is relied upon, not asserted here. |
| **Labour intensity** | Footwear is more labour-intensive than the treated sectors, so it was more exposed to lockdown labour disruption than, say, pharmaceutical formulations. Relevant to the COVID-window comparison. |

---

## 6. Final pre-registered control set

| ID | Basket | HS basis | Role | Continuity |
|---|---|---|---|---|
| **C1** | Leather goods | **Chapter 42 only** (narrowed) | General control | **Clean** — 0 rows |
| **C2** | **Footwear** | **Chapter 64** (replacement) | General control; consumer-durable comparator for B1 and B3 | **Clean** — 0 rows |
| **C3** | Cotton textiles | Chapter 52 + cotton lines of Chapters 61/62 | Sector-matched control for B4 | **Clean** — Ch 52 and Ch 61 have 0 rows; Ch 62 changed only at `6201`/`6202`, which the cotton lines avoid |

**Unchanged and still declared:** there is **no within-industry control for mobile phones**. Every adjacent electronics category is PLI-covered or PLI-adjacent. C1, C2 and C3 are general comparators, not industry matches, and the B1 comparison is weaker for it. This stays in the limitations section.

---

## 7. Residual checks before the controls are used

| # | Check | Blocking? |
|---|---|---|
| 1 | Confirm Chapter 64 has no rows in DGFT Notification 08/2023 Annexure-I (the April 2024 directory). The Finance Act 2023 amendment list does not report Chapter 64, but this has not been confirmed by direct grep in this session. | **Yes** |
| 2 | Fix the exact HS-6 line lists for C1, C2 and C3 | **Yes** |
| 3 | Verify the footwear Quality Control Order dates and scope | No — for the limitations section |

---

## 8. Decision required

- [ ] **Accept** — C2 becomes Chapter 64 footwear; C1 narrows to Chapter 42; residual checks 1 and 2 clear before extraction.
- [ ] **Accept with variation** — substitute Chapter 63 made-up textiles (also continuity-clean, but duplicates C3's textile role).
- [ ] **Reject** — no C2 replacement; proceed with C1 and C3 only, and state the reduced control coverage as a limitation.
