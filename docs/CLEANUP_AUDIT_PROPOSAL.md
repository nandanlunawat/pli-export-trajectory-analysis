# Project Cleanup Audit — Proposal (NO ACTION TAKEN)

**Date:** 8 September 2026. Read-only audit. Nothing has been deleted, moved, renamed, or modified. All classifications below are proposals awaiting explicit approval. Total project size ≈ 7 MB (07_figures 4.7 MB, 99_legacy 1.5 MB) — size is not a constraint anywhere.

Duplicate checks were done on content (md5 / column counts / row-level merges), not filenames.

---

## 1. Two substantive findings first

**F-1 — Reproducibility gap (genuine issue).** `06_results/volatility_results.csv` and `06_results/ITS_R12_quadratic_pretrend.csv` have **no committed generating script or notebook**. They were produced by session scripts that were never saved (grep confirms: no file in `05_analysis/` writes either; `04_forecasting.ipynb` only mentions R12 in markdown). Every other results file traces to committed code. **Proposal:** reconstruct one script/notebook (`05_analysis/05_volatility_R12.py` + a short notebook cellset) that regenerates both CSVs *exactly from the locked specifications* (±24-month windows, MBB block 6/4000 reps/seed 20260902; R12 = baseline + (T/100)²), verify byte-level agreement with the frozen CSVs, and commit it. This reproduces frozen numbers — it is not new analysis — but per rule 8 it awaits your approval.

**F-2 — No root README exists.** There is no `README.md` at the project root (only per-directory stubs). The GitHub-ready README (objective, data, methodology, findings, limitations, reproducibility, appendix→file map) is **not currently sufficient — it is absent**. Already queued as a deliverable.

---

## 2. Classification — every file

### A. MUST RETAIN (reproducibility, evidence, final report, pipeline)

| Path | Role |
|---|---|
| `01_raw_data/raw_trade_data/meidb_hs6_extract_2026-08-29/` (4 files, 29 KB) | Raw extract: panel_compact, b1_code_detail, reconciliation_aggregates, extraction_manifest. Never overwrite. |
| `01_raw_data/raw_trade_data/meidb_continuity_probe_2026-08-29.csv` | Empirical evidence for the B1 HS-transition (Appendix B source). |
| `01_raw_data/raw_trade_data/README.md` | Raw-data provenance stub. |
| `02_policy_sources/pli_intervention_dates.csv` | AUTHORITATIVE date registry (21 cols, merged). |
| `02_policy_sources/source_log.csv` + `README.md` | S01–S42 source log (Appendix A). |
| `03_mapping/hs_mapping_master.csv`, `control_sector_mapping.csv`, `control_hs6_codes.csv` | Basket/control definitions (Appendix B). |
| `04_clean_data/master_monthly_exports.csv` + `SCHEMA.md` | Master dataset + schema. |
| `05_analysis/` — `fetch_meidb.py`, `eda_core.py`, `its_core.py`, `robustness_core.py`, `forecast_core.py`, notebooks `01_EDA` – `04_forecasting`, `README.md` | The complete final pipeline. **All four notebooks are required** (each generates retained results); none is exploratory/obsolete. Scripts are imported by the notebooks; `fetch_meidb.py` is the data pipeline. No absolute paths (all use `Path(__file__)`-relative). |
| `06_results/` — all 12 CSVs | **Authoritative numerical source of truth** (with `08_report/FINAL_EVIDENCE_TABLE.md` as the transcription layer). |
| `07_figures/` — all 44 PNGs (4.7 MB) | All referenced by report main text or appendices D–H. |
| `08_report/` — `FINAL_REPORT.md`, `FINAL_EVIDENCE_TABLE.md`, `research_design_memo.md`, `DATASET_VALIDATION_REPORT.md`, `data_quality_report.md`, `verification_status.md`, `backward_extension_feasibility.md` (Appendix C), `EDA_findings.md`, `ITS_preliminary_findings.md`, `ITS_robustness_findings.md`, `FORECASTING_findings.md` | Final report + locked memo + validation/verification evidence + the four phase-findings memos the appendices and interview defence rest on. |
| `docs/` — `DECISION_LOG.md`, `CHANGE_PROPOSAL_001/002/003`, `source_log.md`, `PROJECT_STATUS.md` | Rule-7/8/10 audit trail. |
| `99_legacy/` — everything (see §4) | Immutable historical archive. The two legacy notebooks are **not** duplicates of each other (different md5, different sizes) — both stay. |

