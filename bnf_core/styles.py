"""
styles.py
---------
BNF PREMIUM — 完全ノンスマイリー & Twitter(X)風ボトムナビCSS定義
"""

CSS = """
<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

:root {
  --black: #000000;
  --s1: #121417;
  --s2: #1A1D21;
  --bdr: #23272C;
  --text: #EFF3F4;
  --muted: #71767B;
  --acc: #d500f9;
  --blue: #1D9BF0;
  --green: #00BA7C;
  --red: #F4212E;
}

/* 全体スタイル */
.stApp {
  background-color: var(--black) !important;
  color: var(--text) !important;
}

section.main > div {
  max-width: 600px;
  margin: 0 auto;
  padding: 0.5rem 1rem 100px 1rem !important;
}

/* ヘッダー */
.bnf-header {
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--bdr);
  margin-bottom: 16px;
}
.bnf-title {
  font-size: 1.2rem;
  font-weight: 900;
  letter-spacing: 0.05em;
  color: var(--acc);
}
.bnf-live-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.7rem;
  font-weight: 800;
  color: var(--green);
  background: rgba(0, 186, 124, 0.12);
  padding: 3px 8px;
  border-radius: 9999px;
}
.bnf-live-dot {
  width: 6px;
  height: 6px;
  background: var(--green);
  border-radius: 50%;
}

/* ══════════════════════════════════════════════════
   ボトムナビゲーション (画像完全再現CSS)
   ══════════════════════════════════════════════════ */
div[data-testid="stRadio"] {
  position: fixed !important;
  bottom: 0 !important;
  left: 0 !important;
  right: 0 !important;
  z-index: 999999 !important;
  background-color: #000000 !important;
  border-top: 1px solid var(--bdr) !important;
  padding: 8px 0 12px 0 !important;
  margin: 0 !important;
}

div[data-testid="stRadio"] > div[role="radiogroup"] {
  display: flex !important;
  flex-direction: row !important;
  justify-content: space-around !important;
  align-items: center !important;
  max-width: 600px !important;
  margin: 0 auto !important;
  width: 100% !important;
}

/* ラベル自体をタップ可能なボタン化 */
div[data-testid="stRadio"] label {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  flex: 1 !important;
  cursor: pointer !important;
  background: transparent !important;
  border: none !important;
  margin: 0 !important;
  padding: 2px 0 !important;
  outline: none !important;
}

/* 「まるぽっち（ラジオディスク）」を完全に非表示 */
div[data-testid="stRadio"] label > div:first-child,
div[data-testid="stRadio"] label input[type="radio"],
div[data-testid="stRadio"] div[data-baseweb="radio"] > div:first-child {
  display: none !important;
}

/* アイコン定義（未選択状態：グレー） */
div[data-testid="stRadio"] label::before {
  font-family: "Font Awesome 6 Free" !important;
  font-weight: 900 !important;
  font-size: 1.4rem !important;
  color: #444444 !important;
  display: block !important;
  margin-bottom: 2px !important;
  transition: all 0.15s ease-in-out !important;
}

/* 画像と同じ5つのFontAwesomeアイコン割り当て */
div[data-testid="stRadio"] label:nth-child(1)::before { content: "\f57d"; } /* 地球儀 (地合い) */
div[data-testid="stRadio"] label:nth-child(2)::before { content: "\f6e3"; } /* 工具 (ツール) */
div[data-testid="stRadio"] label:nth-child(3)::before { content: "\f7c0"; } /* アンテナ (全株スキャン) */
div[data-testid="stRadio"] label:nth-child(4)::before { content: "\f5dc"; } /* 脳 (AI脳内) */
div[data-testid="stRadio"] label:nth-child(5)::before { content: "\f201"; } /* グラフ (ログ) */

/* 未選択時のテキスト非表示 */
div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {
  font-size: 0.65rem !important;
  font-weight: 800 !important;
  margin: 0 !important;
  line-height: 1 !important;
  display: none !important;
}

/* 🟢 押している（アクティブな）ボタンの発光スタイル */
div[data-testid="stRadio"] label:has(input:checked)::before,
div[data-testid="stRadio"] label[aria-checked="true"]::before {
  color: var(--acc) !important;
  transform: scale(1.1) !important;
  filter: drop-shadow(0px 0px 6px rgba(213, 0, 249, 0.8)) !important;
}

/* 🟢 押している（アクティブな）ボタンのみテキストを表示＆ネオン発光 */
div[data-testid="stRadio"] label:has(input:checked) div[data-testid="stMarkdownContainer"] p,
div[data-testid="stRadio"] label[aria-checked="true"] div[data-testid="stMarkdownContainer"] p {
  color: var(--acc) !important;
  display: block !important;
}

/* ボタン類 */
div.stButton > button {
  border-radius: 9999px !important;
  font-weight: 800 !important;
}
button[data-baseweb="tab"] { color: var(--muted) !important; font-weight: 700 !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: var(--acc) !important; }
div[data-baseweb="tab-highlight"] { background-color: var(--acc) !important; }
</style>
"""
