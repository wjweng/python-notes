#!/usr/bin/env python3
"""把章節的 README.md 轉成 Colab notebook。

Python 程式碼區塊變成可執行的 code cell，其餘內容維持 markdown。
notebooks/ 底下的檔案由本腳本產生，不要手動編輯。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "notebooks"

FENCE = re.compile(r"^```(\w*)\n(.*?)^```", re.S | re.M)


def cells(md: str) -> list[dict]:
    out, pos = [], 0

    def md_cell(text: str) -> None:
        if text.strip():
            out.append({"cell_type": "markdown", "metadata": {}, "source": text.strip().splitlines(True)})

    for m in FENCE.finditer(md):
        md_cell(md[pos:m.start()])
        lang, code = m.group(1), m.group(2)
        if lang == "python":
            out.append({"cell_type": "code", "execution_count": None, "metadata": {},
                        "outputs": [], "source": code.rstrip("\n").splitlines(True)})
        else:
            out.append({"cell_type": "markdown", "metadata": {},
                        "source": f"```{lang}\n{code}```".splitlines(True)})
        pos = m.end()
    md_cell(md[pos:])
    return out


def build(chapter: dict) -> Path:
    src = ROOT / "chapters" / chapter["dir"] / "README.md"
    nb = {
        "cells": cells(src.read_text(encoding="utf-8")),
        "metadata": {
            "colab": {"name": chapter["dir"], "provenance": []},
            "kernelspec": {"name": "python3", "display_name": "Python 3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4, "nbformat_minor": 0,
    }
    OUT.mkdir(exist_ok=True)
    dst = OUT / f"{chapter['dir']}.ipynb"
    dst.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    return dst


def load_chapters() -> list[dict]:
    """讀 chapters.json，把所屬單元的名稱與主題色併進每一章。"""
    data = json.loads((ROOT / "chapters.json").read_text(encoding="utf-8"))
    units = {u["id"]: u for u in data["units"]}
    out = []
    for ch in data["chapters"]:
        u = units[ch["unit"]]
        cn = "一二三四五六七八九十"[u["id"] - 1]
        out.append({**ch, "accent": u["accent"], "unit": f"單元{cn}・{u['name']}"})
    return out


def main() -> None:
    chapters = load_chapters()
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for ch in chapters:
        if only and ch["num"] != only:
            continue
        p = build(ch)
        n = len(json.loads(p.read_text(encoding="utf-8"))["cells"])
        print(f"{ch['num']}  {p.relative_to(ROOT)}  {n} cells")


if __name__ == "__main__":
    main()
