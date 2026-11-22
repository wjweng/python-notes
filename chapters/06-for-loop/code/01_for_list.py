"""用 for 迴圈依序取出串列與字串的每一個元素。"""

cities = ["台北", "桃園", "新竹", "台中", "台南"]
print(cities[0])
print(cities[1])
print(cities[2])
print(cities[3])
print(cities[4])

for city in cities:
    print(city)
print("迴圈結束後：" + city)

nums = [1, 2, 3]
for x in nums:
    x = x * 2
print(nums)

for char in "Python":
    print(char)
