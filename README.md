# BMI Calculator – OIBSIP Internship Task 2

A Python-based BMI Calculator developed as part of the Oasis Infobyte Internship Program (OIBSIP).

The application provides a graphical interface for calculating Body Mass Index (BMI), managing multiple users, storing historical records, and visualizing BMI trends.

## Features

- **BMI Calculation:** Calculates BMI using weight (kg) and height (m).
- **BMI Classification:** Underweight, Normal, Overweight, and Obese categories.
- **Graphical Interface:** Built using Python Tkinter.
- **Input Validation:** Handles empty, non-numeric, zero, and negative inputs.
- **Multi-user Support:** Create and select different users.
- **SQLite Database:** Stores user information and BMI history.
- **BMI History:** Displays date, weight, height, BMI, and category.
- **BMI Trend Chart:** Visualizes historical BMI measurements using Matplotlib.
- **Error Handling:** Handles database and input errors.

## BMI Categories

| BMI Range | Category |
|---|---|
| Below 18.5 | Underweight |
| 18.5 – 24.9 | Normal |
| 25 – 29.9 | Overweight |
| 30 and above | Obese |

## Technology Stack

- Python
- Tkinter
- SQLite
- Matplotlib

## Project Structure

```text
Yurekan_2/
├── main.py
├── bmi_calculator.py
├── database.py
├── charts.py
├── test_bmi.py
├── test_database.py
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YUREKAN1/OIBSIP-BMI-Calculator.git
cd OIBSIP-BMI-Calculator
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install matplotlib
```

Tkinter and SQLite are included with standard Python installations on most systems.

### 4. Run the application

```bash
python main.py
```

## Testing

Run the BMI calculation tests:

```bash
python test_bmi.py
```

Run the database tests:

```bash
python test_database.py
```

Check Python syntax:

```bash
python -m compileall -q .
```

## Important Note

BMI is a general screening measure and is not a medical diagnosis.

## Internship

**Program:** Oasis Infobyte Internship Program (OIBSIP)  
**Task:** Task 2 – BMI Calculator  
**Level:** Advanced

## Author

**Yurekan M**

GitHub: https://github.com/YUREKAN1
