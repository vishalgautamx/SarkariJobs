from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Post


class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Post.objects.filter(
            is_published=True
        ).order_by("-updated_at")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("post_detail", kwargs={"slug": obj.slug})


class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "latest_jobs",
            "result",
            "admit_card",
            "answer_key",
            "documents",
            "admission",
            "iti_jobs",
            "outsourcing_jobs",
            "syllabus",
            "contact",
        ]

    def location(self, item):
        return reverse(item)