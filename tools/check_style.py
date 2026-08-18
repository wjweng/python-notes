#!/usr/bin/env python3
"""對照《風格指南 v1》逐條檢查章節 README。

    python3 tools/check_style.py            # 全部章節
    python3 tools/check_style.py 01         # 只檢查第 01 章
    python3 tools/check_style.py --quiet    # 只印不合格的項目
    python3 tools/check_style.py --baseline # 用同一套定義重新量 36 篇舊文

檢查分兩類：
  ❌ 硬規則   排版、標點、AI 腔、小標層級 —— 對錯明確，會讓 exit code 變 1
  📊 參考數據 句長、程式碼比例、段落長度 —— 需要人判斷，只報數字不判定

風格指南：Dropbox/Agent/100_Todo/projects/python-notes/風格指南_v1.md

指南裡的舊文基準（句長 33 字、1 : 0.67）是 2026-08-13 一支沒存檔的腳本量的，
統計定義已不可考，**不要拿來跟本腳本的輸出直接比**。要比就跑 --baseline，
讓新舊兩邊走同一套 clean() 與斷句規則。
"""
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ── 舊文基準（35 篇 Day 系列，2026-08-16 由本腳本 --baseline 量出）──────
# 這組數字與下方的檢查共用同一套 clean() 與斷句規則，所以新舊比得下去。
BASE_SENTENCE_MEDIAN = 67  # 句長中位數，切在。！？
BASE_CLAUSE_MEDIAN = 17    # 分句長中位數，逗號也切
BASE_SHORT_RATIO = 0.15    # 短句 <30 字的佔比
BASE_CODE_RATIO = 0.94     # 文字 ÷ 程式碼，舊文是 1 : 0.94
BASE_BLOCKS = 11.3         # 每篇程式碼區塊數
MAX_PARAGRAPH = 200        # 單段字數上限
SHORT_SENTENCE = 30        # 短句的定義

# 舊文存檔在 Dropbox，兩台電腦的使用者名稱不同，用 glob 自動找
VOCUS_GLOB = "Dropbox/Agent/200_Reference/past-work/vocus"

# AI 腔：舊文 36 篇一次都沒出現過的句式
AI_PHRASES = [
    "在本文中", "本文將", "讓我們一起", "讓我們來", "接下來，讓我們",
    "你是不是也曾", "相信你一定", "希望這篇文章", "總而言之", "綜上所述",
    "首先，我們需要了解", "在這個數位時代", "眾所周知",
]

CJK = r"一-鿿々〆"
CJK_PUNCT = "，。、；：！？「」『』（）《》〈〉—…・"


# ── 把 Markdown 拆成「程式碼」與「文字」兩堆 ──────────────────────────

def split_blocks(text: str) -> tuple[list[str], list[tuple[int, str]]]:
    """回傳（程式碼區塊內容, [(行號, 文字行)]）。行號從 1 起算，方便定位。"""
    code, prose, in_fence = [], [], False
    for i, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        (code if in_fence else prose).append(line if in_fence else (i, line))
    return code, prose


def clean(line: str) -> str:
    """把不該被排版規則管的東西拿掉，留下純中文語境的句子。

    行內程式碼換成 'C'（一個半形字元），這樣「程式碼後接中文要空格」的規則
    仍然檢查得到；連結只留文字、網址整段拿掉。
    """
    line = re.sub(r"`[^`]*`", "C", line)
    line = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)
    line = re.sub(r"https?://\S+", "", line)
    return line


def is_skippable(line: str) -> bool:
    """表格分隔列、水平線、圖片這類沒有句子的行。"""
    s = line.strip()
    return (not s) or bool(re.fullmatch(r"[|:\-\s]+", s)) or s.startswith("![")


# ── 硬規則 ────────────────────────────────────────────────────────────

def check_spacing(prose: list[tuple[int, str]]) -> list[str]:
    """中英文之間、中文與數字之間要空格（新版與舊文相反，最容易寫錯）。"""
    hits = []
    for num, raw in prose:
        if is_skippable(raw):
            continue
        line = clean(raw)
        for m in re.finditer(rf"([{CJK}][A-Za-z0-9])|([A-Za-z0-9][{CJK}])", line):
            hits.append(f"L{num}  缺空格：…{context(line, m.start())}…")
    return hits


