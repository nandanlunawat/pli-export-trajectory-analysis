# PLI Scheme: Export Competitiveness and Export Trajectory Analysis

An interrupted time-series study of PLI-linked sector exports, India, April 2018 – March 2026.

## Research question

How did the export trajectories and volatility of selected PLI-linked product groups evolve around the implementation of the relevant Production Linked Incentive (PLI) schemes?

India's PLI schemes — fourteen sectoral programmes linking incentives to incremental sales of goods manufactured in India — are the country's flagship manufacturing-incentive effort, with export competitiveness among their stated objectives. Whether sectoral export behaviour changed around scheme implementation is the empirical question this project answers. The design is observational: **it estimates sector-level associations around implementation dates, not causal effects of the schemes.**

## Data

- **Source:** DGCI&S Monthly Export Import Data Bank (MEIDB), Department of Commerce, Government of India — monthly commodity-level exports at the HS-6 digit level, US$ million, retrieved 29 August 2026 (revised (R) vintage through March 2026).
- **Period:** April 2018 – March 2026, 96 months (the MEIDB monthly series begins January 2018; backward extension was investigated and is infeasible — see `08_report/backward_extension_feasibility.md`).
- **Panel:** 672 basket-month observations, 7 series, no missing values.
- The raw MEIDB extract is included in the repository (`01_raw_data/raw_trade_data/`) because the retained extract is small (~30 KB); `05_analysis/fetch_meidb.py` re-extracts it from the portal reproducibly.

## Baskets (high level)

| Basket | Product group | HS definition | Scheme date D_s |
|---|---|---|---|
| B1 | Mobile handsets (proxy) | union of 8517.1x codes across both 2022 HS transitions | 2020-08 |
| B2 | Pharmaceutical formulations | 3003 + 3004 | 2022-04 |
| B3 | Air conditioners | 8415 | 2022-04 |
| B4 | MMF textiles | 14 codes from the Textiles PLI annexure | 2024-04 |
| C1–C3 | Leather goods, footwear, cotton woven fabrics | descriptive comparators (not a DiD design) | — |

Baskets are HS-code proxies for scheme scope, **not** measures of PLI beneficiary output. Full definitions and continuity evidence: `03_mapping/` and `08_report/FINAL_REPORT.md` §3. The B1 basket repairs an empirically documented HS-code reallocation in January/April 2022.

## Methodology

Pre-specified segmented (interrupted) time-series regression on log monthly exports — pre-policy trend (β₁), immediate level shift (β₂), change in post-implementation trajectory (β₃) — with month fixed effects, a COVID indicator, and Newey–West HAC inference (lags 3 and 12), locked in a design memo before estimation (`08_report/research_design_memo.md`). Robustness: ARMA-error re-estimation, a stationary growth-rate companion regression, COVID-window exclusion, pre-registered alternative intervention dates, a quadratic pre-trend check, and structural-break diagnostics. Volatility: SD of monthly log growth in ±24-month windows with a moving-block bootstrap. A deliberately secondary exercise compares actuals with pre-policy time-series counterfactual forecasts; seasonal naïve is used for all four baskets, with B1 treated as a benchmark-only case and B2–B4 selected under the pre-specified protocol.

## Key findings

**Across four PLI-linked product groups, the analysis finds no robust evidence of a trajectory change specifically timed to PLI implementation over the study period; the results therefore do not establish either a positive or negative causal effect of the schemes on sector-level exports.**

- B3 (air conditioners) shows the largest positive estimated trajectory change (+0.87 lgp/month, HAC p = 0.0013) — but the estimate fails the growth-space companion and fixed-AR(1) checks, is significant at every candidate date across two years, and is absorbed by smooth curvature (partial correlation 0.970 with the quadratic term). The evidence indicates smooth acceleration from around late 2021, not a dated break at the scheme date.
- B1 (mobile handsets) carries the largest negative point estimate, but its 28-month pre-period — a data-availability constraint ending inside the COVID disruption — supports no directional claim.
- B2 and B4 show no robust evidence of a post-implementation trajectory change.
- The large descriptive volatility declines (B3 −52.7 lgp, B1 −24.0) reverse when COVID months are excluded (+6.2, +1.1); no bootstrap interval excludes zero. There is no robust volatility finding.
- In the counterfactual exercise, every post-policy actual lies inside the 95% forecast interval for every basket at every horizon.

