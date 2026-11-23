# random 模組：種子與狀態

透過 random 模組生成的隨機數並非是真正完全隨機的，而是由一套固定的演算法計算出來的（Python 使用的是梅森旋轉演算法，Mersenne Twister），因此這個特徵也被稱為是偽隨機（pseudo-random）。也因為是計算出來的，隨機數是可以被重現的，而重現隨機數的方式便是透過設定相同的種子（seed），或是設定隨機數生成器的狀態（state）來達成。

## 設定種子

設定隨機數生成器種子的方式如下：

```
random.seed([a])
```

- 當 `a` 被省略時，每次調用 random 模組的方法生成的數就會是隨機的。
- 當 `a` 被設定後，每次使用 `random.seed(a)` 後調用 random 模組的方法生成的數列就會是同一串。

`a` 除了整數，也可以是字串等型別。從 Python 3.11 開始，`a` 只能是 `None`、整數、浮點數、字串、`bytes` 或 `bytearray` 其中一種，例如以下用字串「weijie」當種子：

```python
import random

random.seed("weijie")
print(random.randint(1, 10))
```

執行結果：

```
8
```

以下範例展示利用設定相同的種子，在每個 for 迴圈中都產生同樣的亂數：

```python
import random

for i in range(5):
    random.seed(1)
    rand_int = random.randint(1, 10)
    print(f"loop {i}: {rand_int}")
```

執行結果：

```
loop 0: 3
loop 1: 3
loop 2: 3
loop 3: 3
loop 4: 3
```

### 在程式開頭設定一次種子

上面的範例每一輪都重新設定一次種子，所以每一輪都拿到同一個數字。一般的用法則是在程式開頭設定一次種子，之後產生的一整串隨機數就會固定下來。以下設定兩次相同的種子，各自連續產生 5 個隨機整數：

```python
import random

random.seed(1)
for i in range(5):
    print(random.randint(1, 10), end=" ")
print()

random.seed(1)
for i in range(5):
    print(random.randint(1, 10), end=" ")
print()
```

執行結果：

```
3 10 2 5 2
3 10 2 5 2
```

同一串裡的 5 個數字各不相同，看起來一樣是隨機的，但只要種子相同，整串數字就會完全一樣，重新執行整支程式也一樣。

[第 07 章](../07-random/)提到每次執行的結果都會不同，那是因為沒有設定種子。固定種子在除錯或測試時很有用，程式的結果跟預期不一樣時，固定種子就能讓每次執行都重現同一個情況，方便找出問題；把程式分享給別人時，對方設定同樣的種子，也能得到跟我們一樣的結果。

### 換了 Python 版本，結果可能不同

不過要注意，根據 Python 官方文件，random 模組大部分的演算法與設定種子的方式，都可能隨著 Python 的版本改變，只有 `random()` 函數產生的數列保證不變。因此同一個種子在不同版本的 Python 上，`randint()` 等函數的結果可能會不一樣。本章的執行結果是用 Python 3.13 跑出來的，也在 Python 3.12 實測過，結果相同；如果用其他版本跑出來的數字跟文章不同，並不是程式寫錯了。

## 儲存與還原狀態

我們也可以在調用 random 模組前，先用 `random.getstate()` 把隨機數生成器目前的狀態存起來：

```
rand_state = random.getstate()
```

並在下次調用 random 模組前設定相同的狀態，便可以得到相同的隨機結果：

```
random.setstate(rand_state)
```

以下範例是 `random.getstate()` 與 `random.setstate()` 的用法，先存下目前的狀態，接著產生兩個隨機整數，再還原狀態後產生第三個隨機整數：

```python
import random

rand_state = random.getstate()

rand_int = random.randint(1, 10)
print(f"Generate a random integer: {rand_int}")

rand_int = random.randint(1, 10)
print(f"Generate another random integer: {rand_int}")

random.setstate(rand_state)
rand_int = random.randint(1, 10)
print(f"Generate a random integer after restoring state: {rand_int}")
```

輸出結果每個人會不同，但第一行和第三行的數字一定相同，因為第三個數字是從還原後的同一個狀態產生的：

```
Generate a random integer: 2
Generate another random integer: 7
Generate a random integer after restoring state: 2
```

---

這一章我們學會了用 `random.seed()` 設定種子，讓隨機的結果可以重現，以及用 `random.getstate()` 與 `random.setstate()` 儲存與還原隨機數生成器的狀態。隨機的結果跟預期不一樣、想重現同一個情況時，可以先在程式開頭固定種子；跑出來的數字跟別人不同時，則可以確認雙方的種子與 Python 版本是否相同。

## 本章程式碼

- [GitHub](./code/) — 本章所有可執行範例
<!-- only:github,web -->
- [在 Colab 開啟](https://colab.research.google.com/github/wjweng/python-notes/blob/main/notebooks/08-random-seed.ipynb) — 用 Google 帳號登入就能執行，可以複製一份留在自己的雲端硬碟
<!-- /only -->
<!-- only:github,colab -->
- [在瀏覽器直接執行](https://wjweng.github.io/python-notes/web/08-random-seed.html) — 不用登入，開啟就能改程式碼看結果
<!-- /only -->
