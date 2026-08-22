"""
gemini_client.py
-----------------
Geminiは「数値の生成」には使わない。数値はdata.py/risk.pyで実計算し、
Geminiにはその結果を渡して「コメント・解釈・チャット応答」だけを
担当させる。これにより数値のハルシネーションを排除し、精度を上げる。

新しい google-genai SDK を使用(google-generativeai は非推奨のため)。
"""

from __future__ import annotations
from google import genai
from google.genai import types

MODEL_NAME = "gemini-2.5-flash"


def _get_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)


def market_comment(api_key: str, nikkei: float, nikkei_chg: float,
                    usdjpy: float, score: float) -> str:
    """実データに基づいたB.N.Fスタイルの短評を生成する。"""
    client = _get_client(api_key)
    prompt = (
        "あなたはB.N.F(伝説の個人投資家)のスタイルで短いコメントを返します。\n"
        "以下は実際に取得した本日の市場データです。この数値のみに基づいて、"
        "50字程度の短い一言コメントをカギ括弧付きで返してください。数値を勝手に変えないこと。\n\n"
        f"日経平均: {nikkei:.0f}円 (前日比 {nikkei_chg:+.2f}%)\n"
        f"ドル円: {usdjpy:.2f}円\n"
        f"地合いスコア(0=パニック/100=過熱): {score:.0f}\n"
    )
    resp = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    return resp.text.strip()


def stock_report(api_key: str, code: str, price: float, ma25: float,
                  deviation_pct: float, zone_label: str) -> str:
    """個別銘柄の実データに基づく短い分析コメント。"""
    client = _get_client(api_key)
    prompt = (
        "以下は実際に取得した個別銘柄データです。この数値だけを根拠に、"
        "BNF逆張りロジックの観点から3〜4行で分析コメントを書いてください。"
        "数値の創作・誇張は禁止です。断定的な売買推奨ではなく、あくまで情報整理として書いてください。\n\n"
        f"銘柄コード: {code}\n"
        f"現在値: {price:.1f}円\n"
        f"25日移動平均: {ma25:.1f}円\n"
        f"乖離率: {deviation_pct:.2f}%\n"
        f"判定: {zone_label}\n"
    )
    resp = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    return resp.text.strip()


def chat_reply(api_key: str, history: list[dict], user_message: str,
               context_note: str = "") -> str:
    """
    AI脳内タブのチャット。context_note に直近の実データ(スコア・保有銘柄など)を
    差し込むことで、根拠のある会話にする。
    history: [{"role": "user"|"model", "text": "..."}]
    """
    client = _get_client(api_key)
    chat_history = [
        types.Content(role=h["role"], parts=[types.Part(text=h["text"])])
        for h in history
    ]
    chat = client.chats.create(model=MODEL_NAME, history=chat_history)
    prefix = f"[参考データ]\n{context_note}\n\n" if context_note else ""
    resp = chat.send_message(
        prefix + user_message +
        "\n\n(断定的な投資助言ではなく、リスクにも触れた中立的な回答をしてください)"
    )
    return resp.text.strip()
