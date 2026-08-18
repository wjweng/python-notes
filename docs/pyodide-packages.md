# 瀏覽器版（Pyodide）的能力邊界與套件載入

> 建立：2026-08-17　實測環境：Pyodide 0.26.4（`tools/build_web.py` 目前釘的版本）、Chromium
> 所有數字都是實測的，不是查文件抄的。重跑方式見最後一節。

寫到單元五（turtle）、單元六（pandas）、單元七（tkinter）時會用到這份筆記。

---

## 1. 現況：為什麼第三方套件全都不能用

`build_web.py` 產生的頁面只做了一件事：

```js
pyodide = await loadPyodide();
// ...
await pyodide.runPythonAsync(code);
```

**`runPythonAsync()` 不會自動載入套件。** 這是 Pyodide 0.18 之後刻意拆開的設計——載入套件要下載幾十 MB，不該在使用者按下「執行」時偷偷發生。

所以現在的頁面只跑得動內建模組：

| | 實測結果 |
| :--- | :--- |
| ✅ 可用 | `csv`、`json`、`pathlib`、`random`、`datetime`、`re`、`math` 等標準函式庫；檔案讀寫（虛擬檔案系統，重新整理就消失） |
| ❌ 不可用 | `pandas`、`requests`、`matplotlib`、任何第三方套件 → `ModuleNotFoundError` |
| ❌ 永遠不可用 | `turtle`、`tkinter` |

Pyodide 跑的是 **Python 3.12.1**，不是我們教的 3.13。目前沒有範例受影響，寫到 3.13 才有的語法時要注意。

---

## 2. 三種載入機制

### 2.1 `loadPackagesFromImports(code)` — 最適合我們

掃描程式碼裡的 `import`，自動下載對應的套件。**這是最小改動的解法。**

```js
await pyodide.loadPackagesFromImports(code);
await pyodide.runPythonAsync(code);
```

實測（`import pandas as pd` 然後建一個 DataFrame）：

| 項目 | 實測值 |
| :--- | ---: |
| Pyodide 本身啟動 | 1.4 秒 |
| 第一次載入 pandas | 1.3 秒 |
| 同一頁第二次載入 | 1 毫秒（已在記憶體） |
| 執行結果 | 正確（`df['a'].sum()` → `6`） |

只掃得到**靜態的 import 敘述**。`importlib.import_module("pandas")` 這種動態寫法掃不到，得自己補 `loadPackage`。

### 2.2 `loadPackage(name)` — 指定載入

```js
await pyodide.loadPackage(["pandas", "matplotlib"]);
```

用在 import 掃不到、或想預先載入的場合。

### 2.3 `micropip.install(name)` — 裝 Pyodide 沒內建的

```python
import micropip
await micropip.install("tabulate")   # 實測 OK，從 PyPI 抓純 Python 套件
```

限制很明確：**只裝得動純 Python 的 wheel**。有 C 擴充又沒編成 wasm 的會直接失敗：

```
await micropip.install("psycopg2")
→ ValueError: Can't find a pure Python 3 wheel for 'psycopg2'
```

---

## 3. 內建套件與下載成本

Pyodide 0.26.4 附了 **310 個套件**。教材會用到的：

| 套件 | 版本 | 內建 |
| :--- | :--- | :-- |
| pandas | 2.2.0 | ✅ |
| numpy | 1.26.4 | ✅ |
| matplotlib | 3.5.2 | ✅ |
| requests | 2.31.0 | ✅ |
| beautifulsoup4 | 4.12.3 | ✅ |
| pillow | 10.2.0 | ✅ |
| micropip | 0.6.0 | ✅ |
| pyodide-http | 0.2.1 | ✅ |
| openpyxl | — | ❌ 沒內建（要 micropip） |

**下載量（實測 CDN 實際傳輸位元組，含相依套件）**：

| `import` | 總量 | 明細 |
| :--- | ---: | :--- |
| `pandas` | **35.6 MB** | pandas 22.7 + numpy 11.4 + pytz 1.0 + dateutil 0.4 + six 0.04 |
| `matplotlib` | **35.7 MB** | matplotlib 15.0 + numpy 11.4 + fonttools 4.1 + pillow 2.9 + 其他 8 個 |
| `requests` | **1.3 MB** | urllib3 0.38 + idna 0.30 + certifi 0.29 + requests 0.19 + charset-normalizer 0.16 |
| `beautifulsoup4` | **0.4 MB** | beautifulsoup4 0.26 + soupsieve 0.13 |

**35 MB 是這件事的核心代價**，而且 numpy 佔了三分之一——pandas 與 matplotlib 兩章如果都要，第二章的 numpy 是共用的（同一頁內快取，跨頁則靠瀏覽器 HTTP 快取）。

