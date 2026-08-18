#!/usr/bin/env python3
"""把章節的 README.md 產生成完整的互動網頁。

整篇文章都會渲染出來，其中 Python 程式碼區塊變成可直接執行的編輯器（Pyodide），
其餘區塊維持靜態顯示。產出的 HTML 不需要後端，可直接嵌進個人網站。
"""
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import targets  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "web"
PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js"

# 這些語言的區塊只是給人看的指令，不放執行按鈕
STATIC_LANGS = {"bash", "powershell", "text", "", None}


# --------------------------------------------------------------------------
# 極簡 Markdown 轉 HTML（只支援本專案用得到的語法）
# --------------------------------------------------------------------------
CHAPTER_DIR = ""  # build() 每次設定，圖片的相對路徑要靠它還原


def inline(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    # 圖片要先於連結處理，否則 ![alt](src) 會被當成前面多一個驚嘆號的連結。
    # 相對路徑已由 targets.absolute_links() 轉成 ../chapters/... 的形式。
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)",
               r'<img src="\2" alt="\1" title="點一下放大" loading="lazy">'
               r'<span class="cap">\1</span>', s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s


def render(md: str, static_marks: list[str]) -> tuple[str, int]:
    """回傳 (HTML, 可執行區塊數量)。"""
    out: list[str] = []
    runnable = 0
    lines = md.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]

        # 程式碼區塊
        if line.startswith("```"):
            lang = line[3:].strip()
            body: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            code = "\n".join(body)
            # 有些 python 區塊不適合在瀏覽器跑（例如檢查本機環境的程式，
            # 在 Pyodide 裡回報的是 Pyodide 自己的環境，對讀者沒有意義）
            is_static = any(mark in code for mark in static_marks)
            if lang == "python" and not is_static:
                out.append(
                    f'<div class="demo"><div class="head">'
                    f'<span class="name">可以改改看，按執行</span>'
                    f'<button id="btn{runnable}" onclick="run({runnable})" disabled>執行</button></div>'
                    f'<textarea id="code{runnable}" spellcheck="false" rows="{max(3, len(body))}">'
                    f'{html.escape(code)}</textarea>'
                    f'<pre id="out{runnable}"></pre></div>'
                )
                runnable += 1
            else:
                cls = ' class="lang-python"' if lang == "python" else (
                      f' class="lang-{lang}"' if lang else "")
                out.append(f"<pre class=\"static\"><code{cls}>{html.escape(code)}</code></pre>")
            continue

        # 表格
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1]):
            head = [c.strip() for c in line.strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip("|").split("|")])
                i += 1
            th = "".join(f"<th>{inline(c)}</th>" for c in head)
            tb = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows)
            out.append(f'<div class="tablewrap"><table><thead><tr>{th}</tr></thead>'
                       f"<tbody>{tb}</tbody></table></div>")
            continue

        # 標題
        if m := re.match(r"^(#{1,4})\s+(.*)$", line):
            lv = len(m.group(1))
            if lv > 1:  # h1 由頁面標題負責
                out.append(f"<h{lv}>{inline(m.group(2))}</h{lv}>")
            i += 1
            continue

        # 分隔線。h2 本身就有上框線，緊接著 ## 的話會變成兩條，跳過不畫。
        if re.match(r"^-{3,}$", line.strip()):
            nxt = next((l for l in lines[i + 1:] if l.strip()), "")
            if not re.match(r"^##\s", nxt):
                out.append("<hr>")
            i += 1
            continue

        # 條列
        if re.match(r"^[-*]\s+|^\d+\.\s+", line):
            ordered = bool(re.match(r"^\d+\.\s+", line))
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+|^\d+\.\s+", lines[i]):
                items.append(re.sub(r"^([-*]|\d+\.)\s+", "", lines[i]))
                i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
            continue

        # 引言
        if line.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i].lstrip("> "))
                i += 1
            out.append(f"<blockquote>{inline(' '.join(quote))}</blockquote>")
            continue

        # 段落
        if line.strip():
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(
                r"^(```|\||#{1,4}\s|[-*]\s|\d+\.\s|>|-{3,}$)", lines[i]
            ):
                para.append(lines[i])
                i += 1
            if para:
                out.append(f"<p>{inline(' '.join(para))}</p>")
            continue

        i += 1

    return "\n".join(out), runnable


