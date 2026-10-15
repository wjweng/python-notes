"""把串列指派給另一個變數不是複製；要複製請用 [:] 或 copy()。"""

# 兩個變數指向同一個串列
city = ["台北", "桃園", "新竹"]
my_city = city
my_city.append("台中")
print(city)

# 用 [:] 複製出另一個串列
city = ["台北", "桃園", "新竹"]
my_city = city[:]
my_city.append("台中")
print(city)
print(my_city)

# 複製只有外層，裡面的串列仍然是同一個
city = ["台北", ["花蓮", "台東"]]
my_city = city[:]
my_city[1].append("屏東")
print(city)
