"""
05_volatility_R12.py — volatility and R12 quadratic-pre-trend analyses, producing
06_results/volatility_results.csv and 06_results/ITS_R12_quadratic_pretrend.csv.

PROVENANCE. This file consolidates, verbatim, the two original analysis scripts
that produced these outputs (first run 2 September 2026; consolidated into this
committed module on 8 September 2026). NOTHING METHODOLOGICAL WAS CHANGED:
same locked windows, same COVID-exclusion definition, same straddle handling,
same moving-block bootstrap (block length 6, 4,000 replications, seed 20260902,
identical draw order), same R12 specification (locked baseline + (T/100)^2 only).

The stored CSVs in 06_results/ remain authoritative. Running this script writes
to --outdir (default: a sibling _reproduction directory) precisely so the stored
files are never overwritten; byte-level agreement with the stored results has
been verified.

Usage:
    python 05_volatility_R12.py                 # writes to 06_results_reproduction/
    python 05_volatility_R12.py --outdir PATH   # writes both CSVs to PATH
"""

import argparse
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import statsmodels.api as sm

import its_core as I
import robustness_core as R

ROOT = Path(__file__).resolve().parent.parent

# ----------------------------------------------------------------- R12
# Pre-specified in the Phase-1 robustness matrix:
#   "R12 | Log-linear vs quadratic pre-trend | Piecewise-linear mis-specification"
# Implementation: the LOCKED baseline plus one term, (T/100)^2 for conditioning.
# Nothing else changes: same D_s, same COVID, same month FE, same HAC.

