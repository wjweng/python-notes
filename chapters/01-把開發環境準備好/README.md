# 把開發環境準備好

很多人學 Python 的第一天，卡在還沒寫到程式的地方——裝了 Python、裝了編輯器，然後發現套件裝不起來，或是裝到了奇怪的地方。過幾個月換一台電腦，又要重來一次。

這一章把環境一次弄對，後面就不用再回頭。

## 這一章會用到的工具

| 工具 | 做什麼 |
| :--- | :--- |
| uv | 管理 Python 版本、虛擬環境、套件，一個工具全包 |
| VS Code | 寫程式的編輯器 |

只有兩樣。以前的做法是先到官網裝 Python，再用內建的 pip 裝套件，再另外學 venv 建虛擬環境，中間任何一步裝錯位置，後面就會出現「明明裝了卻找不到」的狀況。

現在 uv 把這三件事包在一起，而且它連 Python 本身都能幫我們裝，所以順序反過來：**先裝 uv，再讓 uv 去裝 Python**。

## 安裝 uv

Windows 開啟 PowerShell，執行：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOS 或 Linux 開啟終端機，執行：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

裝完之後**關掉終端機再重開一次**，否則系統還找不到這個新指令。重開後確認：

```bash
uv --version
```

有印出版本號就成功了。

## 用 uv 安裝 Python

```bash
uv python install 3.13
```

這行會下載 Python 3.13 並交由 uv 管理。它不會動到系統原本的 Python，也不需要設定環境變數（Windows 使用者應該對「Add Python to PATH」那個勾選框不陌生，現在不用管它了）。

想看目前有哪些版本可用：

```bash
uv python list
```

## 建立第一個專案

找一個放程式的資料夾，執行：

```bash
uv init hello-python
cd hello-python
```

uv 會建立一個資料夾，裡面長這樣：

```
hello-python/
├── main.py           # 程式進入點
├── pyproject.toml    # 專案設定與套件清單
├── README.md
└── .python-version   # 這個專案要用哪個 Python 版本
```

`pyproject.toml` 是重點，它記錄這個專案需要哪些套件。有了它，換一台電腦只要一行指令就能把環境還原回來，不用憑記憶回想當初裝過什麼。

執行看看：

```bash
uv run main.py
```

第一次執行時 uv 會自動建立虛擬環境，所以會多花幾秒。畫面上應該會看到：

```
Hello from hello-python!
```

到這裡環境就通了。

## 虛擬環境是什麼

剛才 uv 自動做掉的那件事，值得花一分鐘理解。

假設同時有兩個專案，A 專案需要某套件的 1.0 版，B 專案需要 2.0 版。如果所有套件都裝在同一個地方，這兩個專案就會打架。虛擬環境的做法是**讓每個專案有自己獨立的套件資料夾**，互不干擾。

uv 把虛擬環境放在專案底下的 `.venv/`。裝套件時不需要手動啟動它：

```bash
uv add requests
```

這行會做三件事：裝好 requests、寫進 `pyproject.toml`、更新鎖定檔 `uv.lock`。之後在別台電腦上只要執行 `uv sync`，就會裝回一模一樣的版本。

## 編輯器：VS Code

到 [code.visualstudio.com](https://code.visualstudio.com/) 下載安裝。開啟後裝一個擴充套件就夠了：左側點擴充功能圖示，搜尋 **Python**，安裝微軟出的那個。

裝好後用 VS Code 開啟剛才的 `hello-python` 資料夾。右下角會顯示目前使用的直譯器，確認它指向專案底下的 `.venv`。如果沒有，按 `Ctrl + Shift + P`（macOS 是 `Cmd + Shift + P`），輸入 `Python: Select Interpreter`，選擇 `.venv` 那一個。

這一步沒做對的話，編輯器會用系統的 Python 去檢查程式碼，明明裝好的套件會被畫上紅底線（我當年在這裡卡過很久，以為是套件裝壞了）。

## 第一支程式

把 `main.py` 的內容換成：

```python
print("Hello, Python!")
print("我的第一支程式")
```

執行：

```bash
uv run main.py
```

結果如下：

```
Hello, Python!
我的第一支程式
```

`print()` 是把東西顯示在畫面上的函數，括號裡放要顯示的內容。文字要用引號包起來，單引號或雙引號都可以，但同一個專案裡建議固定用一種。

## 確認環境真的裝對了

寫一支小程式來驗證，新增檔案 `check_env.py`：

```python
import sys
from pathlib import Path


def env_info() -> dict[str, str]:
    """回傳目前的 Python 版本與直譯器位置。"""
    return {
        "version": sys.version.split()[0],
        "executable": sys.executable,
        "in_venv": str(Path(sys.executable).parent.parent.name == ".venv"),
    }


if __name__ == "__main__":
    for key, value in env_info().items():
        print(f"{key}: {value}")
```

執行結果如下：

```
version: 3.13.0
executable: /path/to/hello-python/.venv/bin/python
in_venv: True
```

`in_venv` 是 `True`，代表程式跑在專案自己的虛擬環境裡，不是系統的 Python。這行如果是 `False`，回頭檢查上面 VS Code 選直譯器那一步。

## 互動模式

除了寫成檔案執行，也可以直接在終端機裡試語法：

```bash
uv run python
```

會進入互動模式，提示符號是 `>>>`：

```
>>> 1 + 1
2
>>> print("測試")
測試
>>> exit()
```

想確認某個語法怎麼運作、又不想特地開一個檔案時，這裡最快。輸入 `exit()` 離開。

---

環境的問題就處理到這裡。開頭說的那三種狀況——套件裝不起來、裝到奇怪的地方、換電腦要重來——分別由虛擬環境、uv 統一管理、`pyproject.toml` 解決掉了。

下一章開始寫真正的程式。

## 本章程式碼

- [`code/`](./code/) — 本章所有可執行範例
- [在 Colab 開啟](https://colab.research.google.com/github/wjweng/python-notes/blob/main/notebooks/01-把開發環境準備好.ipynb)
