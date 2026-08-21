"""
app.py
------
BNF CORE AUTOMATION PREMIUM — Python(Streamlit)版
元のHTML/JS単一ファイル版を、実データ計算ベースに置き換えて再構築したもの。

起動:
    streamlit run app.py
"""

from __future__ import annotations
import datetime as dt

import streamlit as st

from bnf_core import data, risk, scanner, storage, tickers, gemini_client

st.set_page_config(page_title="BNF PREMIUM", page_icon="📉", layout="centered")

# ── セッション状態初期化 ──────────────────────────
if "market_snapshot" not in st.session_state:
    st.session_state.market_snapshot = None
if "market_comment" not in st.session_state:
    st.session_state.market_comment = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "scan_results" not in st.session_state:
    st.session_state.scan_results = []

st.markdown(
    "<h2 style='color:#d500f9;letter-spacing:.08em;'>BNF PREMIUM</h2>",
    unsafe_allow_html=True,
)

api_key = st.sidebar.text_input("Gemini APIキー(任意・コメント生成用)", type="password")
st.sidebar.caption("数値計算はAPIキーなしでも全て動作します。APIキーはコメント生成にのみ使用します。")

tab_market, tab_tools, tab_scan, tab_chat, tab_log = st.tabs(
    ["📊 地合い", "🛠 ツール", "📡 全株スキャン", "🧠 AI脳内", "📒 ログ"]
)

# ══════════════════════════════════════════════════
# 地合いタブ
# ══════════════════════════════════════════════════
with tab_market:
    if st.button("🔄 市場データを同期(実データ取得)", use_container_width=True):
        with st.spinner("日経平均・ドル円を取得中..."):
            st.session_state.market_snapshot = data.fetch_market_snapshot()
            st.session_state.market_comment = None

    snap = st.session_state.market_snapshot
    if snap:
        c1, c2, c3 = st.columns(3)
        c1.metric("日経平均", f"{snap.nikkei:,.0f}", f"{snap.nikkei_chg_pct:+.2f}%")
        c2.metric("地合いスコア", f"{snap.down_ratio_score:.0f}/100")
        c3.metric("ドル円", f"{snap.usdjpy:.2f}", f"{snap.usdjpy_chg_pct:+.2f}%")

        if snap.down_ratio_score <= 25:
            st.success("パニック水準に近い → 逆張り好機ゾーン")
        elif snap.down_ratio_score >= 75:
            st.warning("過熱水準 → 新規逆張りは慎重に")
        else:
            st.info("中立圏")

        if api_key:
            if st.button("🧠 AIコメントを生成"):
                with st.spinner("生成中..."):
                    st.session_state.market_comment = gemini_client.market_comment(
                        api_key, snap.nikkei, snap.nikkei_chg_pct,
                        snap.usdjpy, snap.down_ratio_score,
                    )
            if st.session_state.market_comment:
                st.markdown(f"> 「{st.session_state.market_comment}」")
        else:
            st.caption("サイドバーにAPIキーを入力するとB.N.Fスタイルの短評を生成できます。")
    else:
        st.caption("上のボタンで実データを取得してください。")

