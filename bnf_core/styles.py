"""
styles.py
---------
BNF PREMIUM — 完全崩れ防止 & モバイル最適化CSS
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

.stApp {
  background-color: var(--black) !important;
  color: var(--text) !important;
}

section.main > div {
  max-width: 600px;
  margin: 0 auto;
  padding: 0.5rem 1rem 120px 1rem !important;
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
   ボトムナビゲーション (強固な消去 & 強制横並び)
   ══════════════════════════════════════════════════ */
div[data-testid="stRadio"] {
  position: fixed !important;
  bottom: 0 !important;
  left: 0 !important;
  right: 0 !important;
  z-index: 99999 !important;
  background-color: #000000 !important;
  border-top: 1px solid var(--bdr) !important;
  padding: 6px 0 16px 0 !important;
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
  padding: 0 !important;
  min-width: 0 !important;
}

/* ラジオボタンの「丸印」を全ての構造層で非表示 */
div[data-testid="stRadio"] label input,
div[data-testid="stRadio"] label [data-baseweb="radio"],
div[data-testid="stRadio"] label > div:first-child {
  display: none !important;
  width: 0 !important;
  height: 0 !important;
  opacity: 0 !important;
}

/* アイコン表示 (未選択時: グレー) */
div[data-testid="stRadio"] label::before {
  font-family: "Font Awesome 6 Free" !important;
  font-weight: 900 !important;
  font-size: 1.25rem !important;
  color: #444444 !important;
  display: block !important;
  margin-bottom: 2px !important;
  transition: all 0.15s ease !important;
}

div[data-testid="stRadio"] label:nth-child(1)::before { content: "\f57d"; }
div[data-testid="stRadio"] label:nth-child(2)::before { content: "\f6e3"; }
div[data-testid="stRadio"] label:nth-child(3)::before { content: "\f7c0"; }
div[data-testid="stRadio"] label:nth-child(4)::before { content: "\f5dc"; }
div[data-testid="stRadio"] label:nth-child(5)::before { content: "\f201"; }

/* テキスト折り返し防止 */
div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {
  font-size: 0.6rem !important;
  font-weight: 800 !important;
  margin: 0 !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}

/* 🟢 選択中 (発光ネオンパープル) */
div[data-testid="stRadio"] label:has(input:checked)::before,
div[data-testid="stRadio"] label[aria-checked="true"]::before {
  color: var(--acc) !important;
  filter: drop-shadow(0px 0px 6px rgba(213, 0, 249, 0.9)) !important;
}

div[data-testid="stRadio"] label:has(input:checked) div[data-testid="stMarkdownContainer"] p,
div[data-testid="stRadio"] label[aria-checked="true"] div[data-testid="stMarkdownContainer"] p {
  color: var(--acc) !important;
}

/* 一般ボタン */
div.stButton > button {
  border-radius: 9999px !important;
  font-weight: 800 !important;
}
</style>
"""
