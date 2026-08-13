#!/usr/bin/env python3
"""用 headless Chrome 把章節封面算成 PNG。

一次跑完全部章節，確保 36 張封面的字型與配色完全一致。
    python3 tools/build_cover.py          # 全部
    python3 tools/build_cover.py 01       # 只做第 1 章
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "chapters.json"
W, H, SCALE = 1200, 630, 2

TEMPLATE = """<!doctype html>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: {w}px; height: {h}px; overflow: hidden;
    background: #0d1117; color: #e6edf3;
    font-family: 'Noto Sans TC', sans-serif; position: relative;
  }}
  /* 程式碼底紋只佔右半，左側留給文字 */
  .code {{
    position: absolute; top: 0; right: 0; width: 52%; height: 100%;
    font-family: 'JetBrains Mono', monospace;
    font-size: 17px; line-height: 2.25;
    color: {accent}; opacity: .085;
    white-space: pre; padding: 40px 0 0 44px; user-select: none;
    -webkit-mask-image: linear-gradient(90deg, transparent, #000 22%, #000 76%, transparent);
  }}
  .glow {{
    position: absolute; width: 700px; height: 700px; border-radius: 50%;
    background: radial-gradient(circle, {accent}26 0%, transparent 66%);
    right: -230px; top: -270px;
  }}
  .bignum {{
    position: absolute; right: 74px; top: 30px;
    font-family: 'JetBrains Mono', monospace; font-weight: 700;
    font-size: 172px; line-height: 1; color: {accent}; opacity: .17;
  }}
  .bar {{ position: absolute; left: 0; top: 0; width: 9px; height: 100%; background: {accent}; }}
  .inner {{ position: relative; padding: 62px 78px 58px; height: 100%; display: flex; flex-direction: column; }}
  .series {{ font-size: 20px; font-weight: 500; letter-spacing: .3em; color: {accent}; }}
  .titlewrap {{ margin-top: auto; margin-bottom: 40px; }}
  .rule {{ width: 62px; height: 4px; background: {accent}; margin-bottom: 26px; border-radius: 2px; }}
  h1 {{ font-size: {title_size}px; font-weight: 900; line-height: 1.24;
        letter-spacing: -.012em; max-width: 760px; }}
  .foot {{ display: flex; justify-content: space-between; align-items: center;
           font-size: 19px; color: #7d8590; border-top: 1px solid #21262d; padding-top: 22px; }}
  .unit {{ color: {accent}; font-weight: 500; }}
</style>
<div class="code">{snippet}</div>
<div class="glow"></div>
<div class="bignum">{num}</div>
<div class="bar"></div>
<div class="inner">
  <div class="series">Python 學習筆記</div>
  <div class="titlewrap">
    <div class="rule"></div>
    <h1>{title}</h1>
  </div>
  <div class="foot"><span class="unit">{unit}</span><span>weijie</span></div>
</div>
"""


def chrome() -> str:
    for name in ("google-chrome", "chromium", "chromium-browser", "google-chrome-stable"):
        if path := shutil.which(name):
            return path
    sys.exit("找不到 Chrome，無法算圖")


def render(ch: dict, out: Path) -> None:
    title = ch["title"]
    html = TEMPLATE.format(
        w=W, h=H, accent=ch["accent"], num=ch["num"], title=title, unit=ch["unit"],
        title_size=64 if len(title) <= 12 else 54,
        snippet=(ch.get("snippet") or "").replace("<", "&lt;"),
    )
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "cover.html"
        page.write_text(html, encoding="utf-8")
        subprocess.run([
            chrome(), "--headless=new", "--disable-gpu", "--no-sandbox",
            "--hide-scrollbars", "--force-device-scale-factor=%d" % SCALE,
            "--virtual-time-budget=9000",
            f"--window-size={W},{H}",
            f"--screenshot={out}", page.as_uri(),
        ], check=True, capture_output=True, timeout=120)


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
        out = ROOT / "chapters" / ch["dir"] / "cover.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        render(ch, out)
        print(f"{ch['num']}  {out.relative_to(ROOT)}  {out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
