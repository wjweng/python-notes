# random 模組

當我們需要在程式中模擬或實作一些隨機發生的事件，例如模擬猜拳、丟骰子的結果，便需要程式可以根據開發者輸入的數值範圍、型態等，隨機產生一個結果，而 Python 的 random 模組便是用於實現這個功能。

## 匯入 random 模組

使用 `import` 匯入 random 模組。

```python
import random
```

匯入之後，就可以用「模組名稱.函數名稱」的方式呼叫模組裡的函數，例如 `random.randint()`，中間的 `.` 代表這個函數屬於 random 模組。模組的完整觀念會在後面的章節介紹，這一章只要記得使用前先匯入、呼叫時加上 `random.` 就可以了。

### 忘了匯入模組

如果忘了寫 `import random` 就直接呼叫，例如：

```
print(random.randint(1, 9))
```

錯誤訊息的最後一行如下，Python 也會提示我們是不是忘了匯入：

```
NameError: name 'random' is not defined. Did you forget to import 'random'?
```

### 檔案不要取名為 `random.py`

如果把自己的程式存成 `random.py`，`import random` 匯入的會是這個檔案本身，而不是 Python 內建的 random 模組，因此呼叫 `random.randint()` 時就會找不到這個函數。例如以下的程式存成 `random.py` 並執行：

```
import random
print(random.randint(1, 9))
```

錯誤訊息的最後一行很長，開頭如下：

```
AttributeError: module 'random' has no attribute 'randint'
```

這一行的後面，Python 會接著提示這個檔案和內建的 random 模組同名，建議我們把檔案改名（consider renaming）。遇到這個錯誤時，把檔案改成其他名字，例如本章範例使用的 `01_random_int.py` 就可以了。

## 產生隨機整數

以下幾個方法可以產生指定區間的隨機整數：

```
random.randrange([start, ]stop[, step])
```

- `start`：指定區間的起始值，若沒有輸入則預設為 0。
- `stop`：指定區間的結束值，不包含 `stop`。
- `step`：區間遞增的間隔，若沒有輸入則預設為 1。

```
random.randint(a, b)
```

- 產生一個 [`a`, `b`] 區間內的隨機整數。

例如，以下的程式碼會隨機產生 1 到 9 之間的整數：

```python
import random

rand_int = random.randrange(1, 10, 1)
print(rand_int)

rand_int = random.randint(1, 9)
print(rand_int)
```

輸出結果每個人會不同：

```
9
7
```

注意兩個函數結束值的差別：`randrange()` 的 `stop` 和[第 06 章](../06-for-loop/)的 `range()` 一樣不包含在內，所以要寫 10 才會產生到 9；`randint()` 則包含 `b`，寫 9 就會產生到 9。

每次執行的結果都會不同，這正是隨機的用意。如果想讓隨機的結果可以重現，例如除錯時希望每次都拿到同樣的數字，[下一章](../08-random-seed/)會介紹怎麼做。

## 產生隨機浮點數

以下幾個方法可以產生隨機浮點數：

```
random.random()
```

- 產生一個 [0.0, 1.0) 區間內的隨機浮點數。

```
random.uniform(a, b)
```

- 產生一個 [`a`, `b`]（如果 `a <= b`）或 [`b`, `a`]（如果 `b < a`）區間內的隨機浮點數。

```
random.expovariate(lambd)
```

- 產生一個服從指數分布的隨機浮點數，`lambd` 是期望平均值的倒數。參數名稱少了一個字母 a，是因為 `lambda` 在 Python 裡是保留字，不能拿來當參數名稱。

```
random.gauss(mu, sigma)
random.normalvariate(mu, sigma)
```

- 產生一個平均為 `mu`、標準差為 `sigma` 的常態分布的隨機浮點數。

`gauss()` 和 `normalvariate()` 產生的都是常態分布的隨機數。根據 Python 官方文件，`gauss()` 稍微快一些，但在多執行緒（multithreading）的程式裡，兩個執行緒同時呼叫時可能會拿到相同的值；在本章的練習兩者擇一使用即可。

以下範例依序用上面五個函數產生隨機浮點數，其中指數分布的 `lambd` 設為 0.1，兩個常態分布都設為平均 0、標準差 1：

```python
import random

rand_float = random.random()
print(rand_float)

rand_float = random.uniform(0, 1)
print(rand_float)

rand_float = random.expovariate(0.1)
print(rand_float)

rand_float = random.gauss(0, 1)
print(rand_float)

rand_float = random.normalvariate(0, 1)
print(rand_float)
```

