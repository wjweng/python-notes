"""用 random.getstate() 與 random.setstate() 儲存與還原隨機數生成器的狀態。"""

import random

rand_state = random.getstate()

rand_int = random.randint(1, 10)
print(f"Generate a random integer: {rand_int}")

rand_int = random.randint(1, 10)
print(f"Generate another random integer: {rand_int}")

random.setstate(rand_state)
rand_int = random.randint(1, 10)
print(f"Generate a random integer after restoring state: {rand_int}")
