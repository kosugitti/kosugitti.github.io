# WORKLOG

## 2026-04-01（続き）
- タイトルを「Kosugitti Portal」に変更
- CLAUDE.md にユーザ操作サポート手順を追記

## 2026-04-01
- kosugitti.github.io リポジトリ新規作成（kosugitti10 の後継）
- Quarto Website として構築（テーマ: cosmo, lang: ja, docs/デプロイ）
- kosugitti10 のコンテンツ移行: index, notes, support, yuep
- works.qmd を gyouseki.tex からパーサー（parse_gyouseki.py）で自動生成（237件）
- ナビバーにスライドリンク（GitHub Slides / SpeakerDeck）追加
- kosugitti10 にリダイレクトを設置
- gh-pages ブランチの残骸を削除
- CLAUDE.md にユーザ操作サポート手順を追記

## 2026-07-30 notes にソフトウェア公開サイトを追加
- notes.qmd の Rパッケージ節に `tikzomr`（解説サイト https://kosugitti.github.io/tikz-omr/ ＋GitHub）を追加
- 「BibLaTeXスタイルファイル」節を「文献引用スタイル」節に改称し，`jpa-csl-zotero`（Zotero/CSL用）を新規追加。biblatex-jpa2 は元から掲載済み，旧 jecon-jpa は「旧BibTeX版」として末尾へ整理
- quarto render → commit dc2539f → push 済み
- 注記: このセッション中，Bash/Read/Edit のツール出力表示が文字化けする現象が続いた（実ファイルは無事）。最初の WORKLOG 追記は表示化けで成功と誤認し実際は失敗していたため，実内容を再確認して再追記した

## 2026-08-22 git が無応答になっていた件を解消

- `git show -s HEAD` も `git status` も **3分待っても返らない**状態だった。エラーは出ず，ただ止まる
- 原因は**作業ツリーの Dropbox オンライン専用ファイル**。git がそれを読もうとして
  ダウンロード待ちに入っていた。**1ファイルあたり実測2秒**かかるので数十件で数分固まる
- 該当ファイル（`.nojekyll`・`notes/*.html`・`notes/Reigen.pdf`・`docs/site_libs/*` など15件）を
  `cat > /dev/null` で引き落としたところ **`show` 1秒・`status` 0秒**に回復
- 切り分けの目印: `git rev-parse HEAD`（index を読むだけ）は即返るのに，
  オブジェクトや作業ツリーを読むコマンドだけが固まる。この非対称が出たらリポジトリ破損ではない
- **判定式に注意**: `st_blocks==0` だけで未実体化を数えると**サイズ0の空ファイルを全部拾う**。
  必ず `st_blocks==0 && st_size>0` で数える（この件で一度 385件と過大報告した）
- 状態は健全だった。HEAD `fb067a0` はリモートと完全一致，作業ツリーもクリーン
- 再発する（Dropbox が容量節約で再びオンライン専用に戻すため）。恒久策は Dropbox 設定で
  `Dropbox/Git` を「このデバイスに常に保持」にすること（GUI 操作）
