"""if 敘述：縮排的那幾行只在條件成立時執行。"""

is_raining = True
if is_raining:
    print("Take an umbrella.")
print("Go out.")

# 條件不成立時，只會印出 Go out.
is_raining = False
if is_raining:
    print("Take an umbrella.")
print("Go out.")
