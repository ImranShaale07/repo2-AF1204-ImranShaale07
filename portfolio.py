import marimo as mo

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
        r"""
        # Imran Shaale - Data Portfolio

        This portfolio showcases my developing data literacy skills in Python, data analysis,
        visualisation, and reproducible digital workflows.

        It presents a selection of projects that demonstrate how I structure data, analyse
        relationships between variables, create visualisations, and communicate insights clearly.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## About Me

        I am a student developing practical skills in coding, data analysis, and communication.
        This portfolio presents examples of how I use Python to work with structured datasets,
        create visualisations, and explain insights in a clear and professional way.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Skills

        - Python
        - pandas
        - matplotlib
        - Data analysis
        - Data visualisation
        - GitHub and GitHub Pages
        - marimo notebooks
        - Data communication
        """
    )
    return


@app.cell
def __(mo):
    mo.md("## Projects")
    return


@app.cell
def __(pd):
    study_data = pd.DataFrame(
        {
            "Study Hours": [1, 2, 3, 4, 5, 6, 7, 8],
            "Score": [50, 55, 65, 70, 75, 78, 85, 90],
            "Student": ["A", "B", "C", "D", "E", "F", "G", "H"],
        }
    )
    return study_data,


@app.cell
def __(plt, study_data):
    fig1, ax = plt.subplots(figsize=(7, 4.5))
    ax.scatter(study_data["Study Hours"], study_data["Score"])

    for i, student in enumerate(study_data["Student"]):
        ax.annotate(
            student,
            (study_data["Study Hours"][i], study_data["Score"][i]),
            xytext=(5, 5),
            textcoords="offset points",
        )

    ax.set_title("Study Hours vs Exam Score")
    ax.set_xlabel("Study Hours")
    ax.set_ylabel("Exam Score")
    ax.grid(True)
    plt.tight_layout()
    fig1
    return fig1,


@app.cell
def __(mo):
    mo.md(
        r"""
        ### Project 1: Study Time Analysis

        This project investigates the relationship between study time and exam performance.

        I structured the dataset using pandas and created a scatter plot using matplotlib
        to visualise the relationship between study hours and exam scores. Each point
        represents an individual student, allowing comparisons across multiple observations.

        The visualisation shows a clear positive relationship, suggesting that students who
        spend more time studying tend to achieve higher exam scores.

        This project demonstrates my ability to:
        - structure data in a pandas DataFrame
        - identify relationships between variables
        - communicate findings clearly using visualisation
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        **Figure 1.** Scatter plot showing a positive relationship between study hours and exam score.
        """
    )
    return


@app.cell
def __(pd):
    attendance_data = pd.DataFrame(
        {
            "Attendance Rate": [60, 65, 70, 75, 80, 85, 90, 95],
            "Average Score": [48, 52, 58, 63, 68, 74, 81, 88],
        }
    )
    return attendance_data,


@app.cell
def __(attendance_data, plt):
    fig2, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(
        attendance_data["Attendance Rate"].astype(str),
        attendance_data["Average Score"],
    )

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
        r"""
        ### Project 2: Attendance and Performance Analysis

        This project explores the relationship between attendance rate and average academic performance.

        Using pandas, I organised attendance and performance data into a structured dataset.
        I then used matplotlib to create a bar chart comparing average scores across different
        attendance levels.

        The chart suggests that stronger attendance is associated with better academic performance.
        This indicates that regular engagement may contribute positively to outcomes, although
        other factors may also influence results.

        This project demonstrates my ability to:
        - compare grouped data
        - identify trends across categories
        - present data-driven insights clearly
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        **Figure 2.** Bar chart comparing average academic scores across different attendance rates.
        """
    )
    return


@app.cell
def __(pd):
    financial_data = pd.DataFrame(
        {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Company A": [100, 104, 109, 112, 118, 123],
            "Company B": [95, 97, 99, 101, 103, 106],
        }
    )
    return financial_data,


@app.cell
def __(financial_data, plt):
    fig3, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(
        financial_data["Month"],
        financial_data["Company A"],
        marker="o",
        label="Company A",
    )
    ax.plot(
        financial_data["Month"],
        financial_data["Company B"],
        marker="o",
        label="Company B",
    )

    ax.set_title("Financial Trend Comparison")
    ax.set_xlabel("Month")
    ax.set_ylabel("Stock Price Index")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    fig3
    return fig3,


@app.cell
def __(mo):
    mo.md(
        r"""
        ### Project 3: Financial Trend Comparison

        This project presents a simple comparison of financial performance trends across two companies.

        I used pandas to structure time-series style data and matplotlib to create a line chart
        comparing indexed stock price movements over a six-month period. This type of visualisation
        is useful for identifying relative growth patterns and comparing performance across firms.

        The chart shows that both companies experienced upward movement, but Company A demonstrated
        stronger growth over the period shown.

        This project demonstrates my ability to:
        - work with financial-style time-series data
        - compare trends across multiple variables
        - communicate comparative insights using clear visualisation
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        **Figure 3.** Line chart comparing financial trends across two companies over time.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Technical Journey

        Throughout this module, I developed my data literacy skills progressively, beginning
        with foundational Python concepts and advancing towards more structured forms of data
        analysis and communication.

        In the early weeks, I built a strong foundation in Python programming, including data types,
        control flow, indexing, and the use of functions. I also learned how to work with structured
        data using pandas and create visualisations using matplotlib.

        As the module progressed, I developed stronger analytical skills such as data cleaning,
        handling missing values, and producing more meaningful visualisations. My project work reflects
        this development through the analysis of relationships between variables and the communication
        of insights through charts.

        I also explored broader analytical ideas such as structured workflows, regression concepts,
        and the importance of preparing data carefully before analysis. In addition, I extended my
        learning through self-exploration by developing this portfolio using marimo, GitHub, and
        GitHub Pages, which strengthened my ability to present technical work in a more professional
        and accessible format.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Reflection

        Through this portfolio, I developed practical skills in structuring and analysing data
        using pandas, as well as creating clear and effective visualisations using matplotlib.

        One of the most important areas of development for me was learning how to move beyond
        simply writing code and towards interpreting results. I improved my ability to identify
        patterns in datasets, explain their meaning clearly, and communicate technical work in a
        structured and professional way.

        This portfolio reflects my progression from learning fundamental programming concepts to
        applying them in practical data analysis scenarios. It also demonstrates my ability to
        present technical work clearly, which is an essential skill for data-driven and analytical roles.

        Going forward, I aim to continue developing my skills by working with larger real-world
        datasets, applying more advanced analytical methods, and building more interactive and
        automated data applications.
        """
    )
    return


if __name__ == "__main__":
    app.run()