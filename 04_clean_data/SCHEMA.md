# `master_monthly_exports.csv` — field dictionary

**Status: SCHEMA ONLY.** The file contains a header row and zero data rows. It is populated by `05_analysis/build_panel.py` only after checks Q1, Q2 and Q3 pass.

Long format: one row per (month × basket × flow).

| Field | Type | Definition |
|---|---|---|
| `month` | date `YYYY-MM` | calendar month |
| `fy` | string | Indian fiscal year, e.g. `2018-19` |
| `t` | int 1–96 | time index; **April 2018 = 1, March 2026 = 96**. Fixed by calendar position and **never re-indexed**, even when months are excluded from an estimation — re-indexing after an exclusion distorts the trend. |
| `sector` | string | Electronics / Pharmaceuticals / White Goods / Textiles / Control |
| `basket_id` | string | `B1_MOBILE`, `B2_PHARMA_FORM`, `B3_PHARMA_API`, `B4_AC`, `B5_TEX_FABRIC`, `CTL1`–`CTL5`. **Must exist in `03_mapping/hs_mapping_master.csv`** (gate G7). |
| `role` | string | `TREATED` or `CONTROL` |
| `flow` | string | **`export` or `import`.** Imports are pulled for the same HS lines so the gross-versus-net gap can be shown — the pre-registered mitigation for re-export inclusion (`data_quality_report.md` §2.2). Gate G1 requires 96 rows per basket **per flow**. |
| `hs_basis` | string | the codes summed for this basket-month, e.g. `851712+851713+851714` |
| `value_usd_mn` | float | FOB value, US$ million. **The modelled outcome.** |
| `value_inr_cr` | float | FOB value, ₹ crore. Robustness R9. |
| `ln_value_usd` | float | `ln(value_usd_mn)`. **Undefined if the value is zero** — gate G4 fails rather than substituting `ln(Y+1)`. |
| `g_usd` | float | `100 × [ln(Y_t) − ln(Y_{t−1})]`. Null at t=1 and wherever the previous month is excluded (the seam rule, memo §6.2). |
| `post` | 0/1 | `1{t ≥ T_D}` — the level-equation indicator (memo §5.1) |
| `post_plus` | 0/1 | `1{t ≥ T_D + 1}` — the **growth**-equation indicator (memo §5.5). Deliberately distinct: using `post` in the growth equation maps α₂ to β₂ − β₃ rather than β₂. |
| `time_after` | int | `max(0, t − T_D)` — **not** `+1`; see memo §5.1 |
| `break_month` | 0/1 | `1{t = T_D}` |
| `covid_lockdown` | 0/1 | `1` for Mar, Apr, May 2020 (MHA national lockdown) |
| `covid_fy2021` | 0/1 | `1` for Apr 2020 – Mar 2021 (the COVID fiscal year; robustness exclusion) |
| `month_num` | int 1–12 | calendar month number, for the month fixed effects. **Reference month is April** (omitted dummy). |
| `data_vintage` | date | the MEIDB "data last updated" date on the source extract |
| `retrieval_date` | date | when the raw response was fetched |
| `revision_status` | string | `(F)` Final or `(R)` Revised Final, as flagged by MEIDB |
| `notes` | string | free text; e.g. a `*` dropped-code flag observed during check Q2 |

**Derived columns are computed in `build_panel.py`, never entered by hand**, so that a change to an intervention date propagates by re-running rather than by editing.
