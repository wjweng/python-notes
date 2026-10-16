#!/usr/bin/env python3
"""把章節的記憶體示意圖（變數 → 物件的箭頭圖）算成 PNG，算圖方式與 build_flowchart.py 相同。

定義檔放在 chapters/NN-slug/figures/memory.json，一張圖一個 key，輸出同名 PNG：
    python3 tools/build_memory.py 05       # 只做第 05 章
    python3 tools/build_memory.py          # 全部有定義檔的章節

定義檔格式（座標單位是 px）：
    {
      "05-fig1-alias": {
        "titles": [{"text": "my_city = city", "at": [20, 30]}],
        "vars": [{"name": "city", "at": [120, 80], "to": "a"}],
        "lists": [{"id": "a", "at": [240, 80], "items": ["台北", {"ref": "b"}], "new": [1]}],
        "rules": [40]
      }
    }

- titles：小標題（程式碼字型），at 是文字左端
- vars：變數名稱靠右對齊到 at 的 x，後面接一個小方格，箭頭從方格指向 to 的串列
- lists：一排格子，at 是第一格的左緣中點；items 是字串，或 {"ref": id} 表示這格裝的是另一個串列，畫成點加箭頭
- new：要標成新加入的格子索引，用該章單元的配色
- rules：在這些 y 畫一條分隔線
"""
import json
import subprocess
import sys
import tempfile
from html import escape
from pathlib import Path

from build_flowchart import INK, LABEL, SCALE, chrome, tint

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "chapters.json"

CELL_W, CELL_H, SLOT, MARGIN = 84, 40, 20, 24
FONTS = ("https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500"
         "&family=JetBrains+Mono:wght@400&display=swap")


def anchor(src, box):
    """箭頭終點：目標在右邊就接左緣（高度貼近起點，多條箭頭才不會擠在同一點），在上下就接上緣或下緣中點。"""
    (sx, sy), (left, top, w, h) = src, box
    if left - sx >= abs(top + h / 2 - sy):
        return left, min(max(sy, top + 8), top + h - 8)
    cx = left + w / 2
    return (cx, top) if sy < top else (cx, top + h)


def render_svg(fig: dict, accent: str) -> tuple[str, int, int]:
    boxes = {}
    for lst in fig["lists"]:
        x, y = lst["at"]
        boxes[lst["id"]] = (x, y - CELL_H / 2, CELL_W * len(lst["items"]), CELL_H)

    shapes, arrows, refs, texts = [], [], [], []
    xs, ys = [], []

    for t in fig.get("titles", []):
        x, y = t["at"]
        texts.append(f'<text x="{x}" y="{y}" class="mono lbl" style="text-anchor: start">{escape(t["text"])}</text>')
        xs += [x, x + 9.6 * len(t["text"])]
        ys += [y - 10, y + 10]

    for v in fig.get("vars", []):
        x, y = v["at"]
        texts.append(f'<text x="{x}" y="{y}" class="mono" style="text-anchor: end">{escape(v["name"])}</text>')
        sx = x + 10
        shapes.append(f'<rect x="{sx}" y="{y - SLOT / 2}" width="{SLOT}" height="{SLOT}" class="slot"/>')
        start = (sx + SLOT / 2, y)
        shapes.append(f'<circle cx="{start[0]}" cy="{y}" r="3.5" class="dot"/>')
        end = anchor(start, boxes[v["to"]])
        arrows.append(f'<line x1="{start[0]}" y1="{y}" x2="{end[0]}" y2="{end[1]}" class="ln"/>')
        xs += [x - 9.6 * len(v["name"]), sx + SLOT]
        ys += [y - SLOT, y + SLOT]

    for lst in fig["lists"]:
        left, top, w, h = boxes[lst["id"]]
        for i, item in enumerate(lst["items"]):
            cx = left + CELL_W * i
            cls = "cell new" if i in lst.get("new", []) else "cell"
            shapes.append(f'<rect x="{cx}" y="{top}" width="{CELL_W}" height="{h}" class="{cls}"/>')
            mid = (cx + CELL_W / 2, top + h / 2)
            if isinstance(item, dict):
                shapes.append(f'<circle cx="{mid[0]}" cy="{mid[1]}" r="3.5" class="dot"/>')
                end = anchor(mid, boxes[item["ref"]])
                refs.append(f'<line x1="{mid[0]}" y1="{mid[1]}" x2="{end[0]}" y2="{end[1]}" class="ln"/>')
            else:
                texts.append(f'<text x="{mid[0]}" y="{mid[1]}" class="sans">"{escape(item)}"</text>')
        xs += [left, left + w]
        ys += [top, top + h]

    for y in fig.get("rules", []):
        shapes.append(f'<line x1="{min(xs)}" y1="{y}" x2="{max(xs)}" y2="{y}" class="rule"/>')

    left, top = min(xs) - MARGIN, min(ys) - MARGIN
    w, h = round(max(xs) + MARGIN - left), round(max(ys) + MARGIN - top)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{left} {top} {w} {h}">
<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>
<style>
.cell {{ fill: #fff; stroke: {INK}; stroke-width: 1.6 }}
.new {{ fill: {tint(accent)}; stroke: {accent}; stroke-width: 2.2 }}
.slot {{ fill: #fff; stroke: {INK}; stroke-width: 1.4 }}
.dot {{ fill: {INK} }}
.ln {{ fill: none; stroke: {INK}; stroke-width: 1.6; marker-end: url(#arr) }}
.rule {{ stroke: #dddddd; stroke-width: 1; stroke-dasharray: 4 4 }}
text {{ dominant-baseline: central; text-anchor: middle; fill: {INK} }}
.mono {{ font: 16px 'JetBrains Mono', monospace }}
.sans {{ font: 500 16px 'Noto Sans TC', sans-serif }}
.lbl {{ fill: {LABEL} }}
</style>
<rect x="{left}" y="{top}" width="{w}" height="{h}" fill="#fff"/>
{''.join(arrows)}{''.join(shapes)}{''.join(refs)}{''.join(texts)}
</svg>"""
    return svg, w, h


def build(chapter: dict, accent: str) -> None:
    spec_path = ROOT / "chapters" / chapter["dir"] / "figures" / "memory.json"
    if not spec_path.exists():
        return
    figs = json.loads(spec_path.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmp:
        for name, fig in figs.items():
            svg, w, h = render_svg(fig, accent)
            page = Path(tmp) / f"{name}.html"
            page.write_text(f'<!doctype html><meta charset="utf-8"><link href="{FONTS}" rel="stylesheet">'
                            f'<body style="margin:0">{svg}</body>', encoding="utf-8")
            out = spec_path.parent / f"{name}.png"
            subprocess.run([chrome(), "--headless=new", "--disable-gpu", "--no-sandbox",
                            "--hide-scrollbars", f"--force-device-scale-factor={SCALE}",
                            f"--window-size={w},{h}", "--virtual-time-budget=5000",
                            f"--screenshot={out}", page.as_uri()],
                           check=True, capture_output=True)
            print(f"✅ {out.relative_to(ROOT)}（{w * SCALE}×{h * SCALE}）")


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    accents = {u["id"]: u["accent"] for u in manifest["units"]}
    wanted = sys.argv[1:]
    for chapter in manifest["chapters"]:
        if not wanted or chapter["num"] in wanted:
            build(chapter, accents[chapter["unit"]])


if __name__ == "__main__":
    main()
