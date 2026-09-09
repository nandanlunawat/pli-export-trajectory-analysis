# Can the MEIDB monthly HS series be extended back before April 2018?

**Date:** 2 September 2026
**Question:** Can the official MEIDB monthly HS-level series be extended backward beyond April 2018 while preserving comparable product definitions and a defensible intervention design for B1, B2 and B3?
**Status:** Feasibility assessment. **No design change proposed or made.**

---

## Answer

**No — not at HS level, and not while preserving comparable product definitions.**

There is **no official Indian source that publishes monthly HS-level export data before January 2018.** The three Department of Commerce portals were checked directly on 2 September 2026, and the constraint is a property of the dissemination system, not of the query.

Even if such data existed, extending the window would import two major Indian policy shocks into the pre-period, cross a third classification boundary, and — decisively — **would not address what Phase 6 actually found.**

---

## 1. What the official portals actually hold — verified directly

| Portal | Frequency | Granularity | Coverage | Banner (verbatim) |
|---|---|---|---|---|
| **MEIDB** | **Monthly** | **HS 2/4/6/8** | **Jan 2018 – Jun 2026** | *"Data available:Jan 2018 to Jun 2026"* |
| **EIDB** | **Annual (fiscal year)** — no month field exists on the form | HS 2/4/6/8 | 2017-18 – 2025-26 | *"Data available 2017-2018 to 2025-2026"* |
| **FTPA** | Monthly-indexed but **cumulative fiscal-year-to-date** | **191 Principal Commodity groups** — no HS | Jan 2010 – Jun 2026 | *"Data available from January 2010 to Jun 2026"* |

Three separate barriers, each sufficient on its own:

- **MEIDB simply starts in January 2018.** No earlier month can be requested; 2018 is the earliest entry in the year dropdown.
- **EIDB is HS-granular but annual.** Its form has no month control at all, and it begins in FY2017-18 regardless — barely earlier than MEIDB, and useless for a monthly design.
- **FTPA reaches back to January 2010 but is neither HS-level nor monthly.** Its "Detailed Report" returns 191 Principal Commodity groups, and the value columns are **cumulative** — a query for August 2015 returns `Apr-August 2014` against `Apr-August 2015`, not the single month. Individual months would have to be recovered by differencing consecutive cumulative figures, with each monthly value inheriting the revision noise of two cumulations.

---

## 2. Could FTPA proxy the three baskets? — No, and the reason differs by basket

The Principal Commodity groups that come closest:

| Basket | Locked definition | Nearest FTPA group | Verdict |
|---|---|---|---|
| **B1** Telephone sets | `851711+851712+851713+851714+851718` | **P4 TELECOM INSTRUMENTS** | **Not comparable.** P4 merges handsets with base stations, transmission and switching equipment — i.e. it fuses B1 with the **Telecom sector that was deliberately dropped** in Phase 2 for having a different intervention date. Using it would silently reinstate the exact overlap the design excluded. |
| **B2** Pharmaceutical formulations | `3003 + 3004` | **H8 DRUG FORMULATIONS, BIOLOGICALS** | **Closest of the three, still not equivalent.** "Biologicals" adds content that headings 3003/3004 exclude, and a PC group is not an HS union — there is no published concordance from the 191-group taxonomy to HS. |
| **B3** Air conditioners | `8415` | none | **No proxy exists.** Air conditioners are not a Principal Commodity group. They sit inside `15 MACHINERY` / `N4 ELECTRIC MACHINERY AND EQUIPMENT`, orders of magnitude larger and dominated by unrelated products. |

Other groups checked and rejected: `H5 BULK DRUGS, DRUG INTERMEDIATES` (wrong end of the pharma value chain — this is the basket Phase 2 explicitly rejected), `O9 COMPUTER HARDWARE`, `P1 CONSUMER ELECTRONICS`, `P2 ELECTRONICS COMPONENTS`, `P3 ELECTRONICS INSTRUMENTS`.

**This corrects an assumption carried since Phase 1.** The design memo (§4.3, open item O3) contemplated an optional long-history electronics route via FTPA, assuming a usable "electronics group". The actual nearest group is **P4 Telecom Instruments**, which is a *worse* match than assumed because it merges the treated basket with a dropped sector. **Open item O3 should be closed as not viable.**

---

## 3. Three design problems that would remain even with the data

**3.1 — A third classification boundary.** DGCI&S implemented ITC(HS)-2017 from April 2017; before that, ITC(HS)-2012. Extending past April 2017 crosses a boundary this project has never examined, requiring the full Phase-2 continuity verification to be repeated for `851712`, `3003`/`3004` and `8415` against the 2012 schedule. The Phase-6 experience — where an unexamined boundary produced a 38–70% artefact — argues for treating that as a real cost, not a formality.

