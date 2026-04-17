import marimo as mo

app = mo.App()


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    import statsmodels.formula.api as smf
    from collections import Counter
    import re
    from pathlib import Path
    return mo, pd, plt, smf, Counter, re, Path


@app.cell
def __(mo, Path):
    base = mo.notebook_dir() or Path(".")
    return base


@app.cell
def __(mo):
    mo.md(
        r"""
        # Imran Shaale - Data Portfolio

        This portfolio showcases my development in Python, data analysis, visualisation,
        reproducible workflows, and technical communication across the module.

        It combines structured data analysis, visual presentation, introductory statistical
        interpretation, text-based analysis, and reflection on broader topics such as automation
        and AI-supported workflows.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## About Me

        I am a student developing practical skills in coding, data analysis, and communication.
        I am particularly interested in using data to identify patterns, compare outcomes,
        and present evidence-based conclusions in a clear and structured way.

        This portfolio demonstrates how I apply Python tools such as pandas, matplotlib,
        and marimo to work with datasets, create visualisations, and communicate insights
        professionally.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Skills

        - Python programming
        - pandas
        - matplotlib
        - marimo notebooks
        - data preparation and cleaning
        - exploratory data analysis
        - data visualisation
        - interpretation of results
        - summary statistics
        - simple regression
        - introductory text analysis
        - workflow and automation concepts
        - AI literacy and prompt design
        - GitHub and GitHub Pages
        - technical communication
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Module Skills Demonstrated

        This portfolio demonstrates practical skills developed through the module, including:

        - Python programming fundamentals
        - structuring data using pandas DataFrames
        - data visualisation using matplotlib
        - interpretation of relationships between variables
        - reproducible workflows using marimo
        - interactive presentation using notebook-style components
        - communication of analytical findings through written explanation

        In addition to core coding skills, this project also reflects self-directed exploration
        through the use of marimo, GitHub, GitHub Pages, and web presentation techniques.
        """
    )
    return


@app.cell
def __(mo):
    mo.md("## Projects")
    return


@app.cell
def __(mo):
    min_study_hours = mo.ui.slider(1, 8, value=1, label="Minimum study hours to display")
    attendance_threshold = mo.ui.slider(
        60, 95, value=60, step=5, label="Minimum attendance rate to display"
    )
    company_selector = mo.ui.dropdown(
        options=["Both", "Company A", "Company B"],
        value="Both",
        label="Financial trend view",
    )
    return min_study_hours, attendance_threshold, company_selector


@app.cell
def __(company_selector, mo, min_study_hours, attendance_threshold):
    mo.vstack(
        [
            mo.md("## Interactive Controls"),
            min_study_hours,
            attendance_threshold,
            company_selector,
        ]
    )
    return


@app.cell
def __(min_study_hours, pd):
    study_data = pd.DataFrame(
        {
            "Study Hours": [1, 2, 3, 4, 5, 6, 7, 8],
            "Score": [50, 55, 65, 70, 75, 78, 85, 90],
            "Student": ["A", "B", "C", "D", "E", "F", "G", "H"],
        }
    )
    study_filtered = study_data[study_data["Study Hours"] >= min_study_hours.value].copy()
    study_filtered["Performance Category"] = study_filtered["Score"].apply(
        lambda x: "High" if x >= 75 else "Moderate"
    )
    return study_data, study_filtered


@app.cell
def __(plt, study_filtered):
    fig1, ax = plt.subplots(figsize=(7, 4.5))
    ax.scatter(study_filtered["Study Hours"], study_filtered["Score"])

    for i, student in enumerate(study_filtered["Student"]):
        ax.annotate(
            student,
            (study_filtered["Study Hours"].iloc[i], study_filtered["Score"].iloc[i]),
            xytext=(5, 5),
            textcoords="offset points",
        )

    ax.set_title("Study Hours vs Exam Score")
    ax.set_xlabel("Study Hours")
    ax.set_ylabel("Exam Score")
    ax.grid(True)
    plt.tight_layout()
    fig1
    return fig1


