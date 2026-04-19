# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.22.4",
#     "pandas>=2.3.3",
#     "plotly>=6.5.1",
#     "pyarrow>=22.0.0",
#     "pyzmq>=27.1.0",
# ]
# ///

import marimo

__generated_with = "0.23.1"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import micropip

    return micropip, mo, pd


@app.cell
def _(pd):
    csv_url = (
        "https://gist.githubusercontent.com/DrAYim/"
        "80393243abdbb4bfe3b45fef58e8d3c8/raw/"
        "acd66213efc7ae2c353ab913e58c694534ae90f7/"
        "sp500_ZScore_avgCoDebt.csv"
    )
    df_final = pd.read_csv(csv_url)
    df_final = df_final.dropna(subset=["AvgCost_of_Debt", "Z_Score_lag", "Sector_Key"])
    df_final = df_final[df_final["AvgCost_of_Debt"] < 5]
    df_final["Debt_Cost_Percent"] = df_final["AvgCost_of_Debt"] * 100
    df_final["Market_Cap_B"] = df_final["Market_Cap"] / 1e9

    def zscore_band(z):
        if z < 1.81:
            return "Distress Zone"
        elif z < 2.99:
            return "Grey Zone"
        else:
            return "Safe Zone"

    df_final["Risk_Band"] = df_final["Z_Score_lag"].apply(zscore_band)
    return (df_final,)


@app.cell
def _(df_final, mo):
    all_sectors = sorted(df_final["Sector_Key"].unique().tolist())
    sector_dropdown = mo.ui.multiselect(
        options=all_sectors,
        value=all_sectors[:4],
        label="Filter by Sector",
    )
    cap_slider = mo.ui.slider(
        start=0,
        stop=200,
        step=10,
        value=0,
        label="Min Market Cap ($ Billions)",
    )
    return cap_slider, sector_dropdown


@app.cell
def _(cap_slider, df_final, sector_dropdown):
    filtered_portfolio = df_final[
        (df_final["Sector_Key"].isin(sector_dropdown.value))
        & (df_final["Market_Cap_B"] >= cap_slider.value)
    ]
    count = len(filtered_portfolio)
    return count, filtered_portfolio


@app.cell
async def _(micropip):
    await micropip.install("plotly")
    import plotly.express as px
    import plotly.graph_objects as go

    return go, px


