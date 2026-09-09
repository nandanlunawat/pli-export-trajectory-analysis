"""
eda_core.py — Phase 4 exploratory diagnostics for the PLI export panel.

SCOPE: DIAGNOSIS ONLY. This module computes and plots. It does not estimate the
interrupted time series, does not forecast, does not test volatility, does not
run controls, and does not select a model. Nothing here may alter a locked
specification — the locked design is in 08_report/research_design_memo.md and
the outputs of this module are not permitted to change it.

Imported by 05_analysis/01_EDA.ipynb.
"""

from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.stattools import acf, adfuller, kpss, zivot_andrews

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
CLEAN = ROOT / "04_clean_data" / "master_monthly_exports.csv"
FIGS = ROOT / "07_figures"
RESULTS = ROOT / "06_results"
FIGS.mkdir(exist_ok=True)
RESULTS.mkdir(exist_ok=True)

# Locked intervention dates — authority: 02_policy_sources/pli_intervention_dates.csv
D_S = {
    "B1_MOBILE": "2020-08",
    "B2_PHARMA": "2022-04",
    "B3_AC": "2022-04",
    "B4_TEXTILE": "2024-04",
}
TREATED = list(D_S)
LABEL = {
    "B1_MOBILE": "B1 Telephone sets (HS 8517.1x proxy)",
    "B2_PHARMA": "B2 Pharmaceutical formulations",
    "B3_AC": "B3 Air conditioners",
    "B4_TEXTILE": "B4 MMF fabrics",
}
COVID = ("2020-04", "2020-06")

plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 160, "font.size": 9,
    "axes.grid": True, "grid.alpha": 0.25, "axes.spines.top": False,
    "axes.spines.right": False, "figure.autolayout": True,
})


# ---------------------------------------------------------------- data
def load() -> pd.DataFrame:
    df = pd.read_csv(CLEAN)
    df["date"] = pd.PeriodIndex(df["month"], freq="M").to_timestamp()
    df = df.sort_values(["basket_id", "date"])
    df["y"] = df["export_usd_mn"].astype(float)
    df["ln_y"] = np.log(df["y"])
    df["g"] = df.groupby("basket_id")["ln_y"].diff() * 100
    return df


def series(df: pd.DataFrame, b: str) -> pd.DataFrame:
    s = df[df.basket_id == b].set_index("date")
    return s.asfreq("MS")


def _mark(ax, b: str, covid: bool = True):
    ax.axvline(pd.Timestamp(D_S[b] + "-01"), color="crimson", lw=1.6, ls="--",
               label=f"D_s = {D_S[b]}")
    if covid:
        ax.axvspan(pd.Timestamp(COVID[0] + "-01"), pd.Timestamp(COVID[1] + "-01"),
                   color="grey", alpha=0.18, label="COVID Apr–Jun 2020")


def _save(fig, name: str):
    p = FIGS / name
    fig.savefig(p, bbox_inches="tight")
    plt.close(fig)
    return p.name


# ------------------------------------------------- 1-3 levels, logs, growth
def plot_level_log_growth(df: pd.DataFrame) -> list[str]:
    out = []
    for b in TREATED:
        s = series(df, b)
        fig, axes = plt.subplots(3, 1, figsize=(9.5, 8.4), sharex=True)
        axes[0].plot(s.index, s.y, color="#1f4e79", lw=1.4)
        axes[0].set_ylabel("US$ mn"); axes[0].set_title(f"{LABEL[b]} — monthly export level")
        axes[1].plot(s.index, s.ln_y, color="#2e7d32", lw=1.4)
        axes[1].set_ylabel("ln(exports)"); axes[1].set_title("Log exports")
        axes[2].axhline(0, color="black", lw=0.7)
        axes[2].plot(s.index, s.g, color="#8e24aa", lw=1.1)
        axes[2].set_ylabel("log-growth points"); axes[2].set_title("Monthly log growth  g = 100·Δln(Y)  [log-growth points, NOT % growth]")
        for ax in axes:
            _mark(ax, b)
        axes[0].legend(loc="upper left", fontsize=8, framealpha=0.9)
        out.append(_save(fig, f"eda_01_{b}_level_log_growth.png"))
    return out


# ------------------------------------------------------------ 4 seasonality
def plot_seasonality(df: pd.DataFrame) -> list[str]:
    out = []
    for b in TREATED:
        s = series(df, b).copy()
        s["m"] = s.index.month
        s["yr"] = s.index.year
        fig, axes = plt.subplots(1, 2, figsize=(11, 3.9))
        # month-of-year distribution of growth
        data = [s.loc[s.m == k, "g"].dropna().values for k in range(1, 13)]
        axes[0].axhline(0, color="black", lw=0.7)
        axes[0].boxplot(data, tick_labels=list("JFMAMJJASOND"))
        axes[0].set_title(f"{LABEL[b]} — monthly log growth by calendar month")
        axes[0].set_ylabel("log-growth points")
        # seasonal sub-series on log level, deviation from own annual mean
        dev = s.groupby("yr")["ln_y"].transform(lambda x: x - x.mean())
        prof = dev.groupby(s.m).mean() * 100
        axes[1].bar(range(1, 13), prof.values,
                    color=["#c62828" if v > 0 else "#1565c0" for v in prof.values])
        axes[1].set_xticks(range(1, 13)); axes[1].set_xticklabels(list("JFMAMJJASOND"))
        axes[1].axhline(0, color="black", lw=0.7)
        axes[1].set_title("Mean deviation from own-year mean (log points ×100)")
        axes[1].set_ylabel("log points vs year mean")
        out.append(_save(fig, f"eda_02_{b}_seasonality.png"))
    return out


