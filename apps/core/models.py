from django.db import models


# ==========================================
# HOME INFORMATION SECTIONS
# ==========================================

class HomeSection(models.Model):

    title = models.CharField(max_length=255)

    content = models.TextField()

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


# ==========================================
# DISCOVER MORE
# ==========================================

class DiscoverItem(models.Model):

    title = models.CharField(max_length=255)

    url = models.URLField(blank=True)

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


# ==========================================
# FAQ
# ==========================================

class FAQ(models.Model):

    question = models.CharField(max_length=500)

    answer = models.TextField()

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.question


# ==========================================
# TOP SARKARIJOBS PAGES
# ==========================================

class TopPage(models.Model):

    title = models.CharField(max_length=255)

    url = models.URLField(blank=True)

    row = models.PositiveIntegerField(default=1)

    column = models.PositiveIntegerField(default=1)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["row", "column"]

    def __str__(self):
        return self.title

# ==========================================
# ADMIN REGISTRATION REQUEST
# ==========================================

class AdminRegistrationRequest(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    full_name = models.CharField(max_length=150)

    username = models.CharField(
        max_length=150,
        unique=True
    )

    email = models.EmailField(
        unique=True
    )

    password = models.CharField(
        max_length=128
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.username} - {self.status}"
from django.db import models


class Feedback(models.Model):
    page_url = models.URLField(max_length=500, blank=True)
    rating = models.CharField(max_length=20, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} - {self.created_at:%d-%m-%Y %H:%M}"

# ==========================================
# FEEDBACK REPLIES
# ==========================================

class FeedbackReply(models.Model):

    SENDER_CHOICES = [
        ("user", "User"),
        ("admin", "Admin"),
    ]

    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    sender = models.CharField(
        max_length=10,
        choices=SENDER_CHOICES
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender} - {self.created_at:%d-%m-%Y %H:%M}"