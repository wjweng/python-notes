#!/usr/bin/env python3
"""在瀏覽器裡逐段執行網頁版的程式碼，與本機 Python 的結果比對。

    uv run --with playwright python tools/check_web.py        # 全部章節
    uv run --with playwright python tools/check_web.py 02     # 單章
    uv run --with playwright python tools/check_web.py 02 --input 18

要先跑過 build_web.py。檢查的是 `web/` 底下的本機檔案，不是線上的 Pages。

每一段都要能單獨執行（風格指南第六節），所以**倒著按**：先執行後面的區塊，
任何依賴前面區塊變數的程式，這時就會出現 `NameError`。

比對方式：同一段程式碼也丟給本機 Python 執行，兩邊的輸出要相同；出錯的區塊只比最後一行
（錯誤類型與訊息）。**出錯本身只有一種情況可以接受：那是文章刻意示範的錯誤**——錯誤訊息
必須出現在 README 的輸出區塊裡。否則就算本機也一樣出錯（例如依賴前面區塊的變數，兩邊都是
`NameError`），也判定失敗。`input()` 的回答一律用 `--input`（預設 `1`），兩邊都會把回答印在提示文字後面，
跟終端機看到的一樣。

網頁版的 Python（Pyodide）跟本機不同，有些輸出本來就會不一樣（例如第 01 章的環境檢查）。
這種區塊在 chapters.json 的 `web_output_differs` 列出區塊裡的一段文字，只檢查它不出錯、不比輸出——
而且文章裡要寫明成因（《改版流程》決策 16）。

瀏覽器用本機已下載的 Chromium（`~/.cache/ms-playwright/`），也可以用環境變數
`CHROMIUM` 指定。不用 Playwright MCP：它會在工作目錄產生 `.playwright-mcp/`，
而且同一個 session 開第二次常會卡在「Browser is already in use」。
"""
import functools
import http.server
import json
import os
import subprocess
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOT_TIMEOUT = 180_000  # Pyodide 從 CDN 下載，第一次可能要一兩分鐘

# 在本機 Python 跑一段程式：input() 換成「印出提示文字與回答」，跟網頁版的顯示方式一致
RUNNER = r"""
import builtins, sys
answer = sys.argv[1]
def fake_input(prompt=""):
    print(f"{prompt}{answer}")
    return answer
builtins.input = fake_input
src = sys.stdin.read()
exec(compile(src, "<exec>", "exec"), {"__name__": "__main__"})
"""

# 在頁面裡倒著執行每一段，回傳 [{i, code, out, err}]
RUN_ALL = """async (answer) => {
  window.prompt = () => answer;
  const n = document.querySelectorAll('.demo textarea').length;
  const res = [];
  for (let i = n - 1; i >= 0; i--) {
    await run(i);
    const o = document.getElementById('out' + i);
    res.unshift({ i, code: document.getElementById('code' + i).value,
                  out: o.textContent, err: o.className === 'err' });
  }
  return res;
}"""


def chromium() -> str | None:
    if os.environ.get("CHROMIUM"):
        return os.environ["CHROMIUM"]
    found = sorted(Path.home().glob(".cache/ms-playwright/chromium-*/chrome-linux*/chrome"))
    return str(found[-1]) if found else None


def serve() -> http.server.ThreadingHTTPServer:
    """file:// 會擋掉 Pyodide 的載入，開一個只活在這次檢查裡的本機伺服器。"""
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    handler = functools.partial(Quiet, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def local_result(code: str, answer: str) -> tuple[str, bool]:
    r = subprocess.run([sys.executable, "-c", RUNNER, answer], input=code,
                       capture_output=True, text=True, timeout=30)
    if r.returncode == 0:
        return r.stdout, False
    last = [l for l in r.stderr.splitlines() if l.strip()][-1]
    return r.stdout + last + "\n", True


def web_result(out: str, err: bool) -> str:
    """網頁版出錯時顯示的是 traceback，只留錯誤前的輸出加最後一行，跟本機的形式對齊。"""
    if out == "（這段程式沒有輸出）":
        return ""
    if not err:
        return out
    lines = out.splitlines()
    cut = next((k for k, l in enumerate(lines) if l.startswith('  File "<exec>"')), len(lines))
    before = "".join(l + "\n" for l in lines[:cut])
    last = [l for l in lines if l.strip()][-1]
    # 網頁版出錯時，錯誤前的輸出最後一行沒有換行（例如提示文字），traceback 直接接在後面
    return before + last + "\n"


def shown_outputs(ch: dict) -> str:
    """README 裡沒有標語言的區塊——文章貼出來給讀者看的執行結果與錯誤訊息。"""
    md = (ROOT / "chapters" / ch["dir"] / "README.md").read_text(encoding="utf-8")
    out, fence = [], None  # fence：目前所在區塊的語言，"" 是沒標語言的輸出區塊
    for line in md.splitlines():
        if line.startswith("```"):
            fence = line[3:].strip() if fence is None else None
            continue
        if fence == "":
            out.append(line)
    return "\n".join(out)


def check(page, ch: dict, base: str, answer: str) -> list[str]:
    page.goto(f"{base}/web/{ch['dir']}.html")
    page.get_by_text("執行環境就緒").first.wait_for(timeout=BOOT_TIMEOUT)
    differs = ch.get("web_output_differs", [])
    shown = shown_outputs(ch)
    fails = []
    blocks = page.evaluate(RUN_ALL, answer)
    for b in blocks:
        label = f"第 {b['i'] + 1} 段（{b['code'].strip().splitlines()[0][:40]}）"
        got = web_result(b["out"], b["err"])
        if any(mark in b["code"] for mark in differs):
            if b["err"]:
                fails.append(f"{label} 標記為輸出會不同，但網頁版出錯了：{got.splitlines()[-1]}")
            continue
        if b["err"] and got.splitlines()[-1] not in shown:
            fails.append(f"{label} 出錯了，但文章沒有示範這個錯誤（依賴前面區塊的變數？）："
                         f"{got.splitlines()[-1]}")
            continue
        want, _ = local_result(b["code"], answer)
        if got.rstrip() != want.rstrip():
            fails.append(f"{label}\n      網頁版：{got.rstrip()!r}\n      本機　：{want.rstrip()!r}")
    print(f"{ch['num']}  {len(blocks)} 段，倒著執行" + ("，全部與本機相同" if not fails else ""))
    return fails


def main() -> int:
    from playwright.sync_api import sync_playwright

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    answer = "1"
    if "--input" in sys.argv:
        answer = sys.argv[sys.argv.index("--input") + 1]
        args.remove(answer)
    chapters = json.loads((ROOT / "chapters.json").read_text(encoding="utf-8"))["chapters"]
    if args:
        chapters = [c for c in chapters if c["num"] == args[0]]

    print(f"本機 Python {sys.version.split()[0]}；網頁版是 Pyodide 內建的版本，"
          "錯誤訊息若因版本不同而有差異，以文章的本機輸出為準\n")
    server = serve()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    fails: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chromium())
        page = browser.new_page()
        errors: list[str] = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        for ch in chapters:
            fails += [f"{ch['num']} {f}" for f in check(page, ch, base, answer)]
            fails += [f"{ch['num']} 頁面 JavaScript 錯誤：{e}" for e in errors]
            errors.clear()
        browser.close()
    server.shutdown()

    if fails:
        print("\n❌ 有問題：")
        for f in fails:
            print(f"   {f}")
        return 1
    print("\n✅ 每一段都能單獨執行，輸出與本機相同")
    return 0


if __name__ == "__main__":
    sys.exit(main())
