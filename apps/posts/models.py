from django.db import models


class Post(models.Model):

    CATEGORY_CHOICES = [
        ("Latest Jobs", "Latest Jobs"),
        ("Result", "Result"),
        ("Admit Card", "Admit Card"),
        ("Answer Key", "Answer Key"),
        ("Documents", "Documents"),
        ("Admission", "Admission"),
        ("10th/ITI Jobs", "10th/ITI Jobs"),
        ("Outsourcing Jobs", "Outsourcing Jobs"),
        ("Syllabus", "Syllabus"),
    ]

    # Basic Information
    title = models.CharField(max_length=255)

    slug = models.SlugField(unique=True)

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    short_description = models.TextField(blank=True)

    # Important Dates
    application_start = models.CharField(
        max_length=100,
        blank=True
    )

    application_last_date = models.CharField(
        max_length=100,
        blank=True
    )

    exam_date = models.CharField(
        max_length=100,
        blank=True
    )

    # Application Fee
    general_fee = models.CharField(
        max_length=100,
        blank=True
    )

    sc_st_fee = models.CharField(
        max_length=100,
        blank=True
    )

    female_fee = models.CharField(
        max_length=100,
        blank=True
    )

    # Age Limit
    minimum_age = models.CharField(
        max_length=100,
        blank=True
    )

    maximum_age = models.CharField(
        max_length=100,
        blank=True
    )

    age_relaxation = models.TextField(
        blank=True
    )

    # Vacancy
    vacancy_details = models.TextField(
        blank=True
    )

    # Eligibility
    eligibility = models.TextField(
        blank=True
    )

    # Selection Process
    selection_process = models.TextField(
        blank=True
    )

    # Additional Content
    content = models.TextField(
        blank=True
    )

    # Important Links
    apply_link = models.URLField(
        blank=True
    )

    notification_link = models.URLField(
        blank=True
    )

    official_website = models.URLField(
        blank=True
    )

    # Automation
    source_name = models.CharField(
        max_length=100,
        blank=True
    )

    source_url = models.URLField(
        blank=True
    )

    is_automated = models.BooleanField(
        default=False
    )

    is_published = models.BooleanField(
        default=True
    )

    last_checked = models.DateTimeField(
        null=True,
        blank=True
    )
    # Dates
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title

class DiscoverItem(models.Model):

    title = models.CharField(max_length=100)

    link = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)

    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Discover Item"
        verbose_name_plural = "Discover Items"