"""
price_cache.py
---------------
数千銘柄を1件ずつ取得すると非常に時間がかかる(Yahoo Finance側の
レート制限にも抵触しやすい)ため、yfinanceのバッチダウンロード機能で
チャンク単位(既定150銘柄ずつ)にまとめて取得し、計算済みの指標
(現在値・25日移動平均・ATR・乖離率)だけをローカルCSVに保存する。

スキャン自体はこのキャッシュを読むだけなので瞬時に終わる。
キャッシュの更新(全銘柄ぶんの取得)は数分かかる重い処理なので、
「全株スキャン」タブのボタンから明示的に実行する。
"""

from __future__ import annotations
import datetime as dt
from pathlib import Path
from typing import Callable, Optional

import pandas as pd
import yfinance as yf

from .risk import atr_stop_loss  # noqa: F401 (将来の拡張用に残置)

DATA_DIR = Path(__file__).resolve().parent.parent / "data_store"
DATA_DIR.mkdir(exist_ok=True)
CACHE_PATH = DATA_DIR / "price_cache.csv"

CHUNK_SIZE = 150
HISTORY_PERIOD = "3mo"
MA_WINDOW = 25
ATR_WINDOW = 14


def _atr(df: pd.DataFrame) -> float:
    high, low, close = df["High"], df["Low"], df["Close"]
    prev_close = close.shift(1)
    tr = pd.concat(
        [(high - low), (high - prev_close).abs(), (low - prev_close).abs()], axis=1
    ).max(axis=1)
    val = tr.rolling(window=ATR_WINDOW).mean().iloc[-1]
    return float(val) if pd.notna(val) else 0.0


def _process_chunk(codes: list[str]) -> list[dict]:
    symbols = [f"{c}.T" for c in codes]
    data = yf.download(
        tickers=" ".join(symbols), period=HISTORY_PERIOD, group_by="ticker",
        threads=True, progress=False, auto_adjust=True,
    )
    rows = []
    for code, symbol in zip(codes, symbols):
        try:
            df = data[symbol] if len(symbols) > 1 else data
            df = df.dropna(subset=["Close"])
            if len(df) < MA_WINDOW:
                continue
            price = float(df["Close"].iloc[-1])
            ma25 = float(df["Close"].rolling(window=MA_WINDOW).mean().iloc[-1])
            atr14 = _atr(df)
            deviation_pct = (price - ma25) / ma25 * 100 if ma25 else 0.0
            rows.append({
                "code": code, "price": price, "ma25": ma25,
                "atr14": atr14, "deviation_pct": deviation_pct,
            })
        except (KeyError, ValueError, IndexError):
            continue
    return rows


def update_cache(codes: list[str],
                  progress_cb: Optional[Callable[[int, int], None]] = None) -> pd.DataFrame:
    """
    codes を CHUNK_SIZE ごとに分割してバッチ取得し、キャッシュCSVを書き出す。
    progress_cb(done_chunks, total_chunks) を渡すとUI側で進捗表示できる。
    """
    chunks = [codes[i:i + CHUNK_SIZE] for i in range(0, len(codes), CHUNK_SIZE)]
    all_rows: list[dict] = []
    for i, chunk in enumerate(chunks):
        all_rows.extend(_process_chunk(chunk))
        if progress_cb:
            progress_cb(i + 1, len(chunks))

    df = pd.DataFrame(all_rows)
    df["updated_at"] = dt.datetime.now().isoformat(timespec="seconds")
    df.to_csv(CACHE_PATH, index=False, encoding="utf-8")
    return df


def load_cache() -> pd.DataFrame:
    if not CACHE_PATH.exists():
        return pd.DataFrame(columns=["code", "price", "ma25", "atr14", "deviation_pct", "updated_at"])
    return pd.read_csv(CACHE_PATH, dtype={"code": str})


def cache_last_updated() -> Optional[dt.datetime]:
    df = load_cache()
    if df.empty:
        return None
    try:
        return dt.datetime.fromisoformat(df["updated_at"].iloc[0])
    except (ValueError, TypeError):
        return None
