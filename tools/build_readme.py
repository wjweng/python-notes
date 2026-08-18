#!/usr/bin/env python3
"""從 chapters.json 產生根目錄 README 的章節表。

    python3 tools/build_readme.py           # 更新 README.md
    python3 tools/build_readme.py --check    # 只檢查是否過期（CI 用，過期回傳 1）

只覆寫兩個標記之間的內容，README 其餘部分照舊手寫：

    <!-- chapters:start -->
    ...這裡由本腳本產生...
    <!-- chapters:end -->

每一列有三個連結、其中兩個是長網址，36 章手工維護一定會貼錯，所以交給腳本。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = "https://wjweng.github.io/python-notes"
COLAB = "https://colab.research.google.com/github/wjweng/python-notes/blob/main/notebooks"
START, END = "<!-- chapters:start -->", "<!-- chapters:end -->"


def table() -> str:
    data = json.loads((ROOT / "chapters.json").read_text(encoding="utf-8"))
    units = {u["id"]: u for u in data["units"]}
    lines, seen = [], None
    for ch in data["chapters"]:
        u = units[ch["unit"]]
        if u["id"] != seen:  # 換單元時插一列標題，讓 36 章看得出結構
            cn = "一二三四五六七八九十"[u["id"] - 1]
            lines.append(f"\n**單元{cn}・{u['name']}**　{u['desc']}\n")
            lines.append("| # | 章節 | GitHub | Colab | 網頁 |")
            lines.append("| :- | :--- | :-: | :-: | :-: |")
            seen = u["id"]
        d = ch["dir"]
        lines.append(
            f"| {ch['num']} | {ch['title']} "
            f"| [📖](./chapters/{d}/) "
            f"| [▶]({COLAB}/{d}.ipynb) "
            f"| [⚡]({PAGES}/web/{d}.html) |"
        )
    return "\n".join(lines).strip()


def render(readme: str) -> str:
    i, j = readme.index(START), readme.index(END)
    return readme[:i] + START + "\n\n" + table() + "\n\n" + readme[j:]


def main() -> None:
    path = ROOT / "README.md"
    current = path.read_text(encoding="utf-8")
    if START not in current or END not in current:
        sys.exit(f"README.md 裡找不到 {START} / {END} 標記，無法產生")

    updated = render(current)
    if "--check" in sys.argv:
        if updated != current:
            sys.exit("README 的章節表與 chapters.json 不同步，請跑 tools/build_readme.py")
        print("README 章節表是最新的")
        return

    if updated == current:
        print("README 章節表無變化")
        return
    path.write_text(updated, encoding="utf-8")
    n = len(json.loads((ROOT / "chapters.json").read_text(encoding="utf-8"))["chapters"])
    print(f"README.md 章節表已更新（{n} 章）")


if __name__ == "__main__":
    main()
