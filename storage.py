"""
storage.py
----------
ウォッチリストと売買ログをJSONファイルに保存する。
(元のHTML版はブラウザのlocalStorageを使用していたが、
 Python/Streamlit版ではローカルファイルに保存する)
"""

from __future__ import annotations
import json
import datetime as dt
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data_store"
DATA_DIR.mkdir(exist_ok=True)

WATCHLIST_PATH = DATA_DIR / "watchlist.json"
LOG_PATH = DATA_DIR / "logs.json"


def _load(path: Path) -> list:
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def _save(path: Path, data: list) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ── ウォッチリスト ──────────────────────────────
def load_watchlist() -> list[dict]:
    return _load(WATCHLIST_PATH)


def add_to_watchlist(code: str, name: str = "") -> list[dict]:
    wl = load_watchlist()
    if not any(item["code"] == code for item in wl):
        wl.append({"code": code, "name": name})
        _save(WATCHLIST_PATH, wl)
    return wl


def remove_from_watchlist(code: str) -> list[dict]:
    wl = [item for item in load_watchlist() if item["code"] != code]
    _save(WATCHLIST_PATH, wl)
    return wl


# ── 売買ログ ──────────────────────────────────
def load_logs() -> list[dict]:
    return _load(LOG_PATH)


def add_log(entry: dict) -> list[dict]:
    logs = load_logs()
    entry = {**entry, "logged_at": dt.datetime.now().isoformat(timespec="seconds")}
    logs.insert(0, entry)
    _save(LOG_PATH, logs)
    return logs


def clear_logs() -> None:
    _save(LOG_PATH, [])
