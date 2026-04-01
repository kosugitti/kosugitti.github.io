# kosugitti.github.io プロジェクト

## 概要
- **公開URL**: https://kosugitti.github.io/
- **ローカル**: `~/Dropbox/Git/kosugitti.github.io/`
- **形式**: Quarto Website (GitHub Pages, docs/デプロイ)
- **用途**: 個人ポータル（自己紹介・業績・ノート・正誤表・YUEP・スライドリンク）

## 状態
- 初期構築完了、公開済み
- kosugitti10 の内容を移行済み、kosugitti10 はリダイレクト設置済み

## 構成
```
kosugitti.github.io/
├── _quarto.yml       # render: *.qmd のみ、output-dir: docs
├── index.qmd         # 自己紹介・略歴
├── works.qmd         # 業績一覧（gyouseki.tex から自動生成）
├── notes.qmd         # 研究ノート・パッケージ
├── support.qmd       # 正誤表
├── yuep.qmd          # YUEP読書会
├── parse_gyouseki.py # TeXパーサー
├── notes/            # PDF研究ノート（kosugitti10から移行）
├── items/            # 記事HTML（kosugitti10から移行）
├── support/          # 正誤表アセット
└── docs/             # Quarto出力（GitHub Pages配信）
```

---

## ユーザ操作サポート

### 「業績を更新した」「gyouseki.tex を書き換えた」と言われたら

1. パーサーで works.qmd を再生成:
```bash
cd ~/Dropbox/Git/kosugitti.github.io
python parse_gyouseki.py
```
2. ビルド & デプロイ:
```bash
quarto render
git add -A && git commit -m "業績一覧を更新" && git push
```

### 「サイトを更新して」「デプロイして」と言われたら

```bash
cd ~/Dropbox/Git/kosugitti.github.io
quarto render
git add -A && git commit -m "サイト更新" && git push
```

### 「研究ノートを追加したい」と言われたら

1. PDFを `notes/` に置く
2. `notes.qmd` にリンクを追記
3. 上記と同じビルド & デプロイ

### 「正誤表に追加したい」と言われたら

`support.qmd` に誤記情報を追記 → ビルド & デプロイ

### 「YUEPに新しい回を追加したい」と言われたら

`yuep.qmd` の活動記録リストに追記 → ビルド & デプロイ

---

## 注意
- Pages source は `/docs`（username.github.io リポジトリは `/` 配信が効かない場合があった）
- ルートにHTMLを置かない（docs/ に一本化）
- notes/ 内の .Rmd は render 対象外（render: "*.qmd" で制限済み）

## gyouseki.tex との連携
- ソース: `~/Dropbox/公募資料/gyouseki.tex`
- パーサー: `parse_gyouseki.py`（236件、9セクション対応）
- gyouseki.tex を更新したら parse → render → push の3ステップ

## 次
- 業績一覧のカテゴリ別件数表示
- notes.qmd のリンク先整理
