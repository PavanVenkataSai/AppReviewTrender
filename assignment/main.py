import argparse
import os
from datetime import datetime, timedelta
from src.data_ingestion import fetch_reviews_for_date
from src.topic_agent import extract_and_canonicalize_topics
from src.trend_report import generate_trend_report
from src.taxonomy import SEED_TOPICS
import pandas as pd

OUTPUT_DIR = "output"


def main():
    parser = argparse.ArgumentParser(description="Swiggy Play Store Review Trend Analysis Agent")
    parser.add_argument('--app_link', type=str, required=True, help='Google Play Store app link')
    parser.add_argument('--target_date', type=str, required=True, help='Target date in YYYY-MM-DD format')
    args = parser.parse_args()

    app_link = args.app_link
    target_date = datetime.strptime(args.target_date, "%Y-%m-%d").date()
    app_id = app_link.split("id=")[-1]

    # Collect reviews for the last 30 days
    topics_by_date = {}
    for i in range(30, -1, -1):
        day = target_date - timedelta(days=i)
        reviews = fetch_reviews_for_date(app_id, day)
        topics = extract_and_canonicalize_topics(reviews, SEED_TOPICS)
        topics_by_date[day.strftime("%Y-%m-%d")] = topics

    # Generate trend report
    df = generate_trend_report(topics_by_date, (target_date - timedelta(days=30)).strftime("%Y-%m-%d"), target_date.strftime("%Y-%m-%d"))

    # Save report
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, f"trend_report_{target_date}.csv")
    df.to_csv(output_path, index=True)
    print(f"Trend report saved to {output_path}")

if __name__ == "__main__":
    main() 