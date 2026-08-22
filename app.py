"""
app.py
------
BNF PREMIUM (完全画像再現・絵文字100%排除版)
"""

from __future__ import annotations

import streamlit as st

from bnf_core import (
    data, risk, scanner, storage, universe, price_cache,
    gemini_client, notifications, styles, browser_notify,
)

st.set_page_config(page_title="BNF PREMIUM", layout="centered")
st.markdown(styles.CSS, unsafe_allow_html=True)

# ── UI描画関数 ──
def render_market_bar(nikkei, down_ratio, usdjpy):
    n_str = f"{nikkei:,.0f}" if nikkei else "--"
    u_str = f"{usdjpy:.2f}" if usdjpy else "--"
    d_str = f"{down_ratio}" if down_ratio is not None else "--"
    return f"""
    <div style="display:flex; border:1px solid #23272C; background:#121417; border-radius:10px; overflow:hidden; margin-bottom:14px;">
      <div style="flex:1; padding:10px; text-align:center; border-right:1px solid #23272C;">
        <div style="font-size:0.7rem; color:#71767B;">日経平均</div>
        <div style="font-size:1rem; font-weight:800; font-family:monospace; margin-top:2px;">{n_str}</div>
      </div>
      <div style="flex:1; padding:10px; text-align:center; border-right:1px solid #23272C;">
        <div style="font-size:0.7rem; color:#71767B;">値下がり銘柄</div>
        <div style="font-size:1rem; font-weight:800; font-family:monospace; margin-top:2px;">{d_str}</div>
        <div style="font-size:0.65rem; color:#71767B;">東証全体</div>
      </div>
      <div style="flex:1; padding:10px; text-align:center;">
        <div style="font-size:0.7rem; color:#71767B;">ドル円</div>
        <div style="font-size:1rem; font-weight:800; font-family:monospace; margin-top:2px;">{u_str}</div>
      </div>
    </div>
    """

def render_score_hero(score, label):
    s_str = f"{score:.0f}" if score is not None else "--"
    return f"""
    <div style="display:flex; flex-direction:column; align-items:center; padding:20px; border:1px solid #23272C; border-radius:10px; background:#121417; margin-bottom:14px;">
      <div>
        <span style="font-size:3.2rem; font-weight:900; font-family:monospace;">{s_str}</span>
        <span style="font-size:1.2rem; font-weight:700; color:#71767B;">/100</span>
      </div>
      <div style="font-size:0.85rem; font-weight:700; margin-top:6px;">{label}</div>
    </div>
    """

def render_quote(text):
    return f"""
    <div style="display:flex; gap:10px; padding:12px; border:1px solid #23272C; border-radius:10px; background:#121417; margin-bottom:14px;">
      <div style="width:36px; height:36px; border-radius:50%; background:rgba(213,0,249,0.15); border:1px solid #d500f9; display:flex; align-items:center; justify-content:center; font-size:0.65rem; font-weight:900; color:#d500f9; flex-shrink:0;">BNF</div>
      <div>
        <span style="font-size:0.85rem; font-weight:800;">B.N.F</span>
        <span style="font-size:0.75rem; color:#71767B; margin-left:4px;">@market_shadow</span>
        <div style="font-size:0.85rem; margin-top:2px; font-style:italic;">「{text}」</div>
      </div>
    </div>
    """

