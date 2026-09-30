"""型態轉換：把整數轉成字串再相加，或用 f-string 直接帶入。"""

integer_data = 123 + 456

# type conversion
string_integer_data = str(integer_data)
print("Integer data is " + string_integer_data)

# f-string
print(f"Integer data is {integer_data}")

# 帶小數點的字串要先轉成 float，再轉成 int
print(int(float("3.5")))