輸出結果同樣每個人會不同：

```
0.8625930391422392
0.7556453212005825
0.13170214600390084
0.5748607231832283
-0.09085395755220001
```

## 隨機排列與取出元素

和隨機整數及隨機浮點數相同，我們也可在一組序列資料中隨機取出一筆資料或資料集合：

```
random.shuffle(x)
```

- 使序列資料 `x` 重新隨機排列。

```
random.choice(x)
```

- 從序列資料 `x` 中隨機取出一個元素。

```
random.choices(x, weights=None, *, cum_weights=None, k=1)
```

- 從序列資料 `x` 中隨機取出 `k` 個元素，同一個元素可能被重複取出，並可設定每個元素取出的權重（weights）或累積權重（cum_weights）。
- `*` 後面的 `cum_weights` 和 `k` 只能用名稱指定，例如要取出 2 個元素時要寫成 `k=2`，不能只寫 2。

```
random.sample(x, k)
```

- 從序列資料 `x` 中隨機取出 `k` 個不重複的元素。

以下範例以[第 05 章](../05-lists/)串列的例子，展示隨機排列與取出元素的結果：

```python
import random

cities = ["台北", "桃園", "新竹", "台中", "台南"]
random.shuffle(cities)
print(cities)

rand_city = random.choice(cities)
print(rand_city)

rand_city = random.choices(cities, [10, 20, 30, 40, 50], k=2)
print(rand_city)

rand_city = random.sample(cities, 2)
print(rand_city)
```

輸出結果也是每個人會不同：

```
['台中', '台南', '新竹', '桃園', '台北']
桃園
['台北', '桃園']
['台北', '台南']
```

### `shuffle()` 會直接修改原本的串列

`shuffle()` 和[第 05 章](../05-lists/)〈直接修改原本串列的方法〉一樣，是直接打亂原本的串列，並不會回傳一個新的串列，因此把它的結果印出來只會得到 `None`：

```python
import random

cities = ["台北", "桃園", "新竹", "台中", "台南"]
print(random.shuffle(cities))
print(cities)
```

執行結果（第二行每個人會不同）：

```
None
['台北', '新竹', '台南', '桃園', '台中']
```

也因為 `shuffle()` 要修改原本的資料，它不能用在字串這種無法修改的序列上：

```python
import random

random.shuffle("Python")
```

錯誤訊息的最後一行如下：

```
TypeError: 'str' object does not support item assignment
```

### `choices()` 與 `sample()` 的差別

`choices()` 和 `sample()` 都可以一次取出好幾個元素，差別在於 `choices()` 每次都從完整的串列裡取，同一個元素可能被取出好幾次；`sample()` 取出的元素則不會重複。以下兩者都從 5 個城市裡取出 5 個：

```python
import random

cities = ["台北", "桃園", "新竹", "台中", "台南"]
print(random.choices(cities, k=5))
print(random.sample(cities, 5))
```

輸出結果每個人會不同，這次 `choices()` 的結果裡「桃園」和「台北」都出現了兩次，`sample()` 則剛好是 5 個城市各一次：

```
['台南', '桃園', '桃園', '台北', '台北']
['台北', '桃園', '台中', '台南', '新竹']
```

也因為 `sample()` 不會重複，要取出的個數不能超過串列的長度：

```python
import random

cities = ["台北", "桃園", "新竹", "台中", "台南"]
print(random.sample(cities, 6))
```

錯誤訊息的最後一行如下：

```
ValueError: Sample larger than population or is negative
```

---

這一章我們學會了匯入 random 模組，以及產生隨機整數、隨機浮點數，和從串列中隨機排列與取出元素的方法。遇到 `NameError` 時，可以先檢查是不是忘了匯入模組；遇到 `AttributeError` 時，則可以確認自己的檔案是不是取名為 `random.py`。

## 本章程式碼

- [GitHub](./code/) — 本章所有可執行範例
<!-- only:github,web -->
- [在 Colab 開啟](https://colab.research.google.com/github/wjweng/python-notes/blob/main/notebooks/07-random.ipynb) — 用 Google 帳號登入就能執行，可以複製一份留在自己的雲端硬碟
<!-- /only -->
<!-- only:github,colab -->
- [在瀏覽器直接執行](https://wjweng.github.io/python-notes/web/07-random.html) — 不用登入，開啟就能改程式碼看結果
<!-- /only -->
