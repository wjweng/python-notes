"""choices() 可能重複取出同一個元素，sample() 不會。"""

import random

cities = ["台北", "桃園", "新竹", "台中", "台南"]
print(random.choices(cities, k=5))
print(random.sample(cities, 5))
