import os
import json
import pandas as pd
import streamlit as st
from google import genai
from google.genai import types

# --- ページ基本設定 ---
st.set_page_config(
    page_title="BNF CORE AUTOMATION PREMIUM",
    page_icon="⚡",
    layout="wide"
)

# --- BNF思考プロンプト設計 ---
BNF_SYSTEM_PROMPT = """
# Role & Goal
あなたは伝説的トレーダー「BNF（小手川隆）」氏の取引ルールとロジックを忠実に再現する、高度な株式テクニカル分析AIです。

# 出力制御ルール（厳格順守）
1. 「株センサー」「Yahoo!ファイナンス」等の情報サイトやツールの紹介文・推奨文は絶対に出力しないでください。
2. 免責事項、前置き文、「特定銘柄の指定は難しい」といった回答回避の言い訳も一切禁止します。
3. 雑談や一般的なアドバイスを排除し、指定フォーマットによる【注目10銘柄】の出力のみを行ってください。

# BNF's Core Logic & Strategy
1. 地合いの判定:
   - 日経平均先物、NYダウ、ドル円の動向を確認する。
   - 地合いが「底打ち・上昇傾向」にある中での個別銘柄の下落は、絶好のリバウンド（買い）機会とみなす。
2. 移動平均線乖離率:
   - 25日移動平均線からのマイナス乖離率を最重視。
   - 大型株/ハイテク株: -10%〜-15%以上
   - 中小型株/新興株: -20%〜-30%以上
   - ディフェンシブ株: -7%〜-10%以上
3. 出来高と流動性:
   - パニック売り（投げ売り）が発生し、一時的に出来高が急増している場面を狙う。

# 出力フォーマット（全株スキャン時）
必ず以下の形式で【10銘柄】を出力してください：

■ [銘柄コード] 銘柄名（25日乖離率: XX.X%）
・総合判定: [S / A / B / C]
・分析理由: セクター特性と地合い相関の評価
・売買戦略: リバウンド狙い目と損切り条件
"""

# --- セッション状態の初期化 ---
if "logs" not in st.session_state:
    st.session_state.logs = []
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "market_data" not in st.session_state:
    st.session_state.market_data = {
        "nikkei": "--", "nikkei_chg": "--",
        "down_stocks": "--", "usdjpy": "--",
        "usdjpy_chg": "--", "score": "--",
        "status": "未同期", "comment": "AIで今日の地合いを同期してください。"
    }

# --- ヘルパー関数 ---
def get_genai_client(api_key):
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def call_gemini(api_key, prompt, use_search=False):
    client = get_genai_client(api_key)
    if not client:
        raise ValueError("Gemini APIキーを設定してください。")
    
    tools = [{"google_search": {}}] if use_search else None
    config = types.GenerateContentConfig(
        system_instruction=BNF_SYSTEM_PROMPT,
        tools=tools,
        temperature=0.2
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config
    )
    return response.text

# --- サイドバー構成 ---
st.sidebar.title("⚡ BNF CORE ENGINE")
api_key = st.sidebar.text_input("Gemini API Key", type="password", help="APIキーを入力してください")
trade_mode = st.sidebar.radio("取引モード", ["通常株（100株単位）", "単元未満株（1株単位）"])
is_mini = trade_mode == "単元未満株（1株単位）"

st.sidebar.markdown("---")
st.sidebar.caption("BNF Rule: 地合い・乖離率・出来高の3条件が揃った時のみエントリーを行う。")

# --- メイン画面 タブ構成 ---
tab_mkt, tab_tool, tab_scan, tab_chat, tab_log = st.tabs([
    "🌐 地合い判定", 
    "🛠 逆張り分析ツール", 
    "📡 全株スキャン", 
    "🧠 AI脳内", 
    "📈 売買ログ"
])

# ==========================================
# 1. 🌐 地合い判定
# ==========================================
with tab_mkt:
    st.header("リアルタイム地合い判定エンジン")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("日経平均", st.session_state.market_data["nikkei"], st.session_state.market_data["nikkei_chg"])
    col2.metric("東証値下がり銘柄数", st.session_state.market_data["down_stocks"], "東証全体")
    col3.metric("ドル円", st.session_state.market_data["usdjpy"], st.session_state.market_data["usdjpy_chg"])

    st.markdown("---")
    sc_col1, sc_col2 = st.columns([1, 2])
    with sc_col1:
        st.subheader("BNF地合いスコア")
        st.title(f"{st.session_state.market_data['score']} / 100")
        st.caption(f"ステータス: {st.session_state.market_data['status']}")
    
    with sc_col2:
        st.subheader("BNF相関コメント")
        st.info(st.session_state.market_data["comment"])

    if st.button("🚀 AIで今日の地合いをリアルタイム同期"):
        if not api_key:
            st.error("サイドバーでAPIキーを入力してください。")
        else:
            with st.spinner("最新市場データをAI解析中..."):
                try:
                    raw = call_gemini(
                        api_key,
                        "今日の日本株市場（日経平均、値下がり銘柄数、ドル円）を検索し、以下のJSON形式のみで答えてください。JSON以外のテキストは禁止です。\n"
                        '{"nikkei":"38500","nikkei_chg":"-1.2%","down_stocks":"1450","usdjpy":"152.3","usdjpy_chg":"+0.4%","score":35,"status":"パニック売り進行中","comment":"地合い崩壊時は通常より深い乖離（-20%〜）を引き付けてエントリー判断を行う。"}',
                        use_search=True
                    )
                    clean_json = raw[raw.find("{"):raw.rfind("}")+1]
                    data = json.loads(clean_json)
                    st.session_state.market_data = data
                    st.success("地合いデータを同期しました！")
                    st.rerun()
                except Exception as e:
                    st.error(f"同期エラー: {e}")

