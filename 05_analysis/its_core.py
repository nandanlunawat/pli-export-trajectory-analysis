"""
its_core.py — Phase 5 interrupted time series: LOCKED design matrix, baseline fit
and residual diagnostics.

SCOPE — what this module does:
  * builds the exact locked design matrix
  * fits the baseline ITS by OLS
  * reports beta1, beta2, beta3 with HAC standard errors at lags 3 and 12
  * residual ACF/PACF, Ljung-Box, Breusch-Godfrey, ADF-on-residuals
  * the stationary growth-rate companion
  * the pre-specified B1 Jan-Apr 2022 Transition_t robustness

SCOPE — what this module deliberately does NOT do:
  * no forecasting, no volatility inference, no control estimation,
    no full robustness matrix, no alternative break dates, no model selection.

LOCKED SPECIFICATION (08_report/research_design_memo.md; Decision Log D-001..D-003):

    ln(Y_t) = b0 + b1*T + b2*Post + b3*TimeAfter
              + sum_{m=2..12} gamma_m*Month_m + delta*Covid + eps

    T          = 1..96, April 2018 = 1
    Post       = 1{ T >= T_Ds }
    TimeAfter  = max(0, T - T_Ds)        <-- NOT +1; keeps b2 a clean level shift
    Covid      = 1{ Apr, May, Jun 2020 }
    Month      = 11 dummies, APRIL omitted as reference

    Growth companion:
    g_t = a0 + a1*Post + a2*Break + sum phi_m*Month_m
          + sum_k delta_k*CovidMonth_k + u
    Break      = 1{ t == T_Ds }                  differenced level jump
    CovidMonth = separate dummies Apr, May, Jun AND Jul 2020

    B1 only: Transition_t = 1{ Jan 2022 <= t <= Apr 2022 }, reported with and without.

UNITS: g is in LOG-GROWTH POINTS (lgp), not percentage growth.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_breusch_godfrey, acorr_ljungbox
from statsmodels.tsa.stattools import adfuller

ROOT = Path(__file__).resolve().parent.parent
CLEAN = ROOT / "04_clean_data" / "master_monthly_exports.csv"
FIGS = ROOT / "07_figures"
RESULTS = ROOT / "06_results"

# ---- LOCKED constants -------------------------------------------------------
D_S = {"B1_MOBILE": "2020-08", "B2_PHARMA": "2022-04",
       "B3_AC": "2022-04", "B4_TEXTILE": "2024-04"}
TREATED = list(D_S)
PANEL_START = "2018-04"
COVID_MONTHS = ["2020-04", "2020-05", "2020-06"]                 # level block
COVID_MONTHS_DIFF = ["2020-04", "2020-05", "2020-06", "2020-07"]  # differenced
TRANSITION = ("2022-01", "2022-04")                               # B1 only
REF_MONTH = 4                                                     # April omitted
HAC_LAGS = (3, 12)
LABEL = {"B1_MOBILE": "B1 Telephone sets (HS 8517.1x proxy)",
         "B2_PHARMA": "B2 Pharmaceutical formulations",
         "B3_AC": "B3 Air conditioners",
         "B4_TEXTILE": "B4 MMF fabrics"}

plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 160, "font.size": 9,
                     "axes.grid": True, "grid.alpha": 0.25,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "figure.autolayout": True})


# ---------------------------------------------------------------- design
def load_panel() -> pd.DataFrame:
    df = pd.read_csv(CLEAN)
    df["date"] = pd.PeriodIndex(df["month"], freq="M").to_timestamp()
    df["y"] = df["export_usd_mn"].astype(float)
    return df.sort_values(["basket_id", "date"])


def design(df: pd.DataFrame, basket: str, transition: bool = False) -> pd.DataFrame:
    """Construct the exact locked design matrix for one basket."""
    s = df[df.basket_id == basket].set_index("date").asfreq("MS").copy()
    s["ln_y"] = np.log(s["y"])
    s["g"] = s["ln_y"].diff() * 100                      # log-growth points

    start = pd.Timestamp(PANEL_START + "-01")
    s["T"] = ((s.index.year - start.year) * 12 + (s.index.month - start.month)) + 1
    t_ds = int(s.loc[pd.Timestamp(D_S[basket] + "-01"), "T"])

    s["Post"] = (s["T"] >= t_ds).astype(int)
    s["TimeAfter"] = np.maximum(0, s["T"] - t_ds)        # LOCKED: no +1
    s["Break"] = (s["T"] == t_ds).astype(int)            # differenced level jump
    s["Covid"] = s.index.strftime("%Y-%m").isin(COVID_MONTHS).astype(int)
    for m in COVID_MONTHS_DIFF:
        s[f"Cov_{m.replace('-', '')}"] = (s.index.strftime("%Y-%m") == m).astype(int)
    for m in range(1, 13):                               # April omitted
        if m != REF_MONTH:
            s[f"M{m:02d}"] = (s.index.month == m).astype(int)
    if transition:
        lo, hi = (pd.Timestamp(x + "-01") for x in TRANSITION)
        s["Transition"] = ((s.index >= lo) & (s.index <= hi)).astype(int)
    s.attrs["t_ds"] = t_ds
    s.attrs["basket"] = basket
    return s


MONTH_COLS = [f"M{m:02d}" for m in range(1, 13) if m != REF_MONTH]


def _fit(y, X, lags):
    X = sm.add_constant(X, has_constant="add")
    ols = sm.OLS(y, X).fit()
    hac = {L: sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": L, "use_correction": True})
           for L in lags}
    return ols, hac


def fit_baseline(s: pd.DataFrame, transition: bool = False):
    cols = ["T", "Post", "TimeAfter"] + MONTH_COLS + ["Covid"]
    if transition:
        cols += ["Transition"]
    return _fit(s["ln_y"], s[cols], HAC_LAGS)


def fit_growth(s: pd.DataFrame, transition: bool = False):
    d = s.dropna(subset=["g"])
    cov = [f"Cov_{m.replace('-', '')}" for m in COVID_MONTHS_DIFF]
    cols = ["Post", "Break"] + MONTH_COLS + cov
    if transition:
        cols += ["Transition"]
    return _fit(d["g"], d[cols], HAC_LAGS)


# ------------------------------------------------------------- reporting
def coef_row(basket, model, ols, hac, keys, extra=None):
    out = dict(basket_id=basket, model=model, n=int(ols.nobs),
               k=int(ols.df_model) + 1, r2=round(ols.rsquared, 4),
               r2_adj=round(ols.rsquared_adj, 4))
    for nice, name in keys.items():
        if name not in ols.params.index:
            continue
        b = ols.params[name]
        out[f"{nice}"] = round(b, 5)
        out[f"{nice}_se_ols"] = round(ols.bse[name], 5)
        for L, h in hac.items():
            out[f"{nice}_se_hac{L}"] = round(h.bse[name], 5)
            out[f"{nice}_t_hac{L}"] = round(b / h.bse[name], 3)
            out[f"{nice}_p_hac{L}"] = round(h.pvalues[name], 4)
        lo, hi = hac[12].conf_int().loc[name]
        out[f"{nice}_ci95_lo_hac12"] = round(lo, 5)
        out[f"{nice}_ci95_hi_hac12"] = round(hi, 5)
    if extra:
        out.update(extra)
    return out


def diagnostics(basket, model, ols, s=None):
    r = pd.Series(ols.resid)
    d = dict(basket_id=basket, model=model)
    lb = acorr_ljungbox(r, lags=[6, 12, 24], return_df=True)
    for L in (6, 12, 24):
        d[f"ljungbox_lag{L}_p"] = round(lb.loc[L, "lb_pvalue"], 4)
    for L in (6, 12):
        try:
            bg = acorr_breusch_godfrey(ols, nlags=L)
            d[f"breusch_godfrey_lag{L}_p"] = round(bg[3], 4)   # F-test p
        except Exception:
            d[f"breusch_godfrey_lag{L}_p"] = np.nan
    d["durbin_watson"] = round(sm.stats.durbin_watson(r), 3)
    try:
        d["adf_resid_p"] = round(adfuller(r, regression="n", autolag="AIC")[1], 4)
        d["adf_resid_note"] = ("Engle-Granger critical values apply to residuals with "
                               "estimated parameters; treat as suggestive only")
    except Exception:
        d["adf_resid_p"] = np.nan
    d["resid_sd_lgp" if model.startswith("growth") else "resid_sd_log"] = round(r.std(ddof=1), 4)
    return d


def plot_fit(s, ols, basket, tag=""):
    fig, axes = plt.subplots(2, 1, figsize=(9.5, 6.4), sharex=True)
    axes[0].plot(s.index, s["ln_y"], color="#1f4e79", lw=1.4, label="observed ln(Y)")
    axes[0].plot(s.index, ols.fittedvalues, color="#c62828", lw=1.2, ls="--", label="fitted")
    axes[0].axvline(pd.Timestamp(D_S[basket] + "-01"), color="crimson", lw=1.5, ls=":")
    axes[0].set_ylabel("ln(exports)")
    axes[0].set_title(f"{LABEL[basket]} — baseline ITS fit{tag}")
    axes[0].legend(fontsize=8)
    axes[1].axhline(0, color="black", lw=0.7)
    axes[1].plot(s.index, ols.resid, color="#6a1b9a", lw=1.1)
    axes[1].axvline(pd.Timestamp(D_S[basket] + "-01"), color="crimson", lw=1.5, ls=":")
    axes[1].set_ylabel("residual (log)"); axes[1].set_title("Residuals")
    p = FIGS / f"its_01_{basket}_fit{tag.replace(' ', '')}.png"
    fig.savefig(p, bbox_inches="tight"); plt.close(fig)
    return p.name


def plot_resid_diag(ols, basket, model="levels"):
    r = pd.Series(ols.resid)
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.4))
    plot_acf(r, lags=30, ax=axes[0], title=f"Residual ACF — {basket} ({model})")
    plot_pacf(r, lags=30, ax=axes[1], title=f"Residual PACF — {basket} ({model})", method="ywm")
    p = FIGS / f"its_02_{basket}_resid_{model}.png"
    fig.savefig(p, bbox_inches="tight"); plt.close(fig)
    return p.name


def to_pct(lgp: float) -> float:
    """Convert log-growth points to a simple percentage change."""
    return 100 * (np.exp(lgp / 100) - 1)
