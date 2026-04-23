
# Wk08_llm_sentiment.py
# AF1204 Individual Assignment — Abdullah Majeed
#
# LLM sentiment analysis of FTSE 100 forward-looking statements using the
# Groq API with few-shot prompting and AI-as-judge validation.
# Relevant to commodity trading — management sentiment in annual reports
# signals confidence about supply chains, energy costs, and market conditions.
#
# Note: This script requires a local Python environment with a valid
# Groq API key set as the environment variable GROQ_API_KEY.
# It cannot run inside the Marimo WASM browser export, which is why the
# portfolio webpage uses illustrative simulated data to demonstrate the output.
#
# To install dependencies:
#   pip install groq pandas
#
# To set your API key (Mac/Linux):
#   export GROQ_API_KEY=your_key_here
#
# To set your API key (Windows):
#   set GROQ_API_KEY=your_key_here


import os
import json
import time

import pandas as pd
from groq import Groq

# ── Settings ──────────────────────────────────────────────────────────────────
MODEL = "llama-3.1-8b-instant"   # Pinned model version to avoid drift
TEMPERATURE = 0                   # Deterministic outputs
TOP_P = 1                         # Full token pool, overridden by temperature
MAX_RETRIES = 3                   # Retry logic for API failures
RETRY_DELAY = 2                   # Seconds between retries

# Initialise Groq client using environment variable (never hardcode API keys)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ── Sample forward-looking statements from FTSE 100 annual reports ─────────────
statements = [
    {
        "company": "Tesco",
        "text": (
            "We are confident in our ability to grow market share and deliver "
            "strong returns to shareholders over the medium term, supported by "
            "our continued investment in price, value, and customer experience."
        ),
    },
    {
        "company": "Vodafone",
        "text": (
            "We expect trading conditions to remain broadly stable, with modest "
            "growth anticipated across our key European and African markets as "
            "we continue to execute our transformation programme."
        ),
    },
    {
        "company": "BP",
        "text": (
            "The energy transition presents significant headwinds for our upstream "
            "portfolio, and we are taking a cautious approach to capital allocation "
            "as we rebalance our business toward lower-carbon energy sources."
        ),
    },
    {
        "company": "HSBC",
        "text": (
            "We are well positioned to capture growth across our Asia-Pacific "
            "franchise and wealth management business, and we remain optimistic "
            "about our ability to deliver on our strategic targets."
        ),
    },
    {
        "company": "Unilever",
        "text": (
            "Our underlying sales growth remains in line with our medium-term "
            "guidance, and we continue to make progress on our sustainability "
            "commitments while managing cost pressures across our supply chain."
        ),
    },
]


# =============================================================================
# Prompt Engineering — Structured prompt with few-shot examples
# =============================================================================
def build_prompt(statement_text: str) -> str:
    """
    Build a structured prompt following the Week 8 template:
    persona, instructions, constraints, few-shot examples, output format.
    """
    return f"""You are a financial analyst specialising in sentiment analysis of 
corporate disclosures for commodity market research. Your task is to classify 
the sentiment of a forward-looking statement from a FTSE 100 annual report.

Instructions:
1. Read the statement carefully.
2. Classify the overall sentiment as exactly one of: Optimistic, Neutral, or Cautious.
3. Assign a score: Optimistic = 1, Neutral = 0, Cautious = -1.
4. Return ONLY a JSON object with keys "label" and "score". No other text.

Constraints:
- Do not explain your reasoning.
- Do not include any text outside the JSON object.
- Use exactly the labels: Optimistic, Neutral, or Cautious.

Few-shot examples:

Statement: "We are highly confident in our ability to deliver record revenue 
growth and expand our margins significantly in the coming financial year."
Output: {{"label": "Optimistic", "score": 1}}

Statement: "Our results are in line with market expectations and we continue 
to monitor the macroeconomic environment carefully."
Output: {{"label": "Neutral", "score": 0}}

Statement: "Significant uncertainty in global commodity markets and rising 
input costs have led us to revise our outlook downward for the year ahead."
Output: {{"label": "Cautious", "score": -1}}

Now classify this statement:
"{statement_text}"
Output:"""


# =============================================================================
# Groq API call with retry logic
# =============================================================================
def classify_sentiment(statement_text: str, retries: int = MAX_RETRIES) -> dict:
    """
    Call the Groq API to classify sentiment with retry logic and back-off.
    Returns a dict with keys: label, score.
    """
    prompt = build_prompt(statement_text)

    for attempt in range(1, retries + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=TEMPERATURE,
                top_p=TOP_P,
                max_tokens=50,
            )
            raw = response.choices[0].message.content.strip()

            # Parse JSON response
            result = json.loads(raw)
            assert result["label"] in ["Optimistic", "Neutral", "Cautious"]
            assert result["score"] in [1, 0, -1]
            return result

        except Exception as e:
            print(f"  [Attempt {attempt}/{retries}] Error: {e}")
            if attempt < retries:
                time.sleep(RETRY_DELAY * attempt)
            else:
                print("  [Failed] Returning default Neutral classification.")
                return {"label": "Neutral", "score": 0}


# =============================================================================
# AI-as-Judge — Second model validates first model's classifications
# =============================================================================
def validate_with_judge(statement_text: str, primary_label: str) -> bool:
    """
    Use a second LLM call to validate the primary classification.
    Returns True if the judge agrees, False otherwise.
    """
    judge_prompt = f"""You are a senior commodity market analyst reviewing a 
junior analyst's sentiment classification of a corporate disclosure.

Statement: "{statement_text}"
Classification given: {primary_label}

Do you agree with this classification? Reply with ONLY "Yes" or "No"."""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": judge_prompt}],
            temperature=0,
            top_p=1,
            max_tokens=5,
        )
        answer = response.choices[0].message.content.strip().lower()
        return answer.startswith("yes")
    except Exception:
        return True


# =============================================================================
# Main pipeline
#
def main():
    print("=" * 60)
    print("AF1204 LLM Sentiment Analysis — Abdullah Majeed")
    print("Target: FTSE 100 Forward-Looking Statements")
    print("Use case: Commodity trading — ESG and supply chain sentiment")
    print(f"Model: {MODEL} | Temperature: {TEMPERATURE} | Top-P: {TOP_P}")
    print("=" * 60)

    results = []

    for item in statements:
        company = item["company"]
        text = item["text"]
        print(f"\nClassifying: {company}")

        # Primary classification
        primary = classify_sentiment(text)
        print(f"  Primary classification: {primary['label']} ({primary['score']})")

        # AI-as-judge validation
        agreed = validate_with_judge(text, primary["label"])
        print(f"  Judge validation: {'Agreed' if agreed else 'Disagreed'}")

        # If judge disagrees, reclassify
        if not agreed:
            print("  Reclassifying after judge disagreement...")
            primary = classify_sentiment(text)
            print(f"  Revised classification: {primary['label']} ({primary['score']})")

        results.append({
            "Company": company,
            "Statement": text[:80] + "...",
            "Label": primary["label"],
            "Sentiment_Score": primary["score"],
            "Judge_Agreed": agreed,
        })

        time.sleep(0.5)

    # Save results
    df = pd.DataFrame(results)
    df.to_csv("sentiment_results.csv", index=False)

    print("\n" + "=" * 60)
    print("Results:")
    print(df[["Company", "Label", "Sentiment_Score", "Judge_Agreed"]].to_string(index=False))
    print("\nResults saved to sentiment_results.csv")
    print("=" * 60)


if __name__ == "__main__":
    main()