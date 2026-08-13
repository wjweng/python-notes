# Python 學習筆記

從零開始的 Python 學習筆記。每一章都有可直接執行的程式碼，並提供三種閱讀方式：在這裡讀、在 Colab 互動、在瀏覽器直接改程式碼看結果。

## 章節

| # | 章節 | 讀 | Colab | 瀏覽器執行 |
| :- | :--- | :-: | :-: | :-: |
| 01 | 把開發環境準備好 | [📖](./chapters/01-把開發環境準備好/) | [▶](https://colab.research.google.com/github/wjweng/python-notes/blob/main/notebooks/01-把開發環境準備好.ipynb) | [⚡](./web/01-把開發環境準備好.html) |

## 這個 repo 怎麼運作

`chapters/` 是唯一的內容來源，其餘都由腳本產生：

```bash
python3 tools/build_cover.py      # 章節封面 PNG
python3 tools/build_notebook.py   # Colab notebook
python3 tools/build_web.py        # Pyodide 互動頁
```

`notebooks/` 與 `web/` 底下的檔案不要手動編輯，重跑腳本會覆蓋。

每次 push 時 CI 會逐支執行 `chapters/*/code/*.py`，確保筆記裡的程式碼都跑得動。
