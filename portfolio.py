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
        """
        # Imran Shaale - Data Portfolio

        This portfolio showcases my developing data literacy skills in Python, data analysis,
        visualisation, and reproducible digital workflows.

        It presents a selection of small projects that demonstrate how I structure data,
        analyse relationships between variables, create visualisations, and communicate insights clearly.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## About Me

        I am a student building practical skills in coding, data analysis, and communication.
        Through this portfolio, I present examples of how I use Python to explore datasets,
        create visualisations, and explain findings in a clear and accessible way.
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
        - Basic analytical interpretation
        """
    )
    return


@app.cell
def __(mo):
    mo.md("## Projects")
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
    fig1, ax = plt.subplots(figsize=(7, 4.5))
    ax.scatter(study_data["Study Hours"], study_data["Score"])

    for i, student in enumerate(study_data["Student"]):
        ax.annotate(
            student,
            (study_data["Study Hours"][i], study_data["Score"][i]),
            xytext=(5, 5),
            textcoords="offset points"
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
        """
        ### Project 1: Study Time Analysis

        This project investigates the relationship between study time and exam performance
        using Python, pandas, and matplotlib.

        I structured the dataset in a pandas DataFrame and created a scatter plot to visualise
        the relationship between study hours and exam scores. Each point represents an
        individual student, allowing patterns across multiple observations to be compared.

        The visualisation suggests a clear positive relationship between study time and academic
        performance, with students who study more tending to achieve higher scores.

        This project demonstrates my ability to:
        - structure tabular data using pandas
        - visualise relationships between variables
        - communicate findings clearly through annotated charts
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        """
        **Figure 1.** Scatter plot showing a positive relationship between study hours and exam scores.
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
    fig2, ax = plt.subplots(figsize=(7, 4.5))
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
        ### Project 2: Attendance and Performance Analysis

        This project explores the relationship between attendance rate and average academic performance.

        Using pandas, I structured attendance and performance data into a DataFrame and used
        matplotlib to create a bar chart comparing average scores across attendance levels.

        The visualisation suggests that stronger attendance is associated with better academic
        performance. This indicates that regular engagement may contribute positively to outcomes,
        although other factors may also influence results.

        This project demonstrates my ability to:
        - compare grouped data
        - identify trends across categories
        - present data-driven insights in a clear visual format
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        """
        **Figure 2.** Bar chart comparing average academic scores across different attendance rates.
        """
    )
    return


@app.cell
def __(pd):
    stock_data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Company A": [100, 105, 110, 108, 115, 120],
        "Company B": [95, 97, 96, 100, 103, 107]
    })
    return stock_data,


@app.cell
def __(plt, stock_data):
    fig3, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(stock_data["Month"], stock_data["Company A"], marker="o", label="Company A")
    ax.plot(stock_data["Month"], stock_data["Company B"], marker="o", label="Company B")

    ax.set_title("Sample Stock Price Comparison")
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
        """
        ### Project 3: Financial Trend Comparison

        This project presents a simple comparison of stock price movements across two companies
        over time.

        I used pandas to structure time-series data and matplotlib to visualise trends using a
        line chart. This type of analysis is useful for comparing relative performance and
        observing differences in growth patterns over a sequence of periods.

        The chart shows that both companies experienced upward movement overall, although
        Company A displayed stronger growth across the period shown.

        This project demonstrates my ability to:
        - work with time-series style data
        - compare trends across multiple variables
        - present financial-style data visually and clearly
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        """
        **Figure 3.** Line chart comparing sample stock price movements across two companies.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## Technical Journey

        Throughout this module, I developed my data literacy skills progressively, starting with
        foundational Python concepts and advancing towards more structured data analysis and
        communication techniques.

        In the early weeks, I built a foundation in Python programming, including data types,
        control flow, indexing, and working with structured data using pandas. I also developed
        basic visualisation skills using matplotlib and began working with marimo to create
        reactive notebooks and web-based outputs.

        As the module progressed, I developed stronger analytical skills such as data cleaning,
        handling missing values, and producing more meaningful visualisations. My project work
        reflects this development through the analysis of relationships between variables and the
        communication of insights using charts.

        I also explored broader concepts such as structured workflows, regression ideas, and the
        importance of preparing data carefully before analysis. In addition, I extended my learning
        by developing this portfolio using GitHub Pages and presenting my work in a more
        professional and accessible format.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## Reflection

        Through this portfolio, I developed practical skills in structuring and analysing data
        using pandas, as well as creating clear and effective visualisations using matplotlib.

        One of the most important areas of development for me was learning how to move beyond
        writing code and towards interpreting results. I improved my ability to identify patterns
        in datasets, explain their meaning clearly, and present technical work in a structured way.

        This portfolio reflects my progression from learning fundamental programming concepts to
        applying them in practical data analysis scenarios. It also demonstrates my ability to
        present technical work clearly and professionally, which is an important skill for
        data-driven and analytical roles.

        Going forward, I would like to continue developing my skills by working with larger
        real-world datasets, applying more advanced statistical techniques, and building more
        interactive data applications.
        """
    )
    return


if __name__ == "__main__":
    app.run()