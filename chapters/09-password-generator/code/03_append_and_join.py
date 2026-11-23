"""串列 += 字串會拆成字元、append() 不會；用 join() 把串列接成字串。"""

password_list = []
password_list += "ab"
print(password_list)

password_list = []
password_list.append("ab")
print(password_list)

password_list = ["a", "b", "c"]
print("".join(password_list))
print("-".join(password_list))