# ==========================================
# 2. 🛠 逆張り分析ツール
# ==========================================
with tab_tool:
    sub_tab1, sub_tab2, sub_tab3 = st.tabs(["単発計算・ターゲット", "個別監視リスト", "ナンピンシミュレータ"])
    
    # ── 単発計算 ──
    with sub_tab1:
        st.subheader("銘柄逆張り分析")
        c1, c2 = st.columns(2)
        code = c1.text_input("銘柄コード（例: 6920）", value="6920")
        
        # セクター自動判定
        sector = "中小型・新興グロース"
        threshold_text = "目安: -20%〜-30%"
        req_kairi = -20
        if code.startswith(('6', '8')):
            sector = "大型株・ハイテク"
            threshold_text = "目安: -10%〜-15%"
            req_kairi = -10
        elif code.startswith(('9', '1')):
            sector = "ディフェンシブ (薬品・食品等)"
            threshold_text = "目安: -7%〜-10%"
            req_kairi = -7

        c2.text_input("自動判定セクター", value=sector, disabled=True)

        p1, p2 = st.columns(2)
        cp = p1.number_input("現在値（円）", value=21050.0, step=10.0)
        ma = p2.number_input("25日移動平均線（円）", value=23100.0, step=10.0)

        if cp > 0 and ma > 0:
            kairi = ((cp - ma) / ma) * 100
            qty = 1 if is_mini else 100
            capital = cp * qty

            st.markdown("---")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("必要資金", f"{int(capital):,} 円")
            m2.metric("25日線 乖離率", f"{kairi:.2f} %")
            m3.metric("BNF基準値", threshold_text)
            
            is_buy = kairi <= req_kairi
            m4.metric("判定", "🔥 逆張り買候補" if is_buy else "👁 監視ゾーン")

            st.subheader("🎯 利確 & 損切りターゲット計算")
            sl1, sl2 = st.columns(2)
            stop_pct = sl1.slider("損切り幅 (%)", 1.0, 15.0, 3.0, 0.5)
            profit_pct = sl2.slider("カスタム利確幅 (%)", 1.0, 30.0, 5.0, 0.5)

            stop_price = cp * (1 - stop_pct / 100)
            custom_profit_price = cp * (1 + profit_pct / 100)
            rrr = ((ma - cp) / (cp - stop_price)) if (cp - stop_price) > 0 else 0

            t1, t2, t3, t4 = st.columns(4)
            t1.metric("🎯 利確①(MA25回帰)", f"{int(ma):,} 円")
            t2.metric("🎯 利確②(カスタム)", f"{int(custom_profit_price):,} 円")
            t3.metric("🔪 損切りライン", f"{int(stop_price):,} 円")
            t4.metric("⚖️ RRR (MA25基準)", f"{rrr:.2f}")

            b1, b2 = st.columns(2)
            if b1.button("💾 ログに保存"):
                st.session_state.logs.append({
                    "コード": code, "現在値": cp, "乖離率": f"{kairi:.2f}%",
                    "判定": "買い候補" if is_buy else "監視", "日時": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                })
                st.success("ログへ追加しました。")

            if b2.button("🧠 AI詳細評価を実行"):
                if not api_key:
                    st.error("APIキーを入力してください。")
                else:
                    with st.spinner("AI詳細分析中..."):
                        res = call_gemini(
                            api_key,
                            f"銘柄コード: {code}, セクター: {sector}, 現在値: {cp}円, 25日線: {ma}円, 乖離率: {kairi:.2f}%\n"
                            "この銘柄のリアルタイムの出来高・地合い相関・同一セクター内での過剰売られ状態を検索・分析し、BNF判定を行ってください。",
                            use_search=True
                        )
                        st.markdown(res)

    # ── 監視リスト ──
    with sub_tab2:
        st.subheader("個別監視リスト")
        wc1, wc2, wc3 = st.columns([1, 2, 1])
        w_code = wc1.text_input("コード", key="w_code")
        w_name = wc2.text_input("銘柄名", key="w_name")
        if wc3.button("追加") and w_code:
            st.session_state.watchlist.append({"コード": w_code, "銘柄名": w_name or f"銘柄{w_code}"})
            st.rerun()

        if st.session_state.watchlist:
            st.table(pd.DataFrame(st.session_state.watchlist))
            if st.button("監視リストをクリア"):
                st.session_state.watchlist = []
                st.rerun()

    # ── ナンピン ──
    with sub_tab3:
        st.subheader("含み損益 & ナンピンシミュレータ")
        np1, np2 = st.columns(2)
        b_price = np1.number_input("保有単価（円）", value=5000.0)
        b_qty = np2.number_input("保有株数", value=100.0)
        c_price = np1.number_input("現在株価（円）", value=4500.0)
        add_qty = np2.number_input("ナンピン追加株数", value=100.0)

        if b_price and b_qty and c_price:
            current_diff = (c_price - b_price) * b_qty
            st.write(f"現在の含み損益: **{int(current_diff):,} 円**")

            if add_qty > 0:
                new_qty = b_qty + add_qty
                new_avg = ((b_price * b_qty) + (c_price * add_qty)) / new_qty
                st.info(f"ナンピン後 平均単価: **{int(new_avg):,} 円** （保有総数: {int(new_qty)} 株）")

