#!/usr/bin/env python3
"""
fetch_meidb.py — reproducible extraction of monthly HS-6 Indian export data from MEIDB.

Source : DGCI&S / Department of Commerce, Monthly Export Import Data Bank
         https://tradestat.commerce.gov.in/meidb/commoditywise_export

DESIGN NOTES
------------
* MEIDB is a plain Laravel POST form. A GET returns the form shell plus a CSRF token;
  a POST with that token returns a fully server-rendered results table.
* A query for (month M, year Y) returns TWO data columns: M-(Y-1) and M-Y.
  That halves the request count: 48 requests cover the full 96-month panel.
* The results grid holds every HS-6 row (~5,150) in the returned HTML. No paging needed.
* The "Specific HSCode" route 404s unless driven through the modal picker.
  Always use All Commodities -> 6 digit Level and filter client-side.

HARD RULES (project control rules 3 and 4)
------------------------------------------
* Raw responses are written to 01_raw_data/raw_trade_data/ and NEVER overwritten.
  Each file is stamped with its retrieval date; a re-run creates a new dated directory.
* DGCI&S operates a Dynamic Data Revision Policy: prior months of the current financial
  year are restated on every release. The panel must be RE-PULLED in full, never appended.

USAGE
-----
    python fetch_meidb.py --out-root ../01_raw_data/raw_trade_data
    python fetch_meidb.py --resume            # skip requests already cached
    python fetch_meidb.py --build-only        # parse existing cache, skip network
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import gzip
import json
import re
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("requests is required:  pip install requests")

BASE = "https://tradestat.commerce.gov.in/meidb/commoditywise_export"
UA = "Mozilla/5.0 (research; monthly HS-6 export panel; contact: project owner)"
POLITE_DELAY_S = 2.5          # be a good citizen on a public government portal
TIMEOUT_S = 120
MAX_RETRIES = 3

# ---------------------------------------------------------------------------
# Basket definitions — authority: 03_mapping/hs_mapping_master.csv
#                                 03_mapping/control_hs6_codes.csv
# Locked 29 Aug 2026 under Change Proposals 001, 002, 003.
# ---------------------------------------------------------------------------
BASKETS: dict[str, dict] = {
    # ---- treated ----------------------------------------------------------
    "B1_MOBILE": {
        "sector": "Electronics - telephone sets (HS 8517.1x proxy for PLI-LSEM mobile segment)",
        "role": "CORE",
        "mode": "explicit",
        "codes": ["851711", "851712", "851713", "851714", "851718"],
        "parent_hs4": "8517",
    },
    "B2_PHARMA": {
        "sector": "Pharmaceutical formulations",
        "role": "CORE",
        "mode": "prefix",
        "prefixes": ["3003", "3004"],
        "parent_hs4": None,
    },
    "B3_AC": {
        "sector": "Air conditioners",
        "role": "CORE",
        "mode": "prefix",
        "prefixes": ["8415"],
        "parent_hs4": "8415",
    },
    "B4_TEXTILE": {
        "sector": "MMF fabrics (PLI Textiles Annexure-II)",
        "role": "ROBUSTNESS",
        "mode": "explicit",
        "codes": ["540710", "540720", "540742", "540752", "540754", "540761",
                  "540769", "551219", "551511", "551614", "580632", "600192",
                  "600537", "600632"],
        "parent_hs4": None,
    },
    # ---- controls ---------------------------------------------------------
    "C1_LEATHER": {
        "sector": "Leather goods",
        "role": "CONTROL",
        "mode": "prefix",
        "prefixes": ["42"],
        "parent_hs4": None,
    },
    "C2_FOOTWEAR": {
        "sector": "Footwear",
        "role": "CONTROL",
        "mode": "prefix",
        "prefixes": ["64"],
        "parent_hs4": None,
    },
    "C3_COTTON": {
        "sector": "Cotton woven fabrics",
        "role": "CONTROL",
        "mode": "prefix",
        "prefixes": ["5208", "5209", "5210", "5211", "5212"],
        "parent_hs4": None,
    },
}

# Reconciliation aggregates captured alongside the baskets
RECON_PREFIXES = {"HS4_8517": ["8517"], "HS4_8415": ["8415"], "CH52": ["52"]}

PANEL_START = (2018, 4)      # April 2018
PANEL_END = (2026, 3)        # March 2026


# ---------------------------------------------------------------------------
def request_plan() -> list[tuple[int, int]]:
    """(month, year) queries covering Apr-2018..Mar-2026. Each yields two years."""
    plan = []
    for m in range(1, 13):
        years = [2020, 2022, 2024, 2026] if m <= 3 else [2019, 2021, 2023, 2025]
        plan.extend((m, y) for y in years)
    return sorted(plan)


def in_panel(year: int, month: int) -> bool:
    return PANEL_START <= (year, month) <= PANEL_END


def expected_months() -> list[str]:
    out, y, m = [], *PANEL_START
    while (y, m) <= PANEL_END:
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


# ---------------------------------------------------------------------------
class Meidb:
    def __init__(self) -> None:
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": UA})
        self.token: str | None = None

    def _refresh_token(self) -> str:
        r = self.s.get(BASE, timeout=TIMEOUT_S)
        r.raise_for_status()
        m = re.search(r'name="_token"\s+value="([^"]+)"', r.text)
        if not m:
            raise RuntimeError("CSRF token not found on the MEIDB form page")
        self.token = m.group(1)
        return self.token

    def fetch(self, month: int, year: int, report_val: str = "1") -> str:
        """report_val: 1 = US$ million, 3 = Rs crore."""
        if not self.token:
            self._refresh_token()
        payload = {
            "_token": self.token,
            "ddMonth": str(month),
            "ddYear": str(year),
            "comlev": "all",
            "ddCommodityLevel": "6",
            "ddReportVal": report_val,
            "ddReportYear": "2",          # Calendar Year
        }
        for attempt in range(1, MAX_RETRIES + 1):
            r = self.s.post(BASE, data=payload, timeout=TIMEOUT_S)
            if r.status_code == 419 or "PAGE EXPIRED" in r.text.upper():
                payload["_token"] = self._refresh_token()
                continue
            r.raise_for_status()
            if "<table" in r.text.lower():
                return r.text
            time.sleep(POLITE_DELAY_S * attempt)
        raise RuntimeError(f"no table returned for {month}/{year} after {MAX_RETRIES} attempts")


# ---------------------------------------------------------------------------
_CELL = re.compile(r"<t[dh][^>]*>(.*?)</t[dh]>", re.S | re.I)
_ROW = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S | re.I)
_TAG = re.compile(r"<[^>]+>")


def _clean(html: str) -> str:
    return _TAG.sub("", html).replace("&nbsp;", " ").replace("&amp;", "&").strip()


def parse(html: str) -> tuple[list[str], list[list[str]]]:
    """Return (header, rows). Header col 3 and 4 are the two data months."""
    rows = [[_clean(c) for c in _CELL.findall(r)] for r in _ROW.findall(html)]
    rows = [r for r in rows if len(r) >= 5]
    if not rows:
        raise RuntimeError("no parseable rows")
    return rows[0], rows[1:]


_MON = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], start=1)}


def header_month(cell: str) -> str | None:
    """'Mar-2022 (R)' -> '2022-03'."""
    m = re.search(r"([A-Za-z]{3})-(\d{4})", cell)
    return f"{int(m.group(2)):04d}-{_MON[m.group(1)[:3].title()]:02d}" if m else None


def to_float(cell: str) -> float | None:
    c = cell.replace(",", "").strip()
    if c in {"", "-", "--"}:
        return None
    try:
        return float(c)
    except ValueError:
        return None


def matches(code: str, spec: dict) -> bool:
    if spec["mode"] == "explicit":
        return code in spec["codes"]
    return any(code.startswith(p) for p in spec["prefixes"])


# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-root", default="../01_raw_data/raw_trade_data")
    ap.add_argument("--clean-out", default="../04_clean_data/master_monthly_exports.csv")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--build-only", action="store_true")
    ap.add_argument("--currency", default="1", choices=["1", "3"],
                    help="1 = US$ million (primary), 3 = Rs crore (robustness R8)")
    args = ap.parse_args()

    retrieval_date = dt.date.today().isoformat()
    raw_dir = Path(args.out_root) / f"meidb_hs6_{retrieval_date}_cur{args.currency}"
    raw_dir.mkdir(parents=True, exist_ok=True)

    client = None if args.build_only else Meidb()
    plan = request_plan()
    print(f"[plan] {len(plan)} requests -> {len(expected_months())} panel months")

    # month -> code -> value ; and month -> banner/vintage metadata
    values: dict[str, dict[str, float]] = {}
    starred: dict[str, set[str]] = {}
    vintage: dict[str, str] = {}
    india_total: dict[str, float] = {}

    for i, (month, year) in enumerate(plan, 1):
        cache = raw_dir / f"meidb_{year}_{month:02d}_hs6.html.gz"
        if cache.exists() and (args.resume or args.build_only):
            html = gzip.decompress(cache.read_bytes()).decode("utf-8", "replace")
        elif args.build_only:
            print(f"[skip] no cache for {month}/{year}")
            continue
        else:
            print(f"[{i}/{len(plan)}] POST month={month} year={year}")
            html = client.fetch(month, year, args.currency)
            # rule 3/4: raw response written once, never overwritten
            if cache.exists():
                raise SystemExit(f"refusing to overwrite existing raw file: {cache}")
            cache.write_bytes(gzip.compress(html.encode("utf-8")))
            time.sleep(POLITE_DELAY_S)

        header, rows = parse(html)
        m_prev, m_curr = header_month(header[3]), header_month(header[4])
        vflags = [re.search(r"\((R|F)\)", header[j]) for j in (3, 4)]

        for col, mk in ((3, m_prev), (4, m_curr)):
            if not mk:
                continue
            y, mm = int(mk[:4]), int(mk[5:])
            if not in_panel(y, mm):
                continue
            values.setdefault(mk, {})
            starred.setdefault(mk, set())
            flag = vflags[col - 3]
            vintage[mk] = flag.group(1) if flag else "?"
            for r in rows:
                code, desc = r[1].replace(" ", ""), r[2]
                v = to_float(r[col])
                if code.lower().startswith("india") or "total export" in desc.lower():
                    if v is not None:
                        india_total[mk] = v
                    continue
                if not code.isdigit() or len(code) != 6 or v is None:
                    continue
                values[mk][code] = v
                if desc.lstrip().startswith("*"):
                    starred[mk].add(code)

    # ---------------- build the panel -------------------------------------
    months = expected_months()
    out_rows = []
    for mk in months:
        vals = values.get(mk, {})
        for bid, spec in BASKETS.items():
            hits = {c: v for c, v in vals.items() if matches(c, spec)}
            note = []
            if spec["mode"] == "explicit":
                missing = [c for c in spec["codes"] if c not in hits]
                if missing:
                    note.append("no-trade or absent: " + "|".join(missing))
            star = sorted(set(hits) & starred.get(mk, set()))
            if star:
                note.append("dropped-code flag: " + "|".join(star))
            out_rows.append({
                "month": mk,
                "basket_id": bid,
                "sector": spec["sector"],
                "role": spec["role"],
                "export_usd_mn": round(sum(hits.values()), 4) if args.currency == "1" else "",
                "export_inr_cr": round(sum(hits.values()), 4) if args.currency == "3" else "",
                "quantity": "",
                "quantity_unit": "",
                "hs_level_used": 6,
                "codes_summed": "|".join(sorted(hits)),
                "n_codes": len(hits),
                "vintage_flag": vintage.get(mk, ""),
                "retrieval_date": retrieval_date,
                "source_file": str(raw_dir.name),
                "notes": "; ".join(note),
            })

    out = Path(args.clean_out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)

    side = out.parent / "reconciliation_aggregates.csv"
    with side.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["month", "agg_id", "value", "n_codes", "india_total_export", "vintage_flag"])
        for mk in months:
            vals = values.get(mk, {})
            for aid, pfx in RECON_PREFIXES.items():
                hit = {c: v for c, v in vals.items() if any(c.startswith(p) for p in pfx)}
                w.writerow([mk, aid, round(sum(hit.values()), 4), len(hit),
                            india_total.get(mk, ""), vintage.get(mk, "")])

    meta = {
        "retrieval_date": retrieval_date,
        "source": BASE,
        "currency": {"1": "US$ million", "3": "Rs crore"}[args.currency],
        "hs_level": 6,
        "year_type": "Calendar Year",
        "panel": f"{months[0]}..{months[-1]}",
        "n_months": len(months),
        "n_baskets": len(BASKETS),
        "n_rows": len(out_rows),
        "requests_made": len(plan),
        "raw_cache_dir": str(raw_dir),
        "revision_policy": ("DGCI&S Dynamic Data Revision Policy restates prior months of the "
                            "current financial year on every release. Re-pull in full; never append."),
    }
    (out.parent / "extraction_manifest.json").write_text(json.dumps(meta, indent=2))
    print(f"[done] {len(out_rows)} rows -> {out}")
    print(f"[done] raw cache -> {raw_dir}")


if __name__ == "__main__":
    main()
