"""修改串列元素，以及在串列加入元素的幾種方法。"""

# 修改串列元素
student = ["小明", 140, 45]
student[2] = 50
print(student)

# 串列相加
city = ["台北", "桃園", "新竹", "台中", "台南"]
city = city + ["宜蘭"]
print(city)

# append()
city = ["台北", "桃園", "新竹", "台中", "台南"]
city.append(["花蓮", "台東"])
print(city)
print(city[5])
print(city[5][0])

# extend()
city = ["台北", "桃園", "新竹", "台中", "台南"]
city.extend(["澎湖", "金門"])
print(city)

city = ["台北", "桃園", "新竹", "台中", "台南"]
city.extend("宜蘭")
print(city)

# insert()
city = ["台北", "桃園", "新竹", "台中", "台南"]
city.insert(4, "嘉義")
print(city)

# append() 直接修改原本的串列，回傳值是 None
city = ["台北", "桃園", "新竹", "台中", "台南"]
city = city.append("宜蘭")
print(city)