def run_r12(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for b in I.TREATED:
        s = I.design(df, b)
        s["T2"] = (s["T"] / 100.0) ** 2
        base_cols = R.EXOG
        quad_cols = ["T", "T2", "Post", "TimeAfter"] + I.MONTH_COLS + ["Covid"]
        for spec, cols in [("A0_baseline_locked", base_cols),
                           ("R12_quadratic_pretrend", quad_cols)]:
            X = sm.add_constant(s[cols], has_constant="add")
            m = sm.OLS(s["ln_y"], X).fit()
            h3 = sm.OLS(s["ln_y"], X).fit(cov_type="HAC",
                                          cov_kwds={"maxlags": 3, "use_correction": True})
            h12 = sm.OLS(s["ln_y"], X).fit(cov_type="HAC",
                                           cov_kwds={"maxlags": 12, "use_correction": True})
            lo, hi = h12.conf_int().loc["TimeAfter"]
            row = dict(unit=b, spec=spec, n=int(m.nobs), r2_adj=round(m.rsquared_adj, 4),
                       beta3_lgp=round(m.params["TimeAfter"] * 100, 3),
                       se_hac3=round(h3.bse["TimeAfter"] * 100, 3),
                       se_hac12=round(h12.bse["TimeAfter"] * 100, 3),
                       p_hac3=round(h3.pvalues["TimeAfter"], 4),
                       p_hac12=round(h12.pvalues["TimeAfter"], 4),
                       ci_lo=round(lo * 100, 3), ci_hi=round(hi * 100, 3),
                       beta2=round(m.params["Post"], 4),
                       beta2_p12=round(h12.pvalues["Post"], 4))
            if "T2" in cols:
                row.update(T2_coef=round(m.params["T2"], 4),
                           T2_se12=round(h12.bse["T2"], 4),
                           T2_p12=round(h12.pvalues["T2"], 4))
            rows.append(row)
    return pd.DataFrame(rows)


# ----------------------------------------------------------- volatility
# Locked windows (design memo §6.2), COVID exclusion Mar–Sep 2020, straddle
# observation g(D_s) separated, MBB block 6 / 4000 reps / seed 20260902.

WIN = {"B1_MOBILE": (("2018-08", "2020-07"), ("2020-08", "2022-07")),
       "B2_PHARMA": (("2020-04", "2022-03"), ("2022-04", "2024-03")),
       "B3_AC": (("2020-04", "2022-03"), ("2022-04", "2024-03")),
       "B4_TEXTILE": (("2022-04", "2024-03"), ("2024-04", "2026-03"))}
FULL = {"B1_MOBILE": (("2018-05", "2020-07"), ("2020-08", "2026-03")),
        "B2_PHARMA": (("2018-05", "2022-03"), ("2022-04", "2026-03")),
        "B3_AC": (("2018-05", "2022-03"), ("2022-04", "2026-03")),
        "B4_TEXTILE": (("2018-05", "2024-03"), ("2024-04", "2026-03"))}
COVID_EX = ("2020-03", "2020-09")
BLOCK = 6
NBOOT = 4000
SEED = 20260902


def _series(df, b):
    s = df[df.basket_id == b].set_index("date").asfreq("MS").copy()
    s["ln_y"] = np.log(s["y"])
    s["g"] = s["ln_y"].diff() * 100
    return s


def _gwin(s, a, b2, excovid=False, drop=None):
    g = s.g.dropna()
    m = (g.index >= pd.Timestamp(a + "-01")) & (g.index <= pd.Timestamp(b2 + "-01"))
    if excovid:
        m &= ~((g.index >= pd.Timestamp(COVID_EX[0] + "-01"))
               & (g.index <= pd.Timestamp(COVID_EX[1] + "-01")))
    if drop is not None:
        m &= g.index != drop
    return g[m]


def run_volatility(df: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)

    def mbb(x, l=BLOCK):
        x = np.asarray(x)
        n = len(x)
        if n <= l:
            return x[rng.integers(0, n, n)]
        starts = rng.integers(0, n - l + 1, int(np.ceil(n / l)))
        return np.concatenate([x[s0:s0 + l] for s0 in starts])[:n]

    def boot(gp, gq, B=NBOOT):
        # NOTE: evaluation order (post block first, then pre) is fixed —
        # changing it would change the RNG draw sequence and the CIs.
        d = [mbb(gq.values).std(ddof=1) - mbb(gp.values).std(ddof=1) for _ in range(B)]
        return np.percentile(d, [2.5, 97.5])

    rows = []
    for b in I.TREATED:
        s = _series(df, b)
        ds = pd.Timestamp(I.D_S[b] + "-01")
        for wname, (pre, post) in [("symmetric_pm24", WIN[b]), ("full_windows", FULL[b])]:
            for var, exc in [("baseline", False), ("exCOVID_MarSep2020", True)]:
                for st, drop in [("incl_straddle", None), ("excl_straddle", ds)]:
                    gp = _gwin(s, *pre, excovid=exc)
                    gq = _gwin(s, *post, excovid=exc, drop=drop)
                    if len(gp) < 8 or len(gq) < 8:
                        continue
                    sp, sq = gp.std(ddof=1), gq.std(ddof=1)
                    lo, hi = boot(gp, gq)
                    rows.append(dict(
                        basket=b, windows=wname, variant=var, straddle=st,
                        n_pre=len(gp), n_post=len(gq),
                        sigma_pre=round(sp, 2), sigma_post=round(sq, 2),
                        dsigma=round(sq - sp, 2), pct_dsigma=round(100 * (sq - sp) / sp, 1),
                        mbb_ci_lo=round(lo, 2), mbb_ci_hi=round(hi, 2),
                        ci_excl_zero=bool(lo > 0 or hi < 0)))
    return pd.DataFrame(rows)


# --------------------------------------------------- vol_01 figure
# 6-month rolling SD of monthly log growth with the locked ±24-month comparison
# windows shaded (vol_01_rolling_sd_windows.png).

def make_rolling_vol_figure(df: pd.DataFrame, figdir: Path | None = None) -> str:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    figdir = Path(figdir) if figdir else (ROOT / "07_figures")
    fig, axes = plt.subplots(2, 2, figsize=(12, 6.6))
    for ax, b in zip(axes.ravel(), I.TREATED):
        s = df[df.basket_id == b].set_index("date").asfreq("MS").copy()
        s["g"] = np.log(s["y"]).diff() * 100
        rv = s.g.rolling(6).std()
        ax.plot(s.index, rv, color="#ef6c00", lw=1.5)
        (p1, p2), (q1, q2) = WIN[b]
        ax.axvspan(pd.Timestamp(p1 + "-01"), pd.Timestamp(p2 + "-01"),
                   color="#1565c0", alpha=0.10, label="pre ±24 window")
        ax.axvspan(pd.Timestamp(q1 + "-01"), pd.Timestamp(q2 + "-01"),
                   color="#2e7d32", alpha=0.10, label="post ±24 window")
        ax.axvline(pd.Timestamp(I.D_S[b] + "-01"), color="crimson", lw=1.5, ls="--")
        ax.set_title(I.LABEL[b], fontsize=9)
        ax.set_ylabel("6-m rolling SD of g (lgp)")
        ax.grid(alpha=.25)
    axes[0, 0].legend(fontsize=7.5)
    fig.suptitle("6-month rolling volatility of monthly log growth — locked ±24-month "
                 "comparison windows shaded (units: log-growth points)", y=1.0)
    fig.tight_layout()
    p = figdir / "vol_01_rolling_sd_windows.png"
    fig.savefig(p, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return p.name


# ----------------------------------------------------------------- main
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=str(ROOT / "06_results_reproduction"),
                    help="Output directory (default keeps frozen 06_results/ untouched).")
    args = ap.parse_args()
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)

    df = I.load_panel()

    r12 = run_r12(df)
    r12.to_csv(out / "ITS_R12_quadratic_pretrend.csv", index=False)
    print(f"R12 -> {out/'ITS_R12_quadratic_pretrend.csv'}  ({len(r12)} rows)")

    vol = run_volatility(df)
    vol.to_csv(out / "volatility_results.csv", index=False)
    print(f"volatility -> {out/'volatility_results.csv'}  ({len(vol)} rows)")

    fig = make_rolling_vol_figure(df)
    print(f"figure -> 07_figures/{fig}")
