import marimo as mo
import pandas as pd
import matplotlib.pyplot as plt

# Title
mo.md("# Imran Shaale - Data Portfolio")

# About
mo.md("""
## About Me
I am a student developing data literacy skills using Python,
including data analysis and visualisation.
""")

# Skills
mo.md("""
## Skills
- Python
- pandas
- Data visualisation
- GitHub
""")

# ------------------------
# PROJECT 1 
# ------------------------

data = pd.DataFrame({
    "Study Hours": [1, 2, 3, 4, 5, 6, 7, 8],
    "Score": [50, 55, 65, 70, 75, 78, 85, 90],
    "Student": ["A", "B", "C", "D", "E", "F", "G", "H"]
})

plt.figure()
plt.plot(data["Study Hours"], data["Score"], marker='o')

# Add labels to each point
for i, txt in enumerate(data["Student"]):
    plt.annotate(txt, (data["Study Hours"][i], data["Score"][i]))

plt.title("Study Hours vs Exam Score")
plt.xlabel("Study Hours")
plt.ylabel("Score")
plt.grid()

plt.show()

mo.md("""
## Project 1: Study Time Analysis

This project analyses the relationship between study hours and exam performance.
Each data point represents an individual student, allowing comparison across multiple observations.

The visualisation shows a clear positive trend, suggesting that increased study time
is associated with higher academic performance.

Additional enhancements such as data labelling and gridlines improve readability
and support clearer interpretation of the results.
""")
# ------------------------
# PROJECT 2
# ------------------------

attendance_data = pd.DataFrame({
    "Attendance Rate": [60, 65, 70, 75, 80, 85, 90, 95],
    "Average Score": [48, 52, 58, 63, 68, 74, 81, 88]
})

plt.figure()
plt.bar(attendance_data["Attendance Rate"].astype(str), attendance_data["Average Score"])
plt.title("Attendance Rate vs Average Score")
plt.xlabel("Attendance Rate (%)")
plt.ylabel("Average Score")
plt.grid(axis="y")

plt.show()

mo.md("""
## Project 2: Attendance and Performance Analysis

This project explores the relationship between attendance rate and average academic performance.
The bar chart shows that higher attendance is associated with stronger average scores.

This demonstrates my ability to compare grouped data, use visualisation to highlight trends,
and communicate findings clearly.
""")
# ------------------------
# REFLECTION
# ------------------------

mo.md("""
## Reflection

I developed skills in structuring datasets using pandas and creating visualisations
using matplotlib. This project demonstrates my ability to analyse relationships
within data and present insights clearly and effectively.
""")
