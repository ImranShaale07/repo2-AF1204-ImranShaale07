import marimo as mo
import pandas as pd
import matplotlib.pyplot as plt

app = mo.App()

@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    return mo, pd, plt

@app.cell
def __(mo):
    mo.md(
        """
        # Imran Shaale - Data Portfolio

        This portfolio showcases my developing data literacy skills in Python,
        data analysis, visualisation, and reproducible digital workflows.
        """
    )
    return

@app.cell
def __(mo):
    mo.md(
        """
        ## About Me

        I am a student building practical skills in coding, data analysis,
        and communication. This portfolio presents examples of how I use
        Python to explore data, create visualisations, and explain insights clearly.
        """
    )
    return

@app.cell
def __(mo):
    mo.md(
        """
        ## Skills

        - Python
        - pandas
        - matplotlib
        - Data analysis
        - Data visualisation
        - GitHub and GitHub Pages
        - marimo notebooks
        """
    )
    return

@app.cell
def __(pd):
    study_data = pd.DataFrame({
        "Study Hours": [1, 2, 3, 4, 5, 6, 7, 8],
        "Score": [50, 55, 65, 70, 75, 78, 85, 90],
        "Student": ["A", "B", "C", "D", "E", "F", "G", "H"]
    })
    return study_data,

@app.cell
def __(plt, study_data):
    fig, ax = plt.subplots()
    ax.plot(study_data["Study Hours"], study_data["Score"], marker="o")

    for i, student in enumerate(study_data["Student"]):
        ax.annotate(student, (study_data["Study Hours"][i], study_data["Score"][i]))

    ax.set_title("Study Hours vs Exam Score")
    ax.set_xlabel("Study Hours")
    ax.set_ylabel("Score")
    ax.grid(True)

    plt.tight_layout()
    fig
    return fig,

@app.cell
def __(mo):
    mo.md(
        """
        ## Project 1: Study Time Analysis

        This project analyses the relationship between study hours and exam performance.
        Each data point represents an individual student, making it possible to compare
        performance across multiple observations.

        The visualisation shows a clear positive relationship between study time and score.
        This demonstrates my ability to structure data, explore relationships between variables,
        and communicate findings in a clear visual format.
        """
    )
    return

@app.cell
def __(pd):
    attendance_data = pd.DataFrame({
        "Attendance Rate": [60, 65, 70, 75, 80, 85, 90, 95],
        "Average Score": [48, 52, 58, 63, 68, 74, 81, 88]
    })
    return attendance_data,

@app.cell
def __(attendance_data, plt):
    fig2, ax = plt.subplots()
    ax.bar(attendance_data["Attendance Rate"].astype(str), attendance_data["Average Score"])

    ax.set_title("Attendance Rate vs Average Score")
    ax.set_xlabel("Attendance Rate (%)")
    ax.set_ylabel("Average Score")
    ax.grid(axis="y")

    plt.tight_layout()
    fig2
    return fig2,

@app.cell
def __(mo):
    mo.md(
        """
        ## Project 2: Attendance and Performance Analysis

        This project explores the relationship between attendance rate and average academic
        performance. The chart demonstrates a clear positive relationship between attendance
        and academic results.

        This demonstrates my ability to compare grouped data, identify trends, and present
        data-driven insights clearly.
        """
    )
    return

@app.cell
def __(mo):
    mo.md(
        """
        ## Technical Journey

        Throughout this module, I developed my data literacy skills progressively,
        starting with foundational Python concepts and advancing towards more complex
        data analysis and automation techniques.

        In Weeks 1 to 4, I built a foundation in Python programming, including data types,
        control flow, structured data handling, and visualisation. I also began working
        with marimo to create reactive notebooks and web-based outputs.

        As the module progressed, I developed stronger analytical skills such as data cleaning,
        handling missing values, and producing more meaningful visualisations. My project work
        reflects this development through the analysis of relationships between variables.

        I also explored broader analytical concepts including structured workflows, regression
        ideas, and data preparation methods. In addition, I extended my learning through
        self-exploration by developing this portfolio with GitHub Pages and improving its
        presentation using HTML and CSS.
        """
    )
    return

@app.cell
def __(mo):
    mo.md(
        """
        ## Reflection

        Through this portfolio, I developed strong skills in structuring and analysing data
        using pandas, as well as creating clear and effective visualisations using matplotlib.
        I improved my ability to interpret relationships within datasets and communicate
        insights in a structured and professional way.

        This project reflects my progression from learning fundamental programming concepts
        to applying them in practical data analysis scenarios. It also demonstrates my ability
        to present technical work clearly, which is an essential skill for data-driven roles.
        """
    )
    return

if __name__ == "__main__":
    app.run()
