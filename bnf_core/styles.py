"""
styles.py
---------
元のHTML/CSSデザイン（黒背景×紫アクセントのX/Twitter風UI）を完全再現したCSSおよび
HTMLコンポーネント生成モジュール。
st.markdown(CSS, unsafe_allow_html=True) を用いて注入して使用します。
"""

CSS = """
<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

:root {
  --black:#000; --s1:#16181C; --s2:#1C1F23; --bdr:#2F3336;
  --text:#EFF3F4; --muted:#71767B;
  --acc:#d500f9; --acc-dim:rgba(213,0,249,.10);
  --blue:#1D9BF0; --green:#00BA7C; --orange:#FF7527; --red:#F4212E;
  --pill:9999px;
}

/* 全体スタイルリセット */
.stApp {
  background-color: var(--black) !important;
  color: var(--text) !important;
  font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif !important;
}

section.main > div {
  max-width: 720px;
  margin: 0 auto;
  padding: 0.5rem 1rem 2rem 1rem;
}

/* アニメーション */
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:.3;} }

/* --- 元HTMLコンポーネントデザイン --- */

/* ヘッダー */
.app-header {
  height:53px; display:flex; align-items:center; justify-content:space-between; padding:0 16px;
  background:rgba(0,0,0,.85); backdrop-filter:blur(12px);
  border-bottom:1px solid var(--bdr); border-radius:8px; margin-bottom:16px;
}
.hdr-title { font-size:1.05rem; font-weight:800; letter-spacing:.12em; color:var(--acc); }
.live-badge {
  display:flex; align-items:center; gap:5px; font-size:.72rem; font-weight:700;
  color:var(--green); background:rgba(0,186,124,.1); padding:4px 10px; border-radius:var(--pill);
}
.live-dot { width:7px; height:7px; background:var(--green); border-radius:50%; animation:blink 1.5s infinite; }

/* マーケットバー */
.mkt-bar { display:flex; border:1px solid var(--bdr); background:var(--s1); border-radius:10px; overflow:hidden; margin-bottom:12px; }
.mkt-cell { flex:1; padding:10px 12px; text-align:center; border-right:1px solid var(--bdr); }
.mkt-cell:last-child { border-right:none; }
.mkt-lbl { font-size:.65rem; color:var(--muted); font-weight:600; letter-spacing:.03em; }
.mkt-val { font-size:.92rem; font-weight:800; font-family:'Courier New',monospace; margin-top:2px; color:var(--text); }
.mkt-chg { font-size:.7rem; font-weight:700; margin-top:1px; }
.up { color:var(--red); }
.dn { color:var(--blue); }

/* スコアヒーロー */
.score-hero {
  display:flex; flex-direction:column; align-items:center;
  padding:20px 16px 16px; border:1px solid var(--bdr); border-radius:12px; background:var(--s1); margin-bottom:12px;
}
.score-big { font-size:3.8rem; font-weight:900; font-family:'Courier New',monospace; line-height:1; }
.score-suffix { font-size:1.4rem; font-weight:700; color:var(--muted); margin-left:3px; }
.score-label { font-size:.9rem; font-weight:700; margin-top:6px; color:var(--text); }

/* 1400カウントダウン */
.countdown-bar { padding:12px 16px; border:1px solid var(--bdr); border-radius:12px; background:var(--s2); margin-bottom:12px; }
.cd-label { font-size:.75rem; color:var(--muted); margin-bottom:6px; font-weight:600; }
.cd-track { height:8px; background:var(--bdr); border-radius:var(--pill); overflow:hidden; }
.cd-fill { height:100%; background:var(--green); border-radius:var(--pill); transition:width .5s; }
.cd-nums { display:flex; justify-content:space-between; margin-top:5px; font-size:.75rem; }

/* BNFコメント */
.bnf-quote { display:flex; gap:10px; padding:14px 16px; border:1px solid var(--bdr); border-radius:12px; background:var(--s1); margin-bottom:12px; }
.bnf-avatar {
  width:36px; height:36px; border-radius:50%; flex-shrink:0; background:var(--acc-dim);
  border:2px solid var(--acc); display:flex; align-items:center; justify-content:center;
  font-size:.7rem; font-weight:900; color:var(--acc);
}
.bnf-qname { font-size:.85rem; font-weight:700; color:var(--text); }
.bnf-qhandle { font-size:.78rem; color:var(--muted); margin-left:4px; }
.bnf-qtext { font-size:.9rem; margin-top:3px; line-height:1.5; font-style:italic; color:var(--text); }

/* AIレポートカード */
.ai-report-card { background:rgba(213,0,249,.04); border:1px dashed var(--acc); border-radius:12px; padding:14px; margin-bottom:12px; }
.ai-report-hdr { display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; font-size:.85rem; font-weight:800; color:var(--acc); }
.ai-report-body { font-size:.86rem; line-height:1.6; color:var(--text); white-space:pre-wrap; }

/* 全株スキャン結果 */
.scan-result-card { background:rgba(0,186,124,.04); border:1px solid var(--green); border-radius:12px; padding:14px; margin-bottom:12px; }
.scan-result-hdr { font-size:.85rem; font-weight:800; color:var(--green); margin-bottom:10px; display:flex; align-items:center; gap:6px; }
.scan-stock-item { display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px dashed var(--bdr); font-size:.85rem; }
.scan-stock-item:last-child { border-bottom:none; }
.scan-stock-name { flex:1; color:var(--text); }
.scan-stock-kairi { font-family:'Courier New',monospace; font-weight:900; margin:0 10px; color:var(--text); }
.scan-badge { font-size:.7rem; font-weight:800; padding:2px 8px; border-radius:4px; }
.badge-buy { background:rgba(0,186,124,.2); color:var(--green); }
.badge-watch { background:rgba(255,117,39,.2); color:var(--orange); }
.badge-hold { background:rgba(113,118,123,.2); color:var(--muted); }

/* シグナルアラート */
.signal-card { background:rgba(29,155,240,.04); border:1px solid var(--bdr); border-radius:12px; padding:12px 14px; margin-bottom:12px; }
.sig-hdr { display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; }
.sig-title { font-size:.85rem; font-weight:800; color:var(--blue); display:flex; align-items:center; gap:6px; }
.sig-time { font-size:.7rem; color:var(--muted); font-family:'Courier New',monospace; }
.sig-body { font-size:.85rem; line-height:1.5; color:var(--text); }

/* 利確・損切りカード */
.target-card { border:1px solid var(--bdr); border-radius:12px; background:var(--s1); overflow:hidden; margin-bottom:12px; }
.target-hdr { padding:12px 16px 0; font-size:.82rem; font-weight:800; color:var(--acc); display:flex; align-items:center; gap:6px; }
.target-grid { display:grid; grid-template-columns:1fr 1fr; border-top:1px solid var(--bdr); margin-top:10px; }
.target-cell { padding:14px 16px; border-bottom:1px solid var(--bdr); border-right:1px solid var(--bdr); }
.target-cell:nth-child(even) { border-right:none; }
.target-lbl { font-size:.72rem; color:var(--muted); font-weight:600; margin-bottom:4px; }
.target-val { font-size:1.25rem; font-weight:900; font-family:'Courier New',monospace; }
.target-sub { font-size:.75rem; margin-top:2px; }

/* チャットバブル */
.bubble { max-width:85%; padding:10px 14px; border-radius:18px; font-size:.9rem; line-height:1.5; word-break:break-word; margin-bottom:10px; }
.bubble.bnf { background:var(--s2); color:var(--text); border-bottom-left-radius:4px; border:1px solid var(--bdr); }
.bubble.user { background:var(--acc); color:#fff; border-bottom-right-radius:4px; margin-left:auto; }

/* ログ・統計 */
.stats-grid { display:grid; grid-template-columns:repeat(3,1fr); background:var(--s1); border:1px solid var(--bdr); border-radius:12px; overflow:hidden; margin-bottom:12px; }
.stat-cell { padding:12px; text-align:center; border-right:1px solid var(--bdr); }
.stat-cell:last-child { border-right:none; }
.stat-num { font-size:1.2rem; font-weight:900; font-family:'Courier New',monospace; color:var(--text); }
.stat-lbl { font-size:.65rem; color:var(--muted); margin-top:2px; }

/* --- Streamlit 標準ウィジェットの上書き --- */
div.stButton > button, div.stDownloadButton > button {
  display: inline-flex !important; align-items: center !important; justify-content: center !important;
  gap: 7px !important; padding: 9px 20px !important; border-radius: var(--pill) !important;
  font-weight: 700 !important; font-size: .9rem !important; cursor: pointer !important; width: 100% !important;
  background: var(--s2) !important; border: 1px solid var(--bdr) !important; color: var(--text) !important;
}
div.stButton > button:hover, div.stDownloadButton > button:hover {
  border-color: var(--acc) !important; color: var(--acc) !important;
}
div.stButton > button[kind="primary"] {
  background: var(--acc) !important; color: #fff !important; border: none !important;
}

div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
  background-color: var(--s2) !important; border-color: var(--bdr) !important; border-radius: 10px !important;
}
input { color: var(--text) !important; font-family: inherit !important; }

button[data-baseweb="tab"] { font-weight: 700 !important; font-size: .78rem !important; color: var(--muted) !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: var(--acc) !important; }
div[data-baseweb="tab-highlight"] { background-color: var(--acc) !important; }
div[data-baseweb="tab-border"] { background-color: var(--bdr) !important; }
</style>
"""

