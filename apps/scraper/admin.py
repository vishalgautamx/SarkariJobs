from django.contrib import admin

from .models import Source


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "is_active",
        "last_checked",
        "created_at",
    )

    list_filter = (
        "category",
        "is_active",
    )

    search_fields = (
        "name",
        "url",
    )

    ordering = (
        "-created_at",
    )

    list_editable = (
        "is_active",
    )