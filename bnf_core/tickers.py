"""
tickers.py
----------
スキャン対象の証券コード一覧。
無料データソース(yfinance)では東証全銘柄(約3,800)を高速一括取得するのは
現実的ではないため、まずは主要・流動性の高い銘柄リストを対象にする。
必要に応じて自由に追加・削除してよい(例: 東証プライム全銘柄CSVを読み込む形に拡張可能)。
"""

DEFAULT_UNIVERSE = {
    "tech": [
        "6920", "6857", "8035", "6723", "6963", "6702", "9984", "6501",
        "6503", "6146", "6981", "6762", "4004", "6752",
    ],
    "heavy": [
        "7203", "8306", "8316", "8058", "8031", "9432", "9433", "5401",
        "5411", "7267", "7269", "8001", "8053", "9020",
    ],
    "growth": [
        "4385", "4478", "4477", "3697", "4485", "4483", "4425",
    ],
    "defensive": [
        "2914", "4502", "4503", "2502", "2503", "9022",
    ],
}


def all_codes() -> list[str]:
    codes = []
    for lst in DEFAULT_UNIVERSE.values():
        codes.extend(lst)
    return codes


def sector_of(code: str) -> str:
    for sector, lst in DEFAULT_UNIVERSE.items():
        if code in lst:
            return sector
    return "heavy"