def check_parens(prose: list[tuple[int, str]]) -> list[str]:
    """中文語境用全形（），前後不加空格；程式碼括號維持半形（已在 clean 拿掉）。"""
    hits = []
    for num, raw in prose:
        if is_skippable(raw):
            continue
        line = clean(raw)
        for m in re.finditer(r"\(([^)]*)\)", line):
            if re.search(rf"[{CJK}]", m.group(1)):
                hits.append(f"L{num}  半形括號夾中文，應改全形：({m.group(1)})")
        for m in re.finditer(r"\s+（|）\s+", line):
            hits.append(f"L{num}  全形括號前後多了空格：…{context(line, m.start())}…")
    return hits


def check_quotes(prose: list[tuple[int, str]]) -> list[str]:
    """引號一律「」。"""
    hits = []
    for num, raw in prose:
        if is_skippable(raw) or raw.strip().startswith("|"):
            continue
        line = clean(raw)
        if re.search(rf'"[^"]*[{CJK}][^"]*"', line):
            hits.append(f"L{num}  半形雙引號夾中文，應改「」")
    return hits


def check_ai_tone(prose: list[tuple[int, str]]) -> list[str]:
    return [f"L{num}  AI 腔：{p}" for num, raw in prose for p in AI_PHRASES if p in raw]


def check_headings(prose: list[tuple[int, str]]) -> list[str]:
    """只用 ## 與 ###；小標是名詞短語，不是句子也不是問句。"""
    hits = []
    for num, raw in prose:
        m = re.match(r"^(#{1,6})\s+(.*)", raw)
        if not m:
            continue
        level, title = len(m.group(1)), m.group(2).strip()
        if level >= 4:
            hits.append(f"L{num}  小標用到第 {level} 層（只能 ## 與 ###）：{title}")
        # 問句小標是允許的（2026-08-18 weijie 校稿第 01 章時採用「--no-package 是什麼？」）。
        # 擋的是把整句話當標題，以及驚嘆號那種語氣標題。
        if title.endswith(("！", "!", "。")):
            hits.append(f"L{num}  小標寫成句子，應改名詞短語或問句：{title}")
    return hits


def check_cross_links(text: str, chapter_dir: str) -> list[str]:
    """跨版本連結必須指向「本章」的頁面，不是站台首頁、也不是別章。

    36 章各自手寫這兩條長網址，複製上一章忘了改編號是遲早的事，這裡擋住。
    """
    hits = []
    for m in re.finditer(r"https://wjweng\.github\.io/python-notes/(\S*?)[)\s]", text):
        path = m.group(1)
        if path != f"web/{chapter_dir}.html":
            hits.append(f"網頁版連結指到 /{path or ''}，應該是 /web/{chapter_dir}.html")
    for m in re.finditer(r"colab\.research\.google\.com/\S*?/notebooks/(\S*?)\.ipynb", text):
        if m.group(1) != chapter_dir:
            hits.append(f"Colab 連結指到 {m.group(1)}.ipynb，應該是 {chapter_dir}.ipynb")
    return hits


def check_ending(text: str, prose: list[tuple[int, str]]) -> list[str]:
    """收尾要有一段收束（呼應開場），不能像舊文直接貼 GitHub 連結。"""
    tail = [raw.strip() for _, raw in prose if raw.strip()]
    try:
        i = next(i for i, l in enumerate(tail) if l.startswith("## 本章程式碼"))
    except StopIteration:
        return ["找不到「## 本章程式碼」小節"]
    body = [l for l in tail[:i] if not l.startswith(("#", "|", ">", "-", "*"))]
    closing = "".join(body[-3:])
    return [] if len(closing) >= 40 else ["結尾缺少收束段（收尾直接接程式碼連結，是舊文的結構缺陷）"]


def context(line: str, pos: int, span: int = 12) -> str:
    return line[max(0, pos - span):pos + span]


# ── 參考數據 ──────────────────────────────────────────────────────────

SENT_SEP = r"[。！？\n]"      # 完整句子
CLAUSE_SEP = r"[。！？；，\n]"  # 分句：逗號也切，量的是「一口氣讀多長」


def sentences(prose: list[tuple[int, str]], sep: str = SENT_SEP) -> list[str]:
    body = " ".join(clean(raw) for _, raw in prose
                    if not is_skippable(raw) and not raw.strip().startswith(("#", "|")))
    return [s for p in re.split(sep, body) if len(s := re.sub(r"\s+", "", p)) >= 4]