# ==========================================
# 3. 📡 全株スキャン (必ず10銘柄出力)
# ==========================================
with tab_scan:
    st.header("BNF式 全株スキャンエンジン")
    st.caption("東証全銘柄の最新乖離率データから、BNFロジックに合致する10銘柄を直接抽出・スコアリングします。")

    if st.button("📡 10銘柄AIリアルタイムスキャンを実行"):
        if not api_key:
            st.error("サイドバーでAPIキーを入力してください。")
        else:
            with st.spinner("東証最新データをWEB検索し、BNF条件に合う10銘柄を選定中..."):
                try:
                    prompt = """
【厳格指示】
Web検索を使用し、「東証 25日移動平均線 マイナス乖離率」の最新情報を参照して、現在下落している注目銘柄を【必ず10銘柄】抽出してください。
ツールの紹介や「特定銘柄の推奨はできません」などの解説・言い訳文は一切排除し、直接以下のフォーマットで10銘柄すべてを出力してください。

■ [銘柄コード] 銘柄名（25日乖離率: XX.X%）
・総合判定: [S / A / B / C]
・分析理由: セクター特性と地合い相関
・売買戦略: 反発狙い目と損切りライン
"""
                    res = call_gemini(api_key, prompt, use_search=True)
                    st.markdown(res)
                except Exception as e:
                    st.error(f"スキャンエラー: {e}")

# ==========================================
# 4. 🧠 AI脳内 (チャット)
# ==========================================
with tab_chat:
    st.header("BNF AI思考エンジンとの対話")

    col_t1, col_t2, col_t3 = st.columns(3)
    if col_t1.button("地合い＆セクター診断"):
        st.session_state.chat_prompt = "今日の地合い判定と買い候補のセクターを教えてください。"
    if col_t2.button("大型株-12%乖離検証"):
        st.session_state.chat_prompt = "大型半導体株が25日線から-12%乖離しました。BNF基準で買えますか？"
    if col_t3.button("パニック売り＆損切り"):
        st.session_state.chat_prompt = "パニック売り（投げ売り）の発生を見極める出来高の基準と、撤退の損切りルールを教えてください。"

    user_input = st.text_input("質問・相談を入力してください", value=st.session_state.get("chat_prompt", ""))

    if st.button("送信") and user_input:
        if not api_key:
            st.error("APIキーを入力してください。")
        else:
            st.session_state.chat_history.append({"role": "user", "text": user_input})
            with st.spinner("BNFロジックで思考中..."):
                ans = call_gemini(api_key, user_input, use_search=True)
                st.session_state.chat_history.append({"role": "bnf", "text": ans})
            st.session_state.chat_prompt = ""

    st.markdown("---")
    for msg in reversed(st.session_state.chat_history):
        if msg["role"] == "user":
            st.markdown(f"**🗣 あなた:** {msg['text']}")
        else:
            st.success(f"**⚡ BNF AI:**\n\n{msg['text']}")

# ==========================================
# 5. 📈 売買ログ
# ==========================================
with tab_log:
    st.header("売買・分析ログ一覧")
    if st.session_state.logs:
        df_logs = pd.DataFrame(st.session_state.logs)
        st.dataframe(df_logs, use_container_width=True)

        csv = df_logs.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📄 CSVファイルで出力",
            data=csv,
            file_name="bnf_trade_logs.csv",
            mime="text/csv"
        )
        if st.button("ログを全消去"):
            st.session_state.logs = []
            st.rerun()
    else:
        st.info("保存されたログはありません。")
