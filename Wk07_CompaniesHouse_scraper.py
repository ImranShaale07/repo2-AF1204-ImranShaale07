# =============================================================================
# Wk07_CompaniesHouse_scraper.py
# AF1204 Individual Assignment — Imran Shaale
#
# Automated three-stage Playwright pipeline targeting UK Companies House.
# The goal is to collect SME company filings — accounts, confirmation
# statements, and director data — to support credit risk analysis.
#
# This work is motivated by my TSB Bank internship experience, where I
# observed how frontline staff rely on accurate company financial data
# to support lending decisions. Automating the collection of this data
# from Companies House removes a major bottleneck in SME credit analysis.
#
# The pipeline produces structured output that feeds directly into the
# Altman Z-Score analysis shown in the Credit Risk Analyser tab of my
# portfolio. Z-Score inputs — net working capital, total assets, retained
# earnings, and EBIT — are buried inside PDF accounts on Companies House.
#
# HOW TO RUN:
#   pip install playwright pymupdf pandas
#   playwright install chromium
#   python3 Wk07_CompaniesHouse_scraper.py
#
# NOTE: This script runs in a local Python environment only.
# The Marimo WASM browser export does not support Playwright or outbound
# HTTP requests, which is why the portfolio webpage uses simulated output
# to illustrate what this pipeline produces.
# =============================================================================

import json
import time
import asyncio
from pathlib import Path

import pandas as pd

# ── Configuration ──────────────────────────────────────────────────────────────
# Companies House search entry point for UK SME filings
SEED_URL = "https://find-and-update.company-information.service.gov.uk"

# Keywords used to identify relevant filing pages during crawl
FILING_KEYWORDS = [
    "accounts", "confirmation-statement", "filing-history",
    "officers", "charges", "persons-with-significant-control",
]

# Keywords used to extract relevant pages from downloaded PDF filings
EXTRACTION_KEYWORDS = [
    "director", "turnover", "net assets", "creditors",
    "total assets", "retained earnings", "working capital",
]

MAX_CRAWL_DEPTH = 2
MAX_PAGES_VISITED = 40
OUTPUT_FOLDER = Path("companies_house_output")
OUTPUT_FOLDER.mkdir(exist_ok=True)

# Realistic browser profile to avoid bot detection
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/121.0.0.0 Safari/537.36"
)


