# 基本 for 迴圈

當我們需要重複一系列有規則的行為，例如從 1 加到 100，或是取得物件裡面的每一個元素，例如將串列裡面的每個元素印出，重複地撰寫程式碼顯然不切實際，for 迴圈便是可以讓程式對可迭代物件（iterable object）執行迭代（iteration）的工具。

## for 迴圈基本語法

for 迴圈的基本語法如下：

```
for item in object:
    Do something to each item
```

以前面熟悉的串列來說，假如要將 `cities` 串列裡面的所有元素印出，在這之前只能一行一行寫 `print()`：

```python
cities = ["台北", "桃園", "新竹", "台中", "台南"]
print(cities[0])
print(cities[1])
print(cities[2])
print(cities[3])
print(cities[4])
```

利用 for 迴圈，相同的工作，現在只要兩行程式碼就能解決，當串列內的元素愈來愈多後，for 迴圈的優勢便更會顯現出來。

```python
cities = ["台北", "桃園", "新竹", "台中", "台南"]
for city in cities:
    print(city)
```

執行結果：

```
台北
桃園
新竹
台中
台南
```

如同第 04 章的 if 敘述，for 那一行的最後也要有冒號 `:`，下面縮排的程式碼區塊就是每一輪都會執行的部分。每一輪開始時，`city` 會依序指向 `cities` 裡的下一個元素，因此第一輪印出「台北」、第二輪印出「桃園」，直到最後一個元素印完，迴圈就結束了。

### 迴圈結束之後的迴圈變數

迴圈結束之後，`city` 這個變數並不會消失，它的值會停在最後一輪拿到的元素。以下在迴圈之外多印一次 `city`：

```python
cities = ["台北", "桃園", "新竹", "台中", "台南"]
for city in cities:
    print(city)
print("迴圈結束後：" + city)
```

執行結果：

```
台北
桃園
新竹
台中
台南
迴圈結束後：台南
```

### 修改迴圈變數不會改到串列

在迴圈裡替迴圈變數重新指定一個值，並不會改到串列本身的內容：

```python
nums = [1, 2, 3]
for x in nums:
    x = x * 2
print(nums)
```

執行結果：

```
[1, 2, 3]
```

第 05 章〈複製串列〉提到，`my_city = city` 是讓兩個變數指向同一個串列。同樣地，每一輪的 `x` 也只是暫時指向串列裡的一個元素，`x = x * 2` 是讓 `x` 改指向一個新的值，串列裡原本的元素並沒有被替換，因此印出來的 `nums` 還是原來的樣子。要產生一個每個元素都乘以 2 的新串列，後面的章節會介紹更適合的寫法。

## 字串也可以用 for 迴圈

for 迴圈可以用在任何可迭代物件上，不只是串列。例如字串也是可迭代物件，用 for 迴圈就能一個字一個字取出來：

```python
for char in "Python":
    print(char)
```

執行結果：

```
P
y
t
h
o
n
```

## `range()` 函數

`range()` 函數的目的是產生一個等差數列的可迭代物件，它在 for 迴圈的計數中很常被用到，它的語法如下：

```
range(start, stop[, step])
```

- `start`：數列的起始數字，若沒有輸入則預設為 0。
- `stop`：數列到此數字之前必須停止，亦即不包含 `stop`。
- `step`：數列的間隔，若沒有輸入則預設為 1。

由上可知，`range()` 函數可以有三種用法：

- 傳入一個參數

```python
for number in range(5):
    print(number, end=" ")
```

執行結果：

```
0 1 2 3 4
```

`print()` 函數預設每印完一次就會換行，加上 `end=" "` 之後，每次印完改成接一個空白，數字才會排在同一行。

- 傳入兩個參數

```python
for number in range(6, 11):
    print(number, end=" ")
```

執行結果：

```
6 7 8 9 10
```

- 傳入三個參數

```python
for number in range(0, 11, 2):
    print(number, end=" ")
```

執行結果：

```
0 2 4 6 8 10
```

`step` 也可以是負數，這時數列會由大到小倒數，注意 `stop` 一樣不包含在內：

```python
for number in range(10, 0, -2):
    print(number, end=" ")
```

執行結果：

```
10 8 6 4 2
```

### `range()` 產生的不是串列

直接把 `range()` 印出來，看到的並不是一串數字：

```python
print(range(5))
```

執行結果：

```
range(0, 5)
```

`range()` 產生的是一個 range 物件，它不會一次把所有數字存起來，而是在 for 迴圈需要時才依序給出下一個數字。想看看裡面有哪些數字，可以用 `list()` 函數把它轉成串列：

```python
print(list(range(5)))
```

執行結果：

```
[0, 1, 2, 3, 4]
```

## 從 1 加到 100

因此，若要從 1 加到 100，也不用那麼辛苦從 1 + 2 + 3 + ... 一直寫到一百，只要幾行程式就能解決。

```python
total = 0
for number in range(1, 101):
    total += number
print(total)
```

執行結果：

```
5050
```

因為 `range()` 不包含 `stop`，要讓數列算到 100，`stop` 就要寫成 101。若寫成 `range(1, 100)`，數列只會到 99，加總的結果也會少了 100。

### 變數不要取名為 `sum`

這裡的變數取名為 `total`，而不是 `sum`，因為 `sum` 是 Python 內建函數的名字。若把它拿來當變數名稱，這個名字就會改指向一個整數，之後再呼叫 `sum()` 函數時就會產生錯誤：

```python
sum = 0
for number in range(1, 101):
    sum += number
print(sum([1, 2]))
```

錯誤訊息的最後一行如下：

```
TypeError: 'int' object is not callable
```

其實 `sum()` 函數本身就可以把可迭代物件裡的數字全部加起來，從 1 加到 100 也可以只寫一行：

```python
print(sum(range(1, 101)))
```

執行結果：

```
5050
```

### 縮排決定哪些程式碼會重複

前面加總的例子裡，`print(total)` 沒有縮排，它在 for 迴圈之外，等迴圈全部跑完才執行一次。若把它也縮排到迴圈裡面，它就會變成每一輪都執行，印出每一輪加完之後的累計值。為了不要印出 100 行，以下改成從 1 加到 5：

```python
total = 0
for number in range(1, 6):
    total += number
    print(total)
```

執行結果：

```
1
3
6
10
15
```

---

這一章我們學會了用 for 迴圈依序取出串列與字串裡的每一個元素，以及用 `range()` 函數產生要計數的數列。迴圈的結果跟預期的不一樣時，可以先檢查縮排，看看哪些程式碼在迴圈裡面、哪些在外面；數列少了最後一個數字時，則可以確認 `stop` 是不是需要再加 1。

## 本章程式碼

- [GitHub](./code/) — 本章所有可執行範例
<!-- only:github,web -->
- [在 Colab 開啟](https://colab.research.google.com/github/wjweng/python-notes/blob/main/notebooks/06-for-loop.ipynb) — 用 Google 帳號登入就能執行，可以複製一份留在自己的雲端硬碟
<!-- /only -->
<!-- only:github,colab -->
- [在瀏覽器直接執行](https://wjweng.github.io/python-notes/web/06-for-loop.html) — 不用登入，開啟就能改程式碼看結果
<!-- /only -->