PAGE = """<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Python 學習筆記</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
<style>
  :root {{ --accent: {accent}; --bg: #0d1117; --panel: #161b22; --line: #30363d;
           --text: #e6edf3; --dim: #8b949e; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--text); padding: 32px 20px 80px;
          font-family: 'Noto Sans TC', system-ui, sans-serif; line-height: 1.85; }}
  .wrap {{ max-width: 780px; margin: 0 auto; }}
  .unit {{ color: var(--accent); font-size: 14px; font-weight: 500; letter-spacing: .16em; }}
  h1 {{ font-size: 34px; font-weight: 900; margin: 8px 0 26px; line-height: 1.3; }}
  h2 {{ font-size: 23px; font-weight: 700; margin: 46px 0 14px; padding-top: 14px;
        border-top: 1px solid var(--line); }}
  h3 {{ font-size: 18px; font-weight: 700; margin: 30px 0 10px; color: var(--accent); }}
  p {{ margin: 14px 0; }}
  a {{ color: var(--accent); }}
  code {{ font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: .88em;
          background: #1f2430; padding: 2px 6px; border-radius: 4px; }}
  pre.static {{ background: #010409; border: 1px solid var(--line); border-radius: 8px;
                padding: 14px 16px; overflow-x: auto; margin: 16px 0; }}
  pre.static code {{ background: none; padding: 0; font-size: 13.5px; line-height: 1.7; }}
  .tablewrap {{ overflow-x: auto; margin: 18px 0; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 15px; }}
  th, td {{ border: 1px solid var(--line); padding: 9px 13px; text-align: left; }}
  th {{ background: var(--panel); font-weight: 700; }}
  blockquote {{ border-left: 3px solid var(--accent); margin: 18px 0; padding: 6px 16px;
                color: var(--dim); background: #12171f; }}
  ul, ol {{ padding-left: 26px; }}
  li {{ margin: 6px 0; }}
  hr {{ border: 0; border-top: 1px solid var(--line); margin: 38px 0; }}
  img {{ max-width: 100%; height: auto; display: block; margin: 20px auto 6px;
         border: 1px solid var(--line); border-radius: 8px; cursor: zoom-in; }}
  .cap {{ display: block; text-align: center; font-size: 13px; color: var(--dim);
          margin-bottom: 22px; }}
  /* 點圖放大：截圖是 4K 全螢幕，縮到內文寬度會看不清楚 */
  #lightbox {{ position: fixed; inset: 0; z-index: 50; display: none;
               background: rgba(1, 4, 9, .93); cursor: zoom-out;
               padding: 24px 24px 44px; place-items: center; overflow: auto; }}
  #lightbox.on {{ display: grid; }}
  /* 放大到視窗大小就好，超出視窗反而要捲動才看得完。
     高度用 vh 而不是 %：grid 的列高不定時，百分比的 max-height 會失效。 */
  #lightbox img {{ max-width: 100%; max-height: calc(100vh - 68px); width: auto; height: auto;
                   margin: 0; border: 0; border-radius: 4px; cursor: zoom-out; }}
  #lightbox .hint {{ position: fixed; left: 0; right: 0; bottom: 14px; text-align: center;
                     color: var(--dim); font-size: 13px; pointer-events: none; }}
  .demo {{ border: 1px solid var(--line); border-radius: 8px; overflow: hidden; margin: 18px 0; }}
  .head {{ background: var(--panel); padding: 8px 13px; font-size: 13px; color: var(--dim);
           display: flex; justify-content: space-between; align-items: center; }}
  .name {{ font-size: 12.5px; }}
  textarea {{ width: 100%; border: 0; background: #010409; color: var(--text); display: block;
              font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 13.5px;
              line-height: 1.7; padding: 14px 16px; resize: vertical; outline: none; }}
  button {{ background: var(--accent); color: #0d1117; border: 0; border-radius: 5px;
            padding: 4px 15px; font-weight: 700; cursor: pointer; font-size: 13px;
            font-family: inherit; }}
  button:disabled {{ opacity: .4; cursor: default; }}
  pre[id^="out"] {{ margin: 0; padding: 12px 16px; background: var(--panel);
                    border-top: 1px solid var(--line); font-family: 'JetBrains Mono', monospace;
                    font-size: 13.5px; white-space: pre-wrap; min-height: 42px; color: #9ad1c4; }}
  pre.err {{ color: #ff7b72 !important; }}
  #boot {{ position: sticky; top: 0; z-index: 9; background: var(--panel); color: var(--dim);
           font-size: 13px; padding: 9px 14px; border: 1px solid var(--line);
           border-radius: 7px; margin-bottom: 26px; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="unit">{unit}</div>
  <h1>{title}</h1>
  <div id="boot">Python 執行環境載入中⋯⋯（第一次約需 10 秒，之後由瀏覽器快取）</div>
{content}
</div>
<div id="lightbox"><img alt=""><span class="hint">點任意處或按 Esc 關閉</span></div>
<script>
// 點圖放大。原圖是 4K 螢幕截圖，內文寬度只有 780px，不放大看不到細節。
const lb = document.getElementById("lightbox");
const lbImg = lb.querySelector("img");
document.querySelectorAll(".wrap img").forEach(img => {{
  img.addEventListener("click", () => {{
    lbImg.src = img.src;
    lbImg.alt = img.alt;
    lb.classList.add("on");
    lb.scrollTop = 0;
    document.body.style.overflow = "hidden";
  }});
}});
function closeLightbox() {{
  lb.classList.remove("on");
  document.body.style.overflow = "";
}}
lb.addEventListener("click", closeLightbox);
document.addEventListener("keydown", e => {{ if (e.key === "Escape") closeLightbox(); }});
</script>
<script src="{pyodide}"></script>
<script>
let pyodide = null;
async function boot() {{
  const tip = document.getElementById("boot");
  try {{
    pyodide = await loadPyodide();
    tip.textContent = "執行環境就緒 ✓　程式碼可以直接改，改完按「執行」";
    document.querySelectorAll(".demo button").forEach(b => b.disabled = false);
  }} catch (e) {{
    tip.textContent = "執行環境載入失敗，程式碼仍可閱讀：" + e;
  }}
}}
async function run(i) {{
  const out = document.getElementById("out" + i);
  out.className = "";
  out.textContent = "";
  try {{
    pyodide.setStdout({{ batched: (s) => {{ out.textContent += s + "\\n"; }} }});
    pyodide.setStderr({{ batched: (s) => {{ out.textContent += s + "\\n"; }} }});
    await pyodide.runPythonAsync(document.getElementById("code" + i).value);
    if (!out.textContent.trim()) out.textContent = "（這段程式沒有輸出）";
  }} catch (e) {{
    out.className = "err";
    out.textContent = String(e).split("\\n").slice(-6).join("\\n");
  }}
}}
boot();
</script>
</body>
</html>
"""


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


