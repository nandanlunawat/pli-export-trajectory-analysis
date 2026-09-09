# Verification Status — HS Transition for Selected Sectors

> ⚠️ **SUPERSEDED IN PART — point-in-time record, retained for the audit trail.**
> This report states the position on **28 August 2026**, before MEIDB could be queried. On **29 August 2026** the empirical probe overturned two of its conclusions:
> - §A2 states the B1 basket as `851712 ∪ 851713 ∪ 851714`. **Wrong** — there are two transitions, not one, and the basket is now `851711 + 851712 + 851713 + 851714 + 851718` (approved Change Proposal 001).
> - §A2's claim that the union is "invariant to whether the published series switched in January or April 2022" is **false** — the three-code union collapses 70% into January 2022.
>
> For the current position see `08_report/research_design_memo.md` §1.3, `docs/CHANGE_PROPOSAL_001_mobile_basket.md` and `docs/DECISION_LOG.md`. Everything else in this report — the B2/B3/B4 findings, the ruled-out series, the data-access facts and the source inventory — still stands.

**Date:** 28 August 2026
**Scope:** Only the codes relevant to the four selected baskets. No modelling, no data extraction.
**Rule applied:** unfetchable sources are recorded as NOT VERIFIED with the exact URL preserved. Nothing is inferred from memory or substituted from secondary sources.

---

## A. VERIFIED FACTS

### A1 — Primary Indian instruments actually obtained and read

| Document | Status | Covers |
|---|---|---|
| DGCI&S ITC(HS)-2017, Chapter 85 schedule | **READ IN FULL** | Old Indian 8-digit structure, heading 8517 |
| **DGFT Notification No. 54/2015-20 dated 09.02.2022** notifying ITC(HS) 2022, Annexure-II | **READ IN FULL, Chapters 1–97** | Every 8-digit code DELETED and every code created at the HS2017→HS2022 transition |
| **DGFT Notification No. 08/2023 dated 29.05.2023**, Annexure-I | **READ** | Finance Act 2023 changes w.e.f. 01.05.2023 = the content of the **April 2024** DGCI&S directory |
| Budget TRU letters 2025-26 and 2026-27 | **READ** | Finance Act 2025 / 2026 changes = the **April 2026** directory |
| CBIC "Correlation of Customs Tariff between 2021 and 2022" | **Annexure-I ONLY** | Methodology and the SF/DF/NF/DP/NP code scheme. Annexure-II unreachable — see §C1 |
| DGFT "Type of Trade Data available on different sources" (TTDA.pdf) | **READ IN FULL** | Official inventory of Indian trade-data sources and DGCI&S dissemination terms |

### A2 — HS transition, per selected basket

**B1 — Mobile phones (851712 ∪ 851713 ∪ 851714)**

| Vintage | Codes | Source |
|---|---|---|
| ITC(HS) 2017 (implemented at DGCI&S April 2017) | `8517 12 10` Push button type; `8517 12 90` Other. Parts: `8517 70 10` populated PCBs; `8517 70 90` Other | DGCI&S Chapter 85 schedule |
| In force 31.12.2021 | `85171211` Mobile phones other than push button; `85171219` Mobile phones push button; `85171290` Telephones for other wireless networks | DGFT Notn 54 deletion list |
| ITC(HS) 2022 | `851712` **DELETED**; `85171300` Smartphones **NEW**; `85171400` Other telephones for cellular or other wireless networks **NEW**. `851770` **DELETED**; `85177010`→`85177910`; `85177090`→`85177990`; `85177100` aerials **NEW** | DGFT Notn 54 Annexure-II |
| April 2024 directory | Within 8517, only `85176240` (HDSL) and `85176950` (Subscriber end equipment) **DELETED**. `85171300`, `85171400`, `85177100`, `85177910`, `85177990` **unchanged** | DGFT Notn 08/2023 Annexure-I |
| April 2026 directory | **No change to heading 8517** | Budget 2026-27 TRU letter |

