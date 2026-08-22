"""
styles.py
---------
BNF PREMIUM — ネオンUI & FontAwesomeアイコン標準化モジュール
絵文字を一切排し、画像通りの洗練されたボトムナビゲーションを再現。
"""

CSS = """
<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

:root {
  --black: #000000;
  --s1: #16181C;
  --s2: #1C1F23;
  --bdr: #2F3336;
  --text: #EFF3F4;
  --muted: #71767B;
  --acc: #d500f9;
  --acc-dim: rgba(213, 0, 249, 0.12);
  --blue: #1D9BF0;
  --green: #00BA7C;
  --orange: #FF7527;
  --red: #F4212E;
  --pill: 9999px;
}

/* 全体スタイル */
.stApp {
  background-color: var(--black) !important;
  color: var(--text) !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
}

/* メイン領域の余白（ボトムナビと被らない設計） */
section.main > div {
  max-width: 680px;
  margin: 0 auto;
  padding: 0.5rem 1rem 95px 1rem !important;
}

/* ── ヘッダー ── */
.bnf-header {
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 4px;
  margin-bottom: 16px;
  border-bottom: 1px solid var(--bdr);
}
.bnf-title {
  font-size: 1.15rem;
  font-weight: 900;
  letter-spacing: 0.08em;
  color: var(--acc);
}
.bnf-live-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--green);
  background: rgba(0, 186, 124, 0.12);
  padding: 4px 10px;
  border-radius: var(--pill);
}
.bnf-live-dot {
  width: 7px;
  height: 7px;
  background: var(--green);
  border-radius: 50%;
}

/* ── マーケット情報・スコア ── */
.mkt-bar {
  display: flex;
  border: 1px solid var(--bdr);
  background: var(--s1);
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 14px;
}
.mkt-cell {
  flex: 1;
  padding: 12px 8px;
  text-align: center;
  border-right: 1px solid var(--bdr);
}
.mkt-cell:last-child { border-right: none; }
.mkt-lbl { font-size: 0.68rem; color: var(--muted); font-weight: 600; }
.mkt-val { font-size: 1rem; font-weight: 800; font-family: 'Courier New', monospace; margin-top: 2px; }

.score-hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 22px 16px 18px;
  border: 1px solid var(--bdr);
  border-radius: 12px;
  background: var(--s1);
  margin-bottom: 14px;
}
.score-big { font-size: 3.5rem; font-weight: 900; font-family: 'Courier New', monospace; line-height: 1; }
.score-suffix { font-size: 1.3rem; font-weight: 700; color: var(--muted); margin-left: 2px; }
.score-label { font-size: 0.88rem; font-weight: 700; margin-top: 8px; color: var(--text); }

.bnf-quote {
  display: flex;
  gap: 12px;
  padding: 14px 16px;
  border: 1px solid var(--bdr);
  border-radius: 12px;
  background: var(--s1);
  margin-bottom: 14px;
}
.bnf-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  flex-shrink: 0;
  background: var(--acc-dim);
  border: 2px solid var(--acc);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.72rem;
  font-weight: 900;
  color: var(--acc);
}
.bnf-qname { font-size: 0.88rem; font-weight: 800; color: var(--text); }
.bnf-qhandle { font-size: 0.78rem; color: var(--muted); margin-left: 4px; }
.bnf-qtext { font-size: 0.88rem; margin-top: 4px; line-height: 1.45; font-style: italic; color: var(--text); }

/* 紫枠AIカード */
.ai-card {
  background: rgba(213, 0, 249, 0.04);
  border: 1px dashed var(--acc);
  border-radius: 12px;
  padding: 14px;
  margin-bottom: 14px;
}

/* ── 完全画像完全準拠 ボトムナビゲーション ── */
div[data-testid="stRadio"] {
  position: fixed !important;
  bottom: 0 !important;
  left: 0 !important;
  right: 0 !important;
  z-index: 999999 !important;
  background: rgba(0, 0, 0, 0.94) !important;
  backdrop-filter: blur(16px) !important;
  border-top: 1px solid var(--bdr) !important;
  padding: 6px 0 10px 0 !important;
  margin: 0 !important;
}

div[data-testid="stRadio"] > div[role="radiogroup"] {
  display: flex !important;
  justify-content: space-around !important;
  align-items: center !important;
  max-width: 680px !important;
  margin: 0 auto !important;
  width: 100% !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] > label {
  background: transparent !important;
  border: none !important;
  padding: 4px 0 !important;
  margin: 0 !important;
  flex: 1 !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer !important;
}

/* ラジオボタンの円を隠す */
div[data-testid="stRadio"] div[role="radiogroup"] > label input {
  display: none !important;
}

/* FontAwesomeアイコン注入 */
div[data-testid="stRadio"] div[role="radiogroup"] > label::before {
  font-family: "Font Awesome 6 Free" !important;
  font-weight: 900 !important;
  font-size: 1.35rem !important;
  color: #444444 !important;
  transition: all 0.15s ease-in-out !important;
  display: block !important;
  line-height: 1 !important;
}

/* 各アイコンのコード（1:地球, 2:工具, 3:アンテナ, 4:脳, 5:グラフ） */
div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(1)::before { content: "\f57d"; }
div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(2)::before { content: "\f6e3"; }
div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(3)::before { content: "\f7c0"; }
div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(4)::before { content: "\f5dc"; }
div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(5)::before { content: "\f201"; }

/* アクティブ（選択中）時の発光スタイル */
div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked)::before {
  color: var(--acc) !important;
  transform: scale(1.08) !important;
}

/* テキストラベル制御（選択中のみ文字を表示） */
div[data-testid="stRadio"] div[role="radiogroup"] > label p {
  margin: 4px 0 0 0 !important;
  font-size: 0.65rem !important;
  font-weight: 800 !important;
  line-height: 1 !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p {
  color: var(--acc) !important;
  display: block !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] > label:not(:has(input:checked)) p {
  display: none !important;
}

/* ── Streamlit入力フォーム・標準要素の上書き ── */
div.stButton > button {
  background-color: var(--acc) !important;
  color: #ffffff !important;
  border: none !important;
  border-radius: var(--pill) !important;
  font-weight: 800 !important;
  font-size: 0.9rem !important;
  padding: 10px 16px !important;
  width: 100% !important;
}

/* サブタブ */
button[data-baseweb="tab"] { color: var(--muted) !important; font-weight: 700 !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: var(--acc) !important; }
div[data-baseweb="tab-highlight"] { background-color: var(--acc) !important; }
</style>
"""

