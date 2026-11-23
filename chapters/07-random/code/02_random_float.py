"""用五個函數產生不同分布的隨機浮點數。"""

import random

rand_float = random.random()
print(rand_float)

rand_float = random.uniform(0, 1)
print(rand_float)

rand_float = random.expovariate(0.1)
print(rand_float)

rand_float = random.gauss(0, 1)
print(rand_float)

rand_float = random.normalvariate(0, 1)
print(rand_float)
