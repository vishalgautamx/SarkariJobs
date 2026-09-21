
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.posts.models import Post

from apps.scraper.adapters.ssc import (
    get_ssc_notice_data,
    process_ssc_notice,
    detect_ssc_category,
    is_relevant_ssc_notice,
)



MAX_PAGES = 5
NOTICES_PER_PAGE = 10
MAX_NEW_NOTICES_PER_RUN = 3
DRY_RUN = False


class Command(BaseCommand):

    help = "Check SSC notices with pagination and create automated draft posts"

    def handle(self, *args, **options):

        self.stdout.write(
            self.style.NOTICE(
                "Checking SSC notices..."
            )
        )

        total_found = 0
        total_new = 0
        total_skipped = 0
        total_created = 0
        new_notices_processed = 0

        try:

            for page_number in range(
                1,
                MAX_PAGES + 1
            ):

                self.stdout.write("")
                self.stdout.write(
                    self.style.NOTICE(
                        f"========== SSC PAGE {page_number} =========="
                    )
                )

                # --------------------------------
                # FETCH PAGE
                # --------------------------------

                try:

                    notices = get_ssc_notice_data(
                        page=page_number,
                        limit=NOTICES_PER_PAGE,
                    )

                except Exception as e:

                    self.stdout.write(
                        self.style.ERROR(
                            f"SSC API error on page {page_number}: {e}"
                        )
                    )

                    break

                # --------------------------------
                # STOP IF PAGE IS EMPTY
                # --------------------------------

                if not notices:

                    self.stdout.write(
                        self.style.WARNING(
                            "No more notices found. Pagination stopped."
                        )
                    )

                    break

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Found {len(notices)} notices on page {page_number}."
                    )
                )

                total_found += len(notices)

                # --------------------------------
                # PROCESS NOTICES
                # --------------------------------

                for number, notice in enumerate(
                    notices,
                    start=1
                ):

                    headline = notice.get(
                        "headline",
                        ""
                    ).strip()

                    pdf_url = notice.get(
                        "pdf_url",
                        ""
                    ).strip()

                    self.stdout.write("")

                    self.stdout.write(
                        f"{number}. {headline}"
                    )
                    # --------------------------------
# RELEVANCE CHECK
# --------------------------------

                category = detect_ssc_category(
                    headline
                )

                if not is_relevant_ssc_notice(
                    headline
                ):

                    self.stdout.write(
                        self.style.WARNING(
                            f"Not relevant for automation. "
                            f"Category: {category}. Skipping."
                                     )
                                 )
                    total_skipped += 1
                    continue

                    # --------------------------------
                    # NO PDF
                    # --------------------------------

                    if not pdf_url:

                        self.stdout.write(
                            self.style.WARNING(
                                "No PDF found. Skipping."
                            )
                        )

                        total_skipped += 1

                        continue

                    # --------------------------------
                    # SMART DUPLICATE CHECK
                    # --------------------------------

                    existing_post = Post.objects.filter(
                        source_url=pdf_url
                    ).first()

                    if existing_post:

                        self.stdout.write(
                            self.style.WARNING(
                                f"Already exists: Post ID {existing_post.id}"
                            )
                        )

                        self.stdout.write(
                            f"Published: {existing_post.is_published}"
                        )

                        total_skipped += 1

                        continue

               
# NEW NOTICE
# --------------------------------

                    total_new += 1
                    if new_notices_processed >= MAX_NEW_NOTICES_PER_RUN:
                         self.stdout.write(
                              self.style.WARNING(
                                    "Maximum new notices per run reached. "
                                    "Skipping remaining new notices."
                                    )
                                )
                         continue
                    new_notices_processed += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            "New notice found."
                            )
)

                    # --------------------------------
                    # PDF + GEMINI
                    # --------------------------------

                    # --------------------------------
# DRY RUN
# --------------------------------

                    if DRY_RUN:

                               self.stdout.write(
                                   self.style.NOTICE(
                                       "DRY RUN: Gemini extraction skipped."
                                    )
                               )

                               self.stdout.write(
                                   f"Category: {category}"
                               )

                               self.stdout.write(
                                   f"PDF: {pdf_url}"
                               )

                               continue                              

                    try:

                        result = process_ssc_notice(
                            notice
                        )

                        if not result.get(
                            "success"
                        ):

                            self.stdout.write(
                                self.style.ERROR(
                                    "Gemini extraction failed."
                                )
                            )

                            total_skipped += 1

                            continue

                        data = result.get(
                            "data",
                            {}
                        )

                    except Exception as e:

                        error_text = str(e)

                        # Gemini rate limit
                        if (
                            "429" in error_text
                            or "Rate limit exceeded"
                            in error_text
                        ):

                            self.stdout.write(
                                self.style.WARNING(
                                    "Gemini daily rate limit reached."
                                )
                            )

                            self.stdout.write(
                                self.style.WARNING(
                                    "Stopping SSC processing safely."
                                )
                            )

                            return

                        self.stdout.write(
                            self.style.ERROR(
                                f"Processing error: {e}"
                            )
                        )

                        total_skipped += 1

                        continue

                    # --------------------------------
                    # TITLE
                    # --------------------------------

                    title = data.get(
                        "title",
                        ""
                    )

                    if isinstance(
                        title,
                        str
                    ):

                        title = title.strip()

                    if not title:

                        title = headline

                    if not title:

                        title = "SSC Automated Notice"

                    # --------------------------------
                    # CATEGORY
                    # --------------------------------

                    category = detect_ssc_category(
                        headline
                    )

                    # --------------------------------
                    # SLUG
                    # --------------------------------

                    base_slug = slugify(
                        title
                    )

                    if not base_slug:

                        base_slug = (
                            "ssc-automated-notice"
                        )

                    slug = base_slug

                    counter = 2

                    while Post.objects.filter(
                        slug=slug
                    ).exists():

                        slug = (
                            f"{base_slug}-{counter}"
                        )

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
                            pdf_url
                        ),

                        official_website=(
                            "https://ssc.gov.in/"
                        ),

                        source_name=(
                            "Staff Selection Commission"
                        ),

                        source_url=pdf_url,

                        is_automated=True,

                        is_published=False,
                    )

                    total_created += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ Draft created: ID {post.id}"
                        )
                    )

                    self.stdout.write(
                        f"Title: {post.title}"
                    )

                    self.stdout.write(
                        f"Category: {post.category}"
                    )

                    self.stdout.write(
                        f"Published: {post.is_published}"
                    )

            # --------------------------------
            # FINAL SUMMARY
            # --------------------------------

            self.stdout.write("")
            self.stdout.write(
                self.style.NOTICE(
                    "========== SSC SUMMARY =========="
                )
            )

            self.stdout.write(
                f"Total notices found: {total_found}"
            )

            self.stdout.write(
                f"New notices: {total_new}"
            )

            self.stdout.write(
                f"Skipped/existing: {total_skipped}"
            )

            self.stdout.write(
                f"Drafts created: {total_created}"
            )

        except Exception as e:

            self.stdout.write(
                self.style.ERROR(
                    f"✗ SSC automation error: {e}"
                )
            )
