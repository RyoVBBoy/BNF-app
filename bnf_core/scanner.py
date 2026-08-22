"""
scanner.py
----------
price_cache.py が事前にまとめて取得した約3,900銘柄ぶんのキャッシュを
読み込んで、BNFロジックの買い/監視ゾーンに該当する銘柄を抽出する。
ネットワークアクセスが発生しないため一瞬で終わる。
"""

from __future__ import annotations
from dataclasses import dataclass

import pandas as pd

from . import price_cache, risk, universe


@dataclass
class ScanHit:
    code: str
    name: str
    sector: str
    price: float
    ma25: float
    atr14: float
    deviation_pct: float
    zone: str
    zone_label: str


def run_scan(market_score: float, zone_filter: str = "all",
             sector_filter: str = "all", sort_by: str = "kairi",
             limit: int = 10) -> list[ScanHit]:
    cache = price_cache.load_cache()
    if cache.empty:
        return []

    uni = universe.load_universe()
    merged = cache.merge(uni[["code", "name", "group"]], on="code", how="left")
    merged["group"] = merged["group"].fillna("heavy")

    if sector_filter != "all":
        merged = merged[merged["group"] == sector_filter]

    hits: list[ScanHit] = []
    for row in merged.itertuples():
        judgement = risk.judge_zone(row.deviation_pct, row.group, market_score)
        if judgement.zone == "hold":
            continue
        if zone_filter != "all" and judgement.zone != zone_filter:
            continue
        hits.append(ScanHit(
            code=row.code, name=row.name if isinstance(row.name, str) else row.code,
            sector=row.group, price=row.price, ma25=row.ma25, atr14=row.atr14,
            deviation_pct=row.deviation_pct, zone=judgement.zone, zone_label=judgement.label,
        ))

    if sort_by == "kairi":
        hits.sort(key=lambda h: h.deviation_pct)
    else:
        hits.sort(key=lambda h: h.atr14)

    return hits[:limit]


def universe_size() -> int:
    return len(universe.load_universe())
