"""
styles.py
---------
BNF PREMIUM — ネオンUI & FontAwesomeスタイル定義
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

/* ボトムナビゲーション (画像準拠) */
div[data-testid="stRadio"] {
  position: fixed !important;
  bottom: 0 !important;
  left: 0 !important;
  right: 0 !important;
  z-index: 999999 !important;
  background: #000000 !important;
  border-top: 1px solid var(--bdr) !important;
  padding: 8px 0 12px 0 !important;
  margin: 0 !important;
}
div[data-testid="stRadio"] > div[role="radiogroup"] {
  display: flex !important;
  justify-content: space-around !important;
  align-items: center !important;
  max-width: 600px !important;
  margin: 0 auto !important;
  width: 100% !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label {
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
  margin: 0 !important;
  flex: 1 !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  cursor: pointer !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label input {
  display: none !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label::before {
  font-family: "Font Awesome 6 Free" !important;
  font-weight: 900 !important;
  font-size: 1.35rem !important;
  color: #444444 !important;
  transition: all 0.15s ease !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(1)::before { content: "\f57d"; }
div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(2)::before { content: "\f6e3"; }
div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(3)::before { content: "\f7c0"; }
div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(4)::before { content: "\f5dc"; }
div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(5)::before { content: "\f201"; }

div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked)::before {
  color: var(--acc) !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label p {
  font-size: 0.65rem !important;
  font-weight: 800 !important;
  margin-top: 3px !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p {
  color: var(--acc) !important;
  display: block !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label:not(:has(input:checked)) p {
  display: none !important;
}

/* Streamlit標準コンポーネント */
div.stButton > button {
  border-radius: 9999px !important;
  font-weight: 800 !important;
}
button[data-baseweb="tab"] { color: var(--muted) !important; font-weight: 700 !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: var(--acc) !important; }
div[data-baseweb="tab-highlight"] { background-color: var(--acc) !important; }
</style>
"""
