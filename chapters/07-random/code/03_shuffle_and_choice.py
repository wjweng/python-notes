"""隨機排列串列，並從串列中隨機取出元素。"""

import random

cities = ["台北", "桃園", "新竹", "台中", "台南"]
random.shuffle(cities)
print(cities)

rand_city = random.choice(cities)
print(rand_city)

rand_city = random.choices(cities, [10, 20, 30, 40, 50], k=2)
print(rand_city)

rand_city = random.sample(cities, 2)
print(rand_city)

cities = ["台北", "桃園", "新竹", "台中", "台南"]
print(random.shuffle(cities))
print(cities)
