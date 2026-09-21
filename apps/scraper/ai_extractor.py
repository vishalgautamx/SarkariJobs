import os
import json

from google import genai


client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


FIELDS = [
    "title",
    "total_vacancies",
    "short_description",
    "application_start",
    "application_last_date",
    "exam_date",
    "exam_date_link",
    "result_date",
    "result_link",
    "general_fee",
    "ews_fee",
    "obc_fee",
    "sc_st_fee",
    "female_fee",
    "payment_mode",
    "exam_mode",
    "minimum_age",
    "maximum_age",
    "age_relaxation",
    "vacancy_details",
    "eligibility",
    "selection_process",
    "content",
    "apply_link",
    "notification_link",
    "official_website",
    "source_name",
    "source_url",
]


def extract_job_data(source_text, source_url):
    prompt = f"""
You are a structured data extraction system for a government jobs website.

Extract ONLY factual information that is explicitly present in the source text.

IMPORTANT RULES:
1. Do not guess.
2. Do not assume missing information.
3. If a field is not present, return an empty string.
4. Do not copy or generate a full article.
5. Do not add information from your own knowledge.
6. Return ONLY valid JSON.
7. total_vacancies must contain the overall number of posts/vacancies if explicitly mentioned.
8. vacancy_details should contain detailed vacancy/category information if available.
9. Keep content short. Do not generate a long article.
10. Preserve dates and fee information as stated in the source.
11. source_url must be exactly: {source_url}

Return exactly these fields:

{json.dumps(FIELDS, indent=2)}

SOURCE TEXT:
{source_text}
"""

    response = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
    )

    text = response.output_text.strip()

    # Remove accidental markdown JSON fences
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    data = json.loads(text)

    # Make sure every expected field exists
    for field in FIELDS:
        data.setdefault(field, "")

    return data