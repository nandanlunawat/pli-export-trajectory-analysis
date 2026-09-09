# Full Repository Audit — Read-Only (Parts A–M)

**Date:** 8 September 2026. Nothing deleted, moved, renamed, modified, or regenerated. All findings below await approval. Analytical results remain frozen and untouched.

---

## Headline: what this audit found that the previous cleanup did not

**FOUR more results files have no committed generating code** (same class as the F-1 gap fixed last pass):

| Frozen CSV | Situation |
|---|---|
| `06_results/EDA_summary.csv` | `01_EDA.ipynb` only **reads** it (cell 23); the writer was uncommitted session code |
| `06_results/ITS_arma_aic_scan.csv` | `03_robustness_ITS.ipynb` computes the scan but never saves it |
| `06_results/forecast_validation.csv` | `04_forecasting.ipynb` prints validation tables but never saves them |
| `06_results/forecast_counterfactual.csv` | `04_forecasting.ipynb` builds counterfactuals but never saves; the `selection`/`selection_note` columns and `raw_rmse_winner` rows came from session code |

Everything else is in very good shape: **the notebooks contain zero external image references, zero absolute paths, and zero machine dependencies** — the fear that notebooks depend on images elsewhere on the C: drive is unfounded (details in Part C). The one presentation consequence: all four notebooks were committed **without stored outputs**, so on GitHub they show code and prose but no tables or charts until run.

---

## Part A — Complete file inventory

131 files (excluding `__pycache__`). Every file classified; no file's classification was inferred from name/size/date alone — contents, writers, and readers were checked.

### 01_raw_data/ (6 files) — all KEEP (source data; never overwrite)
| File | Purpose / provenance |
|---|---|
| `raw_trade_data/meidb_hs6_extract_2026-08-29/panel_compact.csv` | Raw MEIDB monthly HS-6 extract (48 portal requests). Created by `fetch_meidb.py`. Read by the pipeline that built `master_monthly_exports.csv`. **Authoritative raw input.** |
| `.../b1_code_detail.csv` | Per-code B1 detail — evidence for the HS-transition repair (Appendix B). |
| `.../reconciliation_aggregates.csv` | MEIDB's own totals used for the 0.002% parser reconciliation. |
| `.../extraction_manifest.json` | Retrieval date, query settings, portal banner verbatim — the vintage record. |
| `raw_trade_data/meidb_continuity_probe_2026-08-29.csv` | The D2 probe that discovered the two HS transitions. Evidence file. |
| `raw_trade_data/README.md` | Provenance stub. |

### 02_policy_sources/ (3) — all KEEP
`pli_intervention_dates.csv` (authoritative 21-column date registry; read manually, cited by memo/report Appendix A) · `source_log.csv` (S01–S42) · `README.md`.

### 03_mapping/ (3) — all KEEP
`hs_mapping_master.csv`, `control_sector_mapping.csv`, `control_hs6_codes.csv` — basket/control definitions (Appendix B). The superseded date file already moved to `docs/archive/`.

### 04_clean_data/ (2) — all KEEP
`master_monthly_exports.csv` (672 rows; the input every module loads via `its_core.load_panel()` / `eda_core.load()`) · `SCHEMA.md`.

### 05_analysis/ (11 + `__pycache__`) — all KEEP
| File | Role | Imported/used by |
|---|---|---|
| `fetch_meidb.py` | Raw-data extraction (portal → raw dir). Standalone. | — |
| `eda_core.py` | Phase-4 diagnostics module | `01_EDA.ipynb` |
| `its_core.py` | Locked design matrix + baseline fitters; constants D_S, COVID, HAC | notebooks 02, 03, 04; `robustness_core`, `05_volatility_R12.py` |
| `robustness_core.py` | 6A/6B/6C machinery (ALT_DATES, GRID, break tests) | notebook 03; `05_volatility_R12.py` (EXOG) |
| `forecast_core.py` | Locked forecasting protocol | notebook 04 |
| `05_volatility_R12.py` | Volatility + R12 (byte-identical reproduction, verified) | standalone |
| notebooks `01`–`04` | The four phase notebooks — **all required, none obsolete** | — |
| `README.md` | stub | — |
| `__pycache__/` | Python cache from the validation run — gitignored; deletable trivially | — |

### 06_results/ (12 CSVs) — all KEEP; **authoritative source of truth** (provenance in Part F)

### 07_figures/ (44 PNGs + .gitkeep) — all KEEP (provenance in Part D)