**3.2 — Two major Indian shocks land in the extended pre-period.** **Demonetisation (8 Nov 2016)** and **GST (1 July 2017)**. GST is the more damaging of the two for this design: it disrupted export documentation and IGST refunds through FY2017-18, distorting *measured* exports independently of underlying trade. Buying pre-period length at the price of two new confounders — each needing its own control, each contestable — is a poor trade.

**3.3 — It does not fix what Phase 6 found.** This is the decisive point.

- **B2 and B3 already have 48 pre-policy months.** Sample length is not their binding constraint.
- **B3's failure was not a power problem.** Its β₃ was significant at 2021-04, 2022-01, 2022-04, 2022-07, 2022-10 *and* 2023-04 — dates two years apart. That is a functional-form diagnosis: the segmented model is fitting smooth curvature, not a dated discontinuity. **A longer pre-period makes a piecewise-linear approximation of a curving series worse, not better.**
- **Only B1 would gain**, and only in precision on β₁. But B1's β₃ already attenuates toward zero as error dependence is modelled (−2.92 → −1.55 → −0.97). More pre-period would most likely sharpen a null rather than rescue a finding — which is a legitimate reason to want it, but not the reason usually implied.

---

## 4. Options, with their real costs

| Option | What it does | Cost | Assessment |
|---|---|---|---|
| **A — Do not extend** *(recommended)* | Keep Apr 2018 – Mar 2026. State B1's 28-month pre-period as a limitation. | None. Already the locked design. | The limitation is real and already disclosed. Phase 6 shows length is not the binding constraint. |
| **B — Separate long-history FTPA series** | Build P4 Telecom Instruments and/or H8 Drug Formulations from Jan 2010 as a **distinct, explicitly labelled series answering a different question** | Different product definition; cumulative-to-monthly differencing; no HS concordance; P4 reinstates the dropped Telecom overlap | Viable only if never merged with B1/B2 and clearly labelled. Value is limited given §3.3. |
| **C — UN Comtrade** | India reports monthly HS-6 to Comtrade with longer history | Not an official Indian dissemination channel; different revision practice; coverage gaps; **mixing sources mid-panel is the same defect CP-001 was created to fix** | Would need its own full verification exercise before any use. Not recommended without one. |
| **D — Address functional form rather than sample length** | The Phase-6 diagnosis points at curvature, not data shortage | Would be a **design change** requiring the rule-8 process | **Raised as an observation only. Not proposed, not implemented.** If pursued, it belongs in a change proposal with pre-specification, not in a data-extension decision. |

---

## 5. Recommendation

**Do not extend the panel.** The data does not exist at the required granularity from any official Indian monthly source; the nearest proxies change the product definitions in ways that would undo Phase-2 decisions; and the extension would not address the identification problem Phase 6 actually diagnosed.

**Two housekeeping consequences:**

1. **Close open item O3** (long-history electronics via FTPA) as **not viable** — the nearest group is P4 Telecom Instruments, which merges B1 with the dropped Telecom sector.
2. **Strengthen the limitations text**, which currently says the 28-month B1 pre-period is a constraint. It should also record that it is an **irreducible** constraint: January 2018 is the start of official Indian monthly HS dissemination, not a choice made by this project.

---

## Sources — all verified directly, 2 September 2026

| Claim | Evidence |
|---|---|
| MEIDB monthly HS, Jan 2018 onward | https://tradestat.commerce.gov.in/meidb/commoditywise_export — coverage banner; year dropdown starts 2018 |
| EIDB annual only, FY2017-18 onward | https://tradestat.commerce.gov.in/eidb/commodity_wise_export — banner *"Data available 2017-2018 to 2025-2026"*; form has **no month field** |
| FTPA Jan 2010 onward, 191 PC groups, cumulative | https://tradestat.commerce.gov.in/ftpa/export_commodity_group_new — banner; Detailed Report for Aug-2015 returned 191 rows with columns `Apr-August 2014` / `Apr-August 2015` |
| FTPA group names | Same query: `H5 BULK DRUGS, DRUG INTERMEDIATES`, `H8 DRUG FORMULATIONS, BIOLOGICALS`, `O9 COMPUTER HARDWARE, PERIPHERALS`, `P1 CONSUMER ELECTRONICS`, `P2 ELECTRONICS COMPONENTS`, `P3 ELECTRONICS INSTRUMENTS`, `P4 TELECOM INSTRUMENTS`, `15 MACHINERY`, `N4 ELECTRIC MACHINERY AND EQUIPME` |
| DGFT on portal roles | `https://content.dgft.gov.in/Website/TTDA.pdf` — *"Commodity wise – yearly data at 2,4,6,8 digit ITCHS code level"* (EIDB) |
