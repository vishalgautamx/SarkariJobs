import requests


SSC_NOTICE_API = (
    "https://ssc.gov.in/api/general-website/portal/notice-boards"
)

SSC_ATTACHMENT_BASE = (
    "https://ssc.gov.in/api/attachment/"
)


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


def fetch_ssc_notices(page=1, limit=10):

    params = {
        "page": page,
        "limit": limit,
        "contentType": "notice-boards",
        "key": "createdAt",
        "order": "DESC",
        "isAttachment": "true",
        "language": "english",
        "attributes": (
            "id,headline,examId,contentType,redirectUrl,"
            "startDate,endDate,language,createdAt"
        ),
    }

    response = requests.get(
        SSC_NOTICE_API,
        params=params,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()
def detect_ssc_category(headline):

    text = headline.lower()

    if "answer key" in text:
        return "Answer Key"

    if "result" in text:
        return "Result"

    if "admit card" in text or "hall ticket" in text:
        return "Admit Card"

    if "syllabus" in text:
        return "Syllabus"

    if (
        "recruitment" in text
        or "examination" in text
        or "exam" in text
        or "vacancy" in text
    ):
        return "Latest Jobs"

    return "Documents"

def is_relevant_ssc_notice(headline):

    category = detect_ssc_category(headline)

    relevant_categories = [
        "Latest Jobs",
        "Result",
        "Admit Card",
        "Answer Key",
        "Syllabus",
    ]

    return category in relevant_categories


def get_ssc_notice_data(page=1, limit=10):

    response_data = fetch_ssc_notices(
        page=page,
        limit=limit,
    )

    notices = []

    for item in response_data.get("data", []):

        attachments = item.get(
            "attachments",
            []
        )

        pdf_url = ""

        pdf_filename = ""

        if attachments:

            for attachment in attachments:

                if (
                    attachment.get("type")
                    == "application/pdf"
                ):

                    pdf_filename = attachment.get(
                        "fileName",
                        ""
                    )

                    pdf_path = attachment.get(
                        "path",
                        ""
                    )

                    if pdf_path:

                        pdf_path = pdf_path.replace(
                            "\\",
                            "/"
                        )

                        pdf_url = (
                            SSC_ATTACHMENT_BASE
                            + pdf_path
                        )

                    break

        notices.append(
            {
                "id": item.get("id", ""),
                "headline": item.get(
                    "headline",
                    ""
                ),
                "exam_id": item.get(
                    "examId",
                    ""
                ),
                "created_at": item.get(
                    "createdAt",
                    ""
                ),
                "redirect_url": item.get(
                    "redirectUrl",
                    ""
                ),
                "pdf_filename": pdf_filename,
                "pdf_url": pdf_url,
            }
        )

    return notices

def process_ssc_notice(notice):
    """
    Process one SSC notice through the existing
    PDF + Gemini extraction pipeline.
    """

    from apps.scraper.services import fetch_page, extract_basic_job_data

    pdf_url = notice.get("pdf_url", "")

    if not pdf_url:
        return {
            "success": False,
            "error": "No PDF URL found.",
        }

    page = fetch_page(pdf_url)

    data = extract_basic_job_data(page)

    data["title"] = notice.get(
        "headline",
        data.get("title", "")
    )

    data["source_name"] = "Staff Selection Commission"

    data["source_url"] = pdf_url

    return {
        "success": True,
        "notice_id": notice.get("id", ""),
        "headline": notice.get("headline", ""),
        "pdf_url": pdf_url,
        "data": data,
    }