### 08_report/ (11 md) — all KEEP
`FINAL_REPORT.md` (the deliverable) · `FINAL_EVIDENCE_TABLE.md` (numerical transcription layer) · `research_design_memo.md` (locked design) · `DATASET_VALIDATION_REPORT.md`, `data_quality_report.md`, `verification_status.md` (validation evidence) · `backward_extension_feasibility.md` (Appendix C) · `EDA_findings.md`, `ITS_preliminary_findings.md`, `ITS_robustness_findings.md`, `FORECASTING_findings.md` (phase findings backing appendices D–H).

### docs/ (8 + archive/6) — KEEP (audit trail); `archive/` = ARCHIVE class, gitignored
`PROJECT_STATUS.md`, `DECISION_LOG.md`, `CHANGE_PROPOSAL_001/002/003`, `source_log.md`, `00_PHASE1_AUDIT_AND_DESIGN.md`, `CLEANUP_AUDIT_PROPOSAL.md`, this audit. `archive/`: REPORT_OUTLINE, FINAL_findings_and_recommendation, HOSTILE_METHODOLOGICAL_AUDIT, pli_sector_mapping_PROPOSED.csv/.xlsx, pli_intervention_dates.csv (superseded 03_mapping copy).

### 99_legacy/ (14) — KEEP LOCALLY, immutable, EXCLUDE FROM GITHUB (already gitignored)
The two legacy notebooks are content-distinct (different md5) — both stay. The absolute paths inside them are the *audited defect*, not a dependency.

### Root — `README.md`, `.gitignore` — KEEP.

**Duplicates/superseded:** none remaining in the publication-facing tree (both known duplicates were removed last pass; the superseded files sit in `docs/archive/`).

---

## Part B — Dependency graph

```
MEIDB portal
   │  fetch_meidb.py  (48 POSTs, raw cached, refuses overwrite)
   ▼
01_raw_data/raw_trade_data/meidb_hs6_extract_2026-08-29/panel_compact.csv
   │  (build step inside fetch_meidb.py --build-only)
   ▼
04_clean_data/master_monthly_exports.csv          ◄─ SCHEMA.md documents it
   │
   ├─ 01_EDA.ipynb ── eda_core.py ────────► 07_figures/eda_* (22)   06_results/EDA_summary.csv (GAP: writer uncommitted)
   ├─ 02_ITS_diagnostics.ipynb ── its_core.py ► 07_figures/its_* (13)  06_results/ITS_prelim_* (4 CSVs)
   ├─ 03_robustness_ITS.ipynb ── robustness_core.py (+its_core)
   │                                      ► 07_figures/rob_* (4)    06_results/ITS_robustness_matrix.csv, ITS_structural_breaks.csv
   │                                                                 06_results/ITS_arma_aic_scan.csv (GAP: save not in nb)
   ├─ 04_forecasting.ipynb ── forecast_core.py (+its_core)
   │                                      ► 07_figures/fc_* (4)     06_results/forecast_validation.csv, forecast_counterfactual.csv (GAP: saves not in nb)
   └─ 05_volatility_R12.py ── its_core.py (+robustness_core.EXOG)
                                          ► 06_results/volatility_results.csv, ITS_R12_quadratic_pretrend.csv (byte-verified)
                                            07_figures/vol_01_* + eda_05/06 rolling-vol figures come from eda_core (vol_01 from session script — see Part D)
   ▼
06_results/*.csv ──transcribed──► 08_report/FINAL_EVIDENCE_TABLE.md ──sole numerical source──► 08_report/FINAL_REPORT.md ◄─ 07_figures/*
```

---

## Part C — Notebook + image audit (priority) — **CLEAN**

Every cell of all four notebooks was inspected programmatically.

| Check (your items 1–10) | Result |
|---|---|
| Figures generated by code | All figures come from module functions (`E.plot_*`, `I.plot_fit`, `R.plot_robustness`, `F.plot_cf`) |
| Figures saved to disk | Yes — modules save to `ROOT/07_figures` via `Path(__file__)`, so saving is **independent of working directory** |
| Figures displayed inline | **None** — matplotlib runs on the `Agg` backend; figures go to disk only |
| Markdown cells referencing external images | **Zero.** No `![](...)`, no `<img>` tags, anywhere |
| Image paths outside project root | **Zero** |
| Paths to your personal machine (`C:\Users\...`) | **Zero** in any notebook or module |
| Figures exist in 07_figures | Yes — all 44 |
| Relative paths correct from notebook location | Yes — the only relative paths are `../06_results/*.csv` reads/writes, correct when the notebook runs from `05_analysis/` (the standard Jupyter behaviour: cwd = notebook folder) |
| Notebook renders without external image folders | Yes — nothing external is referenced |
| Stale outputs from older paths/code | **No stored outputs exist at all** (every cell has `outputs: []`) — nothing can be stale |

