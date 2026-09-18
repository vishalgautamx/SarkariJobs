from django import template

from apps.posts.models import Post
from apps.core.models import FAQ, DiscoverItem


register = template.Library()


@register.simple_tag
def dashboard_stats():
    return {
        "total_posts": Post.objects.count(),
        "latest_jobs": Post.objects.filter(
            category="Latest Jobs"
        ).count(),
        "results": Post.objects.filter(
            category="Result"
        ).count(),
        "admit_cards": Post.objects.filter(
            category="Admit Card"
        ).count(),
        "faqs": FAQ.objects.count(),
        "discover_items": DiscoverItem.objects.count(),
    }