import http.server
import socketserver
import threading
import webbrowser
import sys

# HTML/CSS/JavaScript をまとめたアプリデータ
HTML_CONTENT = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BNF CORE AUTOMATION PREMIUM</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
:root {
  --black:#000; --s1:#16181C; --s2:#1C1F23; --bdr:#2F3336;
  --text:#EFF3F4; --muted:#71767B;
  --acc:#d500f9; --acc-dim:rgba(213,0,249,.10);
  --blue:#1D9BF0; --green:#00BA7C; --orange:#FF7527; --red:#F4212E;
  --pill:9999px;
}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--black);color:var(--text);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  display:flex;flex-direction:column;height:100dvh;overflow:hidden;}

header{height:53px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;
  background:rgba(0,0,0,.85);backdrop-filter:blur(12px);
  border-bottom:1px solid var(--bdr);position:sticky;top:0;z-index:100;}
.hdr-title{font-size:1.05rem;font-weight:800;letter-spacing:.12em;color:var(--acc);}
.live-badge{display:flex;align-items:center;gap:5px;font-size:.72rem;font-weight:700;
  color:var(--green);background:rgba(0,186,124,.1);padding:4px 10px;border-radius:var(--pill);}
.live-dot{width:7px;height:7px;background:var(--green);border-radius:50%;animation:blink 1.5s infinite;}
@keyframes blink{0%,100%{opacity:1;}50%{opacity:.3;}}

.content-area{flex:1;overflow-y:auto;padding-bottom:68px;-webkit-overflow-scrolling:touch;}
.screen{display:none;}.screen.active{display:block;}

.cell{padding:14px 16px;border-bottom:1px solid var(--bdr);}
.cell-lbl{font-size:.78rem;color:var(--muted);margin-bottom:6px;font-weight:600;}

input[type="number"],input[type="text"],input[type="password"],select{
  width:100%;padding:10px 14px;background:var(--s2);border:1px solid var(--bdr);
  border-radius:10px;color:var(--text);font-size:1rem;font-family:inherit;
  outline:none;-webkit-appearance:none;transition:border-color .15s;}
input:focus,select:focus{border-color:var(--acc);}
input[readonly]{background:var(--s1);color:var(--muted);}

.btn-pill{display:inline-flex;align-items:center;justify-content:center;
  gap:7px;padding:9px 20px;border:none;border-radius:var(--pill);
  font-weight:700;font-size:.9rem;cursor:pointer;width:100%;
  transition:opacity .15s;font-family:inherit;}