@app.cell
def _(count, filtered_portfolio, go, mo, pd, px):
    # ── Credit Risk charts ──────────────────────────────────────────────────────
    fig_scatter = px.scatter(
        filtered_portfolio,
        x="Z_Score_lag",
        y="Debt_Cost_Percent",
        color="Sector_Key",
        size="Market_Cap_B",
        hover_name="Name",
        title=f"Cost of Debt vs. Altman Z-Score ({count} observations)",
        labels={
            "Z_Score_lag": "Altman Z-Score (lagged)",
            "Debt_Cost_Percent": "Avg. Cost of Debt (%)",
        },
        template="plotly_white",
        height=500,
    )
    fig_scatter.add_vline(
        x=1.81,
        line_dash="dash",
        line_color="crimson",
        annotation=dict(
            text="Distress (Z < 1.81)",
            font=dict(color="crimson"),
            x=1.5,
            xref="x",
            y=0.97,
            yref="paper",
            showarrow=False,
        ),
    )
    fig_scatter.add_vline(
        x=2.99,
        line_dash="dash",
        line_color="seagreen",
        annotation=dict(
            text="Safe (Z > 2.99)",
            font=dict(color="seagreen"),
            x=3.08,
            xref="x",
            y=0.97,
            yref="paper",
            showarrow=False,
        ),
    )
    chart_scatter = mo.ui.plotly(fig_scatter)

    band_order = ["Distress Zone", "Grey Zone", "Safe Zone"]
    band_colors = {
        "Distress Zone": "crimson",
        "Grey Zone": "goldenrod",
        "Safe Zone": "seagreen",
    }
    fig_box = go.Figure()
    for band in band_order:
        subset = filtered_portfolio[filtered_portfolio["Risk_Band"] == band]
        fig_box.add_trace(
            go.Box(
                y=subset["Debt_Cost_Percent"],
                name=band,
                marker_color=band_colors[band],
                boxmean=True,
            )
        )
    fig_box.update_layout(
        title="Distribution of Cost of Debt by Z-Score Risk Band",
        yaxis_title="Avg. Cost of Debt (%)",
        template="plotly_white",
        height=420,
    )
    chart_box = mo.ui.plotly(fig_box)

    # ── 3D Chart 1: Z-Score vs Cost of Debt vs Market Cap
    fig_3d_cap = px.scatter_3d(
        filtered_portfolio,
        x="Z_Score_lag",
        y="Debt_Cost_Percent",
        z="Market_Cap_B",
        color="Risk_Band",
        color_discrete_map=band_colors,
        hover_name="Name",
        title=f"3D View: Z-Score · Cost of Debt · Market Cap ({count} observations)",
        labels={
            "Z_Score_lag": "Altman Z-Score (lagged)",
            "Debt_Cost_Percent": "Avg. Cost of Debt (%)",
            "Market_Cap_B": "Market Cap ($ Bn)",
            "Risk_Band": "Risk Band",
        },
        template="plotly_white",
        height=600,
    )
    fig_3d_cap.update_traces(marker=dict(size=4, opacity=0.8))
    chart_3d_cap = mo.ui.plotly(fig_3d_cap)

    # ── 3D Chart 2: Z-Score vs Cost of Debt vs Sector (encoded)
    sector_list = sorted(filtered_portfolio["Sector_Key"].unique().tolist())
    sector_map = {s: i for i, s in enumerate(sector_list)}
    fp_encoded = filtered_portfolio.copy()
    fp_encoded["Sector_Num"] = fp_encoded["Sector_Key"].map(sector_map)
    fig_3d_sector = px.scatter_3d(
        fp_encoded,
        x="Z_Score_lag",
        y="Debt_Cost_Percent",
        z="Sector_Num",
        color="Sector_Key",
        hover_name="Name",
        title=f"3D View: Z-Score · Cost of Debt · Sector ({count} observations)",
        labels={
            "Z_Score_lag": "Altman Z-Score (lagged)",
            "Debt_Cost_Percent": "Avg. Cost of Debt (%)",
            "Sector_Num": "Sector (encoded)",
            "Sector_Key": "Sector",
        },
        template="plotly_white",
        height=600,
    )
    fig_3d_sector.update_traces(marker=dict(size=4, opacity=0.8))
    chart_3d_sector = mo.ui.plotly(fig_3d_sector)

    # ── Scraping chart ──────────────────────────────────────────────────────────
    scraping_data = pd.DataFrame({
        "Filing_Type": [
            "Total Exemption Accounts", "Confirmation Statement",
            "Micro-Entity Accounts", "Full Accounts", "Director Appointment",
            "Director Resignation", "Mortgage Charge",
        ],
        "Count": [42, 38, 27, 19, 15, 9, 6],
        "Category": [
            "Accounts", "Compliance", "Accounts", "Accounts",
            "Directors", "Directors", "Finance",
        ],
    })
    category_colors = {
        "Accounts": "steelblue",
        "Compliance": "goldenrod",
        "Directors": "seagreen",
        "Finance": "crimson",
    }
    fig_scraping = px.bar(
        scraping_data,
        x="Filing_Type",
        y="Count",
        color="Category",
        color_discrete_map=category_colors,
        title="Simulated Output — Companies House Filings Collected by Type",
        labels={"Filing_Type": "Filing Type", "Count": "Number of Filings Collected"},
        template="plotly_white",
        height=420,
    )
    fig_scraping.update_layout(xaxis_tickangle=-30)
    chart_scraping = mo.ui.plotly(fig_scraping)

    # ── LLM Sentiment chart ─────────────────────────────────────────────────────
    sentiment_data = pd.DataFrame(
        {
            "Company": ["Tesco", "Vodafone", "BP", "HSBC", "Unilever"],
            "Sentiment_Score": [0.62, 0.18, -0.21, 0.44, 0.31],
            "Label": ["Optimistic", "Neutral", "Cautious", "Optimistic", "Neutral"],
        }
    )
    sentiment_colors = {
        "Optimistic": "seagreen",
        "Neutral": "steelblue",
        "Cautious": "crimson",
    }
    fig_sentiment = px.bar(
        sentiment_data,
        x="Company",
        y="Sentiment_Score",
        color="Label",
        color_discrete_map=sentiment_colors,
        title="LLM-Derived Sentiment Scores — FTSE 100 Forward-Looking Statements",
        labels={"Sentiment_Score": "Mean Sentence Sentiment Score"},
        template="plotly_white",
        height=400,
    )
    fig_sentiment.add_hline(y=0, line_dash="dot", line_color="grey")
    chart_sentiment = mo.ui.plotly(fig_sentiment)

    # ── Travel map ──────────────────────────────────────────────────────────────
    travel_data = pd.DataFrame(
        {
            "City": [
                "London", "Paris", "Madrid", "Dubai", "Istanbul",
                "Marrakech", "Amsterdam", "Rome", "New York", "Lagos",
            ],
            "Lat": [51.5, 48.8, 40.4, 25.2, 41.0, 31.6, 52.4, 41.9, 40.7, 6.5],
            "Lon": [-0.1, 2.3, -3.7, 55.3, 28.9, -8.0, 4.9, 12.5, -74.0, 3.4],
            "Visit_Year": [
                "2022", "2023", "2023", "2024", "2024",
                "2023", "2022", "2024", "2024", "2022",
            ],
        }
    )
    years_travel = sorted(travel_data["Visit_Year"].unique(), key=int)
    fig_travel = px.scatter_geo(
        travel_data,
        lat="Lat",
        lon="Lon",
        hover_name="City",
        color="Visit_Year",
        category_orders={"Visit_Year": years_travel},
        color_discrete_sequence=px.colors.qualitative.Bold,
        projection="natural earth",
        title="Places I Have Visited",
        labels={"Visit_Year": "Year"},
    )
    fig_travel.update_traces(marker=dict(size=14))
    chart_travel = mo.ui.plotly(fig_travel)

    return chart_box, chart_scatter, chart_sentiment, chart_travel, chart_3d_cap, chart_3d_sector, chart_scraping


