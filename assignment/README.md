# Swiggy Play Store Review Trend Analysis Agent

## Overview
This project analyzes Google Play Store reviews for Swiggy, extracting and tracking trending topics (issues, requests, feedback) over the past 30 days using an agentic AI approach. The system deduplicates similar topics and dynamically discovers new ones, outputting a daily trend report.

## Features
- Daily ingestion of Swiggy Play Store reviews (from June 1, 2024, onwards)
- LLM-powered agent for topic extraction and canonicalization
- Deduplication and dynamic topic discovery
- Trend analysis report: topics × dates (last 30 days)
- CLI interface for report generation

## Requirements
- Python 3.9+
- OpenAI API key (for LLM agent)
- Google Play review scraper (e.g., `google-play-scraper`)
- pandas, tqdm, requests, etc.

## Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY=your-key-here
   ```

## Usage
To generate a trend report for Swiggy reviews:
```bash
python main.py --app_link "https://play.google.com/store/apps/details?id=in.swiggy.android" --target_date 2024-07-01
```
The report will be saved in the `/output/` folder.

## Deliverables
- Source code (this repo)
- Sample output reports (`/output/`)
- Video demonstration

---
For questions, contact: vatsal@pulsegen.io 