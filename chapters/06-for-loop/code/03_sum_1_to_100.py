"""從 1 加到 100，以及縮排對迴圈的影響。"""

total = 0
for number in range(1, 101):
    total += number
print(total)

print(sum(range(1, 101)))

total = 0
for number in range(1, 6):
    total += number
    print(total)
