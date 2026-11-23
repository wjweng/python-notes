# 專題：密碼產生器

綜合前幾章所學的內容，這裡實作了一個專題－密碼產生器。在這個專題中，我們運用了[變數](../02-variables-and-types/)、[串列](../05-lists/)、[for 迴圈](../06-for-loop/)、[random 模組](../07-random/)等概念，讓使用者可以從數字、符號、英文字母中指定字元的數目，隨機生成一串密碼。

以下分成幾個步驟說明，每一段程式碼都只是完整程式的一部分，要實際執行的話，可以直接使用文末〈完整程式〉的程式碼。

## 匯入模組與準備候選字元

首先，先匯入 random 模組。

```python
import random
```

利用串列定義出隨機密碼的候選字元，在這裡設定了三組集合，分別是數字 0~9、特殊符號、以及英文大小寫字母。

```python
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
symbols = ["~", "!", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+"]
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
           "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
           "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
           "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
```

## 輸入字元數目

接著，我們讓使用者輸入在每組字元的集合中，各選出需要幾個字元來隨機組合出密碼。

```python
print("Password Generator")
num_numbers = int(input("How many numbers would you like in your password?\n"))
num_symbols = int(input("How many symbols would you like in your password?\n"))
num_letters = int(input("How many letters would you like in your password?\n"))
```

這裡用 `int()` 把輸入的內容轉成整數。如同[第 02 章](../02-variables-and-types/)〈`input()` 拿到的都是字串〉提到的，如果輸入的不是整數，例如「三」，`int()` 沒辦法轉換，程式就會出現 `ValueError` 錯誤而中止。

## 隨機取出字元

定義一個空的串列 `password_list`，並從各個集合中利用 `random.choice()` 隨機取出指定個數的字元，逐步加到這個串列中。

```python
password_list = []
for _ in range(num_numbers):
    password_list.append(random.choice(numbers))
for _ in range(num_symbols):
    password_list.append(random.choice(symbols))
for _ in range(num_letters):
    password_list.append(random.choice(letters))
```

這裡的 for 迴圈只是用來重複指定的次數：`range(num_numbers)` 會產生 `num_numbers` 個數字，迴圈就執行幾輪。迴圈變數用不到，因此如同[第 08 章](../08-random-seed/)〈在程式開頭設定一次種子〉提到的，取名為底線 `_`。

### 為什麼用 `append()`

把字元加進串列，用的是[第 05 章](../05-lists/)的 `append()`。如果寫成 `password_list += random.choice(numbers)` 也可以執行，因為串列用 `+=` 加上一個字串時，會把字串拆成一個一個字元再加進去。這裡每個候選字元都只有一個字，所以結果剛好相同，但只要候選裡有兩個字以上的元素，就會被拆開：

```python
password_list = []
password_list += "ab"
print(password_list)

password_list = []
password_list.append("ab")
print(password_list)
```

執行結果：

```
['a', 'b']
['ab']
```

## 洗牌

此時，雖然需要的字元已經隨機被取出，但 `password_list` 中仍是相同類型的字元緊鄰在一起，前段是數字、中段是特殊符號、後段是英文字母，因此我們必須再做一次「洗牌」的動作，才能讓密碼的排列真正變成隨機。

```python
random.shuffle(password_list)
```

## 組合成字串

最後，將串列的內容處理一下變成字串印出。

```python
password = ""
for password_char in password_list:
    password += password_char
print(password)
```

### 用 `join()` 組合字串

把串列裡的字串接成一個字串，也可以用字串的 `join()` 方法一行完成。`join()` 會用前面的字串，把串列裡的每個元素接起來，前面是空字串 `""` 的話，就是直接接在一起：

```python
password_list = ["a", "b", "c"]
print("".join(password_list))
print("-".join(password_list))
```

執行結果：

```
abc
a-b-c
```

因此上面組合密碼的四行程式，也可以寫成 `print("".join(password_list))`。