@app.cell
def __(mo):
    mo.md(
        r"""
        ### Project 1: Study Time Analysis

        This project investigates the relationship between study time and exam performance.

        I structured the dataset using pandas and created a scatter plot using matplotlib
        to visualise the relationship between study hours and exam scores. Each point
        represents an individual student, allowing comparisons across multiple observations.

        The visualisation shows a positive relationship, suggesting that students who
        spend more time studying tend to achieve higher exam scores.

        This project demonstrates my ability to:
        - structure data in a pandas DataFrame
        - identify relationships between variables
        - communicate findings clearly using visualisation
        """
    )
    return


@app.cell
def __(mo, base):
    mo.image(src=str(base / "images" / "study_time.png"), width=500)
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
def __(study_data):
    study_summary = study_data[["Study Hours", "Score"]].describe()
    study_corr = study_data[["Study Hours", "Score"]].corr()
    return study_summary, study_corr


@app.cell
def __(mo, study_corr, study_summary):
    mo.vstack(
        [
            mo.md("#### Additional Analysis: Summary Statistics and Correlation"),
            mo.md(
                "To strengthen the analysis, I also examined summary statistics and the correlation between study time and exam score."
            ),
            mo.md("**Summary statistics**"),
            study_summary,
            mo.md("**Correlation matrix**"),
            study_corr,
        ]
    )
    return


@app.cell
def __(pd, smf, study_data):
    regression_data = study_data.rename(columns={"Study Hours": "study_hours", "Score": "score"})
    model = smf.ols("score ~ study_hours", data=regression_data).fit()

    regression_results = pd.DataFrame(
        {
            "Metric": ["R-squared", "Coefficient on study_hours", "Intercept"],
            "Value": [
                round(model.rsquared, 3),
                round(model.params["study_hours"], 3),
                round(model.params["Intercept"], 3),
            ],
        }
    )
    return model, regression_results


@app.cell
def __(mo, regression_results):
    mo.md(
        r"""
        #### Additional Analysis: Simple Regression

        I also used a simple regression model to estimate the relationship between study hours
        and exam score. This extends the project beyond chart-based interpretation and shows
        an early understanding of how analytical relationships can be tested more formally.
        """
    )
    regression_results
    return


@app.cell
def __(pd, study_filtered):
    study_crosstab = pd.crosstab(study_filtered["Performance Category"], columns="Count")
    return study_crosstab


@app.cell
def __(mo, study_crosstab):
    mo.md(
        r"""
        #### Additional Analysis: Categorisation and Crosstab

        As part of the data preparation process, I also grouped observations into performance
        categories. This demonstrates an understanding of how raw numerical data can be transformed
        into more interpretable analytical groupings.
        """
    )
    study_crosstab
    return


@app.cell
def __(attendance_threshold, pd):
    attendance_data = pd.DataFrame(
        {
            "Attendance Rate": [60, 65, 70, 75, 80, 85, 90, 95],
            "Average Score": [48, 52, 58, 63, 68, 74, 81, 88],
        }
    )
    attendance_filtered = attendance_data[
        attendance_data["Attendance Rate"] >= attendance_threshold.value
    ].copy()

    attendance_filtered["Attendance Band"] = attendance_filtered["Attendance Rate"].apply(
        lambda x: "High" if x >= 85 else "Moderate"
    )
    return attendance_data, attendance_filtered


@app.cell
def __(attendance_filtered, plt):
    fig2, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(
        attendance_filtered["Attendance Rate"].astype(str),
        attendance_filtered["Average Score"],
    )

    ax.set_title("Attendance Rate vs Average Score")
    ax.set_xlabel("Attendance Rate (%)")
    ax.set_ylabel("Average Score")
    ax.grid(axis="y")
    plt.tight_layout()
    fig2
    return fig2


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
def __(mo, base):
    mo.image(src=str(base / "images" / "attendance.png"), width=500)
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
def __(company_selector, pd):
    financial_data = pd.DataFrame(
        {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Company A": [100, 104, 109, 112, 118, 123],
            "Company B": [95, 97, 99, 101, 103, 106],
        }
    )

    if company_selector.value == "Company A":
        financial_view = financial_data[["Month", "Company A"]].copy()
    elif company_selector.value == "Company B":
        financial_view = financial_data[["Month", "Company B"]].copy()
    else:
        financial_view = financial_data.copy()

    return financial_data, financial_view


