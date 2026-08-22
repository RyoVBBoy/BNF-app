CSS = """
<style>
/* ... 前回の基本CSS ... */

/* メインコンテンツが下部ナビと被らないようにパディングを追加 */
section.main > div {
  padding-bottom: 90px !important;
}

/* --- Twitter風 ボトムナビゲーションバー (st.radioのカスタマイズ) --- */
div[data-testid="stRadio"] {
  position: fixed !important;
  bottom: 0 !important;
  left: 0 !important;
  right: 0 !important;
  z-index: 99999 !important;
  background: rgba(0, 0, 0, 0.92) !important;
  backdrop-filter: blur(12px) !important;
  border-top: 1px solid var(--bdr) !important;
  padding: 6px 0 10px 0 !important;
  margin: 0 !important;
}

/* ラジオボタンのコンテナを横並び均等配置 */
div[data-testid="stRadio"] > div[role="radiogroup"] {
  display: flex !important;
  justify-content: space-around !important;
  align-items: center !important;
  max-width: 720px !important;
  margin: 0 auto !important;
  gap: 0 !important;
}

/* ラジオボタンのデフォルトの丸を隠す */
div[data-testid="stRadio"] label {
  background: transparent !important;
  border: none !important;
  padding: 6px 0 !important;
  margin: 0 !important;
  flex: 1 !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer !important;
  color: var(--muted) !important;
}

/* ラジオボタンの丸（input）を非表示化 */
div[data-testid="stRadio"] label input {
  display: none !important;
}
div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {
  font-size: 0.7rem !important;
  font-weight: 700 !important;
  margin: 0 !important;
  text-align: center !important;
  line-height: 1.2 !important;
}

/* 選択されたアクティブタブ（Twitter紫アクセント） */
div[data-testid="stRadio"] label:has(input:checked) {
  color: var(--acc) !important;
}
div[data-testid="stRadio"] label:has(input:checked) p {
  color: var(--acc) !important;
}
</style>
"""