# ── セッション初期化 ──
for key, default in [("market_snapshot", None), ("market_comment", None), ("chat_history", []), ("scan_results", [])]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── ヘッダー ──
st.markdown(
    """
    <div class="bnf-header">
      <div class="bnf-title">BNF PREMIUM</div>
      <div class="bnf-live-badge"><div class="bnf-live-dot"></div>AI LIVE</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("#### 設定")
    api_key = st.text_input("Gemini APIキー", type="password")
    discord_webhook = st.text_input("Discord Webhook URL", type="password")
    ntfy_topic = st.text_input("ntfy.sh トピック名")

# ── 画像完全準拠 ボトムナビゲーション ──
selected_tab = st.radio(
    label="Nav",
    options=["地合い", "ツール", "全株スキャン", "AI脳内", "ログ"],
    horizontal=True,
    label_visibility="collapsed",
    key="bottom_nav",
)

# ══════════════════════════════════════════════════
# 地合い画面 (画像5再現)
# ══════════════════════════════════════════════════
if selected_tab == "地合い":
    snap = st.session_state.market_snapshot
    st.markdown(
        render_market_bar(
            snap.nikkei if snap else None,
            snap.down_ratio_score if snap else None,
            snap.usdjpy if snap else None,
        ),
        unsafe_allow_html=True,
    )

    label = "AIで同期してください"
    if snap:
        label = "パニック水準に近い → 逆張り好機" if snap.down_ratio_score <= 25 else "中立圏"

    st.markdown(render_score_hero(snap.down_ratio_score if snap else None, label), unsafe_allow_html=True)

    # 水色丸ボタン
    st.markdown("""
    <style>
    div.row-widget.stButton > button {
        background-color: #1D9BF0 !important;
        color: white !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("<i class='fa-solid fa-bolt'></i> AIで今日の地合いをリアルタイム同期", use_container_width=True):
        with st.spinner("同期中..."):
            st.session_state.market_snapshot = data.fetch_market_snapshot()
            st.session_state.market_comment = None
            st.rerun()

    comment = st.session_state.market_comment or "AIで同期すると状況コメントが出ます"
    st.markdown(render_quote(comment), unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# ツール画面 (画像2再現)
# ══════════════════════════════════════════════════
elif selected_tab == "ツール":
    st.markdown("<h3 style='margin:0 0 10px 0;'>逆張り分析ツール</h3>", unsafe_allow_html=True)
    sub_calc, sub_watch, sub_pos = st.tabs(["単発計算", "個別監視リスト", "ナンピン計算"])

    with sub_calc:
        col1, col2 = st.columns(2)
        code = col1.text_input("銘柄コード", placeholder="例: 6920")
        sector = col2.text_input("自動判定セクター", value="コード入力で自動判定", disabled=True)

        # エメラルドグリーン丸ボタン
        st.markdown("""
        <style>
        div.row-widget.stButton > button {
            background-color: #00BA7C !important;
            color: white !important;
            border: none !important;
        }
        </style>
        """, unsafe_allow_html=True)

        if st.button("<i class='fa-solid fa-rotate'></i> AIでこの銘柄を即時同期", use_container_width=True):
            if code:
                with st.spinner("取得中..."):
                    fetched = data.fetch_stock_snapshot(code)
                    if fetched:
                        st.session_state["last_fetched"] = fetched

        fetched = st.session_state.get("last_fetched")
        col_a, col_b = st.columns(2)
        price = col_a.number_input("現在値 (円)", min_value=0.0, value=float(fetched.price) if fetched else 0.0)
        ma25 = col_b.number_input("25日移動平均線", min_value=0.0, value=float(fetched.ma25) if fetched else 0.0)

        st.markdown("<hr style='border-color:#23272C; margin:15px 0;'>", unsafe_allow_html=True)
        st.write("**必要資金:** -- 円")
        st.write("**25日線 乖離率:** -- %")
        st.write("**判定:** 未入力")
        st.write("**しきい値 (地合い調整):** --")

        st.markdown("<p style='color:#d500f9; font-weight:800; margin-top:15px;'><i class='fa-regular fa-circle-dot'></i> 利確 & 損切りターゲット</p>", unsafe_allow_html=True)
        st.slider("損切り幅 (エントリー価格から)", 1.0, 15.0, 3.0, 0.5)
        st.slider("利確ターゲット② (カスタム幅)", 1.0, 30.0, 5.0, 0.5)

    with sub_watch:
        st.caption("監視リスト")

    with sub_pos:
        st.caption("ナンピン計算")

# ══════════════════════════════════════════════════
# 全株スキャン画面 (画像4再現)
# ══════════════════════════════════════════════════
elif selected_tab == "全株スキャン":
    st.markdown("<h3 style='margin:0;'>全株スキャン (東証全銘柄対象)</h3>", unsafe_allow_html=True)
    st.caption("最終スキャン: 未実行")

    st.markdown(
        """
        <div style="background:#121417; border:1px dashed #d500f9; border-radius:10px; padding:12px; margin:10px 0 15px 0;">
          <div style="color:#d500f9; font-weight:800; font-size:0.85rem; margin-bottom:4px;">
            <i class="fa-solid fa-circle" style="font-size:0.5rem; vertical-align:middle;"></i> Gemini AIが東証全銘柄をリアルタイム監視
          </div>
          <div style="font-size:0.78rem; color:#71767B; line-height:1.4;">
            Gemini AIのWeb検索機能を使い、東証プライム・スタンダード・グロース市場の約3,800銘柄すべての中からBNFロジックに合致する銘柄をリアルタイム抽出します。
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sc1, sc2 = st.columns(2)
    sc1.selectbox("候補件数", ["10件 (標準)", "20件", "50件"])
    sc2.selectbox("対象セクター", ["全セクター", "大型・主役", "ハイテク"])
    sc3, sc4 = st.columns(2)
    sc3.selectbox("乖離率フィルター", ["全ゾーン"])
    sc4.selectbox("並び替え", ["乖離率が大きい順"])

    # 紫色丸ボタン
    st.markdown("""
    <style>
    div.row-widget.stButton > button {
        background-color: #d500f9 !important;
        color: white !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("<i class='fa-solid fa-satellite-dish'></i> 東証全銘柄をAIスキャン (~30秒)", use_container_width=True):
        st.info("スキャン処理中...")

    st.markdown("<div style='text-align:center; margin-top:10px;'><span style='background:#121417; border:1px solid #23272C; padding:6px 16px; border-radius:9999px; font-size:0.8rem;'><i class='fa-solid fa-bell'></i> 通知許可済み <i class='fa-solid fa-square-check' style='color:#00BA7C;'></i></span></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# AI脳内画面 (画像1再現)
# ══════════════════════════════════════════════════
elif selected_tab == "AI脳内":
    col_k, col_b = st.columns([3, 1])
    col_k.text_input("Gemini APIキーを入力", type="password", label_visibility="collapsed", placeholder="Gemini APIキーを入力")
    
    st.markdown("""
    <style>
    div.row-widget.stButton > button {
        background-color: #d500f9 !important;
        color: white !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    col_b.button("接続する", use_container_width=True)

    st.markdown("<div style='font-size:0.8rem; color:#00BA7C; margin-bottom:12px;'><i class='fa-solid fa-square-check'></i> 接続済み</div>", unsafe_allow_html=True)

    # クイック質問ボタン
    st.markdown("""
    <style>
    div.row-widget.stButton > button {
        background-color: #1A1D21 !important;
        color: var(--text) !important;
        border: 1px solid #23272C !important;
    }
    </style>
    """, unsafe_allow_html=True)
    q1, q2, q3 = st.columns(3)
    q1.button("<i class='fa-solid fa-newspaper'></i> 今日の相場")
    q2.button("<i class='fa-solid fa-circle-question'></i> 今買していい？")
    q3.button("<i class='fa-solid fa-scissors'></i> 損切り判断")

    st.markdown(
        """
        <div style="background:#1A1D21; border-radius:12px; padding:12px; font-size:0.85rem; margin-top:15px; max-width:85%;">
          何か地合いや逆張り戦略についてご質問はありますか？
        </div>
        """,
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════
# ログ画面 (画像3再現)
# ══════════════════════════════════════════════════
elif selected_tab == "ログ":
    st.markdown("<h3 style='margin:0 0 10px 0;'>売買ログ</h3>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("総ログ", 0)
    c2.metric("買いゾーン", 0)
    c3.metric("平均乖離率", "-- %")

    st.markdown("""
    <style>
    div.row-widget.stButton > button {
        background-color: transparent !important;
        color: var(--text) !important;
        border: 1px solid #23272C !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.button("<i class='fa-solid fa-file-csv'></i> CSVエクスポート")

    st.markdown("<div style='text-align:center; padding:40px 0; color:#71767B; font-size:0.9rem;'>ログはありません</div>", unsafe_allow_html=True)

    st.markdown("""
    <style>
    div.row-widget.stButton > button[kind="secondary"] {
        border: 1px solid #F4212E !important;
        color: #F4212E !important;
        background: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.button("すべてリセット", type="secondary", use_container_width=True)
