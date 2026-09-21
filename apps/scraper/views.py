from django.http import JsonResponse
from django.utils.text import slugify

from apps.posts.models import Post
from .services import fetch_page, extract_basic_job_data


# =========================================================
# UPDATE EXISTING POST FROM EXTRACTED DATA
# =========================================================

def update_post_from_data(post, data):
    """
    Update an existing unpublished automated draft.

    Important:
    - Empty AI values do not erase existing data.
    - Published posts are never automatically modified.
    - Existing slug is preserved.
    """

    fields = [
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
        "apply_link",
        "notification_link",
        "official_website",
        "source_name",
    ]

    for field in fields:

        new_value = data.get(field, "")

        if isinstance(new_value, str):
            new_value = new_value.strip()

        # Never replace existing information with empty data.
        if new_value:
            setattr(post, field, new_value)

    post.is_automated = True

    # Never auto-publish.
    post.is_published = False

    post.save()

    return post


# =========================================================
# CREATE JOB DRAFT
# =========================================================

def create_job_draft(request):

    url = request.GET.get("url", "").strip()

    # -----------------------------------------------------
    # 1. URL CHECK
    # -----------------------------------------------------

    if not url:
        return JsonResponse(
            {
                "success": False,
                "error": "Please provide an official URL.",
            },
            status=400,
        )

    try:

        # -------------------------------------------------
        # 2. FETCH OFFICIAL PAGE / PDF
        # -------------------------------------------------

        page = fetch_page(url)

        # -------------------------------------------------
        # 3. EXTRACT STRUCTURED DATA USING GEMINI
        # -------------------------------------------------

        data = extract_basic_job_data(page)

        # -------------------------------------------------
        # 4. FIND TITLE
        # -------------------------------------------------

        title = data.get("title", "")

        if isinstance(title, str):
            title = title.strip()

        if not title:
            title = page.get("title", "")

            if isinstance(title, str):
                title = title.strip()

        if not title:
            title = "Automated Job"

        # -------------------------------------------------
        # 5. CHECK EXISTING SOURCE
        # -------------------------------------------------

        existing_post = Post.objects.filter(
            source_url=url
        ).first()

        # =================================================
        # EXISTING POST FOUND
        # =================================================

        if existing_post:

            # ---------------------------------------------
            # Fields which should be compared
            # ---------------------------------------------

            fields_to_check = [
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
                "apply_link",
                "notification_link",
                "official_website",
                "source_name",
            ]

            # ---------------------------------------------
            # Check whether source contains new information
            # ---------------------------------------------

            has_changes = False

            changed_fields = []

            for field in fields_to_check:

                new_value = data.get(field, "")

                if isinstance(new_value, str):
                    new_value = new_value.strip()

                old_value = getattr(
                    existing_post,
                    field,
                    ""
                )

                if isinstance(old_value, str):
                    old_value = old_value.strip()

                # Only consider non-empty extracted data.
                if new_value and new_value != old_value:

                    has_changes = True

                    changed_fields.append(field)

            # =================================================
            # EXISTING POST IS UNPUBLISHED
            # =================================================

            if not existing_post.is_published:

                if has_changes:

                    updated_post = update_post_from_data(
                        existing_post,
                        data
                    )

                    return JsonResponse(
                        {
                            "success": True,
                            "duplicate": False,
                            "updated": True,

                            "message": (
                                "Existing draft updated successfully."
                            ),

                            "post_id": updated_post.id,
                            "title": updated_post.title,
                            "total_vacancies": (
                                updated_post.total_vacancies
                            ),
                            "slug": updated_post.slug,

                            "changed_fields": changed_fields,
                        }
                    )

                # -----------------------------------------
                # No changes
                # -----------------------------------------

                return JsonResponse(
                    {
                        "success": True,
                        "duplicate": True,
                        "updated": False,

                        "message": (
                            "This source already exists "
                            "and has no changes."
                        ),

                        "post_id": existing_post.id,
                        "title": existing_post.title,
                        "total_vacancies": (
                            existing_post.total_vacancies
                        ),
                        "slug": existing_post.slug,

                        "changed_fields": [],
                    }
                )

            # =================================================
            # EXISTING POST IS ALREADY PUBLISHED
            # =================================================

            if existing_post.is_published:

                return JsonResponse(
                    {
                        "success": True,
                        "duplicate": True,
                        "updated": False,

                        "message": (
                            "Published post already exists. "
                            "Automation did not modify it."
                        ),

                        "post_id": existing_post.id,
                        "title": existing_post.title,
                        "total_vacancies": (
                            existing_post.total_vacancies
                        ),
                        "slug": existing_post.slug,

                        "published": True,

                        "source_has_changes": has_changes,

                        "changed_fields": changed_fields,
                    }
                )

        # =================================================
        # 6. CREATE UNIQUE SLUG
        # =================================================

        base_slug = slugify(title)

        if not base_slug:
            base_slug = "automated-job"

        slug = base_slug
        counter = 2

        while Post.objects.filter(slug=slug).exists():

            slug = f"{base_slug}-{counter}"

            counter += 1

        # =================================================
        # 7. CREATE NEW UNPUBLISHED DRAFT
        # =================================================

        post = Post.objects.create(

            # ---------------------------------------------
            # Basic Information
            # ---------------------------------------------

            title=title,

            slug=slug,

            category="Latest Jobs",

            short_description=data.get(
                "short_description",
                ""
            ),

            total_vacancies=data.get(
                "total_vacancies",
                ""
            ),

            # ---------------------------------------------
            # Important Dates
            # ---------------------------------------------

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

            # ---------------------------------------------
            # Application Fee
            # ---------------------------------------------

            general_fee=data.get(
                "general_fee",
                ""
            ),

            ews_fee=data.get(
                "ews_fee",
                ""
            ),

            obc_fee=data.get(
                "obc_fee",
                ""
            ),

            sc_st_fee=data.get(
                "sc_st_fee",
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

            # ---------------------------------------------
            # Exam
            # ---------------------------------------------

            exam_mode=data.get(
                "exam_mode",
                ""
            ),

            # ---------------------------------------------
            # Age
            # ---------------------------------------------

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

            # ---------------------------------------------
            # Vacancy
            # ---------------------------------------------

            vacancy_details=data.get(
                "vacancy_details",
                ""
            ),

            # ---------------------------------------------
            # Eligibility
            # ---------------------------------------------

            eligibility=data.get(
                "eligibility",
                ""
            ),

            # ---------------------------------------------
            # Selection
            # ---------------------------------------------

            selection_process=data.get(
                "selection_process",
                ""
            ),

            # ---------------------------------------------
            # Content
            # ---------------------------------------------

            # No long AI-generated article.
            content="",

            # ---------------------------------------------
            # Important Links
            # ---------------------------------------------

            apply_link=data.get(
                "apply_link",
                ""
            ),

            notification_link=data.get(
                "notification_link",
                ""
            ),

            official_website=data.get(
                "official_website",
                ""
            ),

            # ---------------------------------------------
            # Source
            # ---------------------------------------------

            source_name=data.get(
                "source_name",
                ""
            ),

            source_url=url,

            # ---------------------------------------------
            # Automation
            # ---------------------------------------------

            is_automated=True,

            # VERY IMPORTANT:
            # Automation never publishes automatically.
            is_published=False,
        )

        # =================================================
        # 8. SUCCESS RESPONSE
        # =================================================

        return JsonResponse(
            {
                "success": True,

                "duplicate": False,

                "updated": False,

                "message": (
                    "Draft post created successfully."
                ),

                "post_id": post.id,

                "title": post.title,

                "total_vacancies": (
                    post.total_vacancies
                ),

                "slug": post.slug,

                "published": post.is_published,

                "data": data,
            }
        )

    # =====================================================
    # 9. ERROR HANDLING
    # =====================================================

    except Exception as e:

        return JsonResponse(
            {
                "success": False,

                "error": str(e),
            },
            status=500,
        )