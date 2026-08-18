# Python 學習筆記

從零開始的 Python 學習筆記。每一章都有可直接執行的程式碼，並提供三種讀法：在 GitHub 讀、在 Colab 互動、在網頁上直接改程式碼看結果。

## 章節

| # | 章節 | GitHub | Colab | 網頁 |
| :- | :--- | :-: | :-: | :-: |
| 01 | 把開發環境準備好 | [📖](./chapters/01-environment-setup/) | [▶](https://colab.research.google.com/github/wjweng/python-notes/blob/main/notebooks/01-environment-setup.ipynb) | [⚡](https://wjweng.github.io/python-notes/web/01-environment-setup.html) |

## 這個 repo 怎麼運作

`chapters/` 是唯一的內容來源，其餘都由腳本產生：

```bash
python3 tools/build_cover.py      # 章節封面 PNG
python3 tools/build_notebook.py   # Colab notebook
python3 tools/build_web.py        # Pyodide 互動頁
```

`notebooks/` 與 `web/` 底下的檔案不要手動編輯，重跑腳本會覆蓋。

## 命名規則

**repo 裡的資料夾與檔名一律英文小寫 slug**（`01-environment-setup`），內容維持中文。
路徑會變成 GitHub Pages 網址、Colab 連結與 CI 的 glob，中文在這些地方會被 encode 成一長串亂碼。

章節資料夾是 `NN-topic`，slug 取**主題**不是標題的翻譯——這樣日後改標題不必連帶改路徑。
`notebooks/`、`web/` 的檔名由 `chapters.json` 的 `dir` 自動衍生，改 `dir` 就好。

```bash
python3 tools/check_style.py    # 含命名檢查，違反會 exit 1
```

每次 push 時 CI 會逐支執行 `chapters/*/code/*.py`，確保筆記裡的程式碼都跑得動。