def seasonal_profile(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for b in TREATED:
        s = series(df, b).copy()
        s["m"], s["yr"] = s.index.month, s.index.year
        dev = s.groupby("yr")["ln_y"].transform(lambda x: x - x.mean()) * 100
        prof = dev.groupby(s["m"]).mean()
        rows.append(dict(basket_id=b, **{f"m{k:02d}": round(prof.get(k, np.nan), 2)
                                         for k in range(1, 13)}))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- 5 STL
def plot_stl(df: pd.DataFrame) -> tuple[list[str], dict]:
    out, strength = [], {}
    for b in TREATED:
        s = series(df, b)
        res = STL(s.ln_y, period=12, robust=True).fit()
        # Hyndman seasonal / trend strength on the decomposition
        rv = np.var(res.resid, ddof=1)
        f_s = max(0.0, 1 - rv / np.var(res.seasonal + res.resid, ddof=1))
        f_t = max(0.0, 1 - rv / np.var(res.trend + res.resid, ddof=1))
        strength[b] = dict(seasonal_strength=round(f_s, 3), trend_strength=round(f_t, 3),
                           resid_sd_lgp=round(np.std(res.resid, ddof=1) * 100, 2))
        fig, axes = plt.subplots(4, 1, figsize=(9.5, 8.6), sharex=True)
        for ax, (dat, ttl) in zip(axes, [
            (s.ln_y, "ln(exports) observed"), (res.trend, "trend"),
            (res.seasonal, "seasonal"), (res.resid, "remainder")]):
            ax.plot(s.index, dat, lw=1.2, color="#1f4e79")
            ax.set_title(ttl, fontsize=9)
            _mark(ax, b, covid=False)
        axes[3].axhline(0, color="black", lw=0.7)
        fig.suptitle(f"{LABEL[b]} — STL decomposition of log exports "
                     f"(F_seasonal={f_s:.2f}, F_trend={f_t:.2f})", y=1.005)
        out.append(_save(fig, f"eda_03_{b}_stl.png"))
    return out, strength


# ------------------------------------------------------------- 6 ACF/PACF
def plot_acf_pacf(df: pd.DataFrame) -> list[str]:
    out = []
    for b in TREATED:
        s = series(df, b)
        g = s.g.dropna()
        fig, axes = plt.subplots(2, 2, figsize=(10.5, 6.2))
        plot_acf(s.ln_y, lags=36, ax=axes[0, 0], title="ACF — ln(exports)")
        plot_pacf(s.ln_y, lags=36, ax=axes[0, 1], title="PACF — ln(exports)", method="ywm")
        plot_acf(g, lags=36, ax=axes[1, 0], title="ACF — monthly log growth")
        plot_pacf(g, lags=36, ax=axes[1, 1], title="PACF — monthly log growth", method="ywm")
        fig.suptitle(f"{LABEL[b]} — autocorrelation structure", y=1.01)
        out.append(_save(fig, f"eda_04_{b}_acf_pacf.png"))
    return out


def acf_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for b in TREATED:
        s = series(df, b)
        g = s.g.dropna()
        a_l = acf(s.ln_y, nlags=13, fft=False)
        a_g = acf(g, nlags=13, fft=False)
        n = len(g)
        rows.append(dict(basket_id=b,
                         acf1_lnY=round(a_l[1], 3), acf12_lnY=round(a_l[12], 3),
                         acf1_growth=round(a_g[1], 3), acf12_growth=round(a_g[12], 3),
                         signif_band_95=round(1.96 / np.sqrt(n), 3), n_growth=n))
    return pd.DataFrame(rows)


# ------------------------------------------------- 7-8 stationarity & breaks
def _adf(x, reg):
    r = adfuller(x, regression=reg, autolag="AIC")
    return r[0], r[1], r[2]


def _kpss(x, reg):
    st, p, lags, _ = kpss(x, regression=reg, nlags="auto")
    return st, p


def stationarity_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for b in TREATED:
        s = series(df, b)
        ln, g = s.ln_y.dropna(), s.g.dropna()
        r = dict(basket_id=b)
        st, p, lag = _adf(ln, "ct")
        r.update(adf_lnY_ct_stat=round(st, 3), adf_lnY_ct_p=round(p, 4), adf_lnY_lags=lag)
        st, p, lag = _adf(g, "c")
        r.update(adf_growth_c_stat=round(st, 3), adf_growth_c_p=round(p, 4), adf_growth_lags=lag)
        st, p = _kpss(ln, "ct")
        r.update(kpss_lnY_ct_stat=round(st, 4), kpss_lnY_ct_p=round(p, 4))
        st, p = _kpss(g, "c")
        r.update(kpss_growth_c_stat=round(st, 4), kpss_growth_c_p=round(p, 4))
        # break-aware unit root: Zivot-Andrews, break in both intercept and trend
        try:
            za = zivot_andrews(ln, regression="ct", autolag="AIC")
            stat, pv, crit, blag, bpidx = za[0], za[1], za[2], za[3], za[4]
            bdate = s.index[int(bpidx)].strftime("%Y-%m")
            r.update(za_lnY_stat=round(stat, 3), za_lnY_p=round(pv, 4),
                     za_lnY_crit5=round(crit["5%"], 3), za_break=bdate)
        except Exception as e:                                   # pragma: no cover
            r.update(za_lnY_stat=np.nan, za_lnY_p=np.nan,
                     za_lnY_crit5=np.nan, za_break=f"FAILED: {e}")
        rows.append(r)
    return pd.DataFrame(rows)


# --------------------------------------------------- 9 rolling volatility
def plot_rolling_vol(df: pd.DataFrame) -> list[str]:
    out = []
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 6.4))
    for ax, b in zip(axes.ravel(), TREATED):
        s = series(df, b)
        rv = s.g.rolling(6).std()
        ax.plot(s.index, rv, color="#ef6c00", lw=1.4)
        _mark(ax, b)
        ax.set_title(f"{LABEL[b]}", fontsize=9)
        ax.set_ylabel("6-m rolling SD of g (lgp)")
    fig.suptitle("6-month rolling volatility of monthly log growth", y=1.01)
    out.append(_save(fig, "eda_05_rolling_volatility_all.png"))
    for b in TREATED:
        s = series(df, b)
        fig, ax = plt.subplots(figsize=(9.5, 3.4))
        ax.plot(s.index, s.g.rolling(6).std(), color="#ef6c00", lw=1.5)
        _mark(ax, b)
        ax.set_title(f"{LABEL[b]} — 6-month rolling SD of monthly log growth")
        ax.set_ylabel("log-growth points"); ax.legend(fontsize=8)
        out.append(_save(fig, f"eda_06_{b}_rolling_vol.png"))
    return out


