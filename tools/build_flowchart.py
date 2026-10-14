#!/usr/bin/env python3
"""把章節的流程圖定義算成 PNG（SVG → headless Chrome，2 倍解析度）。

定義檔放在 chapters/NN-slug/figures/flowcharts.json，一張圖一個 key，輸出同名 PNG：
    python3 tools/build_flowchart.py 04       # 只做第 04 章
    python3 tools/build_flowchart.py          # 全部有定義檔的章節

定義檔格式：
    {
      "04-fig1-if": {
        "nodes": [
          {"id": "start", "type": "terminal", "label": "Start", "at": [0, 0]},
          {"id": "c1", "type": "decision", "label": "condition1", "at": [0, 1]},
          {"id": "a", "type": "process", "label": "Do A", "at": [1, 1]}
        ],
        "edges": [
          {"from": "c1", "to": "a", "label": "Yes"},
          {"from": "a", "to": "end", "via": [[1, 2.2], [0, 2.2]]}
        ]
      }
    }

- at：格線座標 [欄, 列]，可以是小數；一欄 COL px、一列 ROW px
- via：轉折點，同樣用格線座標。連線一律走水平／垂直線段，起點與終點會自動貼到節點邊緣
- 標籤（Yes／No）放在第一段線段旁邊
- 判斷框用該章所屬單元的配色（chapters.json 的 units.accent），跟封面一致
"""
import json
import subprocess
import sys
import tempfile
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "chapters.json"

COL, ROW, MARGIN, SCALE = 290, 130, 30, 2
INK, LABEL = "#333333", "#666666"
# 節點的半寬、半高
HALF = {"terminal": (70, 22), "process": (70, 24), "decision": (110, 50)}

FONTS = ("https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500"
         "&family=JetBrains+Mono:wght@400&display=swap")


def chrome() -> str:
    import shutil
    for name in ("google-chrome", "chromium", "chromium-browser", "google-chrome-stable"):
        if shutil.which(name):
            return name
    sys.exit("找不到 Chrome，無法算圖")


def tint(hex_color: str, ratio: float = 0.9) -> str:
    """把主色往白色混，當判斷框的底色。"""
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    mix = lambda c: round(c + (255 - c) * ratio)
    return f"#{mix(r):02x}{mix(g):02x}{mix(b):02x}"


def px(point):
    return point[0] * COL, point[1] * ROW


def clip(center, toward, kind):
    """從節點中心沿水平或垂直方向走到邊緣。"""
    (cx, cy), (tx, ty) = center, toward
    hw, hh = HALF[kind]
    if abs(tx - cx) >= abs(ty - cy):
        return (cx + hw, cy) if tx > cx else (cx - hw, cy)
    return (cx, cy + hh) if ty > cy else (cx, cy - hh)


def render_svg(chart: dict, accent: str) -> tuple[str, int, int]:
    nodes = {n["id"]: n for n in chart["nodes"]}
    shapes, lines, labels = [], [], []
    xs, ys = [], []

    for n in chart["nodes"]:
        cx, cy = px(n["at"])
        hw, hh = HALF[n["type"]]
        xs += [cx - hw, cx + hw]
        ys += [cy - hh, cy + hh]
        text = escape(n["label"])
        if n["type"] == "decision":
            pts = f"{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}"
            shapes.append(f'<polygon points="{pts}" class="cond"/>'
                          f'<text x="{cx}" y="{cy}" class="mono">{text}</text>')
        else:
            r = hh if n["type"] == "terminal" else 8
            cls = "sans" if n["type"] == "terminal" else "mono"
            shapes.append(f'<rect x="{cx - hw}" y="{cy - hh}" width="{2 * hw}" height="{2 * hh}"'
                          f' rx="{r}" class="box"/><text x="{cx}" y="{cy}" class="{cls}">{text}</text>')

    for e in chart["edges"]:
        src, dst = nodes[e["from"]], nodes[e["to"]]
        mids = [px(p) for p in e.get("via", [])]
        a, b = px(src["at"]), px(dst["at"])
        start = clip(a, mids[0] if mids else b, src["type"])
        end = clip(b, mids[-1] if mids else a, dst["type"])
        pts = [start, *mids, end]
        xs += [p[0] for p in pts]
        ys += [p[1] for p in pts]
        d = " ".join(f"{x},{y}" for x, y in pts)
        lines.append(f'<polyline points="{d}" class="ln" marker-end="url(#arr)"/>')
        if "label" in e:
            (x0, y0), (x1, y1) = pts[0], pts[1]
            if abs(x1 - x0) >= abs(y1 - y0):
                labels.append(f'<text x="{(x0 + x1) / 2}" y="{y0 - 12}" class="lbl">{escape(e["label"])}</text>')
            else:
                labels.append(f'<text x="{x0 + 10}" y="{y0 + (y1 - y0) * 0.45}" class="lbl"'
                              f' style="text-anchor: start">{escape(e["label"])}</text>')

    left, top = min(xs) - MARGIN, min(ys) - MARGIN
    w, h = round(max(xs) + MARGIN - left), round(max(ys) + MARGIN - top)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{left} {top} {w} {h}">
<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>
<style>
.box {{ fill: #fff; stroke: {INK}; stroke-width: 1.6 }}
.cond {{ fill: {tint(accent)}; stroke: {accent}; stroke-width: 2.2 }}
.ln {{ fill: none; stroke: {INK}; stroke-width: 1.6 }}
text {{ dominant-baseline: central; text-anchor: middle; fill: {INK} }}
.mono {{ font: 16px 'JetBrains Mono', monospace }}
.sans {{ font: 500 16px 'Noto Sans', sans-serif }}
.lbl {{ font: 14px 'Noto Sans', sans-serif; fill: {LABEL} }}
</style>
<rect x="{left}" y="{top}" width="{w}" height="{h}" fill="#fff"/>
{''.join(lines)}{''.join(shapes)}{''.join(labels)}
</svg>"""
    return svg, w, h


def build(chapter: dict, accent: str) -> None:
    spec_path = ROOT / "chapters" / chapter["dir"] / "figures" / "flowcharts.json"
    if not spec_path.exists():
        return
    charts = json.loads(spec_path.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmp:
        for name, chart in charts.items():
            svg, w, h = render_svg(chart, accent)
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
