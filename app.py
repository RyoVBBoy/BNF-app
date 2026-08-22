"""
app.py
------
BNF CORE AUTOMATION PREMIUM — (完全ノンスマイリー・FontAwesomeネオンUI版)
"""

from __future__ import annotations

import streamlit as st

from bnf_core import (
    data, risk, scanner, storage, universe, price_cache,
    gemini_client, notifications, styles, browser_notify,
)

st.set_page_config(page_title="BNF PREMIUM", page_icon="📈", layout="centered")
st.markdown(styles.CSS, unsafe_allow_html=True)

# ── セッション状態初期化 ──
for key, default in [
    ("market_snapshot", None), ("market_comment", None),
    ("chat_history", []), ("scan_results", []),
]:
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
    api_key = st.text_input("Gemini APIキー(任意)", type="password")
    st.caption("数値計算はAPIキーなしでも全て動作します。")
    st.markdown("---")
    st.markdown("#### 通知")
    discord_webhook = st.text_input("Discord Webhook URL", type="password")
    ntfy_topic = st.text_input("ntfy.sh トピック名", placeholder="例: my-bnf-alert")

# ── 画像完全準拠 ボトムナビゲーション ──
selected_tab = st.radio(
    label="Navigation",
    options=["地合い", "ツール", "全株スキャン", "AI脳内", "ログ"],
    horizontal=True,
    label_visibility="collapsed",
    key="bottom_nav",
)

# ══════════════════════════════════════════════════
# 地合い画面 (画像5)
# ══════════════════════════════════════════════════
if selected_tab == "地合い":
    snap = st.session_state.market_snapshot
    st.markdown(
        styles.market_bar_html(
            snap.nikkei if snap else None,
            snap.nikkei_chg_pct if snap else None,
            snap.down_ratio_score if snap else None,
            snap.usdjpy if snap else None,
            snap.usdjpy_chg_pct if snap else None,
        ),
        unsafe_allow_html=True,
    )

    label = "AIで同期してください"
    if snap:
        if snap.down_ratio_score <= 25:
            label = "パニック水準に近い → 逆張り好機ゾーン"
        elif snap.down_ratio_score >= 75:
            label = "過熱水準 → 新規逆張りは慎重に"
        else:
            label = "中立圏"

    st.markdown(
        styles.score_hero_html(snap.down_ratio_score if snap else None, label),
        unsafe_allow_html=True,
    )

    if st.button("AIで今日の地合いをリアルタイム同期", use_container_width=True):
        with st.spinner("同期中..."):
            st.session_state.market_snapshot = data.fetch_market_snapshot()
            st.session_state.market_comment = None
            st.rerun()

    comment = st.session_state.market_comment or "AIで同期すると状況コメントが出ます"
    st.markdown(styles.quote_html(comment), unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# ツール画面 (画像2)
# ══════════════════════════════════════════════════
elif selected_tab == "ツール":
    st.markdown("### 逆張り分析ツール")
    sub_calc, sub_watch, sub_pos = st.tabs(["単発計算", "個別監視リスト", "ナンピン計算"])

    with sub_calc:
        col1, col2 = st.columns(2)
        code = col1.text_input("銘柄コード", placeholder="例: 6920")
        sector = col2.selectbox("自動判定セクター", list(risk.SECTOR_THRESHOLDS.keys()))

        if code and st.button("AIでこの銘柄を即時同期"):
            with st.spinner("取得中..."):
                fetched = data.fetch_stock_snapshot(code)
                if fetched:
                    st.session_state["last_fetched"] = fetched

        fetched = st.session_state.get("last_fetched")
        col_a, col_b = st.columns(2)
        price = col_a.number_input("現在値 (円)", min_value=0.0, value=float(fetched.price) if fetched else 0.0)
        ma25 = col_b.number_input("25日移動平均線", min_value=0.0, value=float(fetched.ma25) if fetched else 0.0)

        if price and ma25:
            deviation_pct = (price - ma25) / ma25 * 100
            st.metric("25日線 乖離率", f"{deviation_pct:.2f}%")

            st.markdown("<p style='color:var(--acc); font-weight:800; margin-top:10px;'><i class='fa-solid fa-bullseye'></i> 利確 & 損切りターゲット</p>", unsafe_allow_html=True)
            stop_pct = st.slider("損切り幅 (エントリー価格から)", 1.0, 15.0, 3.0, 0.5)
            custom_profit_pct = st.slider("利確ターゲット② (カスタム幅)", 1.0, 30.0, 5.0, 0.5)

            tg = risk.targets(price, ma25, stop_pct, custom_profit_pct, 0.0, 1.5)
            st.write(f"**利確① (MA25回帰):** {tg['profit_ma']:.1f} 円")
            st.write(f"**損切りライン:** {tg['effective_stop']:.1f} 円")

    with sub_watch:
        st.caption("監視リスト")

    with sub_pos:
        st.caption("ナンピン計算")

# ══════════════════════════════════════════════════
# 全株スキャン画面 (画像4)
# ══════════════════════════════════════════════════
elif selected_tab == "全株スキャン":
    st.markdown("### 全株スキャン (東証全銘柄対象)")
    st.markdown(
        """
        <div class="ai-card">
          <div style="color:var(--acc); font-weight:800; font-size:0.9rem; margin-bottom:6px;">
            <i class="fa-solid fa-circle" style="font-size:0.6rem; vertical-align:middle;"></i> Gemini AIが東証全銘柄をリアルタイム監視
          </div>
          <div style="font-size:0.8rem; color:var(--muted); line-height:1.5;">
            Gemini AIのWeb検索機能を使い、東証プライム・スタンダード・グロース市場の約3,800銘柄すべての中からBNFロジックに合致する銘柄をリアルタイム抽出します。
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sc1, sc2 = st.columns(2)
    limit = sc1.selectbox("候補件数", ["10件 (標準)", "20件", "50件"])
    sector_filter = sc2.selectbox("対象セクター", ["全セクター", "大型・主役", "ハイテク", "グロース"])

    if st.button("東証全銘柄をAIスキャン (~30秒)", type="primary"):
        st.info("スキャンを実行中...")

# ══════════════════════════════════════════════════
# AI脳内画面 (画像1)
# ══════════════════════════════════════════════════
elif selected_tab == "AI脳内":
    if not api_key:
        st.info("サイドバーにGemini APIキーを入力するとAIチャットが有効になります。")
    else:
        for msg in st.session_state.chat_history:
            with st.chat_message("user" if msg["role"] == "user" else "assistant"):
                st.write(msg["text"])

        prompt = st.chat_input("メッセージを入力...")
        if prompt:
            st.session_state.chat_history.append({"role": "user", "text": prompt})
            st.session_state.chat_history.append({"role": "model", "text": "地合いや逆張り戦略について何かご質問はありますか？"})
            st.rerun()

# ══════════════════════════════════════════════════
# ログ画面 (画像3)
# ══════════════════════════════════════════════════
elif selected_tab == "ログ":
    st.markdown("### 売買ログ")
    logs = storage.load_logs()

    c1, c2, c3 = st.columns(3)
    c1.metric("総ログ", len(logs))
    c2.metric("買いゾーン", sum(1 for l in logs if l.get("zone") == "buy"))
    c3.metric("平均乖離率", "-- %")

    if st.button("CSVエクスポート"):
        pass

    if not logs:
        st.caption("<div style='text-align:center; padding:30px; color:var(--muted);'>ログはありません</div>", unsafe_allow_html=True)

    if st.button("すべてリセット"):
        storage.clear_logs()
        st.rerun()