`requests` 與 `beautifulsoup4` 便宜到可以無條件開啟。

---

## 4. 網路請求：能用，但受 CORS 限制

WASM 沒有 socket，照理說 `requests` 不能用。但 Pyodide 附的 **urllib3 是 2.2.1，內建 `urllib3.contrib.emscripten`**，會自動改走瀏覽器的 XHR／fetch。實測不需要任何 patch：

| 目標 | 結果 |
| :--- | :--- |
| 同源（自己的伺服器） | ✅ HTTP 200 |
| 跨域且允許 CORS（`api.github.com`） | ✅ HTTP 200 |
| 跨域但不允許 CORS（`example.com`） | ❌ `ConnectionError: Failed to execute 'send' on 'XMLHttpRequest'` |

所以教爬蟲或 API 時，**範例網址必須挑有開 CORS 的**（GitHub API、大多數公開 JSON API 可以；一般網站不行）。`pyodide-http` 這個套件也內建，`pyodide_http.patch_all()` 實測同樣可用，但在 urllib3 2.x 之後通常不需要了。

---

## 5. 永遠救不回來的

| 項目 | 原因 | 對策 |
| :--- | :--- | :--- |
| `turtle`、`tkinter`（Day 24、30、31、32） | 需要作業系統的視窗系統，WASM 沒有。**Colab 也不行**（無螢幕） | 這 4 章只提供程式碼展示，引導讀者在自己電腦上跑 |
| 有 C 擴充但沒 wasm wheel 的套件 | 沒編過就是沒有 | 換套件，或該章不提供互動版 |
| 檔案持久化 | 虛擬檔案系統，重新整理就清空 | 教檔案讀寫（Day 27）沒問題，但要說明「這裡的檔案不會留下來」 |

matplotlib 在 Pyodide 要搭配 `matplotlib-pyodide` 後端才畫得出圖（已列在相依裡會自動裝），畫布輸出方式與桌面版不同，真的要用時得另外驗。

---

## 6. 建議的實作方式

改動集中在 `build_web.py` 的 `run()`，加一行載入 + 一個載入中的提示：

```js
async function run(i) {
  const out = document.getElementById("out" + i);
  out.className = "";
  out.textContent = "";
  const code = document.getElementById("code" + i).value;
  try {
    // 先把 import 需要的套件抓下來（第一次可能要下載數十 MB）
    if (/^\s*(import|from)\s/m.test(code)) {
      out.textContent = "正在準備套件…";
      await pyodide.loadPackagesFromImports(code);
      out.textContent = "";
    }
    pyodide.setStdout({ batched: (s) => { out.textContent += s + "\n"; } });
    pyodide.setStderr({ batched: (s) => { out.textContent += s + "\n"; } });
    await pyodide.runPythonAsync(code);
    if (!out.textContent.trim()) out.textContent = "（這段程式沒有輸出）";
  } catch (e) {
    out.className = "err";
    out.textContent = String(e).split("\n").slice(-6).join("\n");
  }
}
```

三個要一起處理的細節：

1. **一定要有載入中的提示。** 35 MB 在慢速網路上是十幾秒，畫面沒反應會被當成壞掉。
2. **`chapters.json` 可以加一個欄位標記「這一章很重」**（例如 `"heavy": true`），在頁面頂端先警告「這一章的互動版需要下載約 35 MB」，讓讀者自己決定要不要用 Colab。
3. **`web_static` 的判斷要重新檢視。** 目前是用程式碼內容比對把不適合互動的區塊改成靜態顯示；turtle／tkinter 那 4 章應該整章走靜態。

---

## 7. 怎麼重跑這些量測

套件清單與相依（不需要瀏覽器）：

```bash
curl -s -o /tmp/pyodide-lock.json https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide-lock.json
python3 -c "
import json; pk = json.load(open('/tmp/pyodide-lock.json'))['packages']
p = pk['pandas']; print(p['version'], p['depends'])"
```

實際下載量：lock 檔裡**沒有** `file_size` 欄位，要對 CDN 發請求量：

```bash
curl -s -o /dev/null -w '%{size_download}\n' \
  https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pandas-2.2.0-cp312-cp312-pyodide_2024_0_wasm32.whl
```

瀏覽器端行為：起一個本機伺服器（`file://` 會被 Playwright 擋），用 `browser_evaluate` 直接呼叫 `loadPyodide()` 測。

```bash
cd ~/projects/python-notes && python3 -m http.server 8931
# 然後開 http://localhost:8931/web/<章節>.html
```

> 升 Pyodide 版本時整份重量一次——套件版本、大小、Python 版本都會變。
