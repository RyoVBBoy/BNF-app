"""
data.py
-------
Yahoo Finance (yfinance) から実際の市場データを取得するモジュール。

設計意図:
    元のHTML版はGeminiにJSONで数値を「生成」させていたため、
    ハルシネーション(架空の数値)のリスクがあった。
    このモジュールでは実際の取引データのみを扱い、
    数値の正確性を担保する。AIはこの後段で「解釈・コメント」だけを行う。
"""

from __future__ import annotations
import datetime as dt
from dataclasses import dataclass

import pandas as pd
import yfinance as yf


# ── 定数 ──────────────────────────────────────────────
NIKKEI_TICKER = "^N225"
USDJPY_TICKER = "JPY=X"
HISTORY_PERIOD = "3mo"   # 25日線 + ATR14 を計算するのに十分な期間
MA_WINDOW = 25
ATR_WINDOW = 14


@dataclass
class MarketSnapshot:
    nikkei: float
    nikkei_chg_pct: float
    usdjpy: float
    usdjpy_chg_pct: float
    down_ratio_score: float  # 0〜100 (地合いスコアの元データ)
    fetched_at: dt.datetime


@dataclass
class StockSnapshot:
    code: str
    price: float
    ma25: float
    atr14: float
    deviation_pct: float     # (price - ma25) / ma25 * 100
    history: pd.DataFrame


def _pct_change(series: pd.Series) -> float:
    if len(series) < 2:
        return 0.0
    prev, last = series.iloc[-2], series.iloc[-1]
    if prev == 0:
        return 0.0
    return float((last - prev) / prev * 100)


def _compute_atr(df: pd.DataFrame, window: int = ATR_WINDOW) -> float:
    """True Range の移動平均でATRを計算する。"""
    high, low, close = df["High"], df["Low"], df["Close"]
    prev_close = close.shift(1)
    tr = pd.concat(
        [
            (high - low),
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    atr = tr.rolling(window=window).mean().iloc[-1]
    return float(atr) if pd.notna(atr) else 0.0


def fetch_market_snapshot() -> MarketSnapshot:
    """日経平均・ドル円の最新値を取得する。"""
    nikkei_df = yf.Ticker(NIKKEI_TICKER).history(period="5d")
    usdjpy_df = yf.Ticker(USDJPY_TICKER).history(period="5d")

    nikkei_last = float(nikkei_df["Close"].iloc[-1])
    nikkei_chg = _pct_change(nikkei_df["Close"])
    usdjpy_last = float(usdjpy_df["Close"].iloc[-1])
    usdjpy_chg = _pct_change(usdjpy_df["Close"])

    # 東証の値下がり銘柄数は無料APIでは取得できないため、
    # 日経平均の当日騰落率から簡易的な地合いスコアを算出する
    # (下落が大きいほど「パニック=BNFが好む逆張り局面」に近づく)
    down_ratio_score = max(0.0, min(100.0, 50 - nikkei_chg * 5))

    return MarketSnapshot(
        nikkei=nikkei_last,
        nikkei_chg_pct=nikkei_chg,
        usdjpy=usdjpy_last,
        usdjpy_chg_pct=usdjpy_chg,
        down_ratio_score=down_ratio_score,
        fetched_at=dt.datetime.now(),
    )


def fetch_stock_snapshot(code: str) -> StockSnapshot | None:
    """
    個別銘柄の株価・25日移動平均・ATRを取得する。
    code: 証券コード(例 "6920")。内部で ".T" を付与してTSE銘柄として取得する。
    """
    ticker_symbol = code if code.upper().endswith(".T") else f"{code}.T"
    df = yf.Ticker(ticker_symbol).history(period=HISTORY_PERIOD)
    if df.empty or len(df) < MA_WINDOW:
        return None

    ma25 = float(df["Close"].rolling(window=MA_WINDOW).mean().iloc[-1])
    price = float(df["Close"].iloc[-1])
    atr14 = _compute_atr(df)
    deviation_pct = (price - ma25) / ma25 * 100 if ma25 else 0.0

    return StockSnapshot(
        code=code,
        price=price,
        ma25=ma25,
        atr14=atr14,
        deviation_pct=deviation_pct,
        history=df,
    )


def fetch_many(codes: list[str]) -> list[StockSnapshot]:
    """複数銘柄をまとめて取得(取得失敗銘柄はスキップ)。"""
    results = []
    for code in codes:
        try:
            snap = fetch_stock_snapshot(code)
            if snap is not None:
                results.append(snap)
        except Exception:
            continue
    return results
