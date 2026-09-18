import requests

from apps.posts.automation import create_or_update_automated_post
from .category_detector import detect_category


SSC_URL = "https://ssc.gov.in/"

SSC_NOTICE_API = (
    "https://ssc.gov.in/api/general-website/portal/notice-boards"
)

SSC_ATTACHMENT_BASE = (
    "https://ssc.gov.in/api/attachment/"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "Chrome/153.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Referer": "https://ssc.gov.in/home/notice-board",
}


def build_attachment_url(path):
    """
    Convert SSC API attachment path into
    official downloadable PDF URL.
    """

    if not path:
        return ""

    path = str(path).replace("\\", "/").lstrip("/")

    if path.startswith("uploads/"):
        return (
            SSC_ATTACHMENT_BASE
            + path
        )

    return ""


def fetch_ssc_updates():

    params = {
        "page": 1,
        "limit": 50,
        "contentType": "notice-boards",
        "key": "createdAt",
        "order": "DESC",
        "isAttachment": "true",
        "language": "english",
        "attributes": (
            "id,headline,examId,contentType,"
            "redirectUrl,startDate,endDate,"
            "language,createdAt"
        ),
    }

    try:

        response = requests.get(
            SSC_NOTICE_API,
            headers=HEADERS,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException as error:

        print(
            f"SSC API error: {error}"
        )

        return {
            "success": False,
            "source": "SSC",
            "created": 0,
            "updated": 0,
            "total": 0,
            "items": [],
            "error": str(error),
        }

    except ValueError as error:

        print(
            f"SSC JSON error: {error}"
        )

        return {
            "success": False,
            "source": "SSC",
            "created": 0,
            "updated": 0,
            "total": 0,
            "items": [],
            "error": str(error),
        }

    # -----------------------------
    # GET NOTICE LIST
    # -----------------------------

    notice_list = []

    if isinstance(data, dict):

        if isinstance(
            data.get("data"),
            list
        ):
            notice_list = data["data"]

        elif isinstance(
            data.get("data"),
            dict
        ):

            if isinstance(
                data["data"].get("data"),
                list
            ):
                notice_list = data["data"]["data"]

            elif isinstance(
                data["data"].get("items"),
                list
            ):
                notice_list = data["data"]["items"]

            elif isinstance(
                data["data"].get("results"),
                list
            ):
                notice_list = data["data"]["results"]

        elif isinstance(
            data.get("results"),
            list
        ):
            notice_list = data["results"]

    elif isinstance(data, list):

        notice_list = data

    print(
        f"SSC notices received from API: "
        f"{len(notice_list)}"
    )

    results = []

    # -----------------------------
    # PROCESS NOTICES
    # -----------------------------

    for notice in notice_list:

        if not isinstance(
            notice,
            dict
        ):
            continue

        title = (
            notice.get("headline")
            or notice.get("title")
            or notice.get("name")
            or ""
        )

        title = str(title).strip()

        if not title:
            continue

        # -------------------------
        # ATTACHMENT URL
        # -------------------------

        attachment_url = ""

        attachments = notice.get(
            "attachments"
        )

        if isinstance(
            attachments,
            list
        ):

            for attachment in attachments:

                if not isinstance(
                    attachment,
                    dict
                ):
                    continue

                # SSC API gives "path"
                path = attachment.get(
                    "path"
                )

                attachment_url = (
                    build_attachment_url(
                        path
                    )
                )

                if attachment_url:
                    break

                # Fallback fields
                attachment_url = (
                    attachment.get("url")
                    or attachment.get(
                        "fileUrl"
                    )
                    or attachment.get(
                        "downloadUrl"
                    )
                    or ""
                )

                if attachment_url:
                    break

        # -------------------------
        # FALLBACK URL
        # -------------------------

        if not attachment_url:

            attachment_url = (
                notice.get(
                    "primaryDocumentUrl"
                )
                or notice.get(
                    "documentUrl"
                )
                or notice.get(
                    "attachmentUrl"
                )
                or ""
            )

        redirect_url = (
            notice.get("redirectUrl")
            or ""
        )

        source_url = (
            attachment_url
            or redirect_url
            or SSC_URL
        )

        # -------------------------
        # CATEGORY
        # -------------------------

        category = detect_category(
            title
        )

        # -------------------------
        # CREATE / UPDATE
        # -------------------------

        post, status = (
            create_or_update_automated_post(

                title=title,

                category=category,

                short_description=(
                    "Latest official update "
                    "from Staff Selection "
                    "Commission (SSC)."
                ),

                content=(
                    "This update has been "
                    "collected from the official "
                    "Staff Selection Commission "
                    "(SSC) website.\n\n"
                    "Candidates should verify "
                    "the complete notification "
                    "on the official SSC website "
                    "before applying or taking "
                    "any action."
                ),

                notification_link=(
                    attachment_url
                ),

                official_website=SSC_URL,

                source_name="SSC",

                source_url=source_url,
            )
        )

        results.append({

            "title": title,

            "category": category,

            "url": source_url,

            "status": status,

            "post_id": (
                post.id
                if post
                else None
            ),

        })

    # -----------------------------
    # SUMMARY
    # -----------------------------

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

        "source": "SSC",

        "created": created,

        "updated": updated,

        "total": len(results),

        "items": results,

    }