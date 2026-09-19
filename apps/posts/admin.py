
from django.contrib import admin

from .models import Post, DiscoverItem


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    # =====================================================
    # LIST PAGE
    # =====================================================

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

    # =====================================================
    # POST FORM
    # =====================================================

    fieldsets = (

        (
            "Basic Information",
            {
                "fields": (
                    "title",
                    "slug",
                    "category",
                    "short_description",
                )
            }
        ),

        (
            "Important Dates",
            {
                "fields": (
                    "application_start",
                    "application_last_date",
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
            "Selection Process",
            {
                "fields": (
                    "selection_process",
                )
            }
        ),

        (
            "Additional Information",
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

        # =================================================
        # AUTOMATION
        # =================================================

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

        # =================================================
        # SYSTEM DATES
        # =================================================

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
