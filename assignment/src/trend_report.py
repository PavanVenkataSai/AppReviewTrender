import pandas as pd
from typing import List, Dict

def generate_trend_report(topics_by_date: Dict[str, List[Dict]], start_date: str, end_date: str) -> pd.DataFrame:
    """
    Given a dict mapping dates to lists of topic dicts, generate a trend report DataFrame
    with topics as rows, dates as columns, and frequency counts as cells.
    """
    # Collect all unique topics
    all_topics = set()
    for topic_list in topics_by_date.values():
        for t in topic_list:
            all_topics.add(t['topic'])
    # Prepare date range
    date_range = pd.date_range(start=start_date, end=end_date)
    date_strs = [d.strftime('%Y-%m-%d') for d in date_range]
    # Initialize frequency table
    freq = {topic: {date: 0 for date in date_strs} for topic in all_topics}
    # Fill frequencies
    for date, topic_list in topics_by_date.items():
        for t in topic_list:
            if date in freq[t['topic']]:
                freq[t['topic']][date] += 1
    # Convert to DataFrame
    df = pd.DataFrame.from_dict(freq, orient='index')
    df = df[date_strs]  # Ensure columns are in date order
    df.index.name = 'Topic'
    return df 