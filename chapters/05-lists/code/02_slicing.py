"""串列切片：一次取得多個元素，超出範圍的部分會被忽略。"""

city = ["台北", "桃園", "新竹", "台中", "台南"]
print(city[2:5])
print(city[:2])
print(city[2:])
print(city[1:5:2])
print(city[:])

# 切片超出範圍不會產生錯誤
print(city[3:10])
