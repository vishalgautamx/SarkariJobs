from io import BytesIO
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

from .ai_extractor import extract_job_data


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,application/pdf;q=0.8,*/*;q=0.7"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_pdf_text(url):
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    pdf_file = BytesIO(response.content)

    reader = PdfReader(pdf_file)

    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""

        if text.strip():
            pages.append(text.strip())

    return "\n\n".join(pages)


def is_pdf_response(response):
    """
    Detect PDF even when URL does not end with .pdf.
    """

    content_type = response.headers.get(
        "Content-Type",
        ""
    ).lower()

    return (
        "application/pdf" in content_type
        or response.url.lower().split("?")[0].endswith(".pdf")
    )


def fetch_page(url):
    """
    Fetch an official source page.

    Supports:
    - Normal HTML
    - Direct PDF
    - PDF URLs without .pdf extension
    - JavaScript/API pages (HTML is returned for further inspection)
    """

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
        allow_redirects=True,
    )

    response.raise_for_status()

    final_url = response.url

    # -----------------------------------------
    # PDF
    # -----------------------------------------

    if is_pdf_response(response):

        pdf_file = BytesIO(response.content)

        reader = PdfReader(pdf_file)

        pages = []

        for page in reader.pages:

            text = page.extract_text() or ""

            if text.strip():
                pages.append(text.strip())

        pdf_text = "\n\n".join(pages)

        return {
            "url": final_url,
            "title": "",
            "text": pdf_text,
            "soup": None,
            "content_type": "pdf",
            "status_code": response.status_code,
        }

    # -----------------------------------------
    # HTML
    # -----------------------------------------

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    title = ""

    if soup.title:

        title = soup.title.get_text(
            " ",
            strip=True
        )

    # Remove unnecessary elements
    for tag in soup(
        [
            "script",
            "style",
            "noscript",
            "svg",
        ]
    ):
        tag.decompose()

    text = soup.get_text(
        "\n",
        strip=True
    )

    return {
        "url": final_url,
        "title": title,
        "text": text,
        "soup": soup,
        "content_type": "html",
        "status_code": response.status_code,
    }


def extract_page_links(page):
    """
    Extract all usable links from an HTML page.
    """

    soup = page.get("soup")

    if not soup:
        return []

    source_url = page["url"]

    links = []

    for link in soup.find_all(
        "a",
        href=True
    ):

        link_text = link.get_text(
            " ",
            strip=True
        )

        href = link.get(
            "href",
            ""
        ).strip()

        if not href:
            continue

        full_url = urljoin(
            source_url,
            href
        )

        links.append(
            {
                "text": link_text,
                "url": full_url,
            }
        )

    return links


def extract_basic_job_data(page):
    """
    Extract structured job information
    from an official source.
    """

    text = page["text"]

    source_url = page["url"]

    # -----------------------------------------
    # Extract links
    # -----------------------------------------

    links = extract_page_links(page)

    # -----------------------------------------
    # Gemini extraction
    # -----------------------------------------

    data = extract_job_data(
        source_text=text,
        source_url=source_url,
    )

    # -----------------------------------------
    # Preserve source URL
    # -----------------------------------------

    data["source_url"] = source_url

    # -----------------------------------------
    # Official website fallback
    # -----------------------------------------

    if not data.get("official_website"):

        data["official_website"] = source_url

    # -----------------------------------------
    # Apply link fallback
    # -----------------------------------------

    if not data.get("apply_link"):

        for link in links:

            link_text = link["text"].lower()

            if any(
                word in link_text
                for word in [
                    "apply online",
                    "apply now",
                    "online application",
                    "registration",
                    "apply here",
                    "apply",
                ]
            ):

                data["apply_link"] = link["url"]

                break

    # -----------------------------------------
    # Notification link fallback
    # -----------------------------------------

    if not data.get("notification_link"):

        for link in links:

            link_url = link["url"].lower()

            link_text = link["text"].lower()

            if (
                "notification" in link_text
                or "advertisement" in link_text
                or "notice" in link_text
                or "recruitment" in link_text
                or link_url.endswith(".pdf")
            ):

                data["notification_link"] = link["url"]

                break

    # -----------------------------------------
    # Direct PDF = notification
    # -----------------------------------------

    if (
        page.get("content_type") == "pdf"
        and not data.get("notification_link")
    ):

        data["notification_link"] = source_url

    # -----------------------------------------
    # Detect organization
    # -----------------------------------------

    if not data.get("source_name"):

        source_lower = source_url.lower()

        source_map = [

            (
                "indiapost",
                "India Post"
            ),

            (
                "indiapost.gov.in",
                "India Post"
            ),

            (
                "ssc.gov.in",
                "Staff Selection Commission"
            ),

            (
                "upsc.gov.in",
                "Union Public Service Commission"
            ),

            (
                "rrb",
                "Railway Recruitment Board"
            ),

            (
                "ibps.in",
                "Institute of Banking Personnel Selection"
            ),

            (
                "sbi.co.in",
                "State Bank of India"
            ),

            (
                "employmentnews.gov.in",
                "Employment News"
            ),

            (
                "ncs.gov.in",
                "National Career Service"
            ),
        ]

        for keyword, organization in source_map:

            if keyword in source_lower:

                data["source_name"] = organization

                break

    # -----------------------------------------
    # Never generate long AI article
    # -----------------------------------------

    data["content"] = ""

    return data