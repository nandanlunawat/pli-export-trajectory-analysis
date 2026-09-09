"""
robustness_core.py — Phase 6A/6B/6C.

6A  ARMA-errors cross-check on the identical locked ITS specification.
6B  Pre-specified robustness: COVID-adjusted window, pre-specified alternative
    intervention dates, B1 Transition_t carried forward, structural-break diagnostic.
6C  Controls C1/C2/C3 estimated at each pre-specified treated date.

NOT IN SCOPE: forecasting, volatility inference, any further model.

SELECTION RULES, DECLARED BEFORE ANY COEFFICIENT WAS INSPECTED
--------------------------------------------------------------
ARMA order is chosen by **AIC** over the fixed 9-model grid in GRID below, with
d=D=0 because the deterministic terms already carry trend and season. AIC scores
fit, not the significance of beta3. Only models that CONVERGE are eligible. A fixed
AR(1) variant is reported alongside so order selection is never doing the work alone.

Alternative intervention dates are taken verbatim from
02_policy_sources/pli_intervention_dates.csv. **No date was added, removed or
re-specified after seeing a result.**

INTERPRETATION RULE (binding on all reporting)
----------------------------------------------
A result significant in one specification but not in the stationary companion, the
ARMA-errors fit, or the pre-specified robustness set is **non-robust — not a finding**.
The locked levels specification remains the baseline; robustness variants never
replace it.
"""

from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.statespace.sarimax import SARIMAX

import its_core as I

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
FIGS = ROOT / "07_figures"
RESULTS = ROOT / "06_results"

# ---- pre-specified alternative intervention dates (verbatim from the registry) ----
ALT_DATES = {
    "B1_MOBILE":  {"notification": "2020-04", "elected_year1": "2021-08",
                   "minus3": "2020-05", "plus3": "2020-11", "lag6": "2021-02"},
    "B2_PHARMA":  {"notification": "2021-03", "fermentation_route": "2023-04",
                   "minus3": "2022-01", "plus3": "2022-07", "lag6": "2022-10"},
    "B3_AC":      {"notification": "2021-04", "gestation_2yr": "2023-04",
                   "minus3": "2022-01", "plus3": "2022-07", "lag6": "2022-10"},
    "B4_TEXTILE": {"notification": "2021-09", "gestation_start": "2022-04",
                   "minus3": "2024-01", "plus3": "2024-07"},
}
COVID_DROP = ("2020-03", "2020-09")          # locked robustness window
CONTROLS = ["C1_LEATHER", "C2_FOOTWEAR", "C3_COTTON"]
CONTROL_DATES = ["2020-08", "2022-04", "2024-04"]   # the three distinct treated dates
CTRL_LABEL = {"C1_LEATHER": "C1 Leather goods (Ch 42)",
              "C2_FOOTWEAR": "C2 Footwear (Ch 64)",
              "C3_COTTON": "C3 Cotton woven fabrics (5208-5212)"}

EXOG = ["T", "Post", "TimeAfter"] + I.MONTH_COLS + ["Covid"]


# ------------------------------------------------------------------ helpers
def design_at(df, basket, d_s, transition=False):
    """Locked design matrix, but with an arbitrary (pre-specified) break date."""
    s = df[df.basket_id == basket].set_index("date").asfreq("MS").copy()
    s["ln_y"] = np.log(s["y"])
    s["g"] = s["ln_y"].diff() * 100
    start = pd.Timestamp(I.PANEL_START + "-01")
    s["T"] = ((s.index.year - start.year) * 12 + (s.index.month - start.month)) + 1
    t_ds = int(s.loc[pd.Timestamp(d_s + "-01"), "T"])
    s["Post"] = (s["T"] >= t_ds).astype(int)
    s["TimeAfter"] = np.maximum(0, s["T"] - t_ds)
    s["Break"] = (s["T"] == t_ds).astype(int)
    s["Covid"] = s.index.strftime("%Y-%m").isin(I.COVID_MONTHS).astype(int)
    for m in range(1, 13):
        if m != I.REF_MONTH:
            s[f"M{m:02d}"] = (s.index.month == m).astype(int)
    if transition:
        lo, hi = (pd.Timestamp(x + "-01") for x in I.TRANSITION)
        s["Transition"] = ((s.index >= lo) & (s.index <= hi)).astype(int)
    s.attrs["t_ds"] = t_ds
    return s


