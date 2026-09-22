from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


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

    # ==========================================================
    # Basic Information
    # ==========================================================

    title = models.CharField(
        max_length=255
    )

    slug = models.SlugField(
        unique=True
    )

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    featured_image = models.ImageField(
        upload_to="post-images/",
        blank=True,
        null=True
    )

    short_description = CKEditor5Field(
    config_name="extends",
    blank=True
)

    total_vacancies = models.CharField(
        max_length=100,
        blank=True
    )

    # ==========================================================
    # Important Dates
    # ==========================================================

    application_start = models.CharField(
        max_length=100,
        blank=True
    )

    application_last_date = models.CharField(
        max_length=100,
        blank=True
    )

    correction_date = models.CharField(
        max_length=100,
        blank=True
    )

    admit_card_date = models.CharField(
        max_length=100,
        blank=True
    )

    exam_date = models.CharField(
        max_length=100,
        blank=True
    )

    exam_date_link = models.URLField(
        blank=True
    )

    result_date = models.CharField(
        max_length=100,
        blank=True
    )

    result_link = models.URLField(
        blank=True
    )

    # ==========================================================
    # Application Fee
    # ==========================================================

    general_fee = models.CharField(
        max_length=100,
        blank=True
    )

    ews_fee = models.CharField(
        max_length=100,
        blank=True
    )

    sc_st_fee = models.CharField(
        max_length=100,
        blank=True
    )

    obc_fee = models.CharField(
        max_length=100,
        blank=True
    )

    female_fee = models.CharField(
        max_length=100,
        blank=True
    )

    payment_mode = models.CharField(
        max_length=20,
        choices=[
            ("Online", "Online"),
            ("Offline", "Offline"),
        ],
        blank=True
    )

    # ==========================================================
    # Exam Mode
    # ==========================================================

    exam_mode = models.CharField(
        max_length=20,
        choices=[
            ("Online", "Online"),
            ("Offline", "Offline"),
        ],
        blank=True
    )

    # ==========================================================
    # Age Limit
    # ==========================================================

    minimum_age = CKEditor5Field(
    "Minimum Age",
    config_name="extends",
    blank=True
    )

    maximum_age = CKEditor5Field(
    "Maximum Age",
    config_name="extends",
    blank=True
)

    age_relaxation = CKEditor5Field(
    "Age Relaxation",
    config_name="extends",
    blank=True
    )

    # ==========================================================
    # Vacancy Details
    # ==========================================================
    vacancy_details = CKEditor5Field(
        "Vacancy Details",
        config_name="extends",
        blank=True
    )

    # ==========================================================
    # Eligibility
    # ==========================================================

    eligibility = CKEditor5Field(
        "Eligibility",
        config_name="extends",
        blank=True
    )

    # ==========================================================
    # Selection Process
    # ==========================================================

    selection_process = CKEditor5Field(
        "Selection Process",
        config_name="extends",
        blank=True
    )

    # ==========================================================
    # Post Details
    # ==========================================================

    post_details = CKEditor5Field(
        "Post Details",
        config_name="extends",
        blank=True
    )
    answer_key = CKEditor5Field(
    config_name="extends",
    blank=True
) 
    answer_key_link = models.URLField(
    blank=True
)
    # ==========================================================
    # Syllabus
    # ==========================================================

    syllabus = CKEditor5Field(
        "Syllabus",
        config_name="extends",
        blank=True
    )
    syllabus_link = models.URLField(
    blank=True
)

    # ==========================================================
    # How To Apply
    # ==========================================================

    how_to_apply = CKEditor5Field(
        "How To Apply",
        config_name="extends",
        blank=True
    )

    # ==========================================================
    # Additional Content
    # ==========================================================

    content = CKEditor5Field(
        "Content",
        config_name="extends",
        blank=True
    )

    # ==========================================================
    # Important Links
    # ==========================================================

    apply_link = models.URLField(
        blank=True
    )

    notification_link = models.URLField(
        blank=True
    )

    official_website = models.URLField(
        blank=True
    )

    # ==========================================================
    # Automation
    # ==========================================================

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

    # ==========================================================
    # System Dates
    # ==========================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # ==========================================================
    # String Representation
    # ==========================================================

    def __str__(self):
        return self.title


class DiscoverItem(models.Model):

    title = models.CharField(
        max_length=100
    )

    link = models.URLField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = [
            "order",
            "-created_at"
        ]

        verbose_name = "Discover Item"

        verbose_name_plural = "Discover Items"
class PostFAQ(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="faqs"
    )

    question = models.CharField(max_length=500)

    answer = CKEditor5Field(
        "Answer",
        config_name="extends",
        blank=True
    )

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Post FAQ"
        verbose_name_plural = "Post FAQs"

    def __str__(self):
        return f"{self.post.title} - {self.question}"