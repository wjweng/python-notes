#!/usr/bin/env python3
"""核對方格子上的文章是否與 chapters/NN-slug/README.md 一致。

    python3 tools/check_vocus.py 02 https://vocus.cc/article/61adbd7efd897800011372d7

方格子沒有寫入 API，文章是 weijie 手動貼的。手動貼最常出的錯（第 01、02 章都中過）：

- 從網頁版複製，可執行的程式碼區塊整段消失、網頁版專屬段落被帶過去
- 從 VS Code 預覽複製，`./code/` 變成 `file+wsl-…vscode-resource…` 的本機路徑

逐行比對原稿的每一行（含程式碼），並檢查行內程式碼格式、三個連結、本機路徑。
任何一項不過 exit 1。

`only:` 區塊在方格子上的處理（見《改版流程》階段 8）：

| 區塊 | 方格子 |
| :--- | :--- |
| 沒有標記、`only:github,web`（導向 Colab） | 必須出現 |
| `only:github,colab`（導向網頁版） | 可有可無，只列出來；〈本章程式碼〉的網頁版連結另外檢查 |
| 不含 `github` 的（例如 `only:web`） | 不可出現 |
"""
import html
import json
import random
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO_TREE = "https://github.com/wjweng/python-notes/tree/main/chapters"
COLAB = "https://colab.research.google.com/github/wjweng/python-notes/blob/main/notebooks"
PAGES = "https://wjweng.github.io/python-notes/web"
ONLY_OPEN = re.compile(r"<!--\s*only:([a-z,\s]+?)\s*-->")
ONLY_CLOSE = re.compile(r"<!--\s*/only\s*-->")


def fetch(url: str) -> str:
    """方格子有快取，剛改完立刻抓可能拿到舊版——加亂數參數並要求不用快取。

    傳本機檔案路徑也可以（存下來的頁面，或校準用的錯誤樣本）。
    """
    if Path(url).is_file():
        return Path(url).read_text(encoding="utf-8")
    sep = "&" if "?" in url else "?"
    req = urllib.request.Request(
        f"{url}{sep}nc={random.randrange(10**9)}",
        headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def norm(s: str) -> str:
    """拿掉空白與 `*`：粗體記號在原稿有、頁面上沒有，乘號兩邊都有，一起拿掉才比得下去。"""
    return re.sub(r"[\s*]+", "", s)


def prose_text(line: str) -> str:
    """markdown 一行 → 讀者在頁面上看到的文字。"""
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", line)          # 圖片另外上傳，不比
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)          # 連結只留文字
    s = re.sub(r"^\s*(#+ |> ?|- |\d+\. )", "", s)
    return s.replace("`", "").replace("|", "")


def source_lines(md: str) -> list[tuple[int, str, str, str]]:
    """回傳 [(行號, 原文, 頁面上該看到的文字, 'required' | 'optional' | 'forbidden')]。

    程式碼區塊內的行照原樣比（裡面的 `#`、`|` 是程式碼），標題第一行另外比。
    """
    out, targets, in_fence = [], None, False
    for i, line in enumerate(md.splitlines(), 1):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            if m := ONLY_OPEN.search(line):
                targets = {t.strip() for t in m.group(1).split(",")}
                continue
            if ONLY_CLOSE.search(line):
                targets = None
                continue
            if i == 1 and line.startswith("# "):
                continue
        text = line if in_fence else prose_text(line)
        if len(norm(text)) < 3 or set(norm(text)) <= set("-:"):
            continue
        if targets is None or {"github", "web"} <= targets:
            status = "required"
        elif "github" in targets:
            status = "optional"
        else:
            status = "forbidden"
        out.append((i, line, text, status))
    return out


def inline_code(md: str) -> set[str]:
    """方格子上必須保留程式碼格式的行內程式碼。

    表格裡的不算：方格子的表格不支援行內程式碼（第 01 章實測），貼上去就是純文字。
    不必出現在方格子上的 `only:` 段落也不算。
    """
    spans = set()
    for _, line, _, status in source_lines(md):
        if status == "required" and not line.lstrip().startswith("|"):
            spans.update(re.findall(r"`([^`]+)`", line))
    return spans


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__.split("\n\n")[1])
        return 2
    num, url = sys.argv[1], sys.argv[2]
    chapters = json.loads((ROOT / "chapters.json").read_text(encoding="utf-8"))["chapters"]
    ch = next((c for c in chapters if c["num"] == num), None)
    if ch is None:
        print(f"chapters.json 裡沒有第 {num} 章")
        return 2
    md = (ROOT / "chapters" / ch["dir"] / "README.md").read_text(encoding="utf-8")
    page = fetch(url)

    title = re.search(r"<title[^>]*>([^<]*)", page)
    modified = re.search(r'article:modified_time" content="([^"]+)', page)
    print(f"頁面標題：{html.unescape(title.group(1)) if title else '（找不到）'}")
    print(f"最後修改：{modified.group(1) if modified else '（找不到）'}　← 剛改完的話，確認是剛剛的時間")
    print()

    text = html.unescape(re.sub(r"<[^>]+>", "", page))
    flat = norm(text)
    fails: list[str] = []

    if not title or ch["title"] not in html.unescape(title.group(1)):
        fails.append(f"標題不含章名「{ch['title']}」")

    optional_missing = []
    for i, line, shown, status in source_lines(md):
        present = norm(shown) in flat
        if status == "required" and not present:
            fails.append(f"缺少 L{i}：{line.strip()[:70]}")
        elif status == "forbidden" and present:
            fails.append(f"不該出現（網頁版專屬）L{i}：{line.strip()[:60]}")
        elif status == "optional" and not present:
            optional_missing.append(i)

    codes = {norm(html.unescape(re.sub(r"<[^>]+>", "", c)))
             for c in re.findall(r"<code[^>]*>(.*?)</code>", page, re.S)}
    lost = sorted(s for s in inline_code(md) if norm(s) not in codes)
    if lost:
        fails.append(f"行內程式碼格式不見了（{len(lost)} 處）：{'、'.join(lost[:8])}")

    hrefs = set(re.findall(r'href="([^"]+)"', page))
    expected = {
        "GitHub": f"{REPO_TREE}/{ch['dir']}/code",
        "Colab": f"{COLAB}/{ch['dir']}.ipynb",
        "網頁版": f"{PAGES}/{ch['dir']}.html",
    }
    for name, link in expected.items():
        if not any(h.rstrip("/") == link for h in hrefs):
            fails.append(f"缺少{name}連結，應為 {link}")
    local = sorted(h for h in hrefs if re.search(r"vscode-resource|localhost|^file:", h))
    if local:
        fails.append(f"連結指到本機路徑：{local[0][:90]}")
    if "only:" in text or "&lt;!--" in page:
        fails.append("頁面上看得到 <!-- only --> 標記")

    if optional_missing:
        print(f"ℹ️  導向網頁版的段落沒放（可有可無）：L{', L'.join(map(str, optional_missing))}")
    if fails:
        print("❌ 有問題：")
        for f in fails:
            print(f"   {f}")
        return 1
    print(f"✅ 原稿每一行都在、行內程式碼 {len(inline_code(md))} 處都保留、三個連結正確、沒有本機路徑")
    return 0


if __name__ == "__main__":
    sys.exit(main())