.btn-pill:active{opacity:.75;}
.btn-acc{background:var(--acc);color:#fff;}
.btn-blue{background:var(--blue);color:#fff;}
.btn-green{background:var(--green);color:#fff;}
.btn-outline{background:transparent;border:1px solid var(--bdr);color:var(--text);}
.btn-save{background:linear-gradient(90deg,var(--blue),var(--acc));color:#fff;}

.mkt-bar{display:flex;border-bottom:1px solid var(--bdr);background:var(--s1);}
.mkt-cell{flex:1;padding:10px 12px;text-align:center;border-right:1px solid var(--bdr);}
.mkt-cell:last-child{border-right:none;}
.mkt-lbl{font-size:.65rem;color:var(--muted);font-weight:600;letter-spacing:.03em;}
.mkt-val{font-size:.92rem;font-weight:800;font-family:'Courier New',monospace;margin-top:2px;}
.mkt-chg{font-size:.7rem;font-weight:700;margin-top:1px;}
.up{color:var(--red);}.dn{color:var(--blue);}

.score-hero{display:flex;flex-direction:column;align-items:center;
  padding:20px 16px 16px;border-bottom:1px solid var(--bdr);background:var(--s1);}
.score-big{font-size:3.8rem;font-weight:900;font-family:'Courier New',monospace;line-height:1;}
.score-suffix{font-size:1.4rem;font-weight:700;color:var(--muted);margin-left:3px;}
.score-label{font-size:.9rem;font-weight:700;margin-top:6px;}

.countdown-bar{padding:12px 16px;border-bottom:1px solid var(--bdr);background:var(--s2);}
.cd-label{font-size:.75rem;color:var(--muted);margin-bottom:6px;font-weight:600;}
.cd-track{height:8px;background:var(--bdr);border-radius:var(--pill);overflow:hidden;}
.cd-fill{height:100%;background:var(--green);border-radius:var(--pill);transition:width .5s;}
.cd-nums{display:flex;justify-content:space-between;margin-top:5px;font-size:.75rem;}

.bnf-quote{display:flex;gap:10px;padding:14px 16px;border-bottom:1px solid var(--bdr);background:var(--s1);}
.bnf-avatar{width:36px;height:36px;border-radius:50%;flex-shrink:0;background:var(--acc-dim);
  border:2px solid var(--acc);display:flex;align-items:center;justify-content:center;
  font-size:.7rem;font-weight:900;color:var(--acc);}
.bnf-qname{font-size:.85rem;font-weight:700;}
.bnf-qhandle{font-size:.78rem;color:var(--muted);margin-left:4px;}
.bnf-qtext{font-size:.9rem;margin-top:3px;line-height:1.5;font-style:italic;}

.ai-report-card{background:rgba(213,0,249,.04);border:1px dashed var(--acc);
  border-radius:12px;margin:12px 16px;padding:14px;}
.ai-report-hdr{display:flex;justify-content:space-between;align-items:center;
  margin-bottom:8px;font-size:.85rem;font-weight:800;color:var(--acc);}
.ai-report-body{font-size:.86rem;line-height:1.6;color:var(--text);white-space:pre-wrap;}

.signal-card{background:rgba(29,155,240,.04);border:1px solid var(--bdr);
  border-radius:12px;margin:12px 16px;padding:12px 14px;}
.sig-hdr{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;}
.sig-title{font-size:.85rem;font-weight:800;color:var(--blue);display:flex;align-items:center;gap:6px;}
.sig-time{font-size:.7rem;color:var(--muted);font-family:'Courier New',monospace;}
.sig-body{font-size:.85rem;line-height:1.5;color:var(--text);}

.tool-header{padding:14px 16px 0;background:var(--s1);}
.tool-title{font-size:1.1rem;font-weight:800;}
.mode-toggle{display:flex;background:var(--s2);border:1px solid var(--bdr);
  border-radius:var(--pill);overflow:hidden;width:160px;}
.mode-btn{flex:1;padding:5px 0;text-align:center;font-size:.72rem;font-weight:700;
  color:var(--muted);cursor:pointer;border:none;background:transparent;font-family:inherit;}
.mode-btn.active{background:var(--acc);color:#fff;}
.inner-tabs{display:flex;border-bottom:1px solid var(--bdr);background:var(--s1);margin-top:10px;}
.inner-tab{flex:1;padding:11px 0;text-align:center;font-size:.78rem;font-weight:700;
  color:var(--muted);cursor:pointer;border-bottom:2px solid transparent;}
.inner-tab.active{color:var(--acc);border-bottom-color:var(--acc);}
.inner-pane{display:none;}.inner-pane.active{display:block;}

.result-row{display:flex;justify-content:space-between;align-items:center;
  padding:13px 16px;border-bottom:1px solid var(--bdr);}
.res-val{font-size:1.15rem;font-weight:800;font-family:'Courier New',monospace;}

.key-section{padding:12px 16px;border-bottom:1px solid var(--bdr);background:var(--s1);}
.key-row{display:flex;gap:8px;margin-bottom:6px;}
.key-eye-btn{background:var(--s2);border:1px solid var(--bdr);color:var(--muted);
  border-radius:10px;padding:0 14px;cursor:pointer;font-size:1rem;}
.chat-wrap{display:flex;flex-direction:column;height:calc(100dvh - 53px - 68px);}
.chat-feed{flex:1;overflow-y:auto;padding:12px 16px;display:flex;flex-direction:column;gap:10px;}
.bubble{max-width:85%;padding:10px 14px;border-radius:18px;font-size:.9rem;line-height:1.5;word-break:break-word;}
.bubble.bnf{background:var(--s2);color:var(--text);align-self:flex-start;
  border-bottom-left-radius:4px;border:1px solid var(--bdr);}
.bubble.user{background:var(--acc);color:#fff;align-self:flex-end;border-bottom-right-radius:4px;}
.chat-footer{border-top:1px solid var(--bdr);padding:10px 12px;
  display:flex;align-items:center;gap:10px;background:var(--black);}
.chat-footer input{flex:1;border-radius:var(--pill);padding:10px 16px;font-size:.9rem;}
.send-btn{border:none;background:none;color:var(--acc);font-size:1.2rem;cursor:pointer;padding:6px;}
.tmpl-btn{background:var(--s2);border:1px solid var(--bdr);border-radius:var(--pill);
  color:var(--text);padding:7px 14px;font-size:.78rem;font-weight:600;cursor:pointer;font-family:inherit;white-space:nowrap;}

.nav-bar{position:fixed;bottom:0;left:0;right:0;height:68px;
  background:rgba(0,0,0,.92);backdrop-filter:blur(12px);
  border-top:1px solid var(--bdr);display:flex;z-index:200;}
.nav-item{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;
  gap:4px;color:var(--muted);cursor:pointer;}
.nav-item i{font-size:1.3rem;}
.nav-item span{font-size:.65rem;font-weight:700;display:none;}
.nav-item.active{color:var(--acc);}
.nav-item.active span{display:block;}
.status-line{text-align:center;font-size:.8rem;font-weight:700;padding:4px 16px 8px;color:var(--muted);min-height:26px;}
</style>
<script type="module">
  import {GoogleGenerativeAI} from "https://esm.run/@google/generative-ai";
  window.GoogleGenerativeAI = GoogleGenerativeAI;
</script>
</head>
<body>

<header>
  <div class="hdr-title">BNF PREMIUM</div>
  <div class="live-badge"><div class="live-dot"></div>AI LIVE</div>
</header>

<div class="content-area">

<!-- ══ 地合い ══ -->
<div id="screen-market" class="screen active">
  <div class="mkt-bar">
    <div class="mkt-cell">
      <div class="mkt-lbl">日経平均</div>
      <div class="mkt-val" id="mkt-nikkei">--</div>
      <div class="mkt-chg" id="mkt-nikkei-chg">--</div>
    </div>
    <div class="mkt-cell">
      <div class="mkt-lbl">値下がり銘柄</div>
      <div class="mkt-val" id="mkt-down">--</div>
      <div class="mkt-chg" id="mkt-down-chg" style="color:var(--muted);">東証全体</div>
    </div>
    <div class="mkt-cell">
      <div class="mkt-lbl">ドル円</div>
      <div class="mkt-val" id="mkt-usdjpy">--</div>
      <div class="mkt-chg" id="mkt-usdjpy-chg">--</div>
    </div>
  </div>

  <div class="score-hero">
    <div>
      <span class="score-big" id="live-score">--</span>
      <span class="score-suffix">/100</span>
    </div>
    <div class="score-label" id="live-status">AIで同期してください</div>
  </div>

  <div class="countdown-bar">
    <div class="cd-label">BNF臨界点まで（東証値下がり銘柄 / 1,400銘柄）</div>
    <div class="cd-track"><div class="cd-fill" id="cd-fill" style="width:0%"></div></div>
    <div class="cd-nums">
      <span id="cd-current" style="color:var(--muted);">-- 銘柄が値下がり中</span>
      <span id="cd-remain" style="color:var(--green);">あと -- 銘柄</span>
    </div>
  </div>

  <div class="bnf-quote">
    <div class="bnf-avatar">BNF</div>
    <div>
      <span class="bnf-qname">B.N.F</span>
      <span class="bnf-qhandle">@market_shadow</span>
      <div class="bnf-qtext" id="bnf-comment">「AIで同期すると状況コメントが出ます」</div>
    </div>
  </div>

  <div class="cell">
    <button class="btn-pill btn-blue" onclick="syncMarketWithAI()" id="market-sync-btn">
      <i class="fa-solid fa-bolt"></i> AIで今日の地合いをリアルタイム同期
    </button>
    <div class="status-line" id="market-sync-status"></div>
  </div>

  <div class="ai-report-card">
    <div class="ai-report-hdr">
      <span><i class="fa-solid fa-brain"></i> AI相場観レポート</span>
      <span id="ai-report-time" style="font-size:.7rem;color:var(--muted);">未更新</span>
    </div>
    <div class="ai-report-body" id="ai-report-text">「AI脳内」タブでAPIキーを設定すると、地合い同期時にリアルタイムのAI相場観レポートが生成されます。</div>
  </div>
</div>

<!-- ══ ツール ══ -->
<div id="screen-tools" class="screen">
  <div class="tool-header">
    <div style="display:flex;justify-content:space-between;align-items:center;">
      <div class="tool-title">逆張り分析ツール</div>
    </div>
  </div>
  <div class="inner-tabs">
    <div class="inner-tab active" onclick="switchInner('calc',this)">単発計算</div>
  </div>
  <div id="pane-calc" class="inner-pane active">
    <div class="cell">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
        <div><div class="cell-lbl">現在値（円）</div><input type="number" id="current-price" oninput="calculateMetrics()"></div>
        <div><div class="cell-lbl">25日移動平均線</div><input type="number" id="ma-value" oninput="calculateMetrics()"></div>
      </div>
    </div>
    <div class="result-row"><span>25日線 乖離率</span><span class="res-val" id="res-kairi">-- %</span></div>
  </div>
</div>

<!-- ══ AI脳内 ══ -->
<div id="screen-brain" class="screen">
  <div class="chat-wrap">
    <div class="key-section">
      <div class="key-row">
        <input type="password" id="api-key-input" placeholder="Gemini APIキーを入力">
        <button class="key-eye-btn" onclick="toggleKey()"><i class="fa-solid fa-eye" id="key-icon"></i></button>
      </div>
      <button class="btn-pill btn-acc" onclick="saveApiKey()" style="margin-top:8px;">接続する</button>
      <div id="api-key-status" style="font-size:.75rem;margin-top:6px;color:var(--muted);">未設定</div>
    </div>
    <div class="chat-feed" id="chat-box">
      <div class="bubble bnf">何か地合いや逆張り戦略についてご質問はありますか？</div>
    </div>
    <div class="chat-footer">
      <input type="text" id="chat-input" placeholder="メッセージを入力..." onkeypress="if(event.key==='Enter')sendChat()">
      <button class="send-btn" onclick="sendChat()"><i class="fa-solid fa-paper-plane"></i></button>
    </div>
  </div>
</div>

</div>

<div class="nav-bar">
  <div class="nav-item active" onclick="switchScreen('market',this)"><i class="fa-solid fa-earth-asia"></i><span>地合い</span></div>
  <div class="nav-item" onclick="switchScreen('tools',this)"><i class="fa-solid fa-screwdriver-wrench"></i><span>ツール</span></div>
  <div class="nav-item" onclick="switchScreen('brain',this)"><i class="fa-solid fa-brain"></i><span>AI脳内</span></div>
</div>

<script>
let geminiApiKey = localStorage.getItem("bnf_gemini_key") || "";

function switchScreen(id,el){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));
  document.getElementById('screen-'+id).classList.add('active');
  el.classList.add('active');
}

function switchInner(id,el){
  document.querySelectorAll('.inner-tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.inner-pane').forEach(p=>p.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('pane-'+id).classList.add('active');
}

function toggleKey(){
  const i=document.getElementById('api-key-input');
  i.type=i.type==='password'?'text':'password';
}

function saveApiKey(){
  const k=document.getElementById('api-key-input').value.trim();
  if(!k){alert("APIキーを入力してください。");return;}
  localStorage.setItem("bnf_gemini_key",k);
  geminiApiKey=k;
  document.getElementById('api-key-status').innerText="接続済み ✅";
  document.getElementById('api-key-status').style.color="var(--green)";
}

async function callGemini(prompt,useSearch=false){
  if(!geminiApiKey)throw new Error("APIキー未設定");
  const genAI=new window.GoogleGenerativeAI(geminiApiKey);
  const tools=useSearch?[{googleSearch:{}}]:undefined;
  const model=genAI.getGenerativeModel({model:"gemini-2.5-flash",...(tools&&{tools})});
  const result=await model.generateContent(prompt);
  return result.response.candidates[0].content.parts
    .filter(p=>p.text).map(p=>p.text).join("");
}

async function syncMarketWithAI(){
  if(!geminiApiKey){alert("AI脳内タブでAPIキーを設定してください。");return;}
  const btn=document.getElementById('market-sync-btn');
  const st=document.getElementById('market-sync-status');
  btn.disabled=true;btn.innerHTML='<i class="fa-solid fa-spinner fa-spin"></i> 同期中...';
  st.innerText="日本市場の最新データを検索中...";
  try{
    const raw=await callGemini(
      `今日の日本株市場を検索し、以下のJSONのみで出力してください。説明不要。
{"nikkei":日経平均数値,"nikkei_chg":前日比数値,"usdjpy":ドル円数値,"usdjpy_chg":前日比数値,
 "down_stocks":値下がり銘柄数,"score":0〜100のスコア,"status":"状態一言","comment":"BNFスタイルの短文コメント"}`,
      true
    );
    const m=raw.match(/\{[\\s\\S]*?\}/);
    if(!m)throw new Error("JSON取得失敗");
    const d=JSON.parse(m[0]);

    document.getElementById('mkt-nikkei').innerText=d.nikkei;
    document.getElementById('mkt-nikkei-chg').innerText=d.nikkei_chg + "%";
    document.getElementById('mkt-down').innerText=d.down_stocks;
    document.getElementById('mkt-usdjpy').innerText=d.usdjpy;
    document.getElementById('mkt-usdjpy-chg').innerText=d.usdjpy_chg + "%";
    document.getElementById('live-score').innerText=d.score;
    document.getElementById('live-status').innerText=d.status;
    document.getElementById('bnf-comment').innerText=d.comment;
    document.getElementById('ai-report-text').innerText=d.comment;
    document.getElementById('ai-report-time').innerText=new Date().toLocaleTimeString();

    st.innerText="同期完了";st.style.color="var(--green)";
  }catch(e){
    st.innerText="エラー: "+e.message;st.style.color="var(--red)";
  }finally{
    btn.disabled=false;btn.innerHTML='<i class="fa-solid fa-bolt"></i> AIで今日の地合いをリアルタイム同期';
  }
}

function calculateMetrics(){
  const cp=parseFloat(document.getElementById('current-price').value);
  const ma=parseFloat(document.getElementById('ma-value').value);
  if(cp && ma){
    const kairi=((cp-ma)/ma)*100;
    document.getElementById('res-kairi').innerText=kairi.toFixed(2)+" %";
  }
}

async function sendChat(){
  const input=document.getElementById('chat-input');
  const txt=input.value.trim();
  if(!txt)return;
  const box=document.getElementById('chat-box');
  box.innerHTML+=`<div class="bubble user">${txt}</div>`;
  input.value="";
  
  try{
    const ans=await callGemini("あなたはBNF（小手川隆）スタイルの投資アドバイザーです: "+txt);
    box.innerHTML+=`<div class="bubble bnf">${ans}</div>`;
  }catch(e){
    box.innerHTML+=`<div class="bubble bnf">エラー: ${e.message}</div>`;
  }
  box.scrollTop=box.scrollHeight;
}
</script>
</body>
</html>
"""

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode("utf-8"))

def start_server(port):
    with socketserver.TCPServer(("", port), CustomHandler) as httpd:
        print(f"BNF Core App Running at: http://localhost:{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    PORT = 8000
    # バックグラウンドでローカルサーバーを起動
    server_thread = threading.Thread(target=start_server, args=(PORT,), daemon=True)
    server_thread.start()
    
    # 自動的に既定のブラウザでアプリ画面を表示
    webbrowser.open(f"http://localhost:{PORT}")
    
    print("アプリを停止するには Ctrl+C を押してください。")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nアプリを終了しました。")
        sys.exit()