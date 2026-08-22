"""
browser_notify.py
------------------
アプリを開いている間、ブラウザのネイティブ通知(スマホならロック画面にも
出るWeb Push相当の挙動)を出すための小さなHTMLコンポーネント。
元のHTML版の「ブラウザ通知を許可する」ボタンと同じ Notification API を使う。
"""

import streamlit.components.v1 as components


def request_permission_button():
    components.html(
        """
        <button id="bnf-notif-btn" style="
            width:100%; padding:10px; border-radius:999px; font-weight:700;
            background:#1C1F23; color:#EFF3F4; border:1px solid #2F3336; cursor:pointer;">
            🔔 ブラウザ通知を許可する
        </button>
        <div id="bnf-notif-status" style="font-size:.75rem; color:#71767B; margin-top:6px; text-align:center;"></div>
        <script>
        const btn = document.getElementById('bnf-notif-btn');
        const status = document.getElementById('bnf-notif-status');
        if (!("Notification" in window)) {
            status.innerText = "このブラウザは通知に対応していません";
        } else if (Notification.permission === "granted") {
            status.innerText = "通知許可済み ✅";
        }
        btn.onclick = function() {
            Notification.requestPermission().then(function(perm) {
                status.innerText = perm === "granted" ? "通知許可済み ✅" : "通知が許可されませんでした";
            });
        };
        </script>
        """,
        height=80,
    )


def fire_notification(title: str, body: str):
    """条件に合致した銘柄が見つかったときにブラウザ通知を即座に発火する。"""
    safe_title = title.replace("`", "'")
    safe_body = body.replace("`", "'").replace("\n", "\\n")
    components.html(
        f"""
        <script>
        if ("Notification" in window && Notification.permission === "granted") {{
            new Notification(`{safe_title}`, {{ body: `{safe_body}` }});
        }}
        </script>
        """,
        height=0,
    )
