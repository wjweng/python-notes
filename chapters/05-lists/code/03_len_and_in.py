"""用 len() 取得串列長度，用 in 檢查元素是否在串列裡。"""

city = ["台北", "桃園", "新竹", "台中", "台南"]
print(len(city))
print(city[len(city) - 1])

print("新竹" in city)
print("高雄" in city)
print("高雄" not in city)
