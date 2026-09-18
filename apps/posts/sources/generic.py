import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from apps.posts.automation import create_or_update_automated_post
from .category_detector import detect_category


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "Chrome/153.0.0.0 Safari/537.36"
    )
}


def fetch_generic_source(
    source_name,
    url,
    selectors=None,
):
    """
    Generic source fetcher.

    NOTE:
    Generic scraping should only be enabled after
    verifying the official website structure.
    """

    selectors = selectors or {}

    results = []

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=30,
        )

        response.raise_for_status()

    except requests.RequestException as error:

        print(
            f"{source_name} request error: {error}"
        )

        return {
            "success": False,
            "source": source_name,
            "created": 0,
            "updated": 0,
            "total": 0,
            "items": [],
            "error": str(error),
        }

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    container_selector = selectors.get(
        "container",
        "a",
    )

    links = soup.select(
        container_selector
    )

    seen_urls = set()

    for element in links:

        title = element.get_text(
            " ",
            strip=True,
        )

        href = element.get(
            "href",
            "",
        )

        if not title or not href:
            continue

        full_url = urljoin(
            url,
            href,
        )

        if full_url in seen_urls:
            continue

        seen_urls.add(full_url)

        category = detect_category(
            title
        )

        try:

            post, status = (
                create_or_update_automated_post(
                    title=title,
                    category=category,
                    short_description=(
                        f"Latest official update "
                        f"from {source_name}."
                    ),
                    content=(
                        "This update has been collected "
                        "from the official website.\n\n"
                        "Candidates should verify the "
                        "complete official notification "
                        "before taking any action."
                    ),
                    notification_link=full_url,
                    official_website=url,
                    source_name=source_name,
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

        except Exception as error:

            print(
                f"{source_name} post error: "
                f"{error}"
            )

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
        "source": source_name,
        "created": created,
        "updated": updated,
        "total": len(results),
        "items": results,
    }