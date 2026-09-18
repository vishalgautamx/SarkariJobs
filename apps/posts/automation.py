from django.utils import timezone
from django.utils.text import slugify

from .models import Post


def create_or_update_automated_post(
    title,
    category,
    short_description="",
    application_start="",
    application_last_date="",
    exam_date="",
    general_fee="",
    sc_st_fee="",
    female_fee="",
    minimum_age="",
    maximum_age="",
    age_relaxation="",
    vacancy_details="",
    eligibility="",
    selection_process="",
    content="",
    apply_link="",
    notification_link="",
    official_website="",
    source_name="",
    source_url="",
):
    """
    Create a new automated post or update an existing post.

    This function is reusable for:
    SSC, IBPS, Railway, UPPSC, India Post, etc.
    """

    title = (title or "").strip()
    source_name = (source_name or "").strip()
    source_url = (source_url or "").strip()

    if not title:
        return None, "Title is required."

    if not source_name:
        return None, "Source name is required."

    if not source_url:
        return None, "Source URL is required."

    # -------------------------------------------------
    # 1. Generate base slug
    # -------------------------------------------------

    base_slug = slugify(title)

    if not base_slug:
        base_slug = "automated-post"

    # -------------------------------------------------
    # 2. Duplicate check
    # -------------------------------------------------

    existing_post = Post.objects.filter(
        source_name=source_name,
        source_url=source_url,
    ).first()

    # -------------------------------------------------
    # 3. If source already exists → UPDATE
    # -------------------------------------------------

    if existing_post:

        existing_post.title = title
        existing_post.category = category
        existing_post.short_description = short_description

        existing_post.application_start = application_start
        existing_post.application_last_date = application_last_date
        existing_post.exam_date = exam_date

        existing_post.general_fee = general_fee
        existing_post.sc_st_fee = sc_st_fee
        existing_post.female_fee = female_fee

        existing_post.minimum_age = minimum_age
        existing_post.maximum_age = maximum_age
        existing_post.age_relaxation = age_relaxation

        existing_post.vacancy_details = vacancy_details
        existing_post.eligibility = eligibility
        existing_post.selection_process = selection_process

        existing_post.content = content

        existing_post.apply_link = apply_link
        existing_post.notification_link = notification_link
        existing_post.official_website = official_website

        existing_post.is_automated = True
        existing_post.is_published = True
        existing_post.last_checked = timezone.now()

        existing_post.save()

        return existing_post, "updated"

    # -------------------------------------------------
    # 4. Slug duplicate protection
    # -------------------------------------------------

    slug = base_slug

    counter = 2

    while Post.objects.filter(slug=slug).exists():

        slug = f"{base_slug}-{counter}"

        counter += 1

    # -------------------------------------------------
    # 5. Create NEW automated post
    # -------------------------------------------------

    post = Post.objects.create(

        title=title,

        slug=slug,

        category=category,

        short_description=short_description,

        application_start=application_start,
        application_last_date=application_last_date,
        exam_date=exam_date,

        general_fee=general_fee,
        sc_st_fee=sc_st_fee,
        female_fee=female_fee,

        minimum_age=minimum_age,
        maximum_age=maximum_age,
        age_relaxation=age_relaxation,

        vacancy_details=vacancy_details,

        eligibility=eligibility,

        selection_process=selection_process,

        content=content,

        apply_link=apply_link,
        notification_link=notification_link,
        official_website=official_website,

        source_name=source_name,
        source_url=source_url,

        is_automated=True,
        is_published=True,

        last_checked=timezone.now(),
    )

    return post, "created"