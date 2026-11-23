"""break：跳出迴圈。sort() 排序、break 只跳出最內層、for ... else。"""

import random

# break
random.seed(1)
scores_list = []
for _ in range(10):
    scores_list.append(random.randint(0, 100))
scores_list.sort(reverse=True)
print(scores_list)

for score in scores_list:
    if score > 60:
        print(score, end=" ")
    else:
        break
print()

numbers = [3, 1, 2]
print(numbers.sort())
print(numbers)
numbers.sort(reverse=True)
print(numbers)

for i in range(1, 4):
    for j in range(1, 4):
        if j == 2:
            break
        print(f"i = {i}, j = {j}")

scores_list = [97, 97, 72, 63]
for score in scores_list:
    if score <= 60:
        print(f"Found {score}")
        break
else:
    print("All scores are above 60")

scores_list = [97, 97, 72, 63, 60]
for score in scores_list:
    if score <= 60:
        print(f"Found {score}")
        break
else:
    print("All scores are above 60")
