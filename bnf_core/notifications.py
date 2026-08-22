"""
notifications.py
-----------------
アプリを閉じていても通知を受け取れるようにするための外部通知。
どちらも無料・登録不要:

- Discord Webhook: DiscordサーバーでWebhook URLを発行して貼るだけ
- ntfy.sh: 好きなトピック名を決めてスマホにntfyアプリを入れるだけ
           (https://ntfy.sh/<トピック名> を購読)
"""

from __future__ import annotations
import requests


def send_discord(webhook_url: str, message: str) -> bool:
    try:
        resp = requests.post(webhook_url, json={"content": message}, timeout=10)
        return resp.status_code in (200, 204)
    except requests.RequestException:
        return False


def send_ntfy(topic: str, message: str, title: str = "BNF PREMIUM") -> bool:
    try:
        resp = requests.post(
            f"https://ntfy.sh/{topic}",
            data=message.encode("utf-8"),
            headers={"Title": title},
            timeout=10,
        )
        return resp.status_code == 200
    except requests.RequestException:
        return False


def format_scan_summary(hits: list) -> str:
    if not hits:
        return "スキャン完了: 条件に合致する銘柄はありませんでした。"
    lines = [f"📡 全株スキャン完了: {len(hits)}件ヒット"]
    for h in hits[:10]:
        badge = "🟢買い" if h.zone == "buy" else "🟡監視"
        lines.append(f"{badge} {h.code} {h.name} 乖離{h.deviation_pct:+.1f}%")
    return "\n".join(lines)