# HTMLコンポーネント用ヘルパー関数群

def header_html(title="BNF CORE AUTOMATION PREMIUM") -> str:
    return f"""
    <div class="app-header">
      <div class="hdr-title">{title}</div>
      <div class="live-badge"><div class="live-dot"></div>AI LIVE</div>
    </div>
    """

def market_bar_html(nikkei, nikkei_chg, down_stocks, usdjpy, usdjpy_chg) -> str:
    n_cls = "up" if nikkei_chg >= 0 else "dn"
    u_cls = "up" if usdjpy_chg >= 0 else "dn"
    return f"""
    <div class="mkt-bar">
      <div class="mkt-cell">
        <div class="mkt-lbl">日経平均</div>
        <div class="mkt-val">{nikkei:,.0f}</div>
        <div class="mkt-chg {n_cls}">{nikkei_chg:+.2f}%</div>
      </div>
      <div class="mkt-cell">
        <div class="mkt-lbl">値下がり銘柄</div>
        <div class="mkt-val">{down_stocks}</div>
        <div class="mkt-chg" style="color:var(--muted);">東証全体</div>
      </div>
      <div class="mkt-cell">
        <div class="mkt-lbl">ドル円</div>
        <div class="mkt-val">{usdjpy:.2f}</div>
        <div class="mkt-chg {u_cls}">{usdjpy_chg:+.2f}%</div>
      </div>
    </div>
    """