Per-image problem table: **empty — there are no image references in any notebook.** The concern about a separate image folder on your C: drive does not apply to this project.

The flip side: because outputs were stripped, GitHub renders the notebooks without any tables or plots. If you want viewers to see results without running anything, the notebooks must be re-executed once and committed with outputs — flagged as a decision, not done (re-running would rewrite six frozen CSVs from notebooks 02/03; deterministic OLS outputs should reproduce identically, but ARMA convergence is not guaranteed byte-stable, so this needs the same write-to-separate-directory guard used by `05_volatility_R12.py`, or a run on a copy).

---

## Part D — Figure inventory (44 PNGs)

| Prefix | Count | Generated by | Report use |
|---|---|---|---|
| `eda_00` overview | 1 | `eda_core.plot_overview` via nb 01 | **Figure 1** (main text) |
| `eda_01_*` level/log/growth | 4 | `eda_core.plot_level_log_growth` | Figure 2 (one shown; rest Appendix D) |
| `eda_02_*` seasonality | 4 | `eda_core.plot_seasonality` | Appendix D |
| `eda_03_*` STL | 4 | `eda_core.plot_stl` | **Figure 3** = B3; rest Appendix D |
| `eda_04_*` ACF/PACF | 4 | `eda_core.plot_acf_pacf` | Appendix D |
| `eda_05` rolling vol (all) | 1 | `eda_core.plot_rolling_vol` | Figure 6 candidate / Appendix G |
| `eda_06_*` rolling vol per basket | 4 | `eda_core.plot_rolling_vol` | Appendix G |
| `its_01_*` fits (+B1 Transition variant) | 5 | `its_core.plot_fit` via nb 02 | **Figure 4**; Transition variant Appendix E |
| `its_02_*` residuals | 8 | `its_core.diagnostics` via nb 02 | Appendix E |
| `rob_01_*` forest plots | 4 | `robustness_core.plot_robustness` via nb 03 | **Figure 5** = B3; rest Appendix F |
| `vol_01` rolling SD windows | 1 | **session script (uncommitted)** — same gap family as above; trivially regenerable | Figure 6 / Appendix G |
| `fc_01_*` counterfactuals | 4 | `forecast_core.plot_cf` via nb 04 | **Figure 7** = B4 (+B3); B1/B2 Appendix H |

**Duplicated:** none. **Unused:** none — every figure is either a main-text figure or an appendix D–H member. **Intermediate diagnostics:** `its_02_*` and `eda_04_*` are diagnostic-grade but are exactly what appendices E and D promise, so they stay.

