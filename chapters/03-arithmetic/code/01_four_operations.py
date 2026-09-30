"""四則運算：算術運算子與指派運算子。"""

# addition
integer_x = 1 + 2          # integer_x = 3
integer_x = integer_x + 1  # integer_x = 3 + 1 = 4
integer_x += 1             # integer_x = 4 + 1 = 5
print(integer_x)

# subtraction
integer_x = 5 - 2          # integer_x = 5 - 2 = 3
integer_x = integer_x - 1  # integer_x = 3 - 1 = 2
integer_x -= 1             # integer_x = 2 - 1 = 1
print(integer_x)

# multiplication
integer_x = 1 * 2          # integer_x = 1 * 2 = 2
integer_x = integer_x * 2  # integer_x = 2 * 2 = 4
integer_x *= 2             # integer_x = 4 * 2 = 8
print(integer_x)

# division
float_x = 8 / 2            # float_x = 8 / 2 = 4.0
float_x = float_x / 2      # float_x = 4.0 / 2 = 2.0
float_x /= 2               # float_x = 2.0 / 2 = 1.0
print(float_x)
print(type(float_x))

# 整數與浮點數混合運算，結果是浮點數
print(1 + 2.0)
print(type(1 + 2.0))