### B. RETAIN BUT CLEAN/CONSOLIDATE

| Path | Issue | Proposal |
|---|---|---|
| `docs/PROJECT_STATUS.md`, `docs/00_PHASE1_AUDIT_AND_DESIGN.md`, `docs/source_log.md` | Contain machine-specific absolute paths (`C:\Users\nanda\...`, `/sessions/...`) — harmless but expose local username/layout | Before publication: scrub absolute paths to relative ones, or keep the files out of the public repo (they are process docs). Content otherwise A-grade audit trail. |
| `.gitkeep` × 8 | Redundant once directories contain files | Drop at publication (cosmetic; zero risk). |
| Per-directory `README.md` stubs (02, 05, raw_trade_data) + missing root README | Fragmented | Consolidate into the new root README (queued deliverable); keep stubs or fold in. |

### C. ARCHIVE (audit-trail value; not publication-facing) — propose `docs/archive/`

| Path | Type/size | Why |
|---|---|---|
| `08_report/REPORT_OUTLINE.md` | md, 21 KB | Drafting scaffold; superseded by FINAL_REPORT. |
| `08_report/FINAL_findings_and_recommendation.md` | md, 16 KB | Interim memo superseded by FINAL_REPORT; **but contains the interview script** — retain in archive, feed into the interview-prep sheet. |
| `08_report/HOSTILE_METHODOLOGICAL_AUDIT.md` | md, 30 KB | Audit-trail document; excellent interview prep; not part of the polished report set. |
| `docs/pli_sector_mapping_PROPOSED.csv` / `.xlsx` | 15/18 KB | Phase-1 proposals superseded by `03_mapping/hs_mapping_master.csv`; retained per earlier no-deletion decision. |
| `03_mapping/pli_intervention_dates.csv` | csv, 6 KB, 19 cols | Superseded: verified strictly-additive merge into the 21-column `02_policy_sources` copy (D_s unchanged, 7 distinctive strings preserved). Deletion previously declined → archive instead. |

### D. EXCLUDE FROM GITHUB (keep locally)

| Path | Why | .gitignore? |
|---|---|---|
| `99_legacy/` (1.5 MB) | Prior project (docx/pdf/xlsx/notebooks with outputs); historically immutable but not part of the publication-facing analysis; the legacy notebooks embed local paths | Yes — `99_legacy/` (alternative: include it for provenance; your call — content is your own work and contains nothing sensitive) |
| `docs/archive/` (if created) | Process history, machine paths | Optional |

Nothing else qualifies: raw data is 65 KB (include it — it is the reproducibility anchor), there are no browser caches, HTML dumps, `__pycache__`, checkpoints, or environment files in the tree.

### E. SAFE TO DELETE

| Path | Type / size | Why redundant | Replaced by | Reproducibility impact | .gitignore instead? |
|---|---|---|---|---|---|
| `05_analysis/_tmp_6a.csv` | csv, 1.8 KB | Temporary Phase-6A output; **row-level merge confirms all 8 rows are contained verbatim in `06_results/ITS_robustness_matrix.csv`** | ITS_robustness_matrix.csv | None (regenerable from 03_robustness notebook) | Also add `_tmp_*.csv` pattern |
| `01_raw_data/legacy_annual_data/india_exports_commodities.xlsx` | xlsx, 16.8 KB | **Byte-identical (same md5) to the immutable copy in `99_legacy/data_original/`**; not read by any pipeline code | `99_legacy/data_original/india_exports_commodities.xlsx` | None — final pipeline uses monthly MEIDB only; the annual file is legacy input | No |

