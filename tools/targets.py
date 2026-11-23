#!/usr/bin/env python3
"""同一份 README 要輸出到三個地方，這裡處理它們之間的差異。

三個輸出目標：

| 目標 | 檔案 | 讀者在哪裡 |
| :--- | :--- | :--- |
| `github` | `chapters/*/README.md` 本身 | GitHub 上直接讀 |
| `web`    | `web/*.html`                | Pyodide 互動頁 |
| `colab`  | `notebooks/*.ipynb`         | Colab |

## 只給特定目標看的段落

```markdown
<!-- only:github,colab -->
同樣的內容也製作了[網頁互動版](https://...)。
<!-- /only -->
```

**導流的方向要合理**：網頁版不要再叫讀者去網頁版，Colab 不要再叫讀者去 Colab。
每次加跨版本的連結時，先問「讀者現在人在哪裡」。

注意 `github` 是**沒辦法過濾的**——GitHub 直接渲染 README 原始檔，HTML 註解隱形、
中間的內容照樣顯示。所以 `only:` 的語意是「**產生器**要保留哪些目標」，GitHub 一律
全部顯示。段落的寫法要讓它在 GitHub 上讀起來也通順。

## 相對路徑

章節裡寫 `figures/x.png`、`./code/` 這種相對路徑，在 `web/` 與 Colab 底下都解不到，
由本模組改寫成各目標能用的絕對網址。

## 連到其他章節

內文提到其他章節時寫成 `[第 05 章](../05-lists/)`（2026-11-23 weijie 校稿第 07 章要求）。
GitHub 直接解得到；產生器依「讀者在哪裡」改寫：網頁版連網頁版、Colab 連 Colab。
方格子是手動貼的：build_vocus.py 產生 `vocus/*.html`，章節連結已換成 chapters.json 的 `vocus` 網址，
weijie 從那一頁複製貼上，貼完再由 check_vocus.py 核對（2026-11-23 起，原本是從 VS Code 預覽複製、
手動換網址，常漏）。

## 方格子（`vocus`）

讀者不在網頁版也不在 Colab，`only:` 段落只要有 `github` 就保留（兩個導流連結都放），
不含 `github` 的（例如 `only:web`）拿掉。
"""
import json
from pathlib import Path
import re

REPO = "wjweng/python-notes"
BRANCH = "main"
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/chapters"
TREE = f"https://github.com/{REPO}/tree/{BRANCH}/chapters"
BLOB = f"https://github.com/{REPO}/blob/{BRANCH}/chapters"

BLOCK = re.compile(r"[ \t]*<!--\s*only:([a-z,\s]+?)\s*-->\n(.*?)[ \t]*<!--\s*/only\s*-->\n?",
                   re.S)
IMG = re.compile(r"!\[([^\]]*)\]\((?!https?://|data:)([^)]+)\)")
PAGES = "https://wjweng.github.io/python-notes/web"
COLAB = f"https://colab.research.google.com/github/{REPO}/blob/{BRANCH}/notebooks"
CHAPTER_LINK = re.compile(r"\]\(\.\./(\d\d-[a-z0-9-]+)/\)")

LINK = re.compile(r"(?<!!)\[([^\]]+)\]\((?!https?://|#|mailto:)([^)]+)\)")


def filter_blocks(md: str, target: str) -> str:
    """留下標記給 target 的段落，其餘整段拿掉。"""
    def keep(m: re.Match) -> str:
        targets = {t.strip() for t in m.group(1).split(",")}
        unknown = targets - {"github", "web", "colab"}
        if unknown:
            raise ValueError(f"only: 標記寫了不存在的目標 {unknown}")
        if target == "vocus":
            return m.group(2) if "github" in targets else ""
        return m.group(2) if target in targets else ""
    return BLOCK.sub(keep, md)


def chapter_links(md: str, target: str) -> str:
    """`[第 05 章](../05-lists/)` 改成 target 上那一章的網址。要在 absolute_links() 之前呼叫。"""
    if target == "github":
        return md
    if target == "web":
        return CHAPTER_LINK.sub(lambda m: f"]({PAGES}/{m.group(1)}.html)", md)
    if target == "colab":
        return CHAPTER_LINK.sub(lambda m: f"]({COLAB}/{m.group(1)}.ipynb)", md)
    if target == "vocus":
        return CHAPTER_LINK.sub(lambda m: f"]({vocus_url(m.group(1))})", md)
    raise ValueError(f"不存在的目標 {target}")


def vocus_url(chapter_dir: str) -> str:
    """chapters.json 的 `vocus` 網址。還沒發的章節沒有網址，直接報錯：寧可擋下來，也不要讓讀者點到錯的地方。"""
    chapters = json.loads((Path(__file__).resolve().parent.parent / "chapters.json")
                          .read_text(encoding="utf-8"))["chapters"]
    ch = next((c for c in chapters if c["dir"] == chapter_dir), None)
    if not ch or not ch.get("vocus"):
        raise ValueError(f"chapters.json 的 {chapter_dir} 沒有 vocus 網址，"
                         "先把該章發到方格子並補上網址")
    return ch["vocus"]


def absolute_links(md: str, chapter_dir: str, image_base: str) -> str:
    """相對路徑改成絕對網址。圖片用 image_base，其餘一律指回 GitHub。"""
    md = IMG.sub(lambda m: f"![{m.group(1)}]({image_base}/{clean(m.group(2))})", md)

    def link(m: re.Match) -> str:
        path = clean(m.group(2))
        base = TREE if path.endswith("/") else BLOB
        return f"[{m.group(1)}]({base}/{chapter_dir}/{path})"
    return LINK.sub(link, md)


def clean(path: str) -> str:
    return path[2:] if path.startswith("./") else path