**Heading 8517 is closed.** Every deleted and every new code lies inside 8517; no code from outside moved in. `85195000` (telephone answering machines) was deleted, but DGFT re-attaches its policy condition to `85198100` — heading 8519, not 8517.

→ **The union 851712 ∪ 851713 ∪ 851714 is continuous, and is invariant to whether the published series switched in January or April 2022.**

**B2 — Pharmaceutical formulations (3003 + 3004).** Zero rows for either heading anywhere in DGFT Notn 54 Annexure-II. Chapter 30 absent from the Finance Act 2023 amended-chapter list. Budget 2025-26 TRU letter: *"Chapters 30 to 32: No change"*. **No code created, deleted or renumbered at any boundary.**

**B3 — Air conditioners (8415).** The string `8415` does not occur anywhere in DGFT Notn 54 Annexure-II, which enumerates every deletion and creation across Chapters 1–97. Finance Act 2023 Chapter 84 amendments confined to headings `8414` and `8419`. Finance Acts 2025 and 2026 touch `8415 90 00` on **rate only**. **No code change at any boundary.**

**B4 — MMF fabrics (the 14 PLI Annexure-II codes).** None of `540710, 540720, 540742, 540752, 540754, 540761, 540769, 551219, 551511, 551614, 580632, 600192, 600537, 600632` appears in any change instrument. Chapters 54 and 60 have **zero rows** in Notn 54. Chapter 55's only HS2022 change was the `5501.10` aramid split; Chapter 58's only change was heading `5802` (code `580632` sits in heading 5806). April 2024: the only Chapter 54 change was heading `5402`. April 2026: *"Chapters 42 to 59: No change"*, *"Chapter 57-65: No Change"*.

### A3 — Verified discontinuities (series ruled out)

| Series | Break |
|---|---|
| Any **Chapter-85 aggregate** | Heading `8524` created at HS2022, fed partly from `90138010`/`90138090` — **Chapter 90, outside Chapter 85**. Then completely renumbered in the April 2024 directory: six codes deleted, 24 created. |
| Heading **3002** | `30021100` (Malaria diagnostic test kits) deleted out of Chapter 30 with no successor inside 3002. Heading **3006**: `30062000` (Blood-grouping reagents) likewise. |
| **MMF apparel** `6201`/`6202` | Article-based structure (`..11/..12/..13/..19`, `..91/..92/..93/..99`) collapsed into fibre-based (`..20` wool, `..30` cotton, `..40` MMF, `..90` other). ~24 codes deleted, ~16 created. |

### A4 — Data-access facts

