#!/usr/bin/env python3
"""
gyouseki.tex を解析して works.qmd を生成するスクリプト

入力: /Users/newton/Library/CloudStorage/Dropbox/公募資料/gyouseki.tex
出力: /Users/newton/Dropbox/Git/kosugitti.github.io/works.qmd
"""

import re
import os

# --- パス設定 ---
INPUT_PATH = os.path.expanduser(
    "~/Library/CloudStorage/Dropbox/公募資料/gyouseki.tex"
)
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "works.qmd")


def read_tex(path):
    """TeXファイルを読み込む"""
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()


def clean_latex(text):
    """LaTeXコマンドをMarkdown記法に変換する"""
    # \label{...} を除去
    text = re.sub(r"\\label\{[^}]*\}", "", text)

    # \underline{...} → 中身をそのまま
    text = re.sub(r"\\underline\{([^}]*)\}", r"\1", text)

    # {\bf ...} → **...** （スペースあり・なし両対応）
    text = re.sub(r"\{\\bf\s*([^}]*)\}", r"**\1**", text)

    # {\it ...} → *...* （スペースあり・なし両対応）
    text = re.sub(r"\{\\it\s*([^}]*)\}", r"*\1*", text)

    # \url{...} → Markdownリンク
    text = re.sub(r"\\url\{([^}]*)\}", r"[\1](\1)", text)

    # \& → &
    text = text.replace(r"\&", "&")

    # \LARGE, \bf（単独）, ~ など残存コマンドを除去
    text = re.sub(r"\\LARGE", "", text)
    text = re.sub(r"\\bf\b", "", text)
    text = re.sub(r"~", " ", text)

    # 残存する \コマンド{} は中身だけ残す（安全策）
    # ただし既に処理済みのものは再マッチしない
    # \section, \subsection は別途処理するのでここでは触らない

    # 先頭・末尾の空白を整理
    text = text.strip()

    return text


def parse_tex(lines):
    """TeXの行リストを解析して構造化データを返す"""
    sections = []
    current_section = None
    current_subsection = None
    items = []
    in_enumerate = False
    in_comment_block = False
    current_item_lines = []

    for line in lines:
        stripped = line.strip()

        # コメント行（行頭が%）はスキップ
        if stripped.startswith("%"):
            continue

        # \begin{document} より前はスキップ（プリアンブル）
        # → セクションが見つかるまではスキップする形で対応

        # \section{...} を検出
        section_match = re.match(r"\\section\{(.+?)\}", stripped)
        if section_match:
            # 前のセクション/サブセクションを保存
            if current_item_lines:
                items.append(" ".join(current_item_lines))
                current_item_lines = []
            if current_subsection and current_section:
                current_section["subsections"].append(
                    {"title": current_subsection, "items": items}
                )
                items = []
                current_subsection = None
            elif current_section:
                current_section["items"] = items
                items = []

            if current_section:
                sections.append(current_section)

            section_title = clean_latex(section_match.group(1))
            current_section = {
                "title": section_title,
                "items": [],
                "subsections": [],
            }
            current_subsection = None
            continue

        # \subsection{...} を検出
        subsection_match = re.match(r"\\subsection\{(.+?)\}", stripped)
        if subsection_match:
            # 前のサブセクション/アイテムを保存
            if current_item_lines:
                items.append(" ".join(current_item_lines))
                current_item_lines = []
            if current_subsection and current_section:
                current_section["subsections"].append(
                    {"title": current_subsection, "items": items}
                )
                items = []
            elif current_section and items:
                current_section["items"] = items
                items = []

            current_subsection = clean_latex(subsection_match.group(1))
            continue

        # enumerate環境の開始・終了
        if r"\begin{enumerate}" in stripped:
            in_enumerate = True
            continue
        if r"\end{enumerate}" in stripped:
            in_enumerate = False
            if current_item_lines:
                items.append(" ".join(current_item_lines))
                current_item_lines = []
            continue

        # \item を検出
        if in_enumerate and stripped.startswith(r"\item"):
            # 前のitemを保存
            if current_item_lines:
                items.append(" ".join(current_item_lines))
                current_item_lines = []
            # \item の後のテキストを取得
            item_text = stripped[len(r"\item") :].strip()
            if item_text:
                current_item_lines.append(item_text)
            continue

        # item の継続行（enumerate内でitemでもコマンドでもない行）
        if in_enumerate and stripped and current_item_lines is not None:
            current_item_lines.append(stripped)

    # 最後のセクションを保存
    if current_item_lines:
        items.append(" ".join(current_item_lines))
        current_item_lines = []
    if current_subsection and current_section:
        current_section["subsections"].append(
            {"title": current_subsection, "items": items}
        )
    elif current_section:
        current_section["items"] = items

    if current_section:
        sections.append(current_section)

    return sections


def generate_qmd(sections):
    """構造化データからworks.qmdの内容を生成する"""
    lines = []
    lines.append("---")
    lines.append('title: "業績一覧"')
    lines.append("---")
    lines.append("")

    for section in sections:
        lines.append(f"## {section['title']}")
        lines.append("")

        # 直接のアイテム
        for item in section["items"]:
            cleaned = clean_latex(item)
            if cleaned:
                lines.append(f"- {cleaned}")
        if section["items"]:
            lines.append("")

        # サブセクション
        for subsec in section["subsections"]:
            lines.append(f"### {subsec['title']}")
            lines.append("")
            for item in subsec["items"]:
                cleaned = clean_latex(item)
                if cleaned:
                    lines.append(f"- {cleaned}")
            lines.append("")

    return "\n".join(lines)


def main():
    # TeXファイルを読み込み
    lines = read_tex(INPUT_PATH)

    # 解析
    sections = parse_tex(lines)

    # QMDを生成
    qmd_content = generate_qmd(sections)

    # 出力
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(qmd_content)


if __name__ == "__main__":
    main()
