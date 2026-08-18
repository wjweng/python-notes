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
"""
import re

REPO = "wjweng/python-notes"
BRANCH = "main"
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/chapters"
TREE = f"https://github.com/{REPO}/tree/{BRANCH}/chapters"
BLOB = f"https://github.com/{REPO}/blob/{BRANCH}/chapters"

BLOCK = re.compile(r"[ \t]*<!--\s*only:([a-z,\s]+?)\s*-->\n(.*?)[ \t]*<!--\s*/only\s*-->\n?",
                   re.S)
IMG = re.compile(r"!\[([^\]]*)\]\((?!https?://|data:)([^)]+)\)")
LINK = re.compile(r"(?<!!)\[([^\]]+)\]\((?!https?://|#|mailto:)([^)]+)\)")


def filter_blocks(md: str, target: str) -> str:
    """留下標記給 target 的段落，其餘整段拿掉。"""
    def keep(m: re.Match) -> str:
        targets = {t.strip() for t in m.group(1).split(",")}
        unknown = targets - {"github", "web", "colab"}
        if unknown:
            raise ValueError(f"only: 標記寫了不存在的目標 {unknown}")
        return m.group(2) if target in targets else ""
    return BLOCK.sub(keep, md)


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