- **MEIDB coverage banner, verbatim (28 Aug 2026):** *"Data available:Jan 2018 to Jun 2026 ((R) Revised Final upto Mar 2026, (F) Final upto Jun 2026)"*; *"Data last updated on: 13/08/2026"*.
- **MEIDB serves the whole series under ONE code directory:** *"ITC HS Code of the Commodity is from latest HS Code Directory provided by DGCIS Kolkata on April 2024."* Old codes *"may be either dropped or re-allocated"*; dropped ones flagged `*`.
- **Vintage discrepancy:** the help page says April 2024; the portal front page carries the same warning with respect to **April 2026**.
- **Dynamic Data Revision Policy** (since 2009-10): prior months of the current financial year are restated on every release.
- **Exports include re-exports** (MEIDB help note 2).
- **INR is the compilation currency; USD derived at the RBI monthly average rate** (DGCI&S NMDS §2.6).
- **NEW — a second official route to the same data:** the Department of Commerce **Monitoring Dashboard** (https://dashboard.commerce.gov.in/commercedashboard.aspx) is documented by DGFT as providing *"month-wise and year-wise import, export and balance of trade data for all items at principal commodity group and at 2-digit, 4-digit, 6-digit and 8-digit ITC-HS code level in value terms"*. **Not yet tested.**
- **NEW — DGCI&S FTDDP commercial terms:** free access only to Government/RBI/Embassies/UN bodies; for private users, *"Principal commodity level data for the past 24 months"* free; otherwise **₹1.00 per record**, annual bulk subscription **₹350,000**, with a 60% discount for Indian academic/research institutions on IP-recognition subscription. **The free tier does not cover HS-level monthly history — MEIDB or the Dashboard remain the only free HS-level routes.**
- DGCI&S publishes ITC(HS) schedules on its Indian Trade Classification page **only up to the 2017 edition**.

### A5 — Intervention dates

All five stages (Cabinet approval, notification, guidelines, application window, operational/effective date, first incremental-sales year) verified per scheme from gazette notifications, PIB releases and ministry guidelines. Recorded in `02_policy_sources/pli_intervention_dates.csv`. No change from the locked memo.

---

## B. UNRESOLVED FACTS

| # | Item | Consequence |
|---|---|---|
| **U1** | **CBIC SF/DF/NF/DP/NP correlation letter codes** for Chapters 29, 30, 54, 55, 58, 60, 61, 62, 84, 85. **NOT VERIFIED.** | DGFT Notn 54 records code *additions and deletions*, which rules out a **code-level** break. It does **not** rule out a pure **scope change at an unchanged code** (CBIC's "DF"). Residual risk for B2, B3, B4 — low, since these headings have zero rows across all three change instruments, but not zero. |
| **U2** | Whether the DGCI&S **published monthly series** switches to HS2022 in **January 2022** or **April 2022**. **PARTIALLY VERIFIED.** | Title page of the DGCI&S ITC(HS)-2022 says *"(EFFECTIVE FROM 1ST APRIL, 2022)"*, and the precedent is documented (*"Indian Trade Classification (Harmonised System) - 2017 … (Implemented at DGCI&S from April. 2017)"* despite the tariff changing 01.01.2017). **No DGCI&S circular saying so in terms was found.** Does not affect B1 (union invariant) or B2/B3/B4 (no code change). |
| **U3** | Whether MEIDB **re-mapped historical values** or merely relabelled them under the current directory. **NOT VERIFIED.** | Cannot be settled from documents. Requires a MEIDB query. |
| **U4** | Date of the **intermediate 8-digit change** under `851712` (`85171210`/`85171290` → `85171211`/`85171219`/`85171290`) between April 2017 and December 2021. **NOT VERIFIED.** | Immaterial to the design — the basket is defined at 6-digit — but it is a third documented reason never to build this series at 8-digit. |
| **U5** | Heading **2941** after 01.05.2025. Finance Act 2025 created or modified 18 tariff items in Chapter 29; the government TRU letter does **not** itemise the headings. **NOT VERIFIED.** | Not used in the locked design. Must be cleared before any API basket is added. |
| **U6** | Continuity of **control chapters** 41, 42, 52, 64, 69, 70. **NOT CHECKED.** | Blocks use of controls C1, C2, C3. |
| **U7** | FTPA commodity-group list, start date and units. **NOT VERIFIED.** | Only relevant if the long-history electronics forecasting route is taken. |

---

## C. EXACT REMAINING DATA-ACCESS PROBLEM

Two distinct causes. Neither is a source problem — both documents exist and are public.

### C1 — PDF text-extraction size cap (~65,000 characters)

The CBIC correlation Annexure-II is a ~230-page 8-digit table; Chapters 84–85 sit around page 170. **Every mirror truncates at the same point** because the cap is in the fetching tool, not the server.

| URL (preserved verbatim) | Truncation point |
|---|---|
| `https://gst.kar.nic.in/latestupdates/GuidanceDocumentonCorrelationofCustomsTariffbetween202120222412.pdf` | tariff item `28351020`, p.71 |
| `https://ipga.co.in/wp-content/uploads/2022/08/20.12.2021-Guidance-Document-on-Correlation-of-Customs-Tariff-between-2021-and-2022.pdf` | tariff item `29053100`, p.79 |
| `https://ftddp.dgciskol.gov.in/dgcis/resources/pdfs/PC_composition_HSN2022.pdf` | Chapter 9 (also timed out on one attempt) |
| `https://www.dgciskol.gov.in/Writereaddata/Downloads/ITC-HS_2022.pdf` | Chapter 9 |
| `https://www.indiabudget.gov.in/budget2021-22/doc/Finance_Bill.pdf` | before the Schedules |

### C2 — JavaScript-gated or non-serving hosts; no browser connected to this session

| URL (preserved verbatim) | Failure mode |
|---|---|
| `https://www.cbic.gov.in/Cbec_Revamp_new/htdocs-cbec/customs/cst2022-010222/cst-idx` | *"You must enable JavaScript to view this page."* |
| `https://www.cbic.gov.in/` (all tariff paths) | Same |
| `https://old.cbic.gov.in/htdocs-cbec/customs/cst2023-010223/cst-idx` | Empty body, zero bytes |
| `https://tradestat.commerce.gov.in/meidb/commoditywise_export` | Returns the form shell and `Loading…`; no data |
| `https://www.indiantradeportal.in/vs.jsp?lang=0&id=0,31,24100,24101` | Timed out after 180 s |
| `https://www.dgft.gov.in/CP/?opt=notification` | JS-gated |
| `https://apeda.gov.in/sites/default/files/dgft_notifications/Notification_No_40_2024_25.pdf` | Scanned image, no text layer |
| `https://web.lawcrux.com/newversion/web/Assets/data5t/ft/ftitch/ftitch22_chp85.htm` | JS-gated |

---

## D. MINIMUM ADDITIONAL SOURCES / STEPS

Ordered by cost. **D1 and D2 close everything that blocks the design.**

| # | Step | Closes | Effort |
|---|---|---|---|
| **D1** | **Download the Karnataka GST mirror PDF to disk and read it locally**, rather than through a size-capped fetch. Go to pages ~150–185 (Ch 84–85), ~60–80 (Ch 29–30), ~110–135 (Ch 54–62). Search for the strings `85171211`, `85171290`, `85177010`, `84151010`, `30039011`, `30049099`, `54075200` and record the letter code against each. **This is a local file read — the tooling limitation does not apply once the file is on disk.** | **U1** | ~20 min |
| **D2** | **Four MEIDB queries in a browser.** V1: HS-6, Mar-2022 and Apr-2022, read `851712`/`851713`/`851714`. V2: same for Dec-2021 and Jan-2022. V3: Specific HSCode `8517`, HS-6, Mar-2024 and Apr-2024. V4: Specific HSCode `8415` and `3004`, HS-6, at both boundaries. Pass criterion: the **union total** shows no discontinuity. Record the coverage banner and the `Data last updated on` date verbatim, and note any `*`-prefixed description. | **U2, U3** | ~10 min |
| **D3** | Re-grep the already-retrieved DGFT Notn 54 and Notn 08/2023 text for Chapters **41, 42, 52, 64, 69, 70**. Documents are already local — no fetch needed. | **U6** | ~10 min |
| **D4** | One browser visit to `https://tradestat.commerce.gov.in/ftpa/export_commodity_group_new` — record the group list, earliest month and units. | **U7** | ~5 min |
| **D5** | Read the **Finance Act 2025 Third Schedule** directly (indiacode.nic.in or eGazette) for Chapter 29 heading 2941. Only if an API basket is ever added. | **U5** | optional |
| **D6** | Search DGFT notifications 2017–2021 amending ITC(HS) 2017 Chapter 85 for the intermediate `851712` change. Documentation only. | **U4** | optional |
| **D7** | **Fallback if MEIDB proves unusable:** test the Department of Commerce Monitoring Dashboard (`https://dashboard.commerce.gov.in/commercedashboard.aspx`), documented by DGFT as carrying monthly data at 2/4/6/8-digit ITC-HS level. | extraction route | ~15 min |

**Single highest-leverage action:** connecting the Chrome extension resolves cause **C2** entirely, which covers D2, D4 and D7, and would also let CBIC's own site serve the correlation document that D1 works around.

**Design impact if U1 and U2 remain open indefinitely:** the locked design still stands. B1 is continuous by construction at 6-digit; B2, B3 and B4 have no code change at any boundary in any instrument examined. What would remain unproven is only the absence of a *scope* change at an unchanged code — which must then be carried into the report as a stated limitation rather than treated as resolved.