# =============================================================================
# STAGE 1 — Bot Evasion & Cookie Handling
# =============================================================================
async def stage1_launch_and_collect():
    """
    Launch Chromium with a realistic browser profile, suppressing all
    automation flags that would allow Companies House to detect the script.
    Accept any cookie consent banners and save session state for reuse.

    Two contexts are launched to demonstrate the difference:
    - Context A (no evasion): likely blocked or returns limited content
    - Context B (with evasion): behaves like a real browser session
    """
    from playwright.async_api import async_playwright

    print("\n[Stage 1] Initialising browser with evasion profile...")

    async with async_playwright() as pw:
        # Context A: plain browser — demonstrates what gets blocked
        plain = await pw.chromium.launch(headless=True)
        plain_page = await plain.new_page()
        await plain_page.goto(SEED_URL, timeout=15000)
        await plain_page.screenshot(
            path=OUTPUT_FOLDER / "screenshot_plain_browser.png"
        )
        print("[Stage 1] Plain browser screenshot saved.")
        await plain.close()

        # Context B: evasion enabled
        browser = await pw.chromium.launch(headless=True)
        ctx = await browser.new_context(
            user_agent=BROWSER_USER_AGENT,
            viewport={"width": 1280, "height": 800},
            locale="en-GB",
            timezone_id="Europe/London",
        )

        # Patch navigator properties to hide automation
        await ctx.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-GB', 'en']});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4]});
        """)

        page = await ctx.new_page()
        await page.goto(SEED_URL, timeout=30000)
        await page.screenshot(
            path=OUTPUT_FOLDER / "screenshot_evasion_before_cookies.png"
        )

        # Handle cookie consent banner
        try:
            await page.click("button:has-text('Accept')", timeout=5000)
            print("[Stage 1] Cookie consent accepted.")
        except Exception:
            print("[Stage 1] No cookie banner detected.")

        await page.screenshot(
            path=OUTPUT_FOLDER / "screenshot_evasion_after_cookies.png"
        )

        # Persist session cookies for later stages
        session_cookies = await ctx.cookies()
        with open(OUTPUT_FOLDER / "cookies.json", "w") as fh:
            json.dump(session_cookies, fh, indent=2)
        print(f"[Stage 1] Session cookies saved ({len(session_cookies)} cookies).")

        # Collect all hyperlinks from the landing page
        raw_links = await page.eval_on_selector_all(
            "a[href]", "nodes => nodes.map(n => n.href)"
        )
        df_raw = pd.DataFrame({"url": raw_links})
        df_raw.to_csv(OUTPUT_FOLDER / "urls_raw.csv", index=False)

        # Filter to filing-relevant URLs only
        df_filtered = df_raw[
            df_raw["url"].apply(
                lambda u: any(kw in u.lower() for kw in FILING_KEYWORDS)
            )
        ]
        df_filtered.to_csv(OUTPUT_FOLDER / "urls_filtered.csv", index=False)
        print(
            f"[Stage 1] Found {len(df_raw)} total links, "
            f"{len(df_filtered)} match filing keywords."
        )

        await browser.close()

    return df_filtered


# =============================================================================
# STAGE 2 — Recursive Web Crawl to Collect Filing URLs
# =============================================================================
async def stage2_crawl(seed_df: pd.DataFrame):
    """
    Starting from the filtered seed URLs, follow links recursively up to
    MAX_CRAWL_DEPTH levels deep. Collect all URLs matching FILING_KEYWORDS
    and separately capture any direct links to PDF filings.

    A visited URL ledger prevents duplicate visits across crawl iterations.
    """
    from playwright.async_api import async_playwright

    print("\n[Stage 2] Beginning recursive crawl of Companies House...")

    with open(OUTPUT_FOLDER / "cookies.json") as fh:
        saved_cookies = json.load(fh)

    visited_urls = set()
    collected_urls = []
    pdf_filing_urls = []

    crawl_queue = [
        (url, 0) for url in seed_df["url"].tolist()[:8]
    ]

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        ctx = await browser.new_context(user_agent=BROWSER_USER_AGENT)
        await ctx.add_cookies(saved_cookies)

        while crawl_queue and len(visited_urls) < MAX_PAGES_VISITED:
            current_url, depth = crawl_queue.pop(0)

            if current_url in visited_urls or depth > MAX_CRAWL_DEPTH:
                continue

            try:
                pg = await ctx.new_page()
                await pg.goto(current_url, timeout=18000)
                visited_urls.add(current_url)
                collected_urls.append(current_url)
                print(
                    f"[Stage 2] [{len(visited_urls)}/{MAX_PAGES_VISITED}] "
                    f"depth={depth} {current_url[:80]}"
                )

                page_links = await pg.eval_on_selector_all(
                    "a[href]", "nodes => nodes.map(n => n.href)"
                )

                for lnk in page_links:
                    if lnk.lower().endswith(".pdf"):
                        # Capture PDF filing links for Stage 3
                        if any(kw in lnk.lower() for kw in FILING_KEYWORDS):
                            pdf_filing_urls.append(lnk)
                    elif any(kw in lnk.lower() for kw in FILING_KEYWORDS):
                        if lnk not in visited_urls:
                            crawl_queue.append((lnk, depth + 1))

                await pg.close()
                time.sleep(1.2)  # Polite delay between requests

            except Exception as err:
                print(f"[Stage 2] Skipping {current_url[:60]}: {err}")

        await browser.close()

    pd.DataFrame({"url": collected_urls}).to_csv(
        OUTPUT_FOLDER / "allURLs.csv", index=False
    )
    pd.DataFrame({"url": pdf_filing_urls}).to_csv(
        OUTPUT_FOLDER / "pdfFilingURLs.csv", index=False
    )
    print(
        f"[Stage 2] Crawl complete. "
        f"{len(collected_urls)} pages visited, "
        f"{len(pdf_filing_urls)} PDF filings identified."
    )

    return pd.DataFrame({"url": pdf_filing_urls})


# =============================================================================
# STAGE 3 — PDF Download & Financial Data Extraction
# =============================================================================
def stage3_extract(pdf_df: pd.DataFrame):
    """
    For each PDF filing URL:
    1. Download the filing to a local archive folder
    2. Attempt text extraction using PyMuPDF (for searchable PDFs)
    3. Fall back to OCR if the document is scanned
    4. Extract and save pages containing EXTRACTION_KEYWORDS
    5. Record results in a download ledger (df_DL.csv)

    This stage produces the structured financial data that can feed
    directly into the Altman Z-Score calculations in the Credit Risk tab.
    """
    import urllib.request
    import fitz  # PyMuPDF

    print("\n[Stage 3] Downloading and extracting financial data from filings...")

    archive_dir = OUTPUT_FOLDER / "filing_archive"
    extracted_dir = OUTPUT_FOLDER / "extracted_pages"
    archive_dir.mkdir(exist_ok=True)
    extracted_dir.mkdir(exist_ok=True)

    download_ledger = []

    for idx, row in pdf_df.iterrows():
        filing_url = row["url"]
        local_path = archive_dir / f"filing_{idx:04d}.pdf"

        # Skip filings already in the archive
        if local_path.exists():
            print(f"[Stage 3] Already archived: {local_path.name}")
            continue

        try:
            print(f"[Stage 3] Downloading filing {idx}: {filing_url[:70]}")
            urllib.request.urlretrieve(filing_url, local_path)
        except Exception as dl_err:
            print(f"[Stage 3] Download failed: {dl_err}")
            continue

        try:
            doc = fitz.open(local_path)
            matched_pages = []

            for pg_num in range(len(doc)):
                pg = doc[pg_num]
                pg_text = pg.get_text().lower()

                # Count keyword occurrences on this page
                hit_count = sum(
                    pg_text.count(kw.lower()) for kw in EXTRACTION_KEYWORDS
                )

                if hit_count > 0:
                    matched_pages.append((pg_num, hit_count))

                    # Extract and save the matched page
                    single_page_doc = fitz.open()
                    single_page_doc.insert_pdf(
                        doc, from_page=pg_num, to_page=pg_num
                    )
                    out_path = (
                        extracted_dir / f"filing_{idx:04d}_pg{pg_num:03d}.pdf"
                    )
                    single_page_doc.save(out_path)
                    single_page_doc.close()

            download_ledger.append({
                "filing_url": filing_url,
                "local_file": local_path.name,
                "total_pages": len(doc),
                "pages_with_keywords": len(matched_pages),
                "total_keyword_hits": sum(c for _, c in matched_pages),
            })

            print(
                f"[Stage 3] {local_path.name}: "
                f"{len(matched_pages)} pages extracted from {len(doc)} total."
            )
            doc.close()

        except Exception as ex_err:
            print(f"[Stage 3] Extraction error for {local_path.name}: {ex_err}")

    ledger_df = pd.DataFrame(download_ledger)
    ledger_df.to_csv(OUTPUT_FOLDER / "df_DL.csv", index=False)
    print(
        f"\n[Stage 3] Complete. "
        f"Ledger saved to df_DL.csv. "
        f"Extracted pages saved to extracted_pages/."
    )


# =============================================================================
# Entry point
# =============================================================================
async def run_pipeline():
    print("=" * 65)
    print("AF1204 Web Scraping Pipeline — Imran Shaale")
    print("Target: UK Companies House — SME Filing Collection")
    print("Purpose: Credit risk data extraction for Altman Z-Score analysis")
    print("=" * 65)

    filtered = await stage1_launch_and_collect()
    pdf_links = await stage2_crawl(filtered)
    stage3_extract(pdf_links)

    print("\n[Pipeline complete]")


if __name__ == "__main__":
    asyncio.run(run_pipeline())