Nothing else is proposed for deletion. No file was classified redundant on metadata alone.

---

## 3. Direct answers to your nine questions

1. **Required notebooks:** all four (`01_EDA`, `02_ITS_diagnostics`, `03_robustness_ITS`, `04_forecasting`) — each writes retained results/figures.
2. **Exploratory/obsolete notebooks:** none in `05_analysis/`; the only obsolete notebooks are the two in `99_legacy/` (immutable).
3. **Scripts executed by the final pipeline:** `fetch_meidb.py` (extraction) → notebooks importing `eda_core`, `its_core`, `robustness_core`, `forecast_core`. **Gap:** volatility/R12 script missing (F-1).
4. **Authoritative numerical source of truth:** the 12 CSVs in `06_results/`, transcribed via `08_report/FINAL_EVIDENCE_TABLE.md`.
5. **Raw data vs GitHub:** all raw files are tiny (≤ 29 KB) — include them; only `99_legacy/` is proposed for exclusion, on publication-cleanliness rather than size grounds.
6. **Absolute local paths:** none in any `05_analysis/` code; present only in `docs/PROJECT_STATUS.md`, `docs/00_PHASE1_AUDIT_AND_DESIGN.md`, `docs/source_log.md`, and the two legacy notebooks (immutable). Scrub the three docs before publication.
7. **Credentials/private info:** none found. The `_token` in `fetch_meidb.py` is CSRF-refresh logic against the public MEIDB portal, not a stored secret. Only exposure is the local Windows username inside the three docs files (see 6).
8. **Proposed `.gitignore`:** `__pycache__/`, `*.pyc`, `.ipynb_checkpoints/`, `_tmp_*.csv`, `.DS_Store`, `Thumbs.db`, `*.gz` (any future raw-cache), `99_legacy/` (if excluded), `docs/archive/` (optional).
9. **GitHub-ready README:** does not exist — must be written (queued deliverable).

---

## 4. Proposed CLEAN PROJECT TREE

```
PLI_Export_Project/
├── README.md                      [CREATE — currently missing]
├── .gitignore                     [CREATE — entries in §3.8]
├── 01_raw_data/
│   └── raw_trade_data/            KEEP (extract dir + continuity probe + README)
│       └── legacy_annual_data/india_exports_commodities.xlsx   DELETE (md5-identical to 99_legacy copy)
├── 02_policy_sources/             KEEP (registry, source log)
├── 03_mapping/                    KEEP (3 mapping files)
│   └── pli_intervention_dates.csv ARCHIVE (superseded; merge verified)
├── 04_clean_data/                 KEEP (master CSV + schema)
├── 05_analysis/                   KEEP (5 .py + 4 notebooks)
│   ├── 05_volatility_R12.py       CREATE (F-1 — closes reproducibility gap; needs approval)
│   └── _tmp_6a.csv                DELETE (verbatim subset of robustness matrix)
├── 06_results/                    KEEP (all 12 CSVs — source of truth)
├── 07_figures/                    KEEP (all 44 figures)
├── 08_report/                     KEEP (report, evidence table, memo, validation, phase findings)
│   → REPORT_OUTLINE.md, FINAL_findings_and_recommendation.md,
│     HOSTILE_METHODOLOGICAL_AUDIT.md        ARCHIVE (docs/archive/)
├── docs/                          KEEP (decision log, CPs, status, source log — scrub paths pre-publication)
│   └── archive/                   CREATE (holds items marked ARCHIVE)
└── 99_legacy/                     KEEP LOCALLY, immutable — EXCLUDE FROM GITHUB (or include; your call)
```

**Awaiting approval for:** the 2 deletions, the 5 archive moves, creation of `docs/archive/`, the F-1 reconstruction script, path-scrubbing in 3 docs files, and the 99_legacy GitHub in/out decision. Nothing executed.
