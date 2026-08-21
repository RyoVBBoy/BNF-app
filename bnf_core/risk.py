"""
risk.py
-------
BNF流逆張りロジックのコア計算。
元のHTML版の「セクター別しきい値」「利確・損切りターゲット」に加え、
損失リスクをさらに抑えるための2つの機能を追加:

  1. ATRベースの動的損切りライン
     (固定%ではなく、その銘柄の実際のボラティリティに応じて損切り幅を決める)
  2. 口座リスク%からの適正ロット計算
     (「いくら買うか」ではなく「口座の何%を失う許容があるか」から逆算する)
"""

from __future__ import annotations
from dataclasses import dataclass

SECTOR_THRESHOLDS = {
    "heavy": {"watch": -10, "buy": -15},
    "tech": {"watch": -15, "buy": -20},
    "defensive": {"watch": -10, "buy": -15},
    "growth": {"watch": -30, "buy": -40},
}


@dataclass
class Judgement:
    zone: str          # "buy" / "watch" / "hold"
    label: str


def judge_zone(deviation_pct: float, sector: str, market_score: float) -> Judgement:
    """
    乖離率としきい値から判定する。
    market_score(0〜100、低いほどパニック)が低いほど、しきい値を
    甘め(絶対値を小さく)に調整し、パニック相場ではより早めに拾えるようにする。
    """
    th = SECTOR_THRESHOLDS.get(sector, SECTOR_THRESHOLDS["heavy"])
    # 地合いが悪い(スコアが低い)ほどしきい値を10%緩和する
    adj = 1 - (50 - market_score) / 100 * 0.3
    watch_th = th["watch"] * adj
    buy_th = th["buy"] * adj

    if deviation_pct <= buy_th:
        return Judgement("buy", f"買いゾーン(乖離 {deviation_pct:.1f}% ≦ {buy_th:.1f}%)")
    if deviation_pct <= watch_th:
        return Judgement("watch", f"監視ゾーン(乖離 {deviation_pct:.1f}% ≦ {watch_th:.1f}%)")
    return Judgement("hold", "様子見")


def atr_stop_loss(entry_price: float, atr14: float, atr_multiple: float = 1.5) -> float:
    """ATRの何倍かをエントリー価格から差し引いた損切りラインを返す。"""
    return round(entry_price - atr14 * atr_multiple, 1)


def targets(entry_price: float, ma25: float, stop_pct: float, custom_profit_pct: float,
            atr14: float | None = None, atr_multiple: float = 1.5) -> dict:
    """利確①(MA25回帰)・利確②(カスタム%)・損切り(固定%とATR基準の両方)・RRRを算出。"""
    profit_ma = round(ma25, 1)
    profit_ma_pct = (ma25 - entry_price) / entry_price * 100 if entry_price else 0.0

    profit_custom = round(entry_price * (1 + custom_profit_pct / 100), 1)
    stop_fixed = round(entry_price * (1 - stop_pct / 100), 1)

    stop_atr = atr_stop_loss(entry_price, atr14, atr_multiple) if atr14 else None
    # より安全な(価格が高い=損失が小さい)方を採用
    effective_stop = max(stop_fixed, stop_atr) if stop_atr else stop_fixed

    risk = entry_price - effective_stop
    reward = profit_ma - entry_price
    rrr = round(reward / risk, 2) if risk > 0 else None

    return {
        "profit_ma": profit_ma,
        "profit_ma_pct": round(profit_ma_pct, 2),
        "profit_custom": profit_custom,
        "profit_custom_pct": custom_profit_pct,
        "stop_fixed": stop_fixed,
        "stop_atr": stop_atr,
        "effective_stop": effective_stop,
        "rrr": rrr,
    }


def position_size(account_balance: float, entry_price: float, stop_price: float,
                   risk_pct: float = 1.0, lot_size: int = 100) -> dict:
    """
    口座残高の risk_pct% だけを失う前提で、購入可能な株数(ロット単位)を逆算する。
    これが「損するリスクをさらに軽減する」ための中心的な機能:
    値幅ではなく「口座に対する損失許容額」から数量を決める。
    """
    risk_amount = account_balance * (risk_pct / 100)
    per_share_risk = entry_price - stop_price
    if per_share_risk <= 0:
        return {"shares": 0, "lots": 0, "risk_amount": risk_amount, "capital_required": 0}

    raw_shares = risk_amount / per_share_risk
    lots = int(raw_shares // lot_size)
    shares = lots * lot_size
    capital_required = shares * entry_price

    return {
        "shares": shares,
        "lots": lots,
        "risk_amount": round(risk_amount),
        "capital_required": round(capital_required),
    }
