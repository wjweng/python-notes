"""巢狀 for 迴圈：九九乘法表，以及內外層用了同一個變數名稱。"""

# nested for loop
for i in range(1, 10):
    for j in range(1, 10):
        print(f"{i}*{j}={i*j:<4}", end=" ")
    print()

for i in range(1, 4):
    print(f"外層開始：i = {i}")
    for i in range(1, 3):
        print(f"  內層：i = {i}")
    print(f"外層結束：i = {i}")
