# 05_analysis/

Planned modules. None written yet — the build is gated on checks C1 and C2 in
`08_report/data_quality_report.md`.

    fetch_meidb.py     CSRF-token POST loop, resumable, writes raw HTML to 01_raw_data/
    build_panel.py     parse -> map via 03_mapping/hs_mapping_master.csv -> 04_clean_data/
    validate.py        gates G1-G10 as hard assertions; fails loudly
    eda.py             STL, ACF/PACF, ADF/KPSS/Zivot-Andrews, seasonal subseries
    its.py             segmented regression + growth-rate companion, HAC and ARMA errors
    volatility.py      W1-W4 windows, rolling SD, MAD-shift, moving-block bootstrap
    forecast.py        rolling-origin validation, seasonal naive / ETS / SARIMA
    robustness.py      R1-R14 matrix

Rule: no post-policy data touches the forecast model selection. See memo section 4.4.
