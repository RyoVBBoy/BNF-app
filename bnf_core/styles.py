"""
styles.py
---------
BNF PREMIUM — 純粋HTMLナビ & ネオンUIスタイル
"""

CSS = """
<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

:root {
  --black: #000000;
  --s1: #121417;
  --s2: #1A1D21;
  --bdr: #23272C;
  --text: #EFF3F4;
  --muted: #71767B;
  --acc: #d500f9;
  --blue: #1D9BF0;
  --green: #00BA7C;
  --red: #F4212E;
}

.stApp {
  background-color: var(--black) !important;
  color: var(--text) !important;
}

section.main > div {
  max-width: 600px;
  margin: 0 auto;
  padding: 0.5rem 1rem 120px 1rem !important;
}

/* ヘッダー */
.bnf-header {
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--bdr);
  margin-bottom: 16px;
}
.bnf-title {
  font-size: 1.2rem;
  font-weight: 900;
  letter-spacing: 0.05em;
  color: var(--acc);
}
.bnf-live-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.7rem;
  font-weight: 800;
  color: var(--green);
  background: rgba(0, 186, 124, 0.12);
  padding: 3px 8px;
  border-radius: 9999px;
}
.bnf-live-dot {
  width: 6px;
  height: 6px;
  background: var(--green);
  border-radius: 50%;
}

/* ══════════════════════════════════════════════════
   完全HTMLボトムナビゲーション (画像2完全再現)
   ══════════════════════════════════════════════════ */
.bnf-bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 999999;
  background-color: #000000;
  border-top: 1px solid var(--bdr);
  padding: 10px 0 16px 0;
  display: flex;
  justify-content: space-around;
  align-items: center;
  max-width: 600px;
  margin: 0 auto;
}

.bnf-nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-decoration: none !important;
  color: #444444 !important;
  flex: 1;
  transition: all 0.15s ease;
}

.bnf-nav-item i {
  font-size: 1.35rem;
  margin-bottom: 2px;
}

.bnf-nav-item span {
  font-size: 0.65rem;
  font-weight: 800;
  display: none;
}

/* 🟢 アクティブ（選択中）：ネオンパープル発光 & テキスト表示 */
.bnf-nav-item.active {
  color: var(--acc) !important;
}

.bnf-nav-item.active i {
  filter: drop-shadow(0px 0px 8px rgba(213, 0, 249, 0.9));
  transform: scale(1.05);
}

.bnf-nav-item.active span {
  display: block !important;
  color: var(--acc) !important;
}

/* 🟢 画像2準拠 青色丸ボタン */
.bnf-btn-blue {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  background-color: var(--blue);
  color: #ffffff !important;
  font-weight: 800;
  font-size: 0.95rem;
  padding: 12px 0;
  border-radius: 9999px;
  text-decoration: none !important;
  border: none;
  cursor: pointer;
  margin: 14px 0;
  box-shadow: 0px 4px 12px rgba(29, 155, 240, 0.3);
}

.bnf-btn-blue:active {
  opacity: 0.85;
}

/* カードスタイル */
.bnf-card {
  border: 1px solid var(--bdr);
  background: var(--s1);
  border-radius: 10px;
  padding: 14px;
  margin-bottom: 14px;
}

.bnf-card-purple-dash {
  border: 1px dashed var(--acc);
  background: var(--s1);
  border-radius: 10px;
  padding: 14px;
  margin-bottom: 14px;
}
</style>
"""
