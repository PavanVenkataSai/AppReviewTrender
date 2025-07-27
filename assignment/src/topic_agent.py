from typing import List, Dict
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = (
    "You are an expert product analyst. Given a user review, extract the main issue, request, or feedback as a concise topic. "
    "If the topic matches or is similar to any in the provided taxonomy, use the canonical topic name. "
    "Otherwise, create a new concise topic. Return only the topic."
)

def extract_and_canonicalize_topics(reviews: List[Dict], taxonomy: Dict[str, List[str]]) -> List[Dict]:
    """
    Given a list of review dicts, extract topics using an LLM agent and map them to canonical forms using the provided taxonomy.
    Returns a list of dicts with 'topic' and 'review_id'.
    """
    topics = []
    taxonomy_flat = {variant: canonical for canonical, variants in taxonomy.items() for variant in variants}
    canonical_topics = set(taxonomy.keys())

    for review in reviews:
        content = review.get('content', '')
        review_id = review.get('review_id', None)
        # Prepare taxonomy context for the LLM
        taxonomy_context = "\n".join([f"{k}: {', '.join(v)}" for k, v in taxonomy.items()])
        prompt = (
            f"Taxonomy of known topics and their variants:\n{taxonomy_context}\n"
            f"Review: {content}\n"
            "Extract the main topic as per the instructions."
        )
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=20,
                temperature=0.0
            )
            topic = response.choices[0].message.content.strip()
        except Exception as e:
            topic = "Unknown"
        # Deduplicate: map to canonical if possible
        if topic in canonical_topics:
            canonical = topic
        elif topic in taxonomy_flat:
            canonical = taxonomy_flat[topic]
        else:
            canonical = topic  # New topic
        topics.append({"topic": canonical, "review_id": review_id})
    return topics 