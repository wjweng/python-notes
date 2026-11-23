"""continue：跳過這一輪剩下的程式，直接進入下一輪。"""

# continue
odd_list = []
for i in range(1, 10):
    if i % 2 == 0:
        continue
    odd_list.append(i)
print(odd_list)
