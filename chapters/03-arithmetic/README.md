# 基本數學運算

## 四則運算

Python 的四則運算透過 `+`（加）、`-`（減）、`*`（乘）、`/`（除）等算術運算子，或是 `+=`、`-=`、`*=`、`/=` 等指派運算子來達成。這裡的 `+=` 若寫成 `a += b`，即等同於 `a = a + b` 的意思。

```python
# addition
integer_x = 1 + 2          # integer_x = 3
integer_x = integer_x + 1  # integer_x = 3 + 1 = 4
integer_x += 1             # integer_x = 4 + 1 = 5
print(integer_x)
```

```python
# subtraction
integer_x = 5 - 2          # integer_x = 5 - 2 = 3
integer_x = integer_x - 1  # integer_x = 3 - 1 = 2
integer_x -= 1             # integer_x = 2 - 1 = 1
print(integer_x)
```

```python
# multiplication
integer_x = 1 * 2          # integer_x = 1 * 2 = 2
integer_x = integer_x * 2  # integer_x = 2 * 2 = 4
integer_x *= 2             # integer_x = 4 * 2 = 8
print(integer_x)
```

```python
# division
float_x = 8 / 2            # float_x = 8 / 2 = 4.0
float_x = float_x / 2      # float_x = 4.0 / 2 = 2.0
float_x /= 2               # float_x = 2.0 / 2 = 1.0
print(float_x)
print(type(float_x))
```

須注意一旦做了除法（`/`）的運算，即使原本的資料型態是整數，也會被自動轉換成浮點數。計算結果如下：

```
5
1
8
1.0
<class 'float'>
```

同樣的，整數和浮點數混在一起運算時，結果也會是浮點數：

```python
print(1 + 2.0)
print(type(1 + 2.0))
```

執行結果：

```
3.0
<class 'float'>
```

另外，除數不能是 0，否則會產生錯誤：

```python
print(1 / 0)
```

錯誤訊息的最後一行如下：

```
ZeroDivisionError: division by zero
```

### 浮點數的誤差

浮點數的運算，有時候會得到有點奇怪的結果，例如：

```python
print(0.1 + 0.2)
print(round(0.1 + 0.2, 2))
```

執行結果：

```
0.30000000000000004
0.3
```

這並不是 Python 算錯了，而是電腦用二進位儲存小數，有些小數沒辦法剛好存下來，只能存一個非常接近的值，就像十進位沒辦法把 1/3 完整寫出來一樣。需要顯示結果時，可以用 `round()` 函數取到指定的小數位數，第二個參數就是要保留的位數。之後要比較兩個浮點數是否相等時，也要特別留意這個誤差。

## 商數和餘數

商數透過 `//` 及 `//=`、餘數透過 `%` 及 `%=` 來達成。

```python
# quotient
integer_x = 5 // 2  # 5 / 2 = 2 ... 1
print(integer_x)
```

```python
integer_x = 5
integer_x //= 2
print(integer_x)
```

```python
# remainder
integer_x = 5 % 2  # 5 / 2 = 2 ... 1
print(integer_x)
```

```python
integer_x = 5
integer_x %= 2
print(integer_x)
```

計算結果：

```
2
2
1
1
```

和 `/` 不同，`//` 兩邊都是整數時，計算結果也會是整數。

要注意的是，負數的商數是往比較小的方向取整數，而不是直接把小數去掉，所以 `-5 // 2` 會得到 `-3` 而不是 `-2`，餘數則是 `1`（因為 `-3 * 2 + 1 = -5`）：

```python
print(-5 // 2)
print(-5 % 2)
```

執行結果：

```
-3
1
```

如果商數和餘數都需要，可以用 `divmod()` 函數一次取得，結果會用括號把商數和餘數包在一起：

```python
print(divmod(5, 2))
```

執行結果：

```
(2, 1)
```

## 次方

次方透過 `**` 及 `**=` 來達成。

```python
# exponent
integer_x = 2 ** 3  # integer_x = 2 ** 3 = 8
print(integer_x)
```

```python
integer_x = 2
integer_x **= 3
print(integer_x)
```

計算結果：

```
8
8
```

要注意 Python 的次方是兩個星號，不是數學上常見的 `^`。`^` 在 Python 裡是另一種運算（XOR 位元運算），`2 ^ 3` 並不會得到 8：

```python
print(2 ^ 3)
```

執行結果：

```
1
```

另外，Python 的整數沒有大小上限，次方算出很大的數字也沒問題：

```python
print(2 ** 100)
```

執行結果：

```
1267650600228229401496703205376
```

## 運算的優先順序

如同我們在國小學習的四則運算，需記住一個 PEMDAS 原則，運算時的優先順序依序為括號優先、再來次方、乘除、最後是加減。

| 縮寫 | 英文 | 中文 |
| :--- | :--- | :--- |
| P | Parentheses | 括號 |
| E | Exponents | 次方 |
| MD | Multiplication and Division | 乘除 |
| AS | Addition and Subtraction | 加減 |

例如以下兩行，只差在有沒有括號，結果就不一樣：

```python
print(2 + 3 * 4)
print((2 + 3) * 4)
```

執行結果：

```
14
20
```

有幾個細節要注意：

- `//` 和 `%` 跟乘除在同一層，一樣由左而右計算，例如 `2 * 3 % 4` 會先算 `2 * 3` 得到 6，再取餘數得到 2
- 次方是例外，連續的次方是**由右而左**計算，`2 ** 3 ** 2` 會先算 `3 ** 2`，得到的是 2 的 9 次方
- 負號比次方晚算，`-2 ** 2` 等同於 `-(2 ** 2)`，想算負 2 的平方要寫成 `(-2) ** 2`

```python
print(2 * 3 % 4)
print(2 ** 3 ** 2)
print(-2 ** 2)
print((-2) ** 2)
```

執行結果：

```
2
512
-4
4
```

不確定先算哪一個的時候，加上括號最保險，程式也會比較容易閱讀。

---

這一章我們認識了 Python 的算術運算子與指派運算子，也看到了除法會產生浮點數、浮點數會有誤差、負數的商數往小的方向取整數這些容易踩到的細節。運算的順序大致跟數學一樣，遇到不確定的地方，用括號把想先算的部分包起來就好。

## 本章程式碼

- [GitHub](./code/) — 本章所有可執行範例
<!-- only:github,web -->
- [在 Colab 開啟](https://colab.research.google.com/github/wjweng/python-notes/blob/main/notebooks/03-arithmetic.ipynb) — 用 Google 帳號登入就能執行，可以複製一份留在自己的雲端硬碟
<!-- /only -->
<!-- only:github,colab -->
- [在瀏覽器直接執行](https://wjweng.github.io/python-notes/web/03-arithmetic.html) — 不用登入，開啟就能改程式碼看結果
<!-- /only -->