def score_hero_html(score: int, label: str) -> str:
    color = "var(--acc)" if score >= 70 else ("var(--green)" if score <= 30 else "var(--text)")
    return f"""
    <div class="score-hero">
      <div>
        <span class="score-big" style="color:{color};">{score}</span>
        <span class="score-suffix">/100</span>
      </div>
      <div class="score-label">{label}</div>
    </div>
    """

def countdown_bar_html(current_down: int, target: int = 1400) -> str:
    pct = min(100, int((current_down / target) * 100)) if target > 0 else 0
    remain = max(0, target - current_down)
    return f"""
    <div class="countdown-bar">
      <div class="cd-label">BNF臨界点まで（東証値下がり銘柄 / {target:,}銘柄）</div>
      <div class="cd-track"><div class="cd-fill" style="width:{pct}%"></div></div>
      <div class="cd-nums">
        <span style="color:var(--muted);">{current_down:,} 銘柄が値下がり中</span>
        <span style="color:var(--green);">あと {remain:,} 銘柄</span>
      </div>
    </div>
    """

def quote_html(comment: str) -> str:
    return f"""
    <div class="bnf-quote">
      <div class="bnf-avatar">BNF</div>
      <div>
        <span class="bnf-qname">B.N.F</span>
        <span class="bnf-qhandle">@market_shadow</span>
        <div class="bnf-qtext">「{comment}」</div>
      </div>
    </div>
    """

def ai_report_card_html(report_text: str, update_time: str = "未更新") -> str:
    return f"""
    <div class="ai-report-card">
      <div class="ai-report-hdr">
        <span><i class="fa-solid fa-brain"></i> AI相場観レポート</span>
        <span style="font-size:.7rem;color:var(--muted);">{update_time}</span>
      </div>
      <div class="ai-report-body">{report_text}</div>
    </div>
    """

def target_card_html(profit_ma, profit_ma_pct, profit_custom, profit_custom_pct, stop_val, stop_pct, rrr, rrr_badge) -> str:
    return f"""
    <div class="target-card">
      <div class="target-hdr"><i class="fa-solid fa-bullseye"></i> 利確 & 損切りターゲット</div>
      <div class="target-grid">
        <div class="target-cell">
          <div class="target-lbl">🎯 利確①（MA25回帰）</div>
          <div class="target-val" style="color:var(--green);">{profit_ma:,.1f} 円</div>
          <div class="target-sub" style="color:var(--green);">{profit_ma_pct:+.1f} %</div>
        </div>
        <div class="target-cell">
          <div class="target-lbl">🎯 利確②（カスタム）</div>
          <div class="target-val" style="color:var(--blue);">{profit_custom:,.1f} 円</div>
          <div class="target-sub" style="color:var(--blue);">{profit_custom_pct:+.1f} %</div>
        </div>
        <div class="target-cell">
          <div class="target-lbl">🔪 損切りライン</div>
          <div class="target-val" style="color:var(--red);">{stop_val:,.1f} 円</div>
          <div class="target-sub" style="color:var(--red);">{stop_pct:-.1f} %</div>
        </div>
        <div class="target-cell">
          <div class="target-lbl">⚖️ RRR（MA25基準）</div>
          <div class="target-val">{rrr:.2f}</div>
          <div class="target-sub" style="color:var(--muted);">{rrr_badge}</div>
        </div>
      </div>
    </div>
    """

def chat_bubble_html(text: str, is_bnf: bool = True) -> str:
    cls = "bnf" if is_bnf else "user"
    return f'<div class="bubble {cls}">{text}</div>'
