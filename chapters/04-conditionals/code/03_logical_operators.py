"""邏輯運算子 and、or、not，以及連鎖比較。"""

# and
print((1 < 2) and (2 < 3))
print((1 < 2) and (3 < 2))

# or
print((1 < 2) or (3 < 2))
print((2 < 1) or (3 < 2))

# not
print(not (1 > 2))
print(not (1 < 2))

# chained comparison
bmi = 23.1
print(bmi >= 18.5 and bmi < 24)
print(18.5 <= bmi < 24)
