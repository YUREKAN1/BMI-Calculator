
from bmi_calculator import calculate_bmi, classify_bmi


# Test BMI calculation
weight = 70
height = 1.75

bmi = calculate_bmi(weight, height)
category = classify_bmi(bmi)

print("BMI:", bmi)
print("Category:", category)


# Test all BMI categories
test_values = [17.5, 22.5, 27.5, 32.0]

for value in test_values:
    print(value, "->", classify_bmi(value))


# Test invalid inputs
try:
    calculate_bmi(-70, 1.75)
except ValueError as error:
    print("Validation:", error)
