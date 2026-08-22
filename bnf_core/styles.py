"""
styles.py
---------
BNF PREMIUM — スタイル定義（リンク・アイコン強制定着版）
"""

CSS = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
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
}

.stApp {
  background-color: var(--black) !important;
  color: var(--text) !important;
}

section.main > div {
  max-width: 600px !important;
  margin: 0 auto !important;
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
   固定ボトムナビ（青字・下線の完全打ち消し）
   ══════════════════════════════════════════════════ */
.bnf-bottom-nav {
  position: fixed !important;
  bottom: 0 !important;
  left: 0 !important;
  right: 0 !important;
  z-index: 999999 !important;
  background-color: #000000 !important;
  border-top: 1px solid #23272C !important;
  padding: 10px 0 16px 0 !important;
  display: flex !important;
  justify-content: space-around !important;
  align-items: center !important;
  max-width: 600px !important;
  margin: 0 auto !important;
}

a.bnf-nav-item, 
a.bnf-nav-item:link, 
a.bnf-nav-item:visited, 
a.bnf-nav-item:hover, 
a.bnf-nav-item:active {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  text-decoration: none !important;
  color: #71767B !important;
  flex: 1 !important;
  border: none !important;
  outline: none !important;
}

a.bnf-nav-item i {
  font-size: 1.3rem !important;
  margin-bottom: 3px !important;
  display: block !important;
}

a.bnf-nav-item span {
  font-size: 0.65rem !important;
  font-weight: 800 !important;
  display: block !important;
  line-height: 1 !important;
}

/* 選択中のタブ（ネオンパープル） */
a.bnf-nav-item.active, 
a.bnf-nav-item.active:link, 
a.bnf-nav-item.active:visited {
  color: #d500f9 !important;
}

a.bnf-nav-item.active i {
  filter: drop-shadow(0px 0px 8px rgba(213, 0, 249, 0.9)) !important;
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