def paragraphs(text: str) -> list[tuple[int, str]]:
    """回傳（字數, 開頭片段），只算純文字段落。"""
    out, buf, in_fence = [], [], False
    for line in text.splitlines() + [""]:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            buf = []
            continue
        if in_fence:
            continue
        if line.strip() and not line.strip().startswith(("#", "|", ">", "-", "*")):
            buf.append(clean(line))
        elif buf:
            joined = re.sub(r"\s+", "", " ".join(buf))
            out.append((len(joined), joined[:24]))
            buf = []
    return out


def ratios(code: list[str], prose: list[tuple[int, str]]) -> tuple[int, int, float]:
    n_code = len(re.sub(r"\s+", "", "\n".join(code)))
    n_prose = len(re.sub(r"\s+", "", "".join(clean(raw) for _, raw in prose)))
    return n_code, n_prose, (n_prose / n_code if n_code else float("inf"))


def asides(prose: list[tuple[int, str]]) -> int:
    """口語括號夾註（括號裡有中文），語氣的人味來源，要留 1-2 處。

    全形半形都算：舊文全用半形，新版一律全形，兩邊要能比。新版若出現半形，
    check_parens() 那關就會先擋下來。
    """
    pat = rf"（[^）]*[{CJK}][^）]*）|\([^)]*[{CJK}][^)]*\)"
    return sum(len(re.findall(pat, clean(raw))) for _, raw in prose)


# ── 主流程 ────────────────────────────────────────────────────────────