## 完整程式

把上面的步驟組合起來，完整的程式如下：

```python
import random

numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
symbols = ["~", "!", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+"]
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
           "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
           "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
           "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

print("Password Generator")
num_numbers = int(input("How many numbers would you like in your password?\n"))
num_symbols = int(input("How many symbols would you like in your password?\n"))
num_letters = int(input("How many letters would you like in your password?\n"))

password_list = []
for _ in range(num_numbers):
    password_list.append(random.choice(numbers))
for _ in range(num_symbols):
    password_list.append(random.choice(symbols))
for _ in range(num_letters):
    password_list.append(random.choice(letters))

random.shuffle(password_list)

password = ""
for password_char in password_list:
    password += password_char
print(password)
```

以下是執行結果，最後一行的密碼每個人會不同：

```
Password Generator
How many numbers would you like in your password?
3
How many symbols would you like in your password?
4
How many letters would you like in your password?
5
#n~1$3D7XRo!
```

## 用 secrets 模組產生密碼

這個密碼產生器拿來練習沒有問題，但如果要產生真正要使用的密碼，就不適合用 random 模組。[第 08 章](../08-random-seed/)提到，random 模組的隨機數是由演算法計算出來的，只要知道種子，就能算出同一串數字。這在模擬與除錯時很方便，但用在密碼上，就代表密碼有機會被推算出來。

Python [官方文件](https://docs.python.org/3.13/library/random.html)也提醒，random 模組不應該用在安全相關的用途，而是建議改用 [secrets 模組](https://docs.python.org/3.13/library/secrets.html)。secrets 模組使用作業系統提供的亂數來源，適合用來產生密碼、驗證用的代碼等需要保密的資料。

secrets 模組同樣有 `secrets.choice()`，用法和 `random.choice()` 相同；洗牌則是先用 `secrets.SystemRandom()` 建立一個使用作業系統亂數來源的產生器，再呼叫它的 `shuffle()`。把完整程式裡用到 random 的五行換掉即可，其他程式都不用改：

```python
import secrets

numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
symbols = ["~", "!", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+"]
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
           "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
           "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
           "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

print("Password Generator")
num_numbers = int(input("How many numbers would you like in your password?\n"))
num_symbols = int(input("How many symbols would you like in your password?\n"))
num_letters = int(input("How many letters would you like in your password?\n"))

password_list = []
for _ in range(num_numbers):
    password_list.append(secrets.choice(numbers))
for _ in range(num_symbols):
    password_list.append(secrets.choice(symbols))
for _ in range(num_letters):
    password_list.append(secrets.choice(letters))

secrets.SystemRandom().shuffle(password_list)

password = ""
for password_char in password_list:
    password += password_char
print(password)
```

執行結果，最後一行的密碼同樣每個人會不同：

```
Password Generator
How many numbers would you like in your password?
3
How many symbols would you like in your password?
4
How many letters would you like in your password?
5
77Q((1m$nST&
```

---

這個專題我們綜合了串列、for 迴圈與 random 模組，做出一個可以指定字元數目的密碼產生器，也知道了需要保密的資料應該改用 secrets 模組來產生。程式出現 `ValueError` 時，可以先檢查輸入的是不是整數；密碼裡的字元看起來沒有打亂時，則可以確認洗牌的步驟有沒有執行到。

## 本章程式碼

- [GitHub](./code/) — 本章所有可執行範例
<!-- only:github,web -->
- [在 Colab 開啟](https://colab.research.google.com/github/wjweng/python-notes/blob/main/notebooks/09-password-generator.ipynb) — 用 Google 帳號登入就能執行，可以複製一份留在自己的雲端硬碟
<!-- /only -->
<!-- only:github,colab -->
- [在瀏覽器直接執行](https://wjweng.github.io/python-notes/web/09-password-generator.html) — 不用登入，開啟就能改程式碼看結果
<!-- /only -->