**On the proposed `07_figures/eda|its|robustness|volatility|forecasting/` subfolders:** possible, but it requires touching five code locations (each module's save call) **and** every figure path in FINAL_REPORT.md, README, and findings memos — all on a frozen project — to achieve what the filename prefixes (`eda_`, `its_`, `rob_`, `vol_`, `fc_`) already achieve. **Recommendation: keep 07_figures flat.** The prefixes are the folders. (If you still want subfolders, it is safe if done wholesale with path updates — listed as an option, not the default.)

---

## Part E — Code quality audit

**Overall:** the code is already in the shape you want — small modules with docstrings stating the locked design, constants named (`D_S`, `PANEL_START`, `REF_MONTH`, `HAC_LAGS`, `COVID_MONTHS`), no hard-coded machine paths (everything is `Path(__file__)`-relative), functions of readable size (10–17 per module), and notebooks that call named module functions rather than burying logic in cells.

Specific findings:

| Item | Location | Assessment |
|---|---|---|
| Unused import | `eda_core.py` line 25 imports `acf` and `zivot_andrews`; verify both used (zivot_andrews used in break-aware unit root; `acf` possibly unused) | Cosmetic; harmless. Fix only in a batch pass. |
| Magic numbers | `Z95 = 1.959964` in `forecast_core` (named ✓); MBB `BLOCK=6, NBOOT=4000, SEED` in `05_volatility_R12` (named ✓); `sup_f` 15% trim inside `robustness_core` (named in comment) | Acceptable — all pre-registered values, all named. |
| Duplicated logic | A local `series()`/`_series()` helper exists in `eda_core`, `robustness_core.design_at`, and `05_volatility_R12` — three near-copies of "index by month, log, diff" | Deliberate at the time (kept scripts self-contained). Consolidating into `its_core` is cleaner but **touches frozen-result-generating code paths — recommend leaving unchanged** and documenting instead. |
| Dead code | None found. `_tmp` artifacts removed last pass. | — |
| Working-dir assumption | Notebook `../06_results/` writes assume cwd = `05_analysis` | Standard Jupyter behaviour; document in README (already implied by `cd 05_analysis`). |
| Hidden state between notebooks | None across notebooks (each loads the master CSV itself). Within nb 02, later cells use `base`/`gr` from earlier cells; within nb 04, `tabs` from cell 3 — normal top-to-bottom execution, no cross-notebook state. | Fine. |
| Over-abstraction | None. The most intricate function is `fit_arma` (grid scan) — 20 lines, well-commented. | — |
| Undocumented assumption | `boot()` draw order in `05_volatility_R12.py` — documented in-file ✓ | — |

**Do-not-touch list (changing these could alter frozen results):** `its_core.design` (T/TimeAfter/month-FE construction), `robustness_core.GRID`/`fit_arma`, `forecast_core.f_snaive/f_ets/f_sarima/validate/select`, everything in `05_volatility_R12.py` (RNG order), HAC `use_correction=True` calls.

---

## Part F — Results source-of-truth audit (12 CSVs)

| CSV | Generating code | Cited in report | Reproducible now? |
|---|---|---|---|
| ITS_prelim_baseline_levels / growth_companion / diagnostics / B1_transition | nb 02 (cell 20) | §7, App E | ✔ |
| ITS_robustness_matrix / ITS_structural_breaks | nb 03 (cell 20) | §8, App F | ✔ |
| volatility_results / ITS_R12_quadratic_pretrend | `05_volatility_R12.py` | §8.5, §9, App F/G | ✔ **byte-verified** |
| **EDA_summary** | **uncommitted session code** | §6, App D | ✖ GAP |
| **ITS_arma_aic_scan** | **uncommitted** (nb 03 computes, never saves) | App F | ✖ GAP |
| **forecast_validation** | **uncommitted** (nb 04 prints, never saves) | §10 Table 9, App H | ✖ GAP |
| **forecast_counterfactual** | **uncommitted** (nb 04 builds, never saves; selection columns added in session) | §10 Table 10, App H | ✖ GAP |

No stale/newer duplicate of any result exists anywhere in the tree (the `/tmp` reproduction copies live outside the project and vanish with the sandbox). **Proposed fix (needs approval):** recover the exact saving code from the session transcript — the same method that made F-1 byte-identical — and close all four gaps either by (a) adding the missing `to_csv` lines to the two notebooks plus a small `06_results_reproduction`-guarded script for EDA_summary, or (b) one consolidated `06_reproduce_remaining.py` companion to `05_volatility_R12.py`. Option (b) touches no notebook and is safest.

---

## Part G — Report / figure / result consistency — **PASS**

Every figure filename in FINAL_REPORT.md exists in `07_figures/`; every `06_results/*.csv` and `08_report/*.md` reference exists; the appendix A–H map resolves file-by-file; no reference points to a deleted or archived file (the three archived memos are referenced only from `docs/` audit-trail files, whose paths were updated last pass); report numbers were verified against FINAL_EVIDENCE_TABLE.md in the freeze QA and none has changed since (spot re-verified).

## Part H — Absolute-path audit — no genuine dependencies

| Hits | Classification |
|---|---|
| `99_legacy/` notebooks (27 hits) | (2) historical — the audited defect itself; immutable; gitignored |
| `docs/00_PHASE1…` (4), `docs/PROJECT_STATUS` (2), `docs/source_log` (1) | (2) historical documentation — descriptions of the legacy notebook's hardcoded `D:\PLI_Export_Project` paths and one `/tmp` mention in the cleanup record; deliberately retained |
| `docs/CLEANUP_AUDIT_PROPOSAL` (1) | (2) historical (quotes the old paths it scrubbed) |
| **Category (1) genuine current dependencies: ZERO. Category (3) accidental: ZERO.** | |

## Part I — Reproducibility assessment

- **Python:** 3.10+ (statsmodels 0.15 syntax; `ETSModel`, `zivot_andrews` used). Not pinned anywhere → recommend a `requirements.txt` (needs approval to add).
- **Packages:** pandas, numpy, matplotlib, statsmodels (≥0.14), scipy, ruptures; `requests` for `fetch_meidb.py` only.
- **Execution order:** `fetch_meidb.py` (optional; raw data committed) → notebooks 01→04 (independent of each other except conceptual order) → `05_volatility_R12.py`. Working directory: `05_analysis/`.
- **Required inputs:** `04_clean_data/master_monthly_exports.csv` (committed) — the single file everything reads.
- **Missing pieces:** the four uncommitted writers (Part F) and the uncommitted `vol_01` figure script (Part D); no `requirements.txt`; notebooks have no stored outputs (GitHub rendering).

## Part J — Proposed final structure

**Recommendation: keep the current tree.** The audit shows the conceptual `05_analysis/{notebooks,src,scripts}` and `07_figures/{eda,…}` splits would require editing five module save-paths, four notebooks' import context, and every figure reference in the frozen report — real breakage risk on a frozen project — to gain organization that filename prefixes and the numbered folders already provide. The tree already has clear data flow (01→04 data, 05 code, 06/07 outputs, 08 report, docs process, 99 legacy) and, after the fixes below, zero unexplained files.

```
PLI_Export_Project/
├── README.md · .gitignore · (proposed: requirements.txt)
├── 01_raw_data/          source data (never overwritten)
├── 02_policy_sources/    dates + source log
├── 03_mapping/           basket definitions
├── 04_clean_data/        master panel
├── 05_analysis/          4 notebooks + 6 .py (proposed: +1 reproduction script)
├── 06_results/           12 frozen CSVs (authoritative)
├── 07_figures/           44 PNGs, prefix-organized (kept flat)
├── 08_report/            report + evidence table + memo + findings
├── docs/                 audit trail  ·  docs/archive/ (gitignored)
└── 99_legacy/            immutable, gitignored
```

## Part K — Final classification (delta only; everything else = KEEP as inventoried in Part A)

- KEEP–essential: 01–08 contents, README, .gitignore, docs core files.
- KEEP–supporting evidence: continuity probe, b1_code_detail, verification/validation memos, phase findings.
- ARCHIVE (already done): the 6 files in `docs/archive/`.
- EXCLUDE FROM GITHUB (already gitignored): `99_legacy/`, `docs/archive/`, `__pycache__/`.
- DELETE: **nothing new.** Only candidate: `05_analysis/__pycache__/` (auto-regenerated; already gitignored — deletion optional).

## Part L — "Can I explain it?" test

| Component | What you must be able to say | Opacity flag |
|---|---|---|
| `its_core.design` | How T, Post, TimeAfter, month FE, Covid are built; why TimeAfter = max(0, T−T_Ds) | None — 25 readable lines |
| `robustness_core.fit_arma` | AIC picks the error structure from 9 pre-declared candidates; converged-only; AR(1) always shown too | None |
| `forecast_core.validate/select` | Expanding-origin validation; RMSE-at-12 subject to coverage ∈ [0.85,1] | None |
| `f_snaive` interval math | SE(h) = σ of 12-differences × √⌈h/12⌉ | **Mildly opaque** — one comment would help; explanation: uncertainty grows stepwise each time the forecast stacks another year-over-year difference |
| `05_volatility_R12.py` `mbb/boot` | Moving-block bootstrap: resample 6-month blocks to preserve short-run dependence | None (documented) |
| `sup_f` / `bai_perron` | Diagnostic-only break scans | Fine — report already downgrades them |
| `fetch_meidb.py` CSRF logic | Portal requires a form token; the script refreshes it — not a credential | None |
| Duplicated `series()` helpers (3 files) | "Kept scripts self-contained; consolidation deferred to avoid touching frozen-result code" | Flagged — explanation above IS the answer |

## Part M-13 — Recommended code changes (all deferred, all need approval)

1. **Close the four writer gaps** (Part F) — transcript recovery, option (b) preferred: one guarded reproduction script; byte-verify like F-1.
2. Commit the `vol_01` figure's generating code the same way.
3. Add `requirements.txt` with pinned versions.
4. Add one comment to `f_snaive`'s interval formula.
5. Optional: remove `eda_core`'s unused import(s) — cosmetic only.
6. Decision: re-execute notebooks (on a guarded copy) to commit outputs for GitHub rendering — presentation only.
7. NOT recommended: figure subfolders, `src/` split, `series()` consolidation — churn on frozen code without benefit.

## Part M-14 — Unresolved risks

1. The four uncommitted writers are the only real reproducibility hole (fix #1).
2. Notebooks render output-free on GitHub until decision #6 is taken.
3. Re-running notebooks 02/03 as-is would overwrite frozen CSVs in place (deterministic ones should match; ARMA rows not guaranteed byte-stable) — anyone reproducing should use a guard; worth one README sentence.
4. No environment pin (fix #3): statsmodels API drift could break re-execution years from now.
5. `README.md` stub files in 02/05/raw_trade_data are thin — harmless, could be folded into the root README later.

---

**STOP — read-only audit complete. No action taken. Awaiting approval on fixes #1–#6 and the keep-flat structure recommendation.**