def report(path: Path, quiet: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    code, prose = split_blocks(text)

    hard = [
        ("中英文與數字之間空格", check_spacing(prose)),
        ("中文括號用全形且不留空格", check_parens(prose)),
        ("引號用「」", check_quotes(prose)),
        ("沒有 AI 腔", check_ai_tone(prose)),
        ("小標只用兩層且是名詞短語", check_headings(prose)),
        ("有收尾段", check_ending(text, prose)),
        ("跨版本連結指向本章", check_cross_links(text, path.parent.name)),
    ]

    sents = sentences(prose)
    clauses = sentences(prose, CLAUSE_SEP)
    median = statistics.median(len(s) for s in sents) if sents else 0
    median_clause = statistics.median(len(s) for s in clauses) if clauses else 0
    short = sum(len(s) < SHORT_SENTENCE for s in sents) / len(sents) if sents else 0
    n_code, n_prose, ratio = ratios(code, prose)
    long_paras = [p for p in paragraphs(text) if p[0] > MAX_PARAGRAPH]

    failed = sum(len(h) for _, h in hard)
    print(f"\n{'=' * 62}\n{path.parent.name}\n{'=' * 62}")

    for name, hits in hard:
        if hits:
            print(f"❌ {name}（{len(hits)} 處）")
            for h in hits[:12]:
                print(f"     {h}")
            if len(hits) > 12:
                print(f"     …另有 {len(hits) - 12} 處")
        elif not quiet:
            print(f"✅ {name}")

    print("\n📊 參考數據（需要人判斷，不列入通過與否；舊文欄請用 --baseline 的數字）")
    print(f"   句長中位數      {median:>6.0f} 字      舊文 {BASE_SENTENCE_MEDIAN} 字")
    print(f"   分句長中位數    {median_clause:>6.0f} 字      舊文 {BASE_CLAUSE_MEDIAN} 字")
    print(f"   短句 <{SHORT_SENTENCE} 字佔比  {short:>6.0%}        舊文 {BASE_SHORT_RATIO:.0%}")
    print(f"   程式碼 : 文字   1 : {ratio:.2f}     舊文 1 : {BASE_CODE_RATIO}"
          f"　（程式碼 {n_code} 字 / 文字 {n_prose} 字）")
    print(f"   程式碼區塊      {text.count('```') // 2:>6} 個      舊文平均 {BASE_BLOCKS} 個")
    print(f"   口語括號夾註    {asides(prose):>6} 處      指南建議留 1-2 處")
    if long_paras:
        print(f"   ⚠️ 超過 {MAX_PARAGRAPH} 字的段落 {len(long_paras)} 段：")
        for n, head in long_paras:
            print(f"      {n} 字  {head}…")

    return failed == 0


def check_naming() -> list[str]:
    """repo 內的資料夾與檔名一律英文小寫 slug（2026-08-16 定案）。

    內容是中文，但路徑不是——路徑會變成 GitHub Pages 的網址、Colab 連結、
    CI 的 glob。中文路徑在這些地方會被 percent-encode 成一長串亂碼。
    """
    hits = []
    slug = re.compile(r"[a-z0-9]+(?:[-_.][a-z0-9]+)*")
    for p in sorted(ROOT.rglob("*")):
        if any(part.startswith(".") or part == "__pycache__" for part in p.parts):
            continue  # 點開頭的設定檔與資料夾（.github、.gitignore）不在此規則內
        name = p.name if p.is_dir() else p.stem
        if not slug.fullmatch(name) and name not in {"README", "LICENSE", "CLAUDE"}:
            hits.append(f"{p.relative_to(ROOT)}　←　改成英文小寫 slug（例：01-environment-setup）")
    return hits


def find_vocus() -> Path:
    """找到舊文存檔資料夾（兩台電腦的 Dropbox 路徑不同）。"""
    for base in Path("/mnt/c/Users").glob("*"):
        if (d := base / VOCUS_GLOB).is_dir():
            return d
    sys.exit(f"找不到舊文存檔（*/{VOCUS_GLOB}），無法計算基準")


def baseline() -> None:
    """用與章節檢查完全相同的定義，重新量一次 36 篇舊文。

    指南裡那組數字（33 字、1 : 0.67）出自另一支已遺失的腳本，兩邊不可比。
    """
    files = sorted(find_vocus().glob("*Day-*.md"))
    if not files:
        sys.exit("舊文存檔裡找不到 Day 系列文章")

    all_sents, all_clauses, n_code, n_prose, blocks, n_asides = [], [], 0, 0, 0, 0
    for f in files:
        text = re.sub(r"\A---\n.*?\n---\n", "", f.read_text(encoding="utf-8"), flags=re.S)
        code, prose = split_blocks(text)
        all_sents += sentences(prose)
        all_clauses += sentences(prose, CLAUSE_SEP)
        c, p, _ = ratios(code, prose)
        n_code, n_prose = n_code + c, n_prose + p
        blocks += text.count("```") // 2
        n_asides += asides(prose)

    n = len(files)
    print(f"\n{'=' * 62}\n舊文基準（{n} 篇，與章節檢查同一套統計定義）\n{'=' * 62}")
    print(f"   句長中位數      {statistics.median(len(s) for s in all_sents):>6.0f} 字"
          f"      （切在。！？）")
    print(f"   分句長中位數    {statistics.median(len(s) for s in all_clauses):>6.0f} 字"
          f"      （逗號也切）")
    print(f"   短句 <{SHORT_SENTENCE} 字佔比  "
          f"{sum(len(s) < SHORT_SENTENCE for s in all_sents) / len(all_sents):>6.0%}")
    print(f"   程式碼 : 文字   1 : {n_prose / n_code:.2f}"
          f"　（程式碼 {n_code} 字 / 文字 {n_prose} 字）")
    print(f"   程式碼區塊      {blocks / n:>6.1f} 個／篇")
    print(f"   口語括號夾註    {n_asides / n:>6.1f} 處／篇")
    print("\n把這組數字填回《風格指南 v1》取代舊的那組，之後新舊才比得下去。")


def main() -> None:
    if "--baseline" in sys.argv:
        baseline()
        return
    quiet = "--quiet" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    data = json.loads((ROOT / "chapters.json").read_text(encoding="utf-8"))
    targets = [c for c in data["chapters"] if not args or c["num"] in args]
    if not targets:
        sys.exit(f"chapters.json 裡沒有第 {args[0]} 章")

    ok = all([report(ROOT / "chapters" / c["dir"] / "README.md", quiet) for c in targets])

    naming = check_naming()
    print(f"\n{'=' * 62}\nrepo 命名檢查\n{'=' * 62}")
    if naming:
        print(f"❌ 有 {len(naming)} 個非英文 slug 的路徑：")
        for h in naming:
            print(f"     {h}")
        ok = False
    elif not quiet:
        print("✅ 所有資料夾與檔名都是英文小寫 slug")

    print(f"\n{'—' * 62}")
    print("硬規則全部通過。" if ok else "硬規則有未通過項目，見上方 ❌。")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