@app.cell
def __(company_selector, financial_data, plt):
    fig3, ax = plt.subplots(figsize=(7, 4.5))

    if company_selector.value in ["Both", "Company A"]:
        ax.plot(
            financial_data["Month"],
            financial_data["Company A"],
            marker="o",
            label="Company A",
        )

    if company_selector.value in ["Both", "Company B"]:
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
    return fig3


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
def __(mo, base):
    mo.image(src=str(base / "images" / "financial_trend.png"), width=500)
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
def __(pd):
    workflow_data = pd.DataFrame(
        {
            "Stage": ["Links Found", "Files Selected", "Files Downloaded", "Files Extracted", "Files Prepared"],
            "Count": [12, 10, 9, 8, 7],
        }
    )
    return workflow_data


@app.cell
def __(plt, workflow_data):
    fig4, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(workflow_data["Stage"], workflow_data["Count"])
    ax.set_title("Automation Workflow Stages")
    ax.set_xlabel("Workflow Stage")
    ax.set_ylabel("Number of Documents")
    ax.grid(axis="y")
    plt.xticks(rotation=25)
    plt.tight_layout()
    fig4
    return fig4


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Project 4: Automation and Web Data Workflow

        This section reflects my understanding of how coding can be used not only to analyse
        prepared datasets, but also to support data collection and workflow automation.

        The module introduced the idea of automation pipelines for working with web-based and
        unstructured data. This includes tasks such as locating relevant files, downloading
        documents, extracting content, and preparing data for later analysis.

        The chart below presents a simple workflow-style summary to illustrate how a document
        pipeline can move from discovery to preparation.

        Through this, I developed my understanding of:
        - the difference between structured and unstructured data
        - how automated workflows can reduce repetitive manual tasks
        - why scraping and document extraction require careful preparation and checking
        - the importance of reproducible data pipelines
        """
    )
    return


@app.cell
def __(mo, base):
    mo.image(src=str(base / "images" / "workflow.png"), width=500)
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        **Figure 4.** Example workflow summary showing document movement through an automation pipeline.
        """
    )
    return


@app.cell
def __(pd):
    prompt_data = pd.DataFrame(
        {
            "Prompt Type": ["Generic Prompt", "Detailed Prompt", "Grounded Prompt"],
            "Quality Score": [5, 7, 9],
        }
    )
    return prompt_data


@app.cell
def __(plt, prompt_data):
    fig5, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(prompt_data["Prompt Type"], prompt_data["Quality Score"])
    ax.set_title("Prompt Quality Comparison")
    ax.set_xlabel("Prompt Type")
    ax.set_ylabel("Quality Score")
    ax.grid(axis="y")
    plt.xticks(rotation=20)
    plt.tight_layout()
    fig5
    return fig5


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Project 5: AI Tools and Prompt Design

        Another important area of learning in the module was understanding how large language models
        can support coding, analysis, and communication when used carefully.

        To reflect this, I included a simple comparison of prompt styles. The chart illustrates how
        more detailed and grounded prompts can support higher-quality outputs than vague prompting.

        Through this topic, I developed my understanding of:
        - how LLMs generate text probabilistically
        - why hallucinations and model drift are important limitations
        - how prompt design influences the quality of outputs
        - why grounding and checking outputs against source material is essential

        This helped me think more critically about how AI tools can support analytical work while still
        requiring human judgement, verification, and clear prompting.
        """
    )
    return


@app.cell
def __(mo, base):
    mo.image(src=str(base / "images" / "prompt_quality.png"), width=500)
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        **Figure 5.** Example comparison showing how prompt design can influence output quality.
        """
    )
    return


@app.cell
def __(pd):
    text_data = pd.DataFrame(
        {
            "Document": ["Report A", "Report B", "Report C"],
            "Text": [
                "The company focused on sustainability, growth, and long-term risk management.",
                "The report emphasised supply chain resilience, customer demand, and sustainability goals.",
                "Management discussed growth strategy, financial performance, and operational risk.",
            ],
        }
    )
    return text_data


@app.cell
def __(Counter, pd, re, text_data):
    all_text = " ".join(text_data["Text"]).lower()
    words = re.findall(r"\b[a-z]+\b", all_text)

    stop_words = {
        "the",
        "on",
        "and",
        "of",
        "a",
        "to",
        "with",
        "long",
        "term",
        "this",
        "that",
        "for",
        "in",
    }

    filtered_words = [word for word in words if word not in stop_words]
    word_counts = Counter(filtered_words).most_common(10)

    word_freq_df = pd.DataFrame(word_counts, columns=["Word", "Frequency"])
    return all_text, filtered_words, word_freq_df