**Sector-level associations reported here are not causal estimates.** Anything else that changed around the same dates — global demand, supply-chain reorientation, prices, the exchange rate, COVID — is inseparable from any policy contribution in this design.

## Limitations

No causal identification; HS baskets proxy scheme scope rather than beneficiary output; B1's short, COVID-overlapped pre-period; B3's break-vs-curvature identification boundary; COVID dominates any volatility comparison spanning 2020; B4 has only 24 post-policy months; B2/B3 forecast selection rests on 7 validation origins. Full treatment: `08_report/FINAL_REPORT.md` §11.

## Reproducibility

```
pip install -r requirements.txt
cd 05_analysis
python fetch_meidb.py            # (optional) re-extract raw data from MEIDB
# then run, in order:
#   01_EDA.ipynb                 -> EDA figures + EDA_summary.csv
#   02_ITS_diagnostics.ipynb     -> baseline ITS + 4 ITS_prelim_*.csv
#   03_robustness_ITS.ipynb      -> robustness matrix, break diagnostics, ARMA AIC scan
#   04_forecasting.ipynb         -> forecast validation + counterfactual CSVs
python 05_volatility_R12.py      # volatility + R12 (writes to 06_results_reproduction/)
```

The notebooks are committed **executed**, with results tables and all principal charts rendered inline (secondary residual-diagnostic figures and one retained Transition-fit diagnostic are stored in `07_figures/` only). Every one of the 12 result CSVs in `06_results/` is regenerated by this pipeline, and a full re-execution has been verified to reproduce all 12 **byte-identically** (statsmodels 0.15.0, Python 3.10; `05_volatility_R12.py` uses fixed seed 20260902 and writes to a separate directory by design so the frozen results are never overwritten). Raw data are never overwritten; new vintages get new dated directories.

## Repository structure

```
01_raw_data/        raw MEIDB extract + continuity probe (never overwritten)
02_policy_sources/  intervention-date registry, source log (S01–S42)
03_mapping/         HS basket and control definitions
04_clean_data/      master monthly panel + schema
05_analysis/        pipeline: fetch script, core modules, 4 notebooks, volatility/R12 script
06_results/         AUTHORITATIVE numerical results (12 CSVs)
07_figures/         all 44 figures
08_report/          final report, evidence table, design memo, validation + phase findings
docs/               decision log, change proposals, project status, source log
99_legacy/          original pre-project work — intentionally EXCLUDED from the public
                    repository (.gitignore); retained locally as an immutable archive
```

**Authoritative results:** the CSVs in `06_results/`, transcribed into `08_report/FINAL_EVIDENCE_TABLE.md`, which is the numerical source of truth for `08_report/FINAL_REPORT.md`.

## Appendix-to-file map (report appendices A–H)

| Appendix | Files |
|---|---|
| A — dates & sources | `02_policy_sources/pli_intervention_dates.csv`, `02_policy_sources/source_log.csv` |
| B — codes, extraction, validation | `03_mapping/*.csv`, `01_raw_data/raw_trade_data/`, `05_analysis/fetch_meidb.py`, `08_report/DATASET_VALIDATION_REPORT.md` |
| C — backward extension | `08_report/backward_extension_feasibility.md` |
| D — EDA | `07_figures/eda_*`, `06_results/EDA_summary.csv`, `08_report/EDA_findings.md` |
| E — baseline regressions & diagnostics | `06_results/ITS_prelim_*.csv`, `07_figures/its_*` |
| F — robustness | `06_results/ITS_robustness_matrix.csv`, `ITS_arma_aic_scan.csv`, `ITS_R12_quadratic_pretrend.csv`, `07_figures/rob_*` |
| G — volatility | `06_results/volatility_results.csv`, `07_figures/vol_01_*`, `eda_05/06_*` |
| H — forecasting | `06_results/forecast_validation.csv`, `forecast_counterfactual.csv`, `07_figures/fc_01_*` |

## Author

Nandan Lunawat — September 2026.
