from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

from apps.scraper.services import fetch_page, extract_basic_job_data


INDIA_POST_VACANCIES_URL = (
    "https://www.indiapost.gov.in/vacancies"
)

HEADLESS = True


def fetch_india_post_vacancies():

    notices = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=HEADLESS
        )

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/140.0 Safari/537.36"
            )
        )

        page.goto(
            INDIA_POST_VACANCIES_URL,
            wait_until="networkidle",
            timeout=60000,
        )

        # Give JavaScript-rendered content time to appear.
        page.wait_for_timeout(3000)

        # --------------------------------
        # COLLECT LINKS
        # --------------------------------

        links = page.locator(
            "a[href]"
        ).all()

        for link in links:

            try:

                text = link.inner_text(
                    timeout=3000
                ).strip()

                href = link.get_attribute(
                    "href"
                )

            except Exception:
                continue

            if not href:
                continue

            full_url = urljoin(
                INDIA_POST_VACANCIES_URL,
                href
            )

            # --------------------------------
            # IGNORE NAVIGATION LINKS
            # --------------------------------

            if full_url.rstrip("/") in [
                INDIA_POST_VACANCIES_URL.rstrip("/"),
                "https://www.indiapost.gov.in/vacancies/recruitments",
                "https://www.indiapost.gov.in/vacancies/online-gds",
            ]:
                continue

            # --------------------------------
            # DOCUMENT / RECRUITMENT LINKS
            # --------------------------------

            lower_url = full_url.lower()
            lower_text = text.lower()

            is_document = (
                ".pdf" in lower_url
                or "/api/documents/file/" in lower_url
            )

            recruitment_words = [
                "recruitment",
                "vacanc",
                "driver",
                "artisan",
                "manager",
                "engagement",
                "filling up",
                "direct recruitment",
            ]

            looks_like_recruitment = any(
                word in lower_text
                for word in recruitment_words
            )

            if not (
                is_document
                or looks_like_recruitment
            ):
                continue

            notices.append(
                {
                    "headline": text,
                    "pdf_url": full_url,
                }
            )

        browser.close()

    # --------------------------------
    # REMOVE DUPLICATES
    # --------------------------------

    unique = []

    seen = set()

    for notice in notices:

        key = (
            notice["pdf_url"]
            or notice["headline"]
        )

        if key in seen:
            continue

        seen.add(key)

        unique.append(notice)

    return unique


def detect_india_post_category(headline):

    text = headline.lower().strip()

    # Result
    if "result" in text:
        return "Result"

    # Answer Key
    if "answer key" in text:
        return "Answer Key"

    # Admit Card
    if (
        "admit card" in text
        or "hall ticket" in text
    ):
        return "Admit Card"

    # Syllabus
    if "syllabus" in text:
        return "Syllabus"

    # Actual recruitment/job related keywords
    recruitment_keywords = [
        "recruitment",
        "vacancy",
        "vacancies",
        "engagement",
        "direct recruitment",
        "filling up",
        "appointment",
        "selection",
        "driver",
        "artisan",
        "postman",
        "postal assistant",
        "sorting assistant",
        "mts",
        "gds",
        "gramin dak sevak",
    ]

    if any(
        keyword in text
        for keyword in recruitment_keywords
    ):
        return "Latest Jobs"

    # Everything else = Documents
    return "Documents"

def is_relevant_india_post_notice(headline):         
           
    category = detect_india_post_category(
        headline
    
    )

    return category in [
        "Latest Jobs",
        "Result",
        "Admit Card",
        "Answer Key",
        "Syllabus",
    ]


def process_india_post_notice(notice):

    pdf_url = notice.get(
        "pdf_url",
        ""
    ).strip()

    if not pdf_url:
        return {
            "success": False,
            "error": "No document URL found.",
        }

    try:

        page = fetch_page(
            pdf_url
        )

        data = extract_basic_job_data(
            page
        )

        headline = notice.get(
            "headline",
            ""
        ).strip()

        if headline:
            data["title"] = headline

        data["source_name"] = (
            "India Post"
        )

        data["source_url"] = (
            pdf_url
        )

        return {
            "success": True,
            "headline": headline,
            "pdf_url": pdf_url,
            "data": data,
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e),
        }