@app.cell
def __(plt, word_freq_df):
    fig6, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(word_freq_df["Word"], word_freq_df["Frequency"])
    ax.set_title("Top Words in Sample Business Text")
    ax.set_xlabel("Word")
    ax.set_ylabel("Frequency")
    ax.grid(axis="y")
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig6
    return fig6


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Project 6: Introductory Text Analysis

        To extend my skills beyond structured numerical datasets, I also explored a simple text-analysis
        workflow using Python. I created a small dataset of business-style text, cleaned the text,
        removed common stop words, counted word frequency, and visualised the most common terms.

        This demonstrates an early understanding of:
        - unstructured text data
        - basic natural language processing preparation
        - frequency-based text analysis
        - how business themes can be identified through repeated terms

        This links to the broader module theme of working not only with tables of numbers, but also
        with text-based data that may require additional cleaning before analysis.
        """
    )
    return


@app.cell
def __(mo, base):
    mo.image(src=str(base / "images" / "text_analysis.png"), width=500)
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        **Figure 6.** Bar chart showing the most frequent words in a small sample of business text.
        """
    )
    return


@app.cell
def __(pd):
    development_data = pd.DataFrame(
        {
            "Area": ["Coding", "Analysis", "Visualisation", "Workflow", "Communication"],
            "Development Score": [6, 7, 7, 8, 8],
        }
    )
    return development_data


@app.cell
def __(development_data, plt):
    fig7, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(development_data["Area"], development_data["Development Score"])
    ax.set_title("Development Across Analytical Skills")
    ax.set_xlabel("Skill Area")
    ax.set_ylabel("Development Score")
    ax.grid(axis="y")
    plt.tight_layout()
    fig7
    return fig7


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Project 7: Extended Analytical Development

        As the module developed, I also strengthened my understanding of how different tools,
        workflows, and analytical approaches can be combined within one project.

        The chart below summarises key areas of development across the portfolio, showing that
        the project involved not only coding and chart production, but also workflow awareness,
        interpretation, and communication.

        This broader development helped me move from producing isolated code outputs towards
        building a more complete analytical workflow that combines coding, interpretation,
        presentation, and reflection.
        """
    )
    return


@app.cell
def __(mo, base):
    mo.image(src=str(base / "images" / "development.png"), width=500)
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        **Figure 7.** Summary chart showing development across key analytical skill areas.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Technical Journey

        Throughout this module, I developed my skills progressively from foundational Python
        concepts towards more structured and analytical data workflows.

        In the early stages, I built confidence in core programming concepts such as variables,
        control flow, indexing, and functions. These foundations supported later work with
        structured datasets and visual outputs.

        Through this portfolio, I applied pandas to organise data in DataFrames, used matplotlib
        to create visualisations, and used marimo to structure the project in a reproducible and
        reactive notebook environment. The addition of interactive controls strengthened the project
        by showing how user inputs can update outputs dynamically.

        I also extended the analysis beyond simple chart production by including summary statistics,
        correlation analysis, categorisation, simple regression, and introductory text analysis.
        This helped me move from basic visual exploration towards a more analytical workflow.

        Alongside the technical coding work, I developed my communication skills by presenting the
        project through a portfolio structure and by explaining what each chart and result shows
        in a clear and professional way.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Reflection

        This portfolio reflects my development from foundational coding skills towards a more
        structured approach to data analysis and communication.

        A key area of progress for me was learning that effective analysis involves more than
        producing code or charts. It also requires careful data organisation, appropriate choice
        of visualisation, and clear explanation of what the results suggest.

        Through this work, I strengthened my ability to use pandas for structuring data,
        matplotlib for visual communication, and marimo for building a reproducible and interactive
        workflow. I also developed my understanding of how summary statistics, correlation, simple
        regression, and text analysis can support more rigorous interpretation.

        The project also reflects self-directed exploration through the use of marimo, GitHub,
        GitHub Pages, and HTML-based presentation. This helped me improve the professionalism
        and accessibility of my work.

        Going forward, I would like to continue developing these skills by working with larger
        real-world datasets, using more advanced statistical techniques, and building more
        interactive and automated analytical applications.
        """
    )
    return


if __name__ == "__main__":
    app.run()
