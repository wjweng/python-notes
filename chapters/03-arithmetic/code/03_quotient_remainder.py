"""商數與餘數。"""

# quotient
integer_x = 5 // 2  # 5 / 2 = 2 ... 1
print(integer_x)

integer_x = 5
integer_x //= 2
print(integer_x)

# remainder
integer_x = 5 % 2  # 5 / 2 = 2 ... 1
print(integer_x)

integer_x = 5
integer_x %= 2
print(integer_x)

# 負數的商數往比較小的方向取整數
print(-5 // 2)
print(-5 % 2)

# 一次取得商數和餘數
print(divmod(5, 2))
