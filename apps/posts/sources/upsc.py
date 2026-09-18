import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from apps.posts.automation import create_or_update_automated_post
from .category_detector import detect_category


UPSC_URL = "https://www.upsc.gov.in/"

UPSC_RECRUITMENT_URL = (
    "https://www.upsc.gov.in/recruitment/"
    "recruitment-advertisement"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "Chrome/153.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,*/*;q=0.8"
    ),
}


def fetch_upsc_updates():

    results = []

    try:

        response = requests.get(
            UPSC_RECRUITMENT_URL,
            headers=HEADERS,
            timeout=30,
        )

        response.raise_for_status()

    except requests.RequestException as error:

        print(f"UPSC request error: {error}")

        return {
            "success": False,
            "source": "UPSC",
            "created": 0,
            "updated": 0,
            "total": 0,
            "items": [],
            "error": str(error),
        }

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # ----------------------------------------
    # FIND RECRUITMENT ADVERTISEMENT LINKS
    # ----------------------------------------

    links = soup.find_all("a")

    seen_urls = set()

    for link in links:

        title = link.get_text(
            " ",
            strip=True
        )

        href = link.get(
            "href",
            ""
        )

        if not title or not href:
            continue

        full_url = urljoin(
            UPSC_URL,
            href
        )

        title_lower = title.lower()

        # Only recruitment advertisement items
        if (
            "advertisement no." not in title_lower
            and "advertisement no" not in title_lower
        ):
            continue

        if full_url in seen_urls:
            continue

        seen_urls.add(full_url)

        category = detect_category(
            title
        )

        post, status = (
            create_or_update_automated_post(

                title=title,

                category=category,

                short_description=(
                    "Latest official recruitment "
                    "advertisement from the "
                    "Union Public Service Commission "
                    "(UPSC)."
                ),

                content=(
                    "This update has been collected "
                    "from the official Union Public "
                    "Service Commission (UPSC) website.\n\n"
                    "Candidates should read the complete "
                    "official advertisement carefully "
                    "before applying.\n\n"
                    "Eligibility, vacancies, dates, "
                    "application fee and other conditions "
                    "should be verified from the official "
                    "notification."
                ),

                notification_link=full_url,

                official_website=UPSC_URL,

                source_name="UPSC",

                source_url=full_url,
            )
        )

        results.append({
            "title": title,
            "category": category,
            "url": full_url,
            "status": status,
            "post_id": (
                post.id
                if post
                else None
            ),
        })

    created = sum(
        1
        for item in results
        if item["status"] == "created"
    )

    updated = sum(
        1
        for item in results
        if item["status"] == "updated"
    )

    return {
        "success": True,
        "source": "UPSC",
        "created": created,
        "updated": updated,
        "total": len(results),
        "items": results,
    }