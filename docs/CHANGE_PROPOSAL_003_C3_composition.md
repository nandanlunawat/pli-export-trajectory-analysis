# CHANGE PROPOSAL 003 — Composition of control basket C3 (cotton)

**Raised:** 29 August 2026, during the O5 code enumeration
**Status:** **PROPOSED — NOT IMPLEMENTED.** Raised under control rule 8.
**Affects:** C3 in `03_mapping/control_sector_mapping.csv`, `03_mapping/control_hs6_codes.csv`, and §8.2 of `08_report/research_design_memo.md`.
**Evidence:** MEIDB HS-6 code inventory at two vintages (Mar-2019, ITC(HS)-2017 basis; Apr-2024, ITC(HS)-2022 basis), plus DGFT Notification 08/2023 Annexure-I/II.

> **No export values informed any part of this proposal.** Codes were assessed on chapter membership, product description and vintage validity only.

---

## 1. What the enumeration turned up

C3 is currently specified as *"Chapter 52 + cotton lines of Chapters 61/62"*, with the role **sector-matched control for B4**. Enumerating it surfaced three issues.

### Issue A — C3 is not actually fibre-matched to B4

**B4 is MMF *fabrics*** — the 14 codes the Ministry of Textiles names in Annexure-II are woven and knitted synthetic and artificial **fabrics** (Ch 54, 55, 58, 60). No apparel, no yarn, no fibre.

C3 as specified spans four different value-chain stages:

| Component | Headings | What it is | Matched to B4? |
|---|---|---|---|
| **C3a** cotton woven fabrics | 5208–5212 | Fabric | **YES — exact fibre-matched analogue** |
| **C3b** cotton yarn and thread | 5204–5207 | One stage upstream | Partly |
| **C3c** raw cotton, waste, carded/combed | 5201–5203 | **Agricultural commodity** | **No** |
| **C3d** cotton apparel | Ch 61/62 cotton lines | One stage downstream | No |

The whole point of C3 was that it differs from the treated basket **only in fibre**. As specified it also differs in *value-chain stage*, which dilutes exactly the property that made it the strongest control in the design.

### Issue B — raw cotton (5201–5203) has drivers the treated series does not

Heading 5201 is unginned/unprocessed cotton — an agricultural export governed by the crop cycle, minimum support prices, and India's periodic cotton export restrictions and import-duty changes. None of those touch MMF fabric production. Including it injects an entirely unrelated shock process into a control whose job is to absorb *shared* shocks.

*(An 8-digit change also sits here: DGFT Notification 08/2023 deleted `52010020` and created `52010021`–`52010025`, splitting by staple length. At HS-6 `520100` is unchanged, so this does not break an HS-6 series — but it confirms the heading is being actively re-cut for agricultural policy reasons.)*

### Issue C — the Chapter 62 cotton lines are discontinuous, exactly like B1

Comparing the two vintages:

| | Mar-2019 (HS2017) | Apr-2024 (HS2022) |
|---|---|---|
| Mens/boys cotton overcoats | `620112` | — |
| Mens/boys cotton anoraks | `620192` | — |
| **merged successor** | — | `620130` |
| Womens/girls cotton overcoats | `620212` | — |
| Womens/girls cotton anoraks | `620292` | — |
| **merged successor** | — | `620230` |
| All other Ch 62 cotton lines (20) | present | present |

This is the **same trap as B1**: two article-based headings merged into one fibre-based heading at April 2022. Taking the Apr-2024 code list at face value would produce a control with a break in the middle of the panel — and a *control* with a spurious break is worse than no control, because it would appear to validate a treated-series break.

**Everything else checks out clean.** Chapter 42 (20 codes), Chapter 64 (25 codes), Chapter 52 (124 codes) and the Chapter 61 cotton lines (25 codes) are **identical at both vintages**.

---

## 2. Proposed change

> **C3 = cotton woven fabrics, headings 5208–5212 only.**

**Rationale.** This is the true fibre-matched analogue to B4: same product (woven fabric), same industry, same mills in many cases, same buyers, same logistics, same global demand and freight exposure — differing **only in fibre**, which is precisely the boundary the PLI Scheme for Textiles itself draws. It restores the property that made C3 the strongest control in the design.

**Excluded, with reasons:**

| Component | Decision | Reason |
|---|---|---|
| C3c raw cotton 5201–5203 | **Exclude** | Agricultural commodity with unrelated drivers (crop, MSP, export restrictions) |
| C3d cotton apparel Ch 61/62 | **Exclude** | Different value-chain stage from B4; and Ch 62 carries the 6201/6202 discontinuity |
| C3b cotton yarn 5204–5207 | **Exclude from the primary; available as a named wider variant** | One stage upstream; defensible but not fibre-*and*-stage matched |

---

## 3. Options

- [ ] **Option 1 — RECOMMENDED. C3 = headings 5208–5212** (cotton woven fabrics). Tightest fibre-match to B4. Excludes raw cotton, yarn and apparel.
- [ ] **Option 2 — C3 = headings 5204–5212** (cotton yarn + fabrics). Wider, still manufactured, still excludes raw cotton and apparel.
- [ ] **Option 3 — keep the current specification** (all of Chapter 52 + Ch 61/62 cotton lines). **If chosen, the Ch 62 union must be applied**: `620112 + 620192 + 620130` and `620212 + 620292 + 620230`, exactly as for B1. Not recommended — mixes four value-chain stages and imports agricultural drivers.

**Under every option**, C1 (Ch 42) and C2 (Ch 64) are unaffected and remain fully enumerated and continuity-clean.

---

## 4. Impact if Option 1 is accepted

| Item | Effect |
|---|---|
| C3 definition | Narrows from ~173 codes across four stages to the 5208–5212 fabric headings |
| C3 role | **Strengthened** — becomes a genuine fibre-only contrast with B4 |
| C1, C2 | Unchanged |
| B1, B2, B3, B4 | Unchanged |
| Study window, dates, volatility windows, forecast design, COVID treatment | **All unchanged** |
| Ch 62 discontinuity | Becomes moot — those codes leave the design |
| Residual task | Enumerate the exact HS-6 lines under 5208–5212 at extraction time |

**No research question, intervention date or hypothesis changes.** This sharpens one control.

---

## 5. Decision required

Select Option 1, 2 or 3. Nothing is implemented until recorded in `docs/DECISION_LOG.md`.