# ══════════════════════════════════════════════════
# ツールタブ(単発計算・監視リスト・ナンピン計算)
# ══════════════════════════════════════════════════
with tab_tools:
    sub_calc, sub_watch, sub_pos = st.tabs(["単発計算", "監視リスト", "ナンピン計算"])

    with sub_calc:
        code = st.text_input("銘柄コード(例: 6920)")
        sector = st.selectbox("セクター", list(risk.SECTOR_THRESHOLDS.keys()))

        fetched = None
        if code and st.button("この銘柄を実データ同期"):
            with st.spinner("取得中..."):
                fetched = data.fetch_stock_snapshot(code)
                if fetched is None:
                    st.error("データを取得できませんでした。コードを確認してください。")
                else:
                    st.session_state["last_fetched"] = fetched

        fetched = st.session_state.get("last_fetched")

        col_a, col_b = st.columns(2)
        default_price = fetched.price if fetched else 0.0
        default_ma = fetched.ma25 if fetched else 0.0
        price = col_a.number_input("現在値(円)", min_value=0.0, value=float(default_price))
        ma25 = col_b.number_input("25日移動平均(円)", min_value=0.0, value=float(default_ma))
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
            st.caption(f"この損切りラインに達した場合の想定損失: 約{pos['risk_amount']:,}円(口座の{risk_pct}%)")

            if api_key and fetched and st.button("🧠 AI分析コメントを生成"):
                with st.spinner("生成中..."):
                    comment = gemini_client.stock_report(
                        api_key, code, price, ma25, deviation_pct, judgement.label
                    )
                    st.info(comment)

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
            snap = data.fetch_stock_snapshot(item["code"])
            row = st.columns([1, 2, 1, 0.6])
            row[0].write(f"**{item['code']}**")
            row[1].write(item.get("name", ""))
            if snap:
                row[2].write(f"{snap.deviation_pct:+.1f}%")
            else:
                row[2].write("取得失敗")
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
                    st.write(f"残資金で最大 **{max_additional:,}株** 追加可能 → 平均取得単価は **{new_avg:,.1f}円** に")

# ══════════════════════════════════════════════════
# 全株スキャンタブ
# ══════════════════════════════════════════════════
with tab_scan:
    st.caption(
        f"対象ユニバース: {len(tickers.all_codes())}銘柄(主要銘柄。tickers.py で編集可能)。"
        " 実データで乖離率・ATRを計算し、BNFロジックに合致する銘柄を抽出します。"
    )
    sc1, sc2 = st.columns(2)
    limit = sc1.selectbox("候補件数", [5, 10, 20], index=1)
    sector_filter = sc2.selectbox("対象セクター", ["all"] + list(tickers.DEFAULT_UNIVERSE.keys()))
    sc3, sc4 = st.columns(2)
    zone_filter = sc3.selectbox("ゾーンフィルター", ["all", "buy", "watch"])
    sort_by = sc4.selectbox("並び替え", ["kairi", "risk"])

    market_score = st.session_state.market_snapshot.down_ratio_score if st.session_state.market_snapshot else 50.0

    if st.button("📡 スキャン実行", use_container_width=True):
        with st.spinner("実データを取得・計算中(銘柄数によっては数十秒かかります)..."):
            st.session_state.scan_results = scanner.run_scan(
                market_score, zone_filter, sector_filter, sort_by, limit
            )

    results = st.session_state.scan_results
    if results:
        for hit in results:
            badge = "🟢 買い" if hit.zone == "buy" else "🟡 監視"
            with st.container(border=True):
                st.write(f"**{hit.code}** ({hit.sector}) — {badge}")
                st.write(f"現在値 {hit.price:.1f}円 / MA25 {hit.ma25:.1f}円 / 乖離 {hit.deviation_pct:+.2f}%")
                st.caption(hit.zone_label)
    elif st.session_state.get("scan_results") == []:
        st.caption("条件に合致する銘柄はありませんでした。")

# ══════════════════════════════════════════════════
# AI脳内(チャット)タブ
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
            snap = st.session_state.market_snapshot
            context = (
                f"地合いスコア: {snap.down_ratio_score:.0f}/100, 日経平均: {snap.nikkei:.0f}円"
                if snap else "市場データ未取得"
            )
            with st.spinner("考え中..."):
                reply = gemini_client.chat_reply(
                    api_key, st.session_state.chat_history[:-1], prompt, context
                )
            st.session_state.chat_history.append({"role": "model", "text": reply})
            st.rerun()

# ══════════════════════════════════════════════════
# ログタブ
# ══════════════════════════════════════════════════
with tab_log:
    logs = storage.load_logs()
    if logs:
        wins = sum(1 for l in logs if l.get("rrr") and l["rrr"] > 1)
        c1, c2, c3 = st.columns(3)
        c1.metric("記録件数", len(logs))
        c2.metric("平均RRR", f"{sum(l.get('rrr') or 0 for l in logs) / len(logs):.2f}")
        c3.metric("RRR>1件数", wins)

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
