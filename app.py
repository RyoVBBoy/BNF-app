"""
app.py
------
BNF CORE AUTOMATION PREMIUM — Python(Streamlit)版

起動:
    streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from bnf_core import (
    data, risk, scanner, storage, universe, price_cache,
    gemini_client, notifications, styles, browser_notify,
)

st.set_page_config(page_title="BNF PREMIUM", page_icon="📉", layout="centered")
st.markdown(styles.CSS, unsafe_allow_html=True)

# ── セッション状態初期化 ──────────────────────────
for key, default in [
    ("market_snapshot", None), ("market_comment", None),
    ("chat_history", []), ("scan_results", []),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── ヘッダー ──────────────────────────────
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
    api_key = st.text_input("Gemini APIキー(任意・コメント生成用)", type="password")
    st.caption("数値計算はAPIキーなしでも全て動作します。")
    st.markdown("---")
    st.markdown("#### 通知(アプリを閉じていてもOK)")
    discord_webhook = st.text_input("Discord Webhook URL(任意)", type="password")
    ntfy_topic = st.text_input("ntfy.sh トピック名(任意)", placeholder="例: my-bnf-alert-xyz")
    st.caption("スキャン完了時に結果をここへ送信します。")

tab_market, tab_tools, tab_scan, tab_chat, tab_log = st.tabs(
    ["📊 地合い", "🛠 ツール", "📡 全株スキャン", "🧠 AI脳内", "📒 ログ"]
)

# ══════════════════════════════════════════════════
# 地合いタブ
# ══════════════════════════════════════════════════
with tab_market:
    if st.button("⚡ 市場データを同期(実データ取得)", use_container_width=True):
        with st.spinner("日経平均・ドル円を取得中..."):
            st.session_state.market_snapshot = data.fetch_market_snapshot()
            st.session_state.market_comment = None

    snap = st.session_state.market_snapshot
    if snap:
        st.markdown(
            styles.market_bar_html(snap.nikkei, snap.nikkei_chg_pct, snap.down_ratio_score,
                                    snap.usdjpy, snap.usdjpy_chg_pct),
            unsafe_allow_html=True,
        )
        if snap.down_ratio_score <= 25:
            label = "パニック水準に近い → 逆張り好機ゾーン"
        elif snap.down_ratio_score >= 75:
            label = "過熱水準 → 新規逆張りは慎重に"
        else:
            label = "中立圏"
        st.markdown(styles.score_hero_html(snap.down_ratio_score, label), unsafe_allow_html=True)

        if api_key:
            if st.button("🧠 AIコメントを生成"):
                with st.spinner("生成中..."):
                    st.session_state.market_comment = gemini_client.market_comment(
                        api_key, snap.nikkei, snap.nikkei_chg_pct, snap.usdjpy, snap.down_ratio_score,
                    )
            if st.session_state.market_comment:
                st.markdown(styles.quote_html(st.session_state.market_comment), unsafe_allow_html=True)
            else:
                st.markdown(styles.quote_html("AIで同期すると状況コメントが出ます"), unsafe_allow_html=True)
        else:
            st.markdown(styles.quote_html("APIキーを設定すると状況コメントが出ます"), unsafe_allow_html=True)
    else:
        st.caption("上のボタンで実データを取得してください。")

# ══════════════════════════════════════════════════
# ツールタブ
# ══════════════════════════════════════════════════
with tab_tools:
    sub_calc, sub_watch, sub_pos = st.tabs(["単発計算", "監視リスト", "ナンピン計算"])

    with sub_calc:
        code = st.text_input("銘柄コード(例: 6920)")
        sector = st.selectbox("セクター", list(risk.SECTOR_THRESHOLDS.keys()))

        if code and st.button("この銘柄を実データ同期"):
            with st.spinner("取得中..."):
                fetched = data.fetch_stock_snapshot(code)
                if fetched is None:
                    st.error("データを取得できませんでした。コードを確認してください。")
                else:
                    st.session_state["last_fetched"] = fetched

        fetched = st.session_state.get("last_fetched")
        col_a, col_b = st.columns(2)
        price = col_a.number_input("現在値(円)", min_value=0.0,
                                    value=float(fetched.price) if fetched else 0.0)
        ma25 = col_b.number_input("25日移動平均(円)", min_value=0.0,
                                   value=float(fetched.ma25) if fetched else 0.0)
        atr14 = fetched.atr14 if fetched else 0.0
        market_score = st.session_state.market_snapshot.down_ratio_score if st.session_state.market_snapshot else 50.0

        if price and ma25:
            deviation_pct = (price - ma25) / ma25 * 100
            judgement = risk.judge_zone(deviation_pct, sector, market_score)
            st.metric("25日線 乖離率", f"{deviation_pct:.2f}%")
            st.write(f"**判定:** {judgement.label}")

            st.markdown("##### 🎯 利確・損切りターゲット")
            stop_pct = st.slider("損切り幅(%)", 1.0, 15.0, 3.0, 0.5)
            custom_profit_pct = st.slider("利確ターゲット②(カスタム%)", 1.0, 30.0, 5.0, 0.5)
            atr_multiple = st.slider("ATR倍率(損切りに使用)", 0.5, 3.0, 1.5, 0.1)

            tg = risk.targets(price, ma25, stop_pct, custom_profit_pct, atr14, atr_multiple)
            t1, t2 = st.columns(2)
            t1.metric("利確①(MA25回帰)", f"{tg['profit_ma']:.1f}円", f"{tg['profit_ma_pct']:+.2f}%")
            t2.metric("利確②(カスタム)", f"{tg['profit_custom']:.1f}円", f"+{custom_profit_pct:.1f}%")
            t3, t4 = st.columns(2)
            t3.metric("損切りライン(実効)", f"{tg['effective_stop']:.1f}円",
                       help=f"固定%: {tg['stop_fixed']}円 / ATR基準: {tg['stop_atr']}円")
            t4.metric("RRR(MA25基準)", f"{tg['rrr']}" if tg["rrr"] else "—")

            st.markdown("##### ⚖️ 資金管理(口座リスク%からロット逆算)")
            balance = st.number_input("口座残高(円)", min_value=0, value=1_000_000, step=10000)
            risk_pct = st.slider("1トレードで許容するリスク(口座比 %)", 0.5, 5.0, 1.0, 0.1)
            pos = risk.position_size(balance, price, tg["effective_stop"], risk_pct)
            p1, p2 = st.columns(2)
            p1.metric("推奨購入株数", f"{pos['shares']:,}株")
            p2.metric("必要資金", f"{pos['capital_required']:,}円")
            st.caption(f"損切りライン到達時の想定損失: 約{pos['risk_amount']:,}円(口座の{risk_pct}%)")

            if api_key and fetched and st.button("🧠 AI分析コメントを生成"):
                with st.spinner("生成中..."):
                    st.info(gemini_client.stock_report(api_key, code, price, ma25, deviation_pct, judgement.label))

            if st.button("💾 ログに保存"):
                storage.add_log({
                    "code": code, "sector": sector, "price": price, "ma25": ma25,
                    "deviation_pct": round(deviation_pct, 2), "zone": judgement.zone,
                    "stop": tg["effective_stop"], "profit_ma": tg["profit_ma"],
                    "rrr": tg["rrr"], "shares": pos["shares"],
                })
                st.success("保存しました。「ログ」タブで確認できます。")

    with sub_watch:
        st.caption("お気に入り銘柄のクイック確認リスト(東証全銘柄スキャンは「全株スキャン」タブへ)")
        wc1, wc2, wc3 = st.columns([1, 1.4, 0.6])
        new_code = wc1.text_input("コード", key="wl_code")
        new_name = wc2.text_input("銘柄名(任意)", key="wl_name")
        if wc3.button("追加"):
            if new_code:
                storage.add_to_watchlist(new_code, new_name)
                st.rerun()

        wl = storage.load_watchlist()
        if not wl:
            st.caption("まだ登録がありません。")
        for item in wl:
            snap2 = data.fetch_stock_snapshot(item["code"])
            row = st.columns([1, 2, 1, 0.6])
            row[0].write(f"**{item['code']}**")
            row[1].write(item.get("name", ""))
            row[2].write(f"{snap2.deviation_pct:+.1f}%" if snap2 else "取得失敗")
            if row[3].button("削除", key=f"del_{item['code']}"):
                storage.remove_from_watchlist(item["code"])
                st.rerun()

    with sub_pos:
        st.markdown("##### 含み損益・ナンピンシミュレータ")
        buy = st.number_input("購入単価(円)", min_value=0.0, value=0.0)
        qty = st.number_input("保有株数", min_value=0, value=0, step=100)
        now = st.number_input("現在の株価(円)", min_value=0.0, value=0.0)
        cash = st.number_input("口座残高(円)", min_value=0, value=0, step=10000)
        if buy and qty and now:
            pl = (now - buy) * qty
            pl_pct = (now - buy) / buy * 100
            st.metric("含み損益", f"{pl:,.0f}円", f"{pl_pct:+.2f}%")
            if cash and now > 0:
                max_additional = int(cash // now // 100 * 100)
                if max_additional > 0:
                    new_avg = (buy * qty + now * max_additional) / (qty + max_additional)
                    st.write(f"残資金で最大 **{max_additional:,}株** 追加可能 → 平均取得単価は **{new_avg:,.1f}円**")

# ══════════════════════════════════════════════════
# 全株スキャンタブ
# ══════════════════════════════════════════════════
with tab_scan:
    uni_updated = universe.universe_last_updated()
    cache_updated = price_cache.cache_last_updated()
    uni_size = scanner.universe_size() if uni_updated else 0

    st.caption(
        f"銘柄マスタ: {uni_size:,}銘柄"
        + (f"(更新: {uni_updated:%Y-%m-%d})" if uni_updated else "(未取得)")
        + " / 価格キャッシュ: "
        + (f"{cache_updated:%Y-%m-%d %H:%M}時点" if cache_updated else "未取得")
    )

    step1, step2 = st.columns(2)
    if step1.button("① 銘柄マスタ更新(JPX・月1回で十分)", use_container_width=True):
        with st.spinner("JPXから東証上場銘柄一覧を取得中..."):
            df = universe.refresh_universe()
        st.success(f"{len(df):,}銘柄を取得しました。")
        st.rerun()

    if step2.button("② 価格キャッシュ更新(全銘柄・数分かかります)", use_container_width=True):
        uni = universe.load_universe()
        codes = uni["code"].tolist()
        progress = st.progress(0.0, text="準備中...")

        def _cb(done, total):
            progress.progress(done / total, text=f"取得中... {done}/{total}チャンク")

        with st.spinner(f"{len(codes):,}銘柄を取得中(バッチ処理・数分かかります)..."):
            price_cache.update_cache(codes, progress_cb=_cb)
        progress.empty()
        st.success("価格キャッシュを更新しました。")
        st.rerun()

    st.markdown("---")
    sc1, sc2 = st.columns(2)
    limit = sc1.selectbox("候補件数", [5, 10, 20, 50], index=1)
    sector_filter = sc2.selectbox("対象セクター", ["all", "heavy", "tech", "growth", "defensive"])
    sc3, sc4 = st.columns(2)
    zone_filter = sc3.selectbox("ゾーンフィルター", ["all", "buy", "watch"])
    sort_by = sc4.selectbox("並び替え", ["kairi", "risk"])

    market_score = st.session_state.market_snapshot.down_ratio_score if st.session_state.market_snapshot else 50.0

    if st.button("📡 スキャン実行(キャッシュから瞬時)", use_container_width=True, type="primary"):
        if not cache_updated:
            st.warning("先に①②のキャッシュ更新を実行してください。")
        else:
            st.session_state.scan_results = scanner.run_scan(
                market_score, zone_filter, sector_filter, sort_by, limit
            )
            hits = st.session_state.scan_results
            summary = notifications.format_scan_summary(hits)
            if discord_webhook:
                notifications.send_discord(discord_webhook, summary)
            if ntfy_topic:
                notifications.send_ntfy(ntfy_topic, summary)
            if hits:
                browser_notify.fire_notification(
                    "BNF PREMIUM: スキャン完了", f"{len(hits)}件ヒットしました"
                )

    results = st.session_state.scan_results
    if results:
        for hit in results:
            st.markdown(styles.scan_hit_card_html(hit), unsafe_allow_html=True)
    elif st.session_state.get("scan_results") == []:
        st.caption("条件に合致する銘柄はありませんでした。")

    st.markdown("---")
    browser_notify.request_permission_button()

# ══════════════════════════════════════════════════
# AI脳内タブ
# ══════════════════════════════════════════════════
with tab_chat:
    if not api_key:
        st.info("サイドバーにGemini APIキーを入力するとチャットできます。")
    else:
        for msg in st.session_state.chat_history:
            with st.chat_message("user" if msg["role"] == "user" else "assistant"):
                st.write(msg["text"])

        prompt = st.chat_input("メッセージを入力...")
        if prompt:
            st.session_state.chat_history.append({"role": "user", "text": prompt})
            snap3 = st.session_state.market_snapshot
            context = (
                f"地合いスコア: {snap3.down_ratio_score:.0f}/100, 日経平均: {snap3.nikkei:.0f}円"
                if snap3 else "市場データ未取得"
            )
            with st.spinner("考え中..."):
                reply = gemini_client.chat_reply(api_key, st.session_state.chat_history[:-1], prompt, context)
            st.session_state.chat_history.append({"role": "model", "text": reply})
            st.rerun()

# ══════════════════════════════════════════════════
# ログタブ
# ══════════════════════════════════════════════════
with tab_log:
    logs = storage.load_logs()
    if logs:
        c1, c2, c3 = st.columns(3)
        c1.metric("記録件数", len(logs))
        c2.metric("平均RRR", f"{sum(l.get('rrr') or 0 for l in logs) / len(logs):.2f}")
        c3.metric("買いゾーン件数", sum(1 for l in logs if l.get("zone") == "buy"))

        st.dataframe(logs, use_container_width=True)

        csv_lines = ["code,sector,price,ma25,deviation_pct,zone,stop,profit_ma,rrr,shares,logged_at"]
        for l in logs:
            csv_lines.append(",".join(str(l.get(k, "")) for k in [
                "code", "sector", "price", "ma25", "deviation_pct", "zone",
                "stop", "profit_ma", "rrr", "shares", "logged_at",
            ]))
        st.download_button("📥 CSVエクスポート", "\n".join(csv_lines), file_name="bnf_logs.csv")

        if st.button("🗑 すべてリセット"):
            storage.clear_logs()
            st.rerun()
    else:
        st.caption("まだログがありません。「ツール」タブで計算後に保存してください。")
