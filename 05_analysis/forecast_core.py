"""
forecast_core.py — limited exploratory counterfactual forecasting (pre-specified protocol).

PURPOSE: execute the pre-planned counterfactual component. NOT a search for a PLI
effect. The existing conclusion — "no basket shows a trajectory change that survives
the pre-specified robustness framework" — is NOT subject to revision by this exercise.

LOCKED PROTOCOL
---------------
* Training and model selection use PRE-POLICY observations only. Post-policy data is
  never touched until one model per basket is selected and frozen.
* Candidates (declared, closed set):
    1. Seasonal naive:  yhat(t+h) = y(t+h-12), on ln(Y).
    2. ETS: additive Holt-Winters state-space on ln(Y) (error=add, trend=add,
       seasonal=add, s=12), damped and undamped variants. Within-family choice by
       the same validation criterion.
    3. SARIMA(0,1,1)(0,1,1)[12] on ln(Y) — the single pre-declared "airline"
       specification. ADMISSION RULE (diagnostics-based, fixed here): SARIMA is
       admitted for a basket because the Phase-4 diagnostics showed significant
       seasonal autocorrelation in monthly log growth for that basket family;
       NO order search is performed.
* Validation: expanding-origin, minimum training window m = 30. For horizon h the
  h-step-ahead error is collected from every origin o in {m, ..., N_pre - h}.
* Selection criterion (locked): lowest RMSE of the 12-step-ahead errors across
  origins, subject to pooled 95% interval coverage in [0.85, 1.00] where intervals
  exist. If no candidate meets coverage, fall back to seasonal naive and report the
  failure. Post-policy performance plays NO role in selection.
* Horizons: h=12 primary, h=6 secondary, h=18 for B4 only.
* B1_MOBILE: SEASONAL NAIVE ONLY. Not model-selected. 28 pre-policy months; training
  ends in the COVID-distorted period. No substantive counterfactual claim.
* The gap is "actual minus pre-policy time-series counterfactual". It is never a
  PLI effect, impact, treatment effect, or causal estimate. No significance testing
  on gaps.
"""

from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.exponential_smoothing.ets import ETSModel
from statsmodels.tsa.statespace.sarimax import SARIMAX

import its_core as I

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
FIGS = ROOT / "07_figures"
RESULTS = ROOT / "06_results"

M_MIN = 30
HORIZONS = {"B1_MOBILE": [6, 12], "B2_PHARMA": [6, 12],
            "B3_AC": [6, 12], "B4_TEXTILE": [6, 12, 18]}
PRIMARY_H = 12
Z95, Z80 = 1.959964, 1.281552


# ----------------------------------------------------------- fit/forecast
def f_snaive(y_tr: pd.Series, h: int):
    """Seasonal naive on ln(Y) with intervals from training 12-differences."""
    last12 = y_tr.iloc[-12:].values
    point = np.array([last12[i % 12] for i in range(h)])
    d = (y_tr - y_tr.shift(12)).dropna().values
    sd = d.std(ddof=1) if len(d) > 2 else np.nan
    k = np.array([np.sqrt(np.ceil((i + 1) / 12)) for i in range(h)])
    se = sd * k
    return point, se


def f_ets(y_tr: pd.Series, h: int, damped: bool):
    m = ETSModel(y_tr, error="add", trend="add", damped_trend=damped,
                 seasonal="add", seasonal_periods=12).fit(disp=False)
    pr = m.get_prediction(start=len(y_tr), end=len(y_tr) + h - 1)
    sf = pr.summary_frame(alpha=0.05)
    point = sf["mean"].values
    se = (sf["pi_upper"].values - sf["pi_lower"].values) / (2 * Z95)
    return point, se


def f_sarima(y_tr: pd.Series, h: int):
    m = SARIMAX(y_tr, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12),
                enforce_stationarity=True, enforce_invertibility=True
                ).fit(disp=False, maxiter=300, method="lbfgs")
    fc = m.get_forecast(h)
    return fc.predicted_mean.values, fc.se_mean.values


CANDS = {"snaive": lambda y, h: f_snaive(y, h),
         "ets": lambda y, h: f_ets(y, h, damped=False),
         "ets_damped": lambda y, h: f_ets(y, h, damped=True),
         "sarima_airline": lambda y, h: f_sarima(y, h)}


# ------------------------------------------------------------- validation
def validate(y_pre: pd.Series, h_max: int, models=None):
    """Expanding-origin validation. Returns per-model metrics and per-step records."""
    models = models or list(CANDS)
    n = len(y_pre)
    recs = []
    for name in models:
        fails = 0
        for o in range(M_MIN, n - 1):                       # origin = train length
            h_here = min(h_max, n - o)
            if h_here < 1:
                continue
            try:
                point, se = CANDS[name](y_pre.iloc[:o], h_here)
            except Exception:
                fails += 1
                continue
            act = y_pre.iloc[o:o + h_here].values
            for i in range(h_here):
                err = act[i] - point[i]
                cov = (abs(err) <= Z95 * se[i]) if np.isfinite(se[i]) else np.nan
                recs.append(dict(model=name, origin=o, h=i + 1,
                                 err=err, abs_err=abs(err),
                                 pct_err=abs(err / act[i]) * 100,
                                 cov95=cov))
        if fails:
            recs.append(dict(model=name, origin=-1, h=0, err=np.nan,
                             abs_err=np.nan, pct_err=np.nan, cov95=np.nan))
    return pd.DataFrame(recs)


def metrics(recs: pd.DataFrame, h: int):
    out = []
    for name, d in recs[recs.h == h].groupby("model"):
        out.append(dict(model=name, h=h, n_origins=len(d),
                        rmse=np.sqrt((d.err ** 2).mean()),
                        mae=d.abs_err.mean(), mape=d.pct_err.mean()))
    return pd.DataFrame(out)


def coverage(recs: pd.DataFrame, h_max: int):
    d = recs[(recs.h >= 1) & (recs.h <= h_max)].dropna(subset=["cov95"])
    return d.groupby("model").cov95.agg(["mean", "count"]).rename(
        columns={"mean": "cov95_pooled", "count": "n_points"})


def select(recs: pd.DataFrame, h: int = PRIMARY_H):
    """Locked rule: lowest RMSE of h-step errors, subject to pooled 95% coverage
    in [0.85, 1.00]. Fall back to seasonal naive if none qualifies."""
    met = metrics(recs, h).set_index("model")
    cov = coverage(recs, h)
    tab = met.join(cov)
    ok = tab[(tab.cov95_pooled >= 0.85) & (tab.cov95_pooled <= 1.00)]
    if len(ok):
        return ok.rmse.idxmin(), tab.reset_index(), False
    return "snaive", tab.reset_index(), True     # coverage failure -> benchmark


# --------------------------------------------------------- counterfactual
def counterfactual(y: pd.Series, n_pre: int, model: str, h: int):
    y_pre = y.iloc[:n_pre]
    point, se = CANDS[model](y_pre, h)
    idx = y.index[n_pre:n_pre + h]
    act = y.iloc[n_pre:n_pre + h].values
    rows = []
    for i in range(len(idx)):
        gap_log = act[i] - point[i]
        rows.append(dict(
            month=idx[i].strftime("%Y-%m"), h=i + 1, model=model,
            actual_lnY=round(act[i], 4), cf_lnY=round(point[i], 4),
            cf_lo95=round(point[i] - Z95 * se[i], 4),
            cf_hi95=round(point[i] + Z95 * se[i], 4),
            cf_lo80=round(point[i] - Z80 * se[i], 4),
            cf_hi80=round(point[i] + Z80 * se[i], 4),
            actual_usd=round(float(np.exp(act[i])), 2),
            cf_usd=round(float(np.exp(point[i])), 2),
            gap_log_pts=round(gap_log * 100, 2),
            gap_pct=round(100 * (np.exp(gap_log) - 1), 1),
            inside_95=bool(abs(gap_log) <= Z95 * se[i]) if np.isfinite(se[i]) else None))
    return pd.DataFrame(rows)


def plot_cf(y, n_pre, cf, basket, model, ds):
    fig, ax = plt.subplots(figsize=(9.8, 4.2))
    ax.plot(y.index, y.values, color="#1f4e79", lw=1.4, label="actual ln(Y)")
    ci = pd.PeriodIndex(cf.month, freq="M").to_timestamp()
    ax.plot(ci, cf.cf_lnY, color="#c62828", lw=1.6, ls="--",
            label=f"counterfactual ({model}, pre-policy fit)")
    ax.fill_between(ci, cf.cf_lo95, cf.cf_hi95, color="#c62828", alpha=0.12,
                    label="95% interval")
    ax.fill_between(ci, cf.cf_lo80, cf.cf_hi80, color="#c62828", alpha=0.18)
    ax.axvline(pd.Timestamp(ds + "-01"), color="crimson", lw=1.4, ls=":")
    ax.set_xlim(y.index[max(0, n_pre - 30)], ci[-1] + pd.DateOffset(months=2))
    ax.set_ylabel("ln(exports, US$ mn)")
    ax.set_title(f"{I.LABEL[basket]} — actual vs pre-policy time-series counterfactual "
                 f"(descriptive; NOT a causal estimate)", fontsize=9.5)
    ax.legend(fontsize=8); ax.grid(alpha=.25)
    p = FIGS / f"fc_01_{basket}_counterfactual.png"
    fig.savefig(p, dpi=160, bbox_inches="tight"); plt.close(fig)
    return p.name
