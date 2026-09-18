from django.contrib import admin

from .models import (
    HomeSection,
    DiscoverItem,
    FAQ,
    TopPage,
    AdminRegistrationRequest,
    Feedback,
    FeedbackReply,
)


# ==========================================
# HOME INFORMATION SECTIONS
# ==========================================

@admin.register(HomeSection)
class HomeSectionAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "order",
        "is_active",
    )

    list_editable = (
        "order",
        "is_active",
    )

    search_fields = (
        "title",
        "content",
    )

    ordering = (
        "order",
    )


# ==========================================
# DISCOVER MORE
# ==========================================

@admin.register(DiscoverItem)
class DiscoverItemAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "url",
        "order",
        "is_active",
    )

    list_editable = (
        "order",
        "is_active",
    )

    search_fields = (
        "title",
    )

    ordering = (
        "order",
    )


# ==========================================
# FAQ
# ==========================================

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):

    list_display = (
        "question",
        "order",
        "is_active",
    )

    list_editable = (
        "order",
        "is_active",
    )

    search_fields = (
        "question",
        "answer",
    )

    ordering = (
        "order",
    )


# ==========================================
# TOP SARKARIJOBS PAGES
# ==========================================

@admin.register(TopPage)
class TopPageAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "row",
        "column",
        "is_active",
    )

    list_editable = (
        "row",
        "column",
        "is_active",
    )

    search_fields = (
        "title",
    )

    ordering = (
        "row",
        "column",
    )


# ==========================================
# ADMIN REGISTRATION REQUESTS
# ==========================================

@admin.register(AdminRegistrationRequest)
class AdminRegistrationRequestAdmin(admin.ModelAdmin):

    list_display = (
        "username",
        "email",
        "full_name",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "username",
        "email",
        "full_name",
    )

    ordering = (
        "-created_at",
    )


# ==========================================
# FEEDBACK REPLIES INLINE
# ==========================================

class FeedbackReplyInline(admin.TabularInline):

    model = FeedbackReply

    extra = 1

    fields = (
        "sender",
        "message",
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "created_at",
    )


# ==========================================
# FEEDBACK
# ==========================================

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "rating",
        "message",
        "page_url",
        "created_at",
    )

    list_filter = (
        "rating",
        "created_at",
    )

    search_fields = (
        "message",
        "page_url",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    inlines = [
        FeedbackReplyInline,
    ]


# ==========================================
# FEEDBACK REPLIES
# ==========================================

@admin.register(FeedbackReply)
class FeedbackReplyAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "feedback",
        "sender",
        "message",
        "created_at",
    )

    list_filter = (
        "sender",
        "created_at",
    )

    search_fields = (
        "message",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )