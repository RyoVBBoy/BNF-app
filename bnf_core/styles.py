"""
styles.py
---------
元のHTML版(黒背景×紫アクセントのX/Twitter風ダークUI)に近づけるための
CSS。st.markdown(..., unsafe_allow_html=True) で注入して使う。
スマホ(縦長)・PC(横長)どちらでも崩れないよう、最大幅とパディングを
メディアクエリで調整している。
"""

CSS = """
<style>
:root {
  --bnf-black:#000000; --bnf-s1:#16181C; --bnf-s2:#1C1F23; --bnf-bdr:#2F3336;
  --bnf-text:#EFF3F4; --bnf-muted:#71767B;
  --bnf-acc:#d500f9; --bnf-acc-dim:rgba(213,0,249,.10);
  --bnf-blue:#1D9BF0; --bnf-green:#00BA7C; --bnf-orange:#FF7527; --bnf-red:#F4212E;
}

/* 全体背景 */
.stApp {
  background: var(--bnf-black) !important;
  color: var(--bnf-text);
}
section.main > div {
  max-width: 720px;
  margin: 0 auto;
  padding-top: 0.5rem;
}
@media (max-width: 600px) {
  section.main > div { padding-left: 0.6rem; padding-right: 0.6rem; }
}

/* ヘッダー */
.bnf-header {
  display:flex; align-items:center; justify-content:space-between;
  padding: 10px 4px 14px 4px; border-bottom:1px solid var(--bnf-bdr); margin-bottom: 10px;
}
.bnf-title {
  font-size:1.3rem; font-weight:900; letter-spacing:.08em; color: var(--bnf-acc);
}
.bnf-live-badge {
  display:inline-flex; align-items:center; gap:6px; font-size:.72rem; font-weight:700;
  color: var(--bnf-green); background: rgba(0,186,124,.12); padding:5px 12px; border-radius:999px;
}
.bnf-live-dot {
  width:7px; height:7px; background:var(--bnf-green); border-radius:50%;
  animation: bnf-blink 1.5s infinite;
}
@keyframes bnf-blink { 0%,100%{opacity:1;} 50%{opacity:.25;} }

/* マーケットバー */
.bnf-mkt-bar { display:flex; border:1px solid var(--bnf-bdr); border-radius:14px; overflow:hidden; margin-bottom:14px; }
.bnf-mkt-cell { flex:1; padding:12px 10px; text-align:center; border-right:1px solid var(--bnf-bdr); background:var(--bnf-s1); }
.bnf-mkt-cell:last-child { border-right:none; }
.bnf-mkt-lbl { font-size:.66rem; color:var(--bnf-muted); font-weight:700; letter-spacing:.03em; }
.bnf-mkt-val { font-size:1rem; font-weight:900; font-family:'Courier New',monospace; margin-top:3px; }
.bnf-mkt-chg { font-size:.72rem; font-weight:700; margin-top:2px; }
.bnf-up { color: var(--bnf-red); }
.bnf-dn { color: var(--bnf-blue); }

/* スコアヒーロー */
.bnf-score-hero {
  display:flex; flex-direction:column; align-items:center;
  padding:22px 16px 18px; border:1px solid var(--bnf-bdr); border-radius:16px;
  background: var(--bnf-s1); margin-bottom:14px;
}
.bnf-score-big { font-size:3.2rem; font-weight:900; font-family:'Courier New',monospace; line-height:1; }
.bnf-score-suffix { font-size:1.2rem; font-weight:700; color:var(--bnf-muted); margin-left:4px; }
.bnf-score-label { font-size:.9rem; font-weight:700; margin-top:8px; }

/* BNFコメント */
.bnf-quote { display:flex; gap:12px; padding:14px 16px; border:1px solid var(--bnf-bdr);
  border-radius:14px; background:var(--bnf-s1); margin-bottom:14px; }
.bnf-avatar { width:38px; height:38px; border-radius:50%; flex-shrink:0; background:var(--bnf-acc-dim);
  border:2px solid var(--bnf-acc); display:flex; align-items:center; justify-content:center;
  font-size:.68rem; font-weight:900; color:var(--bnf-acc); }
.bnf-qname { font-size:.85rem; font-weight:800; }
.bnf-qhandle { font-size:.76rem; color:var(--bnf-muted); margin-left:5px; }
.bnf-qtext { font-size:.88rem; margin-top:4px; line-height:1.55; font-style:italic; color:var(--bnf-text); }

/* カード(スキャン結果など) */
.bnf-card {
  border:1px solid var(--bnf-bdr); border-radius:14px; padding:14px 16px;
  background: var(--bnf-s1); margin-bottom:10px;
}
.bnf-card-buy { border-color: var(--bnf-green); background: rgba(0,186,124,.05); }
.bnf-card-watch { border-color: var(--bnf-orange); background: rgba(255,117,39,.05); }
.bnf-badge {
  display:inline-block; font-size:.68rem; font-weight:800; padding:2px 10px; border-radius:999px;
}
.bnf-badge-buy { background: rgba(0,186,124,.2); color: var(--bnf-green); }
.bnf-badge-watch { background: rgba(255,117,39,.2); color: var(--bnf-orange); }

/* Streamlitボタンをピル型・アクセントカラーに */
div.stButton > button, div.stDownloadButton > button {
  border-radius: 999px !important;
  font-weight: 700 !important;
  border: 1px solid var(--bnf-bdr) !important;
  background: var(--bnf-s2) !important;
  color: var(--bnf-text) !important;
  padding: 0.5rem 1rem !important;
}
div.stButton > button:hover, div.stDownloadButton > button:hover {
  border-color: var(--bnf-acc) !important;
  color: var(--bnf-acc) !important;
}
div.stButton > button[kind="primary"] {
  background: linear-gradient(90deg, var(--bnf-blue), var(--bnf-acc)) !important;
  border: none !important; color: #fff !important;
}

/* タブ */
button[data-baseweb="tab"] { font-weight:700; color: var(--bnf-muted); }
button[data-baseweb="tab"][aria-selected="true"] { color: var(--bnf-acc) !important; }
div[data-baseweb="tab-highlight"] { background-color: var(--bnf-acc) !important; }
div[data-baseweb="tab-border"] { background-color: var(--bnf-bdr) !important; }

/* メトリクス・カード風コンテナ */
div[data-testid="stMetric"] {
  background: var(--bnf-s1); border:1px solid var(--bnf-bdr); border-radius:12px; padding:10px 12px;
}
div[data-testid="stMetricValue"] { font-family:'Courier New',monospace; color: var(--bnf-text); }

/* サイドバー */
section[data-testid="stSidebar"] { background: var(--bnf-s1); border-right:1px solid var(--bnf-bdr); }

/* コンテナ(st.container(border=True)) */
div[data-testid="stVerticalBlockBorderWrapper"] {
  border-color: var(--bnf-bdr) !important; border-radius: 14px !important; background: var(--bnf-s1);
}
</style>
"""