def market_bar_html(nikkei, nikkei_chg, down_ratio, usdjpy, usdjpy_chg) -> str:
    n_str = f"{nikkei:,.0f}" if nikkei else "--"
    u_str = f"{usdjpy:.2f}" if usdjpy else "--"
    d_str = f"{down_ratio}" if down_ratio is not None else "--"
    return f"""
    <div class="mkt-bar">
      <div class="mkt-cell">
        <div class="mkt-lbl">日経平均</div>
        <div class="mkt-val">{n_str}</div>
      </div>
      <div class="mkt-cell">
        <div class="mkt-lbl">値下がり銘柄</div>
        <div class="mkt-val">{d_str}</div>
        <div class="mkt-lbl" style="margin-top:2px;">東証全体</div>
      </div>
      <div class="mkt-cell">
        <div class="mkt-lbl">ドル円</div>
        <div class="mkt-val">{u_str}</div>
      </div>
    </div>
    """

def score_hero_html(score, label) -> str:
    s_str = f"{score:.0f}" if score is not None else "--"
    return f"""
    <div class="score-hero">
      <div>
        <span class="score-big" style="color:var(--text);">{s_str}</span>
        <span class="score-suffix">/100</span>
      </div>
      <div class="score-label">{label}</div>
    </div>
    """

def quote_html(text) -> str:
    return f"""
    <div class="bnf-quote">
      <div class="bnf-avatar">BNF</div>
      <div>
        <span class="bnf-qname">B.N.F</span>
        <span class="bnf-qhandle">@market_shadow</span>
        <div class="bnf-qtext">「{text}」</div>
      </div>
    </div>
    """

def scan_hit_card_html(hit) -> str:
    return f"""
    <div style="background:var(--s1); border:1px solid var(--bdr); border-radius:10px; padding:12px; margin-bottom:8px;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-weight:800; font-size:0.95rem;">{hit.get('code')} {hit.get('name', '')}</span>
        <span style="color:var(--acc); font-family:monospace; font-weight:800;">{hit.get('deviation_pct', 0):+.1f}%</span>
      </div>
    </div>
    """
