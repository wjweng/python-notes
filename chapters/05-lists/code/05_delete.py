"""刪除串列元素：del、pop()、remove()。"""

# del
city = ["台北", "桃園", "新竹", "台中", "台南"]
del city[4]
print(city)

# pop()
city = ["台北", "桃園", "新竹", "台中", "台南"]
print(city.pop())
print(city)
print(city.pop(1))
print(city)

# remove()
city = ["台北", "桃園", "新竹", "台中", "台南"]
city.remove("台中")
print(city)
