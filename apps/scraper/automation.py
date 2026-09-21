from django.utils.text import slugify

from apps.posts.models import Post
from apps.scraper.models import Source
from apps.scraper.adapters import SOURCE_ADAPTERS

from apps.scraper.adapters.india_post import (
    fetch_india_post_vacancies,
    process_india_post_notice,
    detect_india_post_category,
)

from apps.scraper.adapters.ssc import (
    get_ssc_notice_data,
    process_ssc_notice,
    detect_ssc_category,
)


MAX_NEW_PER_SOURCE = 3


def create_draft_from_data(data, category, source_url, source_name):
    """
    Create one unpublished automated draft.
    """

    title = data.get("title", "")

    if isinstance(title, str):
        title = title.strip()

    if not title:
        title = "Automated Notice"

    # --------------------------------
    # DUPLICATE CHECK
    # --------------------------------

    existing = Post.objects.filter(
        source_url=source_url
    ).first()

    if existing:

        return {
            "created": False,
            "duplicate": True,
            "post": existing,
        }

    # --------------------------------
    # SLUG
    # --------------------------------

    base_slug = slugify(title)

    if not base_slug:
        base_slug = "automated-notice"

    slug = base_slug
    counter = 2

    while Post.objects.filter(
        slug=slug
    ).exists():

        slug = f"{base_slug}-{counter}"
        counter += 1

    # --------------------------------
    # CREATE DRAFT
    # --------------------------------

    post = Post.objects.create(

        title=title,

        slug=slug,

        category=category,

        short_description=data.get(
            "short_description",
            ""
        ),

        total_vacancies=data.get(
            "total_vacancies",
            ""
        ),

        application_start=data.get(
            "application_start",
            ""
        ),

        application_last_date=data.get(
            "application_last_date",
            ""
        ),

        exam_date=data.get(
            "exam_date",
            ""
        ),

        exam_date_link=data.get(
            "exam_date_link",
            ""
        ),

        result_date=data.get(
            "result_date",
            ""
        ),

        result_link=data.get(
            "result_link",
            ""
        ),

        general_fee=data.get(
            "general_fee",
            ""
        ),

        ews_fee=data.get(
            "ews_fee",
            ""
        ),

        sc_st_fee=data.get(
            "sc_st_fee",
            ""
        ),

        obc_fee=data.get(
            "obc_fee",
            ""
        ),

        female_fee=data.get(
            "female_fee",
            ""
        ),

        payment_mode=data.get(
            "payment_mode",
            ""
        ),

        exam_mode=data.get(
            "exam_mode",
            ""
        ),

        minimum_age=data.get(
            "minimum_age",
            ""
        ),

        maximum_age=data.get(
            "maximum_age",
            ""
        ),

        age_relaxation=data.get(
            "age_relaxation",
            ""
        ),

        vacancy_details=data.get(
            "vacancy_details",
            ""
        ),

        eligibility=data.get(
            "eligibility",
            ""
        ),

        selection_process=data.get(
            "selection_process",
            ""
        ),

        content="",

        apply_link=data.get(
            "apply_link",
            ""
        ),

        notification_link=data.get(
            "notification_link",
            ""
        ) or source_url,

        official_website=data.get(
            "official_website",
            ""
        ),

        source_name=source_name,

        source_url=source_url,

        is_automated=True,

        is_published=False,
    )

    return {
        "created": True,
        "duplicate": False,
        "post": post,
    }


def run_ssc_automation():
    """
    Run SSC automation.
    """

    results = {
        "found": 0,
        "new": 0,
        "created": 0,
        "duplicates": 0,
        "errors": 0,
    }

    notices = get_ssc_notice_data(
        page=1,
        limit=10,
    )

    results["found"] = len(notices)

    processed = 0

    for notice in notices:

        if processed >= MAX_NEW_PER_SOURCE:
            break

        headline = notice.get(
            "headline",
            ""
        ).strip()

        pdf_url = notice.get(
            "pdf_url",
            ""
        ).strip()

        if not pdf_url:
            continue

        # --------------------------------
        # DUPLICATE CHECK
        # --------------------------------

        existing = Post.objects.filter(
            source_url=pdf_url
        ).first()

        if existing:

            results["duplicates"] += 1

            continue

        # --------------------------------
        # CATEGORY
        # --------------------------------

        category = detect_ssc_category(
            headline
        )

        # --------------------------------
        # GEMINI
        # --------------------------------

        try:

            result = process_ssc_notice(
                notice
            )

            if not result.get(
                "success"
            ):
                results["errors"] += 1
                continue

            data = result.get(
                "data",
                {}
            )

            # --------------------------------
            # CREATE DRAFT
            # --------------------------------

            draft_result = create_draft_from_data(
                data=data,
                category=category,
                source_url=pdf_url,
                source_name="Staff Selection Commission",
            )

            if draft_result["created"]:

                results["created"] += 1

            else:

                results["duplicates"] += 1

            processed += 1
            results["new"] += 1

        except Exception:

            results["errors"] += 1

    return results

def run_india_post_automation():

    results = {
        "found": 0,
        "new": 0,
        "created": 0,
        "duplicates": 0,
        "errors": 0,
    }

    notices = fetch_india_post_vacancies()

    results["found"] = len(notices)

    processed = 0

    for notice in notices:

        if processed >= MAX_NEW_PER_SOURCE:
            break

        headline = notice.get(
            "headline",
            ""
        ).strip()

        document_url = notice.get(
            "pdf_url",
            ""
        ).strip()

        if not document_url:
            continue

        # --------------------------------
        # DUPLICATE CHECK
        # --------------------------------

        existing = Post.objects.filter(
            source_url=document_url
        ).first()

        if existing:

            results["duplicates"] += 1
            continue

        # --------------------------------
        # CATEGORY
        # --------------------------------

        category = detect_india_post_category(
            headline
        )

        # --------------------------------
        # GEMINI
        # --------------------------------

        try:

            result = process_india_post_notice(
                notice
            )

            if not result.get("success"):
                results["errors"] += 1
                continue

            data = result.get(
                "data",
                {}
            )

            # --------------------------------
            # CREATE DRAFT
            # --------------------------------

            draft_result = create_draft_from_data(
                data=data,
                category=category,
                source_url=document_url,
                source_name="India Post",
            )

            if draft_result["created"]:
                results["created"] += 1
            else:
                results["duplicates"] += 1

            results["new"] += 1
            processed += 1

        except Exception as e:

            error_text = str(e)

            if (
                "429" in error_text
                or "Rate limit exceeded" in error_text
            ):
                raise

            results["errors"] += 1

    return results
def run_all_sources():

    results = {}

    sources = Source.objects.filter(
        is_active=True
    )

    for source in sources:

        source_name = source.name.strip()

        # --------------------------------
        # SSC
        # --------------------------------

        if source_name == "SSC":

            results[source_name] = (
                run_ssc_automation()
            )

            continue

        # --------------------------------
        # INDIA POST
        # --------------------------------

        if source_name == "India Post":

            results[source_name] = (
                run_india_post_automation()
            )

            continue

        # --------------------------------
        # FUTURE ADAPTER
        # --------------------------------

        results[source_name] = {
            "status": "adapter_not_connected",
            "message": (
                "Official source adapter "
                "is not connected yet."
            ),
        }

    return results