def drop_covid(s):
    lo, hi = (pd.Timestamp(x + "-01") for x in COVID_DROP)
    return s[~((s.index >= lo) & (s.index <= hi))]


def ols_row(basket, spec, s, cols=None, note=""):
    cols = cols or EXOG
    X = sm.add_constant(s[cols], has_constant="add")
    m = sm.OLS(s["ln_y"], X).fit()
    h3 = sm.OLS(s["ln_y"], X).fit(cov_type="HAC",
                                  cov_kwds={"maxlags": 3, "use_correction": True})
    h12 = sm.OLS(s["ln_y"], X).fit(cov_type="HAC",
                                   cov_kwds={"maxlags": 12, "use_correction": True})
    lo, hi = h12.conf_int().loc["TimeAfter"]
    return dict(
        unit=basket, spec=spec, estimator="OLS+HAC", n=int(m.nobs),
        beta2_level=round(m.params["Post"], 5),
        beta2_se_hac3=round(h3.bse["Post"], 5), beta2_se_hac12=round(h12.bse["Post"], 5),
        beta2_p_hac12=round(h12.pvalues["Post"], 4),
        beta3_trendchange=round(m.params["TimeAfter"], 5),
        beta3_se_hac3=round(h3.bse["TimeAfter"], 5),
        beta3_se_hac12=round(h12.bse["TimeAfter"], 5),
        beta3_p_hac3=round(h3.pvalues["TimeAfter"], 4),
        beta3_p_hac12=round(h12.pvalues["TimeAfter"], 4),
        beta3_ci_lo=round(lo, 5), beta3_ci_hi=round(hi, 5),
        beta3_lgp_per_month=round(m.params["TimeAfter"] * 100, 3),
        beta1_pretrend=round(m.params["T"], 5),
        r2_adj=round(m.rsquared_adj, 4), converged=True, note=note)


# --------------------------------------------------------------- 6A  ARMA
# Pre-declared candidate error structures. Fixed BEFORE any coefficient was seen.
# Deliberately small: 96 observations and ~16 exogenous regressors will not support a
# wide ARMA search, and a large grid invites over-fitting the error process.
GRID = [(1, 0, 0, 0),   # AR(1)
        (2, 0, 0, 0),   # AR(2)
        (0, 1, 0, 0),   # MA(1)
        (1, 1, 0, 0),   # ARMA(1,1)
        (0, 0, 1, 0),   # seasonal AR(1)
        (0, 0, 0, 1),   # seasonal MA(1)
        (1, 0, 1, 0),   # AR(1) + seasonal AR(1)
        (1, 0, 0, 1),   # AR(1) + seasonal MA(1)
        (0, 1, 0, 1)]   # MA(1) + seasonal MA(1)


def fit_arma(s, cols=None, grid=GRID):
    """SARIMAX with the identical exog matrix. Order chosen by AIC (fit, not
    significance). Returns best fit, its order, and the full AIC scan."""
    cols = cols or EXOG
    y, X = s["ln_y"], s[cols]
    scan, best, best_key = [], None, None
    for (p, q, P, Q) in grid:
        try:
            m = SARIMAX(y, exog=X, order=(p, 0, q),
                        seasonal_order=(P, 0, Q, 12),
                        trend="c", enforce_stationarity=True,
                        enforce_invertibility=True).fit(disp=False, maxiter=500,
                                                        method="lbfgs")
            scan.append(dict(order=f"({p},0,{q})({P},0,{Q})[12]", aic=round(m.aic, 3),
                             bic=round(m.bic, 3), converged=bool(m.mle_retvals.get("converged", True))))
            if m.mle_retvals.get("converged", True) and (best is None or m.aic < best.aic):
                best, best_key = m, (p, q, P, Q)
        except Exception:
            scan.append(dict(order=f"({p},0,{q})({P},0,{Q})[12]", aic=np.nan,
                             bic=np.nan, converged=False))
    return best, best_key, pd.DataFrame(scan).sort_values("aic")