def build(ch: dict) -> tuple[Path, int]:
    global CHAPTER_DIR
    CHAPTER_DIR = ch["dir"]
    md = (ROOT / "chapters" / ch["dir"] / "README.md").read_text(encoding="utf-8")
    md = re.sub(r"^# .*\n", "", md, count=1)          # h1 交給頁面標題
    md = targets.filter_blocks(md, "web")
    md = targets.absolute_links(md, ch["dir"], f"../chapters/{ch['dir']}")
    content, runnable = render(md, ch.get("web_static", []))
    OUT.mkdir(exist_ok=True)
    dst = OUT / f"{ch['dir']}.html"
    dst.write_text(PAGE.format(title=ch["title"], unit=ch["unit"], accent=ch["accent"],
                               content=content, pyodide=PYODIDE), encoding="utf-8")
    return dst, runnable


INDEX = """<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Python 學習筆記</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: #0d1117; color: #e6edf3; padding: 64px 20px 90px;
          font-family: 'Noto Sans TC', system-ui, sans-serif; line-height: 1.8; }}
  .wrap {{ max-width: 760px; margin: 0 auto; }}
  h1 {{ font-size: 40px; font-weight: 900; margin: 0 0 10px; }}
  .lead {{ color: #8b949e; margin-bottom: 46px; }}
  .unit {{ font-size: 14px; font-weight: 500; letter-spacing: .15em; margin: 38px 0 12px; }}
  a.ch {{ display: flex; align-items: center; gap: 14px; text-decoration: none; color: inherit;
          border: 1px solid #30363d; border-radius: 9px; padding: 15px 18px; margin-bottom: 9px;
          transition: border-color .15s, background .15s; }}
  a.ch:hover {{ background: #161b22; }}
  .n {{ font-family: ui-monospace, monospace; font-size: 15px; opacity: .65; }}
  .t {{ font-weight: 700; font-size: 17px; }}
  .go {{ margin-left: auto; font-size: 13px; color: #8b949e; }}
  footer {{ margin-top: 60px; color: #8b949e; font-size: 14px;
            border-top: 1px solid #30363d; padding-top: 22px; }}
  footer a {{ color: #58a6ff; }}
</style>
</head>
<body><div class="wrap">
<h1>Python 學習筆記</h1>
<div class="lead">每一章的程式碼都可以直接在這裡改、直接執行，不用安裝任何東西。</div>
{items}
<footer>作者 weijie ・ 原始碼與程式碼範例在 <a href="https://github.com/wjweng/python-notes">GitHub</a></footer>
</div></body>
</html>
"""


def build_index(chapters: list[dict]) -> Path:
    items, seen = "", None
    for ch in chapters:
        if ch["unit"] != seen:
            seen = ch["unit"]
            items += f'<div class="unit" style="color:{ch["accent"]}">{seen}</div>\n'
        items += (f'<a class="ch" href="./web/{ch["dir"]}.html">'
                  f'<span class="n" style="color:{ch["accent"]}">{ch["num"]}</span>'
                  f'<span class="t">{ch["title"]}</span>'
                  f'<span class="go">開啟 →</span></a>\n')
    dst = ROOT / "index.html"
    dst.write_text(INDEX.format(items=items), encoding="utf-8")
    return dst


def main() -> None:
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for ch in load_chapters():
        if only and ch["num"] != only:
            continue
        p, n = build(ch)
        print(f"{ch['num']}  {p.relative_to(ROOT)}  {p.stat().st_size // 1024} KB"
              f"　可執行區塊 {n} 個")
    idx = build_index(load_chapters())
    print(f"    索引頁：{idx.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
