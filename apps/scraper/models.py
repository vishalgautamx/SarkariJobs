from django.db import models


class Source(models.Model):

    CATEGORY_CHOICES = [
        ("Latest Jobs", "Latest Jobs"),
        ("Result", "Result"),
        ("Admit Card", "Admit Card"),
        ("Answer Key", "Answer Key"),
        ("Admission", "Admission"),
        ("Syllabus", "Syllabus"),
        ("Documents", "Documents"),
        ("10th/ITI Jobs", "10th/ITI Jobs"),
        ("Outsourcing Jobs", "Outsourcing Jobs"),
    ]

    name = models.CharField(
        max_length=150
    )

    url = models.URLField(
        unique=True
    )

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default="Latest Jobs"
    )

    is_active = models.BooleanField(
        default=True
    )

    last_checked = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name