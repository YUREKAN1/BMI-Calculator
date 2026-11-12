
def calculate_bmi(weight, height):
    """Calculate BMI using weight in kg and height in metres."""

    if weight <= 0:
        raise ValueError("Weight must be greater than zero.")

    if height <= 0:
        raise ValueError("Height must be greater than zero.")

    bmi = weight / (height ** 2)

    return round(bmi, 2)


def classify_bmi(bmi):
    """Classify BMI into standard categories."""

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"
