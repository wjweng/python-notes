# 註解、變數與資料型態

## 註解

註解是 Python 直譯器會跳過不執行的部分，但它可以補充說明程式背後的設計思維、摘要、或是預期會產生什麼樣的結果，它可以讓程式的可讀性更高，尤其是經過一段時間後再回來閱讀，或是對於多人合作開發的大型程式，都可以加速對程式的理解。

程式註解的方法有以下三種：

```python
# 這是單行註解

'''
這是多行註解
'''

"""
這也是多行註解
"""
```

嚴格來說，後面兩種三引號的寫法其實是字串，並不是真正的註解，Python 還是會讀到它，只是沒有把它存進變數或拿來使用，所以對程式的執行不會有任何影響，也因此常被拿來當作多行註解。三引號字串如果放在函數的第一行，還會變成這個函數的說明文件（docstring），之後講到函數時會再看到。

`#` 也可以接在程式碼的後面，這種寫法叫做行尾註解，`#` 之後的內容同樣不會被執行：

```python
print("Hello World!")  # 這是行尾註解
```

單行註解的方式除了可手動打字外，在 VS Code 裡面也可將輸入位置停在想要註解的行數上，按下 `Ctrl + /` 快速鍵（macOS 是 `Cmd + /`）來達成；因此，若要達成多行註解，也可將要註解的行數反白，再按下 `Ctrl + /` 完成多個單行註解。

## `print()` 函數基本功能

可將資料打印輸出，例如以下程式可在 VS Code 下方的終端機印出「Hello World!」字串，以便開發者初步測試程式的正確性。

```python
# print to console
print("Hello World!")
```

執行結果：

```
Hello World!
```

## `input()` 函數基本功能

可接收使用者輸入的資料，例如程式執行到以下的函數便會停下來等待使用者輸入後再往下執行。

```python
# input function
input("What's your name? ")
```

執行結果如下，前方的「What's your name?」為程式輸出，「weijie」為使用者輸入。提示文字的最後多留了一個空格，使用者輸入的內容才不會跟提示文字黏在一起。

```
What's your name? weijie
```

## 變數與資料型態

變數為程式暫存資料的地方，例如前方的 Hello World 程式，我們可用一個變數儲存要打印的字串資料，再用 `print()` 函數將此字串打印出來，此變數的型態便為字串資料型態。

```python
# string
string_data = "Hello World!"
print(string_data)
print(type(string_data))
```

`type()` 函數可回傳變數的資料型態。

```
Hello World!
<class 'str'>
```

其它常見的基本資料型態還有整數、浮點數、布林值等。

```python
# integer
integer_data = 123 + 456
print(integer_data)
print(type(integer_data))
```

```python
# float
float_data = 3.1415926
print(float_data)
print(type(float_data))
```

```python
# boolean
bool_data = True
print(bool_data)
print(type(bool_data))
```

輸出結果：

```
579
<class 'int'>
3.1415926
<class 'float'>
True
<class 'bool'>
```

更精確地說，資料型態是跟著「值」走的，而不是跟著變數。同一個變數可以先放整數，之後再改放字串，它的型態也會跟著改變：

```python
data = 5
print(type(data))
data = "five"
print(type(data))
```

執行結果：

```
<class 'int'>
<class 'str'>
```

須注意雖然 Python 宣告變數時不用指定變數型態，但當此變數存放了整數資料，它便是整數的資料型態，存放了字串資料，它便是字串的資料型態，因此在某些情境下，兩種變數是不能混用的，例如：

```python
integer_data = 123 + 456
print("Integer data is " + integer_data)
```

此時 `print()` 函數內前方是字串資料，後方是整數型態的變數，兩者相加便會產生錯誤，錯誤訊息的最後一行如下：

```
TypeError: can only concatenate str (not "int") to str
```

為了解決此問題，可透過強制資料型態的轉換，讓兩者型態一致：

```python
integer_data = 123 + 456

# type conversion
string_integer_data = str(integer_data)
print("Integer data is " + string_integer_data)
```

另一種更簡潔的方式是使用 f-string 將字串格式化：

```python
integer_data = 123 + 456

# f-string
print(f"Integer data is {integer_data}")
```

以上兩種方式都可以得到正確的結果：

```
Integer data is 579
```

### 變數的命名規則

前面的範例中，我們建立了 `string_data`、`integer_data` 等變數。變數的名字大致可以自由決定，但有幾條規則要遵守：

- 由字母、數字、底線 `_` 組成，而且**不能用數字開頭**，例如 `1data` 會出現錯誤（中文字其實也算字母，但習慣上還是用英文）
- 中間不能有空格或 `-`，例如 `my-name` 會被當成 `my` 減去 `name`
- 不能使用 Python 保留的關鍵字，例如 `class`、`if`、`for`
- **英文大小寫視為不同的名字**，`name` 與 `Name` 是兩個不同的變數

大小寫這一條也適用在 Python 內建的名稱上，例如布林值要寫成 `True`，寫成小寫的 `true` 會被當成一個沒有定義過的變數：

```python
print(true)
```

錯誤訊息的最後一行如下，Python 也會提示你是不是要寫 `True`：

```
NameError: name 'true' is not defined. Did you mean: 'True'?
```

多個英文單字組成的變數名稱，在 Python 習慣上用底線連接，例如 `string_data`。

### `input()` 拿到的都是字串

了解型態轉換之後，我們再回頭看前面的 `input()` 函數。不論使用者輸入的是什麼，`input()` 拿到的一律是字串，就算輸入的是數字也一樣，因此直接拿來計算，會產生和前面一樣的錯誤：

```python
age = input("How old are you? ")
print(age + 1)
```

輸入 `18` 之後，錯誤訊息的最後一行如下：

```
TypeError: can only concatenate str (not "int") to str
```

這時就要用 `int()` 把它轉成整數，再拿來計算：

```python
age = int(input("How old are you? "))
print(age + 1)
```

執行結果：

```
How old are you? 18
19
```

要注意的是，`int()` 只能轉換看起來就是整數的字串，如果輸入的是 `十八` 或 `18.5`，`int()` 都沒辦法轉換，會出現 `ValueError` 錯誤：

```
ValueError: invalid literal for int() with base 10: '18.5'
```

帶小數點的字串，可以先用 `float()` 轉成浮點數，再用 `int()` 轉成整數，小數的部分會直接捨去：

```python
print(int(float("3.5")))
```

執行結果：

```
3
```

至於使用者輸入了無法轉換的內容時，要怎麼讓程式不要中斷，之後講到異常處理時再來說明。

---

這一章我們學會了用註解替程式加上說明，用 `print()` 與 `input()` 讓程式和使用者互動，也認識了字串、整數、浮點數與布林值這四種基本資料型態。型態不同的資料不能直接混在一起運算，遇到型態不合的錯誤時，可以先用 `type()` 確認它是什麼型態，再決定要怎麼轉換。

## 本章程式碼

- [GitHub](./code/) — 本章所有可執行範例
<!-- only:github,web -->
- [在 Colab 開啟](https://colab.research.google.com/github/wjweng/python-notes/blob/main/notebooks/02-variables-and-types.ipynb) — 用 Google 帳號登入就能執行，可以複製一份留在自己的雲端硬碟
<!-- /only -->
<!-- only:github,colab -->
- [在瀏覽器直接執行](https://wjweng.github.io/python-notes/web/02-variables-and-types.html) — 不用登入，開啟就能改程式碼看結果
<!-- /only -->
