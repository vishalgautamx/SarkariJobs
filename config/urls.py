from django.contrib.sitemaps.views import sitemap
from apps.posts.sitemaps import PostSitemap, StaticViewSitemap
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include
from apps.core.views import home, contact
from django.conf import settings
from django.conf.urls.static import static

from apps.posts.views import (
    search_suggestions,
    search_results,
    category_posts,
    post_detail,
)


admin.site.site_header = "SarkariJobs Administration"
admin.site.site_title = "SarkariJobs Admin"
admin.site.index_title = "SarkariJobs Dashboard"
admin.site.index_template = "admin/dashboard_index.html"


sitemaps = {
    "posts": PostSitemap,
    "static": StaticViewSitemap,
}


urlpatterns = [

    path("admin/", admin.site.urls),

    # CKEditor 5
    path(
        "ckeditor5/",
        include("django_ckeditor_5.urls")
    ),

    path("", include("apps.core.urls")),
    path("", home, name="home"),

    path(
        "search-suggestions/",
        search_suggestions,
        name="search_suggestions"
    ),

    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain"
        ),
        name="robots_txt",
    ),

    path(
        "search/",
        search_results,
        name="search"
    ),

    path(
        "result/",
        category_posts,
        {"category": "Result"},
        name="result"
    ),

    path(
        "admit-card/",
        category_posts,
        {"category": "Admit Card"},
        name="admit_card"
    ),

    path(
        "latest-jobs/",
        category_posts,
        {"category": "Latest Jobs"},
        name="latest_jobs"
    ),

    path(
        "answer-key/",
        category_posts,
        {"category": "Answer Key"},
        name="answer_key"
    ),

    path(
        "documents/",
        category_posts,
        {"category": "Documents"},
        name="documents"
    ),

    path(
        "admission/",
        category_posts,
        {"category": "Admission"},
        name="admission"
    ),

    path(
        "10th-iti-jobs/",
        category_posts,
        {"category": "10th/ITI Jobs"},
        name="iti_jobs"
    ),

    path(
        "outsourcing-jobs/",
        category_posts,
        {"category": "Outsourcing Jobs"},
        name="outsourcing_jobs"
    ),

    path(
        "syllabus/",
        category_posts,
        {"category": "Syllabus"},
        name="syllabus"
    ),

    path(
        "post/<slug:slug>/",
        post_detail,
        name="post_detail"
    ),

    path(
        "contact/",
        contact,
        name="contact"
    ),

    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django_sitemap",
    ),
]


# Media files — development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )