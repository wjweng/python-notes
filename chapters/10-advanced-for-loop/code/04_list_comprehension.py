"""串列綜合運算（list comprehension）。"""

import random

random.seed(1)
scores_list = []
for _ in range(10):
    scores_list.append(random.randint(0, 100))
print(scores_list)

random.seed(1)
scores_list = [random.randint(0, 100) for _ in range(10)]
print(scores_list)

odd_list = [i for i in range(1, 10) if i % 2 == 1]
print(odd_list)

add_to_10 = [[i, j] for i in range(1, 10) for j in range(1, 10) if i + j == 10]
print(add_to_10)

add_to_10 = []
for i in range(1, 10):
    for j in range(1, 10):
        if i + j == 10:
            add_to_10.append([i, j])
print(add_to_10)

numbers = [i if i % 2 == 1 else 0 for i in range(1, 10)]
print(numbers)
