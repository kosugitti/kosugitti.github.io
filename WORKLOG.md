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
