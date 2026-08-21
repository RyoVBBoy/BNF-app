"""
scanner.py
----------
tickers.py のユニバースを実データでスキャンし、BNFロジックの
買い/監視ゾーンに該当する銘柄を抽出する。
Geminiには使わず、完全に計算ベース(=再現性・精度が高い)で行う。
"""

from __future__ import annotations
from dataclasses import dataclass

from . import data, risk, tickers


@dataclass
class ScanHit:
    code: str
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
    codes = tickers.DEFAULT_UNIVERSE.get(sector_filter) if sector_filter != "all" else tickers.all_codes()
    snapshots = data.fetch_many(codes)

    hits: list[ScanHit] = []
    for snap in snapshots:
        sector = tickers.sector_of(snap.code)
        judgement = risk.judge_zone(snap.deviation_pct, sector, market_score)
        if judgement.zone == "hold":
            continue
        if zone_filter != "all" and judgement.zone != zone_filter:
            continue
        hits.append(ScanHit(
            code=snap.code, sector=sector, price=snap.price, ma25=snap.ma25,
            atr14=snap.atr14, deviation_pct=snap.deviation_pct,
            zone=judgement.zone, zone_label=judgement.label,
        ))

    if sort_by == "kairi":
        hits.sort(key=lambda h: h.deviation_pct)  # 乖離が深い(マイナスが大きい)順
    else:  # risk = ATRが小さい(値動きが穏やか)順
        hits.sort(key=lambda h: h.atr14)

    return hits[:limit]
