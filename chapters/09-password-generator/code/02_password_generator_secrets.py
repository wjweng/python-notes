"""密碼產生器：用 secrets 模組產生密碼（字元數目直接寫在變數裡）。"""

import secrets

numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
symbols = ["~", "!", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+"]
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
           "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
           "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
           "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

# 文章裡的版本用 input() 讓使用者輸入；這裡直接指定數目，CI 才能在沒有人輸入的情況下執行
num_numbers = 3
num_symbols = 4
num_letters = 5

password_list = []
for _ in range(num_numbers):
    password_list.append(secrets.choice(numbers))
for _ in range(num_symbols):
    password_list.append(secrets.choice(symbols))
for _ in range(num_letters):
    password_list.append(secrets.choice(letters))

secrets.SystemRandom().shuffle(password_list)

password = ""
for password_char in password_list:
    password += password_char
print(password)