def market_bar_html(nikkei, nikkei_chg, score, usdjpy, usdjpy_chg) -> str:
    n_cls = "bnf-up" if nikkei_chg >= 0 else "bnf-dn"
    u_cls = "bnf-up" if usdjpy_chg >= 0 else "bnf-dn"
    return f"""
    <div class="bnf-mkt-bar">
      <div class="bnf-mkt-cell">
        <div class="bnf-mkt-lbl">日経平均</div>
        <div class="bnf-mkt-val">{nikkei:,.0f}</div>
        <div class="bnf-mkt-chg {n_cls}">{nikkei_chg:+.2f}%</div>
      </div>
      <div class="bnf-mkt-cell">
        <div class="bnf-mkt-lbl">地合いスコア</div>
        <div class="bnf-mkt-val">{score:.0f}/100</div>
        <div class="bnf-mkt-chg" style="color:var(--bnf-muted);">0=パニック</div>
      </div>
      <div class="bnf-mkt-cell">
        <div class="bnf-mkt-lbl">ドル円</div>
        <div class="bnf-mkt-val">{usdjpy:.2f}</div>
        <div class="bnf-mkt-chg {u_cls}">{usdjpy_chg:+.2f}%</div>
      </div>
    </div>
    """


def score_hero_html(score, label) -> str:
    color = "var(--bnf-green)" if score <= 30 else ("var(--bnf-red)" if score >= 70 else "var(--bnf-text)")
    return f"""
    <div class="bnf-score-hero">
      <div><span class="bnf-score-big" style="color:{color};">{score:.0f}</span>
      <span class="bnf-score-suffix">/100</span></div>
      <div class="bnf-score-label">{label}</div>
    </div>
    """


def quote_html(comment: str) -> str:
    return f"""
    <div class="bnf-quote">
      <div class="bnf-avatar">BNF</div>
      <div>
        <span class="bnf-qname">B.N.F</span><span class="bnf-qhandle">@market_shadow</span>
        <div class="bnf-qtext">「{comment}」</div>
      </div>
    </div>
    """


def scan_hit_card_html(hit) -> str:
    cls = "bnf-card-buy" if hit.zone == "buy" else "bnf-card-watch"
    badge_cls = "bnf-badge-buy" if hit.zone == "buy" else "bnf-badge-watch"
    badge_txt = "買いゾーン" if hit.zone == "buy" else "監視ゾーン"
    return f"""
    <div class="bnf-card {cls}">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div><b>{hit.code}</b> {hit.name} <span style="color:var(--bnf-muted);font-size:.78rem;">({hit.sector})</span></div>
        <span class="bnf-badge {badge_cls}">{badge_txt}</span>
      </div>
      <div style="margin-top:6px; font-size:.85rem; color:var(--bnf-text);">
        現在値 {hit.price:.1f}円 / MA25 {hit.ma25:.1f}円 / 乖離 {hit.deviation_pct:+.2f}%
      </div>
    </div>
    """