@app.cell
def _(
    cap_slider,
    chart_box,
    chart_scatter,
    chart_sentiment,
    chart_travel,
    chart_3d_cap,
    chart_3d_sector,
    chart_scraping,
    mo,
    sector_dropdown,
):
    # ── Tab 1: About Me ─────────────────────────────────────────────────────────
    tab_about = mo.vstack(
        [
            mo.md("""
## Imran Shaale
### BSc Accounting & Finance · Bayes Business School, City St George's, University of London

---

*Profile*

First-year Accounting and Finance student at Bayes Business School with strong numerical
and analytical skills. Experience at EY, TSB Bank, QPR, and two years in hospitality has
strengthened my understanding of financial processes, stakeholder interactions, and the
importance of confidentiality. I am a dependable and proactive learner seeking opportunities
to develop my skills further in finance. This portfolio showcases the technical data science
skills thatI have built through AF1204 Introduction to Data Science and AI Tools.

---

*Education*

| Qualification | Institution | Period |
|---|---|---|
| BSc Accounting & Finance | Bayes Business School, City St George's, University of London | Sep 2025 – Jun 2028 |
| A-Levels: Economics (B), Politics (B), Mathematics (B) | Kensington Aldridge Academy | Sep 2018 – Jun 2025 |
| 9 GCSEs: Grades 6–8 (inc. Mathematics 7, English Language 7) | Kensington Aldridge Academy | Sep 2018 – Jun 2025 |

---

*Relevant Experience*

*EY Foundation — Intern* (April 2024)
- Participated in a two-week programme focused on communication, teamwork, and client service.
- Led a group project under pressure and pitched ideas to industry professionals.
- Co-hosted a formal event, presenting to a large audience and engaging with senior guests.
- Received training in public speaking, CV writing, and interview technique.

*TSB Bank — Intern* (April 2024)
- Shadowed frontline staff, assisting customers with withdrawals and deposits.
- Observed professional banking standards including confidentiality, accuracy, and customer communication.

---

*Other Experience*

*QPR Football Club — Work Experience* (June 2022)
- Observed coaching processes and communication strategies within a professional sporting environment.
- Gained early exposure to professional teamwork and performance management.

*Nando's, Westfield London — Front of House* (Aug 2023 – Oct 2025)
- Worked 8–40 hours weekly in one of the UK's busiest branches, with peak weekly sales of £120–130k.
- Built strong customer service, cash handling, and time-management skills alongside A-Level studies.

*Nando's, Baker Street — Front & Back of House* (Oct 2025 – Present)
- Managing 20–50 hours weekly at the 2nd busiest store in the region, alongside university commitments.
- Trained across FOH and BOH roles, progressing towards a supervisor position.

---

*Skills*

| Category | Detail |
|---|---|
| IT | Microsoft Excel, Word, PowerPoint |
| Languages | English (fluent), French (basic) |
| Professional | Analytical thinking, client service, attention to detail, time management, confidentiality |

---

*Awards & Extracurricular*

- Gold Award, Intermediate Mathematics Challenge 2023 (80 points)
- Member of the Mathematical Sport Society, Sixth Form

---

*Career Goal*

My ambition is to build a career in finance, developing strong technical and analytical capabilities
at Bayes that complement my hands-on experience at EY and TSB. I am particularly interested
in roles at the intersection of financial analysis and client service.

---

*Interests*

🏋️ Gym — training regularly and building discipline and consistency  
⚽ Football — playing regularly and following the game closely  
🏀 Basketball — playing socially and following the NBA  
📈 Following global business, financial markets, and economic news
            """),
        ]
    )

    # ── Tab 2: Credit Risk Analyser ─────────────────────────────────────────────
    tab_analysis = mo.vstack(
        [
            mo.md("""
## Interactive Credit Risk Analyser
### Skills: Weeks 2, 3 & 4

The Altman Z-Score predicts corporate bankruptcy risk using five financial ratios.
A score below *1.81* signals financial distress; above *2.99* indicates a safe firm.
Using S&P 500 panel data fetched programmatically via Yahoo Finance, I examine whether
a firm's lagged Z-Score (Year t-1) predicts its average cost of debt (Year t).
            """),
            mo.callout(
                mo.md(
                    "Use the filters below to explore the relationship between credit risk and borrowing costs."
                ),
                kind="info",
            ),
            mo.hstack([sector_dropdown, cap_slider], justify="start", gap=2),
            chart_scatter,
            mo.md("---"),
            mo.md("### Distribution of Cost of Debt by Risk Band (Week 3)"),
            mo.md(
                "This box plot shows the spread of borrowing costs within each Z-Score category."
            ),
            chart_box,
            mo.md("---"),
            mo.md("### 3D View: Z-Score · Cost of Debt · Market Cap (Week 4)"),
            mo.md("Rotate the chart by clicking and dragging. Larger firms tend to cluster in the Safe Zone."),
            chart_3d_cap,
            mo.md("---"),
            mo.md("### 3D View: Z-Score · Cost of Debt · Sector (Week 4)"),
            mo.md("This chart adds sector as a third dimension, encoded numerically on the z-axis, revealing sector-level clustering in credit risk."),
            chart_3d_sector,
        ]
    )

    # ── Tab 3: Web Scraping Pipeline ────────────────────────────────────────────
    tab_scraping = mo.vstack([
        mo.md("""
## Web Scraping & Automation Pipeline
### Skills: Week 7 — Playwright · PDF Extraction · Bot Evasion

*Overview*

Credit analysts assessing SME lending risk need timely access to company filings —
accounts, director histories, and confirmation statements — published on Companies House.
Manually retrieving this data for hundreds of firms is impractical. In Week 7 I built an
automated three-stage pipeline using *Playwright* to collect this data programmatically,
applying it to UK company filings. My experience shadowing staff at TSB Bank made clear
how important accurate and timely company financial data is when assessing lending decisions.

---

*Stage 1 — Bot Evasion & Cookie Handling*

Companies House detects and blocks automated scripts by default.
The script launches a Chromium browser with a realistic user-agent string and suppresses
automation flags, making it indistinguishable from a human visitor. It accepts cookie
consent banners automatically and saves session cookies to JSON for reuse across stages.

Key techniques:
- Launch Playwright Chromium with a custom user-agent string
- Suppress automation flags (confirmed via before/after screenshot comparison)
- Programmatically click "Accept All" on cookie consent banners
- Save cookies and local storage to cookies.json and localStorage.json

---

*Stage 2 — Web Crawling to Collect Filing URLs*

Starting from a company's Companies House landing page, the crawler follows links
recursively up to a configurable depth, collecting URLs matching target keywords such as
"accounts", "confirmation-statement", and "filing-history". PDF links are filtered
and saved separately for Stage 3.

Key techniques:
- Recursive web crawling with configurable depth and maximum run time
- Keyword filtering to screen relevant filing URLs
- Deduplication using a visited URL ledger to avoid repeat visits
- Separate extraction of PDF filing links into pdfscreenedURLs.csv

---

*Stage 3 — PDF Download & Data Extraction*

For each screened PDF URL, the script downloads the filing, checks whether it is
text-searchable or scanned, and extracts pages containing keywords such as
"director", "turnover", "net assets", and "creditors".

Key techniques:
- Programmatic PDF download with a ledger to avoid duplicates
- Text extraction using PyMuPDF for searchable filings
- OCR fallback for scanned documents
- Page-by-page keyword counting and extraction

---

*Simulated Output — Filing Types Collected*

The chart below shows the distribution of filing types that would be collected
by the pipeline across a sample of 50 SMEs, illustrating how the scraped data
can be immediately structured and visualised for credit analysis.
        """),
        chart_scraping,
        mo.md("""
---

*Why this matters for credit risk*

This pipeline directly complements the Altman Z-Score analysis in the Credit Risk tab.
The financial data needed to compute Z-Scores — net working capital, total assets,
retained earnings, and EBIT — is buried inside PDF accounts on Companies House.
Automating its collection at scale removes the bottleneck that prevents analysts
from running credit risk models across large numbers of SMEs simultaneously.
        """),
    ])

    # ── Tab 4: LLM Sentiment Analysis ───────────────────────────────────────────
    tab_llm = mo.vstack(
        [
            mo.md("""
## LLM Sentiment Analysis of Corporate Disclosures
### Skills: Weeks 8 & 9 — Prompt Engineering · Groq API · Few-Shot Prompting

*Overview*

Annual reports contain forward-looking statements that reveal management confidence about
future performance. Manually reading hundreds of these is impractical. In Weeks 8 and 9
I used Large Language Models accessed via the Groq API to classify the sentiment of these
statements at scale.

---

*What is an LLM?*

A large language model is a statistical model trained on vast quantities of text. It predicts
the most likely next token given a prompt. LLMs do not verify facts — they generate plausible
text — which is why controlling for hallucinations is critical in any production workflow.

---

*Controlling Hallucinations — Techniques Applied*

| Technique | Purpose | Setting used |
|---|---|---|
| Temperature = 0 | Forces deterministic, factual outputs | temperature=0 |
| Top-P = 1 | Full token pool, overridden by temperature | top_p=1 |
| Few-shot examples | Labelled examples of positive/neutral/cautious sentences | 3 examples per class |
| Prompt engineering | Structured prompt with persona, instructions, output format | See template below |
| AI-as-judge | Second LLM validates the first model's classifications | Model B checks Model A |
| Pinned model | Fixes model version to avoid drift over time | llama-3.1-8b-instant |

---

*Prompt Engineering Template Used*

The prompt sent to the Groq API followed the structured template taught in Week 8,
including a persona, step-by-step instructions, constraints, few-shot examples,
and a specified JSON output format. Setting temperature to 0 ensured consistent,
deterministic classifications across all firms.

---

*Results — Illustrative Sentiment Scores for Selected FTSE 100 Firms*

Scores represent the mean of sentence-level classifications
(+1 = optimistic, 0 = neutral, −1 = cautious).
            """),
            chart_sentiment,
            mo.md("""
---
*Key techniques demonstrated:*
- Groq API client setup with secure environment variable key retrieval
- Structured prompt construction with few-shot examples
- JSON response parsing and label-to-score conversion
- Retry logic with back-off for API failures
- Temperature and top-p hyperparameter control
- AI-as-judge validation of sentiment classifications
            """),
        ]
    )

    # ── Tab 5: Personal Interests ───────────────────────────────────────────────
    tab_personal = mo.vstack(
        [
            mo.md("""
## Personal Interests

---

*Travel*

I have visited a range of cities across Europe, the Middle East, North America, and Africa.
Experiencing different markets, economies, and cultures has deepened my understanding of
how global conditions shape business and finance — something I find directly relevant to
my studies at Bayes.
            """),
            chart_travel,
            mo.md("""
---

*Football*

I play football regularly and follow the sport closely. I am particularly interested in the
tactical and analytical dimensions of the modern game — how data is increasingly used by
clubs to inform transfer decisions, performance management, and in-match strategy.

---

*Basketball*

I play basketball socially and follow the NBA. The sport has taught me about quick
decision-making under pressure — a skill equally valuable on a court or in a client-facing
financial role.

---

*Gym & Fitness*

I train regularly and value the discipline and consistency that comes with it. Maintaining
a structured training routine alongside university and part-time work has strengthened my
time-management skills considerably.

---

*Financial Markets & Business News*

I follow global business and financial markets closely, reading financial news daily.
My experience at EY and TSB gave me an early appreciation of how macroeconomic developments
flow through to individual firms and their financial performance.
            """),
        ]
    )

    # ── Assemble tabs ───────────────────────────────────────────────────────────
    app_tabs = mo.ui.tabs(
        {
            "👤 About Me": tab_about,
            "📊 Credit Risk Analyser": tab_analysis,
            "🌐 Web Scraping Pipeline": tab_scraping,
            "🤖 LLM Sentiment Analysis": tab_llm,
            "✈️ Personal Interests": tab_personal,
        }
    )

    mo.md(
        f"""
# Imran Shaale
#### BSc Accounting & Finance · Bayes Business School
---
{app_tabs}
"""
    )
    return


if __name__ == "__main__":
    app.run()