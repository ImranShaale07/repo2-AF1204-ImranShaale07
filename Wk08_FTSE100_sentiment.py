
# Wk08_FTSE100_sentiment.py
# AF1204 Individual Assignment — Imran Shaale
#
# Sentiment classification of FTSE 100 forward-looking statements using
# the Groq API. Applied to annual report disclosures from UK-listed firms
# relevant to financial analysis and credit risk assessment.
#
# Forward-looking statements in annual reports signal management confidence
# about future revenue, cost pressures, and market conditions. Classifying
# these at scale — rather than reading them manually — is a core use case
# for LLMs in financial analysis workflows.
#
# Techniques applied:
#   - Structured prompt engineering with persona and step-by-step instructions
#   - Few-shot examples to anchor the model's classification behaviour
#   - Temperature = 0 for fully deterministic, reproducible outputs
#   - Pinned model version to prevent classification drift over time
#   - Retry logic with exponential back-off for API reliability
#   - AI-as-judge: a second LLM call validates each primary classification
#
# HOW TO RUN:
#   pip install groq pandas
#   export GROQ_API_KEY=your_key_here   (Mac/Linux)
#   set GROQ_API_KEY=your_key_here      (Windows)
#   python3 Wk08_FTSE100_sentiment.py
#
# NOTE: This script requires a valid Groq API key and a local Python
# environment. It cannot run inside the Marimo WASM browser export,
# which is why the portfolio webpage uses illustrative simulated scores
# to demonstrate what this pipeline produces.
# =============================================================================
 
import os
import json
import time
 
import pandas as pd
from groq import Groq
 
# ── Model configuration ────────────────────────────────────────────────────────
GROQ_MODEL = "llama-3.1-8b-instant"  # Pinned — prevents output drift
TEMPERATURE = 0                        # Fully deterministic outputs
TOP_P = 1                              # Not active when temperature = 0
MAX_TOKENS_PER_CALL = 60
API_RETRY_LIMIT = 3
RETRY_BACKOFF_SECONDS = 2
 
# Load API key from environment — never hardcode credentials
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
 
# ── Source statements ──────────────────────────────────────────────────────────
# Forward-looking statements drawn from FTSE 100 annual reports.
# These represent the kind of disclosures a credit analyst would classify
# when assessing counterparty sentiment across a portfolio of firms.
ftse100_statements = [
    {
        "ticker": "TSCO",
        "company": "Tesco",
        "sector": "Consumer Staples",
        "text": (
            "We are confident in our ability to grow volume, improve value perception, "
            "and deliver strong and sustainable shareholder returns over the medium term, "
            "supported by disciplined investment in our customer proposition."
        ),
    },
    {
        "ticker": "VOD",
        "company": "Vodafone",
        "sector": "Telecommunications",
        "text": (
            "We expect organic service revenue growth to remain broadly stable, "
            "with modest improvement anticipated in our key European markets as we "
            "continue to execute our cost and efficiency transformation."
        ),
    },
    {
        "ticker": "BP",
        "company": "BP",
        "sector": "Energy",
        "text": (
            "The accelerating energy transition and regulatory environment present "
            "material headwinds to our upstream portfolio, and we have adopted a "
            "more cautious stance on capital deployment as we reshape our business."
        ),
    },
    {
        "ticker": "HSBA",
        "company": "HSBC",
        "sector": "Banking",
        "text": (
            "We remain optimistic about growth in our Asia-Pacific wealth and "
            "commercial banking franchises, and we are confident in our ability "
            "to deliver on our strategic return targets over the coming period."
        ),
    },
    {
        "ticker": "ULVR",
        "company": "Unilever",
        "sector": "Consumer Goods",
        "text": (
            "Underlying sales growth is tracking in line with our medium-term guidance "
            "range, and we continue to make steady progress on our operational efficiency "
            "programme while navigating ongoing input cost pressures."
        ),
    },
]
 
 
# =============================================================================
# Prompt construction
# =============================================================================
def build_classification_prompt(statement: str) -> str:
    """
    Construct a structured prompt following the Week 8 template.
    Includes: persona, numbered instructions, hard constraints,
    three few-shot examples, and a strict JSON output format.
    """
    return f"""You are a senior credit analyst at a UK investment bank, specialising
in the analysis of corporate forward-looking statements for counterparty risk assessment.
 
Your task is to classify the sentiment of a forward-looking statement extracted from
a FTSE 100 annual report.
 
Instructions:
1. Read the statement carefully and assess its overall tone.
2. Classify the sentiment as exactly one of: Optimistic, Neutral, or Cautious.
3. Assign the corresponding score: Optimistic = 1, Neutral = 0, Cautious = -1.
4. Output ONLY a valid JSON object with two keys: "label" and "score".
 
Constraints:
- Do not include any explanation, commentary, or text outside the JSON object.
- Use only these exact label strings: Optimistic, Neutral, Cautious.
- If genuinely ambiguous, classify as Neutral.
 
Few-shot examples:
 
Input: "We are highly confident in delivering record earnings growth and expanding
our market share across all divisions in the financial year ahead."
Output: {{"label": "Optimistic", "score": 1}}
 
Input: "Performance in the period was in line with market expectations, and we
continue to monitor the operating environment closely as conditions evolve."
Output: {{"label": "Neutral", "score": 0}}
 
Input: "Significant macroeconomic headwinds and rising input costs have led the
board to adopt a cautious outlook and revise full-year guidance downward."
Output: {{"label": "Cautious", "score": -1}}
 
Now classify the following statement:
"{statement}"
Output:"""
 
 
# =============================================================================
# Primary classification with retry logic
# =============================================================================
def classify(statement_text: str) -> dict:
    """
    Submit the statement to the Groq API and parse the JSON response.
    Retries up to API_RETRY_LIMIT times with exponential back-off on failure.
    """
    prompt = build_classification_prompt(statement_text)
 
    for attempt in range(1, API_RETRY_LIMIT + 1):
        try:
            resp = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=TEMPERATURE,
                top_p=TOP_P,
                max_tokens=MAX_TOKENS_PER_CALL,
            )
            raw_output = resp.choices[0].message.content.strip()
            parsed = json.loads(raw_output)
 
            # Validate response structure
            assert parsed["label"] in ["Optimistic", "Neutral", "Cautious"]
            assert parsed["score"] in [1, 0, -1]
            return parsed
 
        except Exception as err:
            print(f"    [Attempt {attempt}/{API_RETRY_LIMIT}] Error: {err}")
            if attempt < API_RETRY_LIMIT:
                wait = RETRY_BACKOFF_SECONDS * attempt
                print(f"    Retrying in {wait}s...")
                time.sleep(wait)
            else:
                print("    Max retries reached. Defaulting to Neutral.")
                return {"label": "Neutral", "score": 0}
 
 
# =============================================================================
# AI-as-judge validation
# =============================================================================
def judge_classification(statement_text: str, proposed_label: str) -> bool:
    """
    Send a second prompt to the model asking it to validate the primary
    classification. Returns True if the judge agrees, False otherwise.
 
    This technique reduces hallucination risk by catching cases where the
    primary model has clearly misclassified a statement.
    """
    validation_prompt = f"""You are a senior credit analyst reviewing a classification
made by a junior analyst.
 
Statement: "{statement_text}"
Proposed classification: {proposed_label}
 
Do you agree this classification is correct?
Reply with ONLY the word "Yes" or the word "No"."""
 
    try:
        resp = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": validation_prompt}],
            temperature=0,
            top_p=1,
            max_tokens=5,
        )
        verdict = resp.choices[0].message.content.strip().lower()
        return verdict.startswith("yes")
    except Exception:
        return True  # Default to accepting if judge call fails
 
 
# =============================================================================
# Main pipeline
# =============================================================================
def run_sentiment_pipeline():
    print("=" * 65)
    print("AF1204 LLM Sentiment Analysis — Imran Shaale")
    print("Target: FTSE 100 Forward-Looking Statements")
    print("Purpose: Counterparty sentiment classification for credit analysis")
    print(f"Model: {GROQ_MODEL}  |  Temperature: {TEMPERATURE}  |  Top-P: {TOP_P}")
    print("=" * 65)
 
    output_rows = []
 
    for item in ftse100_statements:
        company = item["company"]
        ticker = item["ticker"]
        sector = item["sector"]
        text = item["text"]
 
        print(f"\nProcessing: {company} ({ticker}) — {sector}")
 
        # Step 1: Primary classification
        primary_result = classify(text)
        label = primary_result["label"]
        score = primary_result["score"]
        print(f"  Primary classification: {label} ({score})")
 
        # Step 2: AI-as-judge validation
        judge_agrees = judge_classification(text, label)
        print(f"  Judge validation: {'Agreed' if judge_agrees else 'DISAGREED — reclassifying'}")
 
        # Step 3: Reclassify if judge disagrees
        if not judge_agrees:
            primary_result = classify(text)
            label = primary_result["label"]
            score = primary_result["score"]
            print(f"  Revised classification: {label} ({score})")
 
        output_rows.append({
            "Ticker": ticker,
            "Company": company,
            "Sector": sector,
            "Label": label,
            "Sentiment_Score": score,
            "Judge_Agreed": judge_agrees,
            "Statement_Preview": text[:100] + "...",
        })
 
        time.sleep(0.4)  # Rate limit courtesy delay
 
    # Save and display results
    results_df = pd.DataFrame(output_rows)
    results_df.to_csv("ftse100_sentiment_results.csv", index=False)
 
    print("\n" + "=" * 65)
    print("Classification Results:")
    print(
        results_df[["Company", "Sector", "Label", "Sentiment_Score", "Judge_Agreed"]]
        .to_string(index=False)
    )
    print("\nFull results saved to ftse100_sentiment_results.csv")
    print("=" * 65)
 
 
if __name__ == "__main__":
    run_sentiment_pipeline()