"""range() 函數的三種用法、倒數，以及轉成串列。"""

for number in range(5):
    print(number, end=" ")
print()

for number in range(6, 11):
    print(number, end=" ")
print()

for number in range(0, 11, 2):
    print(number, end=" ")
print()

for number in range(10, 0, -2):
    print(number, end=" ")
print()

print(range(5))
print(list(range(5)))
