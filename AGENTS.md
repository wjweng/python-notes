# python-notes — 給接手者的說明

從零開始的 Python 學習筆記，把舊版教學逐章改版成 GitHub／Colab／網頁互動版三種讀法。
repo 怎麼運作（內容來源、產生腳本、命名規則）見 `README.md`，這裡不重複。

## 文件在哪

改版的流程、已定案的決策、repo 結構與工具速查，都在作者的 Dropbox 資料夾
`Dropbox/Agent/100_Todo/projects/python-notes/`（該資料夾的 `README.md` 指回這裡）：

- `改版流程.md`——**唯一的流程與決策文件，改任何一章之前必讀**
- `風格指南_v1.md`——寫作規則；第一到八節是正式規則，第十節「待驗證觀察」也要看

## 動手前的三條

- `chapters/NN-slug/README.md` 是唯一內容來源；`notebooks/`、`web/`、`index.html` 由 `tools/` 產生，不要手改
- 路徑一律英文小寫 slug，內容維持中文；`python3 tools/check_style.py` 違反會 exit 1
- 改版既有文章預設原文照搬，只修知識錯誤、與新程式碼對不上的敘述、真的讀不通的句子；交稿時說明哪些照搬、哪些改了、為什麼
