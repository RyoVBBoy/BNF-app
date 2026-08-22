"""
universe.py
-----------
JPX(日本取引所グループ)が毎月公式に公開している「東証上場銘柄一覧」
(data_j.xls)を取得し、約3,900銘柄の証券コード・銘柄名・業種を
ローカルにキャッシュする。

これにより、tickers.py にハードコードした数十銘柄ではなく、
実際の東証上場銘柄ほぼ全数を対象にスキャンできるようになる。
JPXは毎月第3営業日に前月末データへ更新するため、
キャッシュは30日を超えたら自動的に再取得する。
"""

from __future__ import annotations
import datetime as dt
import io
from pathlib import Path

import pandas as pd
import requests

JPX_URL = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"

DATA_DIR = Path(__file__).resolve().parent.parent / "data_store"
DATA_DIR.mkdir(exist_ok=True)
UNIVERSE_PATH = DATA_DIR / "universe.csv"

# 対象とする市場区分(現物の普通株のみ。ETF/ETN/REIT/PRO Marketなどは除外)
VALID_MARKET_KEYWORDS = ("プライム", "スタンダード", "グロース")

# 33業種区分 → アプリ内の4分類(セクター別しきい値のグルーピング用)
SECTOR33_TO_GROUP = {
    "水産・農林業": "defensive", "食料品": "defensive", "医薬品": "defensive",
    "電気・ガス業": "defensive", "陸運業": "defensive",
    "鉱業": "heavy", "建設業": "heavy", "金属製品": "heavy", "ガラス・土石製品": "heavy",
    "鉄鋼": "heavy", "非鉄金属": "heavy", "機械": "heavy", "輸送用機器": "heavy",
    "化学": "heavy", "石油・石炭製品": "heavy", "ゴム製品": "heavy", "パルプ・紙": "heavy",
    "繊維製品": "heavy", "その他製品": "heavy", "銀行業": "heavy", "保険業": "heavy",
    "その他金融業": "heavy", "証券、商品先物取引業": "heavy", "不動産業": "heavy",
    "海運業": "heavy", "空運業": "heavy", "倉庫・運輸関連業": "heavy",
    "卸売業": "heavy", "小売業": "heavy",
    "電気機器": "tech", "精密機器": "tech", "情報・通信業": "tech", "サービス業": "tech",
}


def _download_jpx_xls() -> pd.DataFrame:
    resp = requests.get(JPX_URL, timeout=30)
    resp.raise_for_status()
    return pd.read_excel(io.BytesIO(resp.content), engine="xlrd")


def _normalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=lambda c: str(c).strip())
    code_col = next(c for c in df.columns if "コード" in c and "業種" not in c and "規模" not in c)
    name_col = next(c for c in df.columns if "銘柄名" in c)
    market_col = next(c for c in df.columns if "市場" in c and "商品" in c)
    sector_col = next(c for c in df.columns if c.strip() == "33業種区分")

    out = pd.DataFrame({
        "code": df[code_col].astype(str).str.strip(),
        "name": df[name_col].astype(str).str.strip(),
        "market": df[market_col].astype(str).str.strip(),
        "sector33": df[sector_col].astype(str).str.strip(),
    })
    out = out[out["market"].str.contains("|".join(VALID_MARKET_KEYWORDS), na=False)]
    out["group"] = out["sector33"].map(SECTOR33_TO_GROUP).fillna("heavy")
    return out.reset_index(drop=True)


def refresh_universe() -> pd.DataFrame:
    """JPXから最新の全銘柄マスタを取得し、ローカルCSVに保存する。"""
    raw = _download_jpx_xls()
    df = _normalize(raw)
    df.to_csv(UNIVERSE_PATH, index=False, encoding="utf-8")
    return df


def load_universe(max_age_days: int = 30) -> pd.DataFrame:
    """
    キャッシュが存在し、かつ十分新しければそれを返す。
    存在しない/古い場合はJPXから再取得する。
    """
    if UNIVERSE_PATH.exists():
        age = dt.datetime.now() - dt.datetime.fromtimestamp(UNIVERSE_PATH.stat().st_mtime)
        if age.days <= max_age_days:
            return pd.read_csv(UNIVERSE_PATH, dtype={"code": str})
    return refresh_universe()


def universe_last_updated() -> dt.datetime | None:
    if UNIVERSE_PATH.exists():
        return dt.datetime.fromtimestamp(UNIVERSE_PATH.stat().st_mtime)
    return None
