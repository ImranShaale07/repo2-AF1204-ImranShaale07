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

# Sample data
data = pd.DataFrame({
    "Category": ["A", "B", "C"],
    "Values": [10, 20, 15]
})

# Plot
plt.figure()
plt.bar(data["Category"], data["Values"])
plt.title("Sample Data Chart")
plt.xlabel("Category")
plt.ylabel("Values")
plt.show()

# Project description
mo.md("""
## Project 1
This project demonstrates a simple data visualisation using Python.
""")

# Reflection
mo.md("""
## Reflection
I learned how to analyse and present data clearly using Python tools.
""")
