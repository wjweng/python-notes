"""用 random.seed() 設定種子，讓隨機的結果可以重現。"""

import random

random.seed("weijie")
print(random.randint(1, 10))

for i in range(5):
    random.seed(1)
    rand_int = random.randint(1, 10)
    print(f"loop {i}: {rand_int}")

random.seed(1)
for i in range(5):
    print(random.randint(1, 10), end=" ")
print()

random.seed(1)
for i in range(5):
    print(random.randint(1, 10), end=" ")
print()