# --------------------------------------------------------------- overview
def plot_overview(df: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(10.5, 4.4))
    for b in TREATED:
        s = series(df, b)
        ax.plot(s.index, s.ln_y, lw=1.4, label=LABEL[b])
    for b, c in zip(TREATED, ["crimson", "darkorange", "darkorange", "purple"]):
        ax.axvline(pd.Timestamp(D_S[b] + "-01"), color=c, lw=1.0, ls=":", alpha=0.8)
    ax.axvspan(pd.Timestamp("2020-04-01"), pd.Timestamp("2020-06-01"),
               color="grey", alpha=0.15)
    ax.set_ylabel("ln(exports, US$ mn)")
    ax.set_title("All treated baskets — log exports, with intervention dates marked")
    ax.legend(fontsize=8, ncol=2)
    return _save(fig, "eda_00_overview_log_all_baskets.png")


# ------------------------------------------------------------ descriptives
def descriptives(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for b in TREATED:
        s = series(df, b)
        ds = pd.Timestamp(D_S[b] + "-01")
        pre, post = s[s.index < ds], s[s.index >= ds]
        gp, gq = pre.g.dropna(), post.g.dropna()
        rows.append(dict(
            basket_id=b, n=len(s), n_pre=len(pre), n_post=len(post),
            level_min=round(s.y.min(), 2), level_max=round(s.y.max(), 2),
            level_mean=round(s.y.mean(), 2),
            ratio_max_min=round(s.y.max() / s.y.min(), 1),
            growth_sd_full=round(s.g.std(), 2),
            growth_sd_pre=round(gp.std(), 2), growth_sd_post=round(gq.std(), 2),
            growth_min=round(s.g.min(), 2), growth_max=round(s.g.max(), 2),
            n_growth_pre=len(gp), n_growth_post=len(gq),
        ))
    return pd.DataFrame(rows)


def heteroskedasticity_check(df: pd.DataFrame) -> pd.DataFrame:
    """Is dispersion proportional to level? Supports (or not) the log transform.
    Compares CV of levels against SD of log growth, and correlates |g| with ln(Y)."""
    rows = []
    for b in TREATED:
        s = series(df, b).dropna(subset=["g"])
        cv_level = s.y.std() / s.y.mean()
        corr_absg_lvl = np.corrcoef(np.abs(s.g), s.ln_y)[0, 1]
        yearly = s.groupby(s.index.year).agg(m=("y", "mean"), sd=("y", "std")).dropna()
        corr_sd_mean = np.corrcoef(yearly.m, yearly.sd)[0, 1] if len(yearly) > 2 else np.nan
        rows.append(dict(basket_id=b,
                         cv_of_levels=round(cv_level, 3),
                         corr_annual_sd_vs_mean_LEVEL=round(corr_sd_mean, 3),
                         corr_abs_growth_vs_lnY=round(corr_absg_lvl, 3)))
    return pd.DataFrame(rows)