def arma_row(unit, spec, m, key, extra_note=""):
    conv = bool(m.mle_retvals.get("converged", True))
    lb = acorr_ljungbox(pd.Series(m.resid).iloc[1:], lags=[12], return_df=True)
    ci = m.conf_int()
    return dict(
        unit=unit, spec=spec,
        estimator=f"SARIMAX({key[0]},0,{key[1]})({key[2]},0,{key[3]})[12]",
        n=int(m.nobs),
        beta2_level=round(m.params["Post"], 5),
        beta2_se_hac3=np.nan, beta2_se_hac12=round(m.bse["Post"], 5),
        beta2_p_hac12=round(m.pvalues["Post"], 4),
        beta3_trendchange=round(m.params["TimeAfter"], 5),
        beta3_se_hac3=np.nan, beta3_se_hac12=round(m.bse["TimeAfter"], 5),
        beta3_p_hac3=np.nan, beta3_p_hac12=round(m.pvalues["TimeAfter"], 4),
        beta3_ci_lo=round(ci.loc["TimeAfter", 0], 5),
        beta3_ci_hi=round(ci.loc["TimeAfter", 1], 5),
        beta3_lgp_per_month=round(m.params["TimeAfter"] * 100, 3),
        beta1_pretrend=round(m.params["T"], 5),
        r2_adj=np.nan, converged=conv,
        note=(f"AIC={m.aic:.2f}; LB(12) on resid p={lb.loc[12,'lb_pvalue']:.4f}; "
              f"{extra_note}").strip("; "))


# ------------------------------------------------- 6B  structural break
def sup_f(s, trim=0.15):
    """Quandt-Andrews supF for a break in intercept AND trend, scanning candidate
    dates with symmetric trimming. Classical max-Chow; the argmax is a point
    estimate of an unknown break, not a test that a given date is the break."""
    y = s["ln_y"].values
    base = ["T"] + I.MONTH_COLS + ["Covid"]
    X0 = sm.add_constant(s[base].values, has_constant="add")
    rss0 = sm.OLS(y, X0).fit().ssr
    n = len(y)
    lo, hi = int(np.floor(trim * n)), int(np.ceil((1 - trim) * n))
    out = []
    for i in range(lo, hi):
        post = (np.arange(n) >= i).astype(float)
        ta = np.maximum(0, np.arange(n) - i).astype(float)
        X1 = np.column_stack([X0, post, ta])
        rss1 = sm.OLS(y, X1).fit().ssr
        k = X1.shape[1]
        f = ((rss0 - rss1) / 2) / (rss1 / (n - k))
        out.append((s.index[i], f))
    d = pd.DataFrame(out, columns=["date", "F"])
    r = d.loc[d.F.idxmax()]
    return d, r.date, float(r.F)


def bai_perron(s, n_bkps=2):
    """Bai-Perron-style multiple-break detection (ruptures, Binseg on a linear
    model) applied to the seasonally-and-COVID-adjusted log series."""
    import ruptures as rpt
    base = ["T"] + I.MONTH_COLS + ["Covid"]
    X = sm.add_constant(s[base], has_constant="add")
    resid = sm.OLS(s["ln_y"], X).fit().resid.values.reshape(-1, 1)
    algo = rpt.Binseg(model="l2").fit(resid)
    idx = algo.predict(n_bkps=n_bkps)[:-1]
    return [s.index[i].strftime("%Y-%m") for i in idx]


# ------------------------------------------------------------ plotting
def plot_robustness(mat, basket):
    d = mat[(mat.unit == basket) & mat.beta3_se_hac12.notna()].copy()
    if d.empty:
        return None
    d = d.reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(9.5, max(3.0, 0.42 * len(d))))
    yv = np.arange(len(d))
    ax.errorbar(d.beta3_lgp_per_month, yv,
                xerr=1.96 * d.beta3_se_hac12 * 100, fmt="o", color="#1f4e79",
                ecolor="#90a4ae", capsize=3, ms=5)
    ax.axvline(0, color="crimson", lw=1.2, ls="--")
    ax.set_yticks(yv); ax.set_yticklabels(d.spec, fontsize=7.5)
    ax.invert_yaxis()
    ax.set_xlabel("β₃  (log-growth points per month), 95% CI")
    ax.set_title(f"{I.LABEL.get(basket, basket)} — β₃ across specifications")
    p = FIGS / f"rob_01_{basket}_beta3_forest.png"
    fig.savefig(p, bbox_inches="tight"); plt.close(fig)
    return p.name
