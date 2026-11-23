#!/usr/bin/env python3
"""產生方格子專用版 `vocus/NN-slug.html`，weijie 從這一頁複製、貼到方格子。

    python3 tools/build_vocus.py [NN]

方格子沒有寫入 API，只能手動貼。以前從 VS Code 的 Markdown 預覽複製，相對路徑
（`./code/`、`../05-lists/`）會變成 `file+wsl-…vscode-resource…` 的本機路徑，每次都要
逐一手動換網址，常漏（第 01、02、07、09 章都中過）。這一頁在產生時就把連結換好：

- 連到其他章節 → chapters.json 的 `vocus` 網址（讀者在方格子就留在方格子）
- `./code/` → GitHub 網址
- `only:` 段落照 targets.filter_blocks(md, "vocus") 的規則取捨

頁面放在 GitHub Pages（`/vocus/`），不從首頁連過去，並設 noindex。
程式碼區塊一律靜態顯示：可執行的編輯器（textarea）複製不到內容。
貼完照舊跑 check_vocus.py 核對。
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import targets  # noqa: E402
from build_web import load_chapters, render  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "vocus"

PAGE = """<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>方格子版 {num}｜{title}</title>
<style>
  :root {{ --bg: #ffffff; --text: #1f2328; --dim: #59636e; --line: #d1d9e0; --note: #fff8c5; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--text); padding: 24px 16px 80px;
          font-family: system-ui, sans-serif; line-height: 1.8; }}
  .wrap {{ max-width: 760px; margin: 0 auto; }}
  .tool {{ position: sticky; top: 0; z-index: 5; background: var(--note); border: 1px solid #d4a72c;
           border-radius: 8px; padding: 12px 16px; margin-bottom: 28px; font-size: 14px; }}
  .tool b {{ font-size: 15px; }}
  .tool button {{ font: inherit; font-weight: 700; padding: 6px 16px; margin-right: 10px;
                  border-radius: 6px; border: 1px solid #1f2328; background: #1f2328; color: #fff;
                  cursor: pointer; }}
  .tool .msg {{ color: #1a7f37; font-weight: 700; }}
  .tool ol {{ margin: 8px 0 0; padding-left: 22px; }}
  .tool code {{ font-size: 13px; }}
  pre {{ background: #f6f8fa; border: 1px solid var(--line); border-radius: 6px; padding: 12px 14px;
         overflow-x: auto; }}
  code {{ font-family: ui-monospace, monospace; }}
  table {{ border-collapse: collapse; }}
  th, td {{ border: 1px solid var(--line); padding: 6px 12px; }}
  img {{ max-width: 100%; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="tool">
    <b>第 {num} 章　{title}</b>（方格子專用版，產生於 commit 當下的原稿）<br>
    <button type="button" id="copy">複製內文</button><span class="msg" id="msg"></span>
    <ol>
      <li>按「複製內文」，到方格子{target}全選內文、貼上。標題另外填；圖和圖說會一起貼過去，不用另外上傳</li>
      <li>貼完跑 <code>python3 tools/check_vocus.py {num} &lt;文章網址&gt;</code></li>
    </ol>
  </div>
  <article id="article">
{content}
  </article>
</div>
<script>
const article = document.getElementById("article");
const msg = document.getElementById("msg");
document.getElementById("copy").addEventListener("click", () => {{
  // 用「選取整篇再複製」，跟滑鼠選取按 Ctrl+C 完全一樣。不要改回 navigator.clipboard.write：
  // 2026-11-23 第 10 章實測，那樣寫進剪貼簿的 HTML 貼到方格子後，清單裡的三個連結都不見了，
  // 內文段落裡的連結卻還在；同一頁用滑鼠選取複製，連結全都在。
  const range = document.createRange();
  range.selectNodeContents(article);
  const sel = getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
  msg.textContent = document.execCommand("copy") ? "已複製 ✓" : "已選取，請按 Ctrl+C";
}});
</script>
</body>
</html>
"""


def build(ch: dict) -> Path:
    md = (ROOT / "chapters" / ch["dir"] / "README.md").read_text(encoding="utf-8")
    md = re.sub(r"^# .*\n", "", md, count=1)          # 標題在方格子另外填
    md = targets.filter_blocks(md, "vocus")
    md = targets.chapter_links(md, "vocus")
    md = targets.absolute_links(md, ch["dir"], f"{targets.RAW}/{ch['dir']}")
    # runnable_marks=[]：沒有任何區塊可執行，全部是靜態的 <pre>
    content, _, _ = render(md, [], [])
    # render() 給標題加了目錄用的 id，方格子用不到
    content = re.sub(r'<(h[23]) id="s\d+">', r"<\1>", content)
    # 圖說在網頁版是 <span class="cap">。方格子貼上時會把 <img> 的 alt 當成圖說（第 10 章實測），
    # 這裡再留一份文字就重複了
    content = re.sub(r'<span class="cap">[^<]*</span>', "", content)
    if ch.get("vocus"):
        target = f'的<a href="{ch["vocus"]}">這篇文章</a>（編輯模式）'
    else:
        target = "新增一篇文章，發布後把網址補進 chapters.json 的 <code>vocus</code>，"
    OUT.mkdir(exist_ok=True)
    dst = OUT / f"{ch['dir']}.html"
    dst.write_text(PAGE.format(num=ch["num"], title=html.escape(ch["title"]), target=target,
                               content=content), encoding="utf-8")
    return dst


def main() -> None:
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for ch in load_chapters():
        if only and ch["num"] != only:
            continue
        try:
            p = build(ch)
        except ValueError as e:
            print(f"{ch['num']}  ❌ {e}")
            continue
        print(f"{ch['num']}  {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
