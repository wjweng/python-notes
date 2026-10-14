"""BMI 計算機。文章中的版本用 input() 讀入身高和體重，這裡直接寫在程式裡。"""

height = 180.0  # centimeter
weight = 75.0   # kilogram

# calculate BMI
bmi = weight / ((height / 100) ** 2)

# BMI interpretation
if bmi < 18.5:
    print(f"Your BMI is {bmi}, and you are underweight.")
elif bmi < 24:
    print(f"Your BMI is {bmi}, and you have a normal weight.")
elif bmi < 27:
    print(f"Your BMI is {bmi}, and you are overweight.")
else:
    print(f"Your BMI is {bmi}, and you are obese.")
