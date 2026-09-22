from django.contrib import admin
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Post, DiscoverItem, PostFAQ


class PostFAQInline(admin.TabularInline):
    model = PostFAQ
    extra = 0
    fields = (
        "question",
        "answer",
        "order",
        "is_active",
    )
    ordering = ("order",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "source_name",
        "is_automated",
        "is_published",
        "created_at",
        "last_checked",
    )

    list_filter = (
        "category",
        "source_name",
        "is_automated",
        "is_published",
        "created_at",
    )

    search_fields = (
        "title",
        "content",
        "short_description",
        "source_name",
        "source_url",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    list_editable = (
        "is_published",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "last_checked",
    )

    inlines = [
        PostFAQInline,
    ]

    fieldsets = (

        (
            "Basic Information",
            {
                "fields": (
                    "title",
                    "featured_image",
                    "slug",
                    "category",
                    "short_description",
                    "total_vacancies",
                )
            }
        ),

        (
            "Important Dates",
            {
                "fields": (
                    "application_start",
                    "application_last_date",
                    "correction_date",
                    "admit_card_date",
                    "exam_date",
                    "exam_date_link",
                    "result_date",
                    "result_link",
                )
            }
        ),

        (
            "Application Fee",
            {
                "fields": (
                    "general_fee",
                    "ews_fee",
                    "obc_fee",
                    "sc_st_fee",
                    "female_fee",
                    "payment_mode",
                )
            }
        ),

        (
            "Exam Information",
            {
                "fields": (
                    "exam_mode",
                )
            }
        ),

        (
            "Age Limit",
            {
                "fields": (
                    "minimum_age",
                    "maximum_age",
                    "age_relaxation",
                )
            }
        ),

        (
            "Vacancy Details",
            {
                "fields": (
                    "vacancy_details",
                )
            }
        ),

        (
            "Eligibility",
            {
                "fields": (
                    "eligibility",
                )
            }
        ),

        (
            "Post Details",
            {
                "fields": (
                    "post_details",
                )
            }
        ),

        (
            "Selection Process",
            {
                "fields": (
                    "selection_process",
                )
            }
        ),

        (
            "Syllabus",
            {
                "fields": (
                    "syllabus",
                )
            }
        ),

        (
            "How To Apply",
            {
                "fields": (
                    "how_to_apply",
                )
            }
        ),

        (
            "Additional Content",
            {
                "fields": (
                    "content",
                )
            }
        ),

        (
            "Important Links",
            {
                "fields": (
                    "apply_link",
                    "notification_link",
                    "official_website",
                )
            }
        ),

        (
            "Automation",
            {
                "fields": (
                    "source_name",
                    "source_url",
                    "is_automated",
                    "is_published",
                    "last_checked",
                )
            }
        ),

        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            }
        ),

    )


@admin.register(DiscoverItem)
class DiscoverItemAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "link",
        "is_active",
        "order",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "title",
        "link",
    )

    list_editable = (
        "is_active",
        "order",
    )

    ordering = (
        "order",
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )


@admin.register(PostFAQ)
class PostFAQAdmin(admin.ModelAdmin):

    list_display = (
        "question",
        "post",
        "order",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "post",
    )

    search_fields = (
        "question",
        "answer",
        "post__title",
    )

    list_editable = (
        "order",
        "is_active",
    )

    ordering = (
        "post",
        "order",
    )

    readonly_fields = (
        "created_at",
    )