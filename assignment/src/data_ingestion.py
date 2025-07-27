import datetime
from typing import List, Dict
from google_play_scraper import reviews, Sort

def fetch_reviews_for_date(app_id: str, date: datetime.date) -> List[Dict]:
    """
    Fetch reviews for the given app_id from Google Play Store for the specified date.
    Returns a list of review dicts with at least 'content', 'date', and 'rating'.
    """
    all_reviews = []
    count = 200  # Number of reviews to fetch per call (max 200 per call)
    continuation_token = None
    while True:
        result, continuation_token = reviews(
            app_id,
            lang='en',
            country='in',
            sort=Sort.NEWEST,
            count=count,
            continuation_token=continuation_token
        )
        for review in result:
            review_date = review.get('at')
            if isinstance(review_date, datetime.datetime):
                review_date = review_date.date()
            if review_date == date:
                all_reviews.append({
                    'content': review.get('content', ''),
                    'date': review_date,
                    'rating': review.get('score', None),
                    'review_id': review.get('reviewId', None)
                })
            elif review_date < date:
                # Since reviews are sorted by newest, we can stop early
                return all_reviews
        if not continuation_token:
            break
    return all_reviews 