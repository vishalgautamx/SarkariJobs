
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Post, DiscoverItem


# =========================================================
# SEARCH SUGGESTIONS
# =========================================================

def search_suggestions(request):

    query = request.GET.get("q", "").strip()

    if not query:
        return JsonResponse([], safe=False)

    posts = Post.objects.filter(
        title__icontains=query,
        is_published=True
    ).values(
        "title",
        "slug"
    )[:8]

    return JsonResponse(
        list(posts),
        safe=False
    )


# =========================================================
# CATEGORY PAGE
# =========================================================

def category_posts(request, category):

    posts = Post.objects.filter(
        category__iexact=category,
        is_published=True
    ).order_by("-created_at")

    paginator = Paginator(posts, 20)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "category.html",
        {
            "posts": page_obj,
            "category_name": category,
        }
    )


# =========================================================
# INDIVIDUAL POST PAGE
# =========================================================

def post_detail(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug,
        is_published=True
    )

    return render(
        request,
        "post.html",
        {
            "post": post,
        }
    )


# =========================================================
# HOME PAGE
# =========================================================

def home(request):

    latest_jobs = Post.objects.filter(
        category="Latest Jobs",
        is_published=True
    ).order_by("-created_at")[:8]

    discover_items = DiscoverItem.objects.filter(
        is_active=True
    ).order_by("order")[:3]

    return render(
        request,
        "home.html",
        {
            "latest_jobs": latest_jobs,
            "discover_items": discover_items,
        }
    )


# =========================================================
# LATEST JOBS PAGE
# =========================================================

def latest_jobs(request):

    jobs = Post.objects.filter(
        category="Latest Jobs",
        is_published=True
    ).order_by("-created_at")

    return render(
        request,
        "latest_jobs.html",
        {
            "jobs": jobs
        }
    )


# =========================================================
# SEARCH RESULTS
# =========================================================

def search_results(request):

    query = request.GET.get("q", "").strip()

    posts = Post.objects.none()

    if query:

        posts = Post.objects.filter(
            is_published=True
        ).filter(

            Q(title__icontains=query) |

            Q(category__icontains=query) |

            Q(short_description__icontains=query) |

            Q(vacancy_details__icontains=query) |

            Q(eligibility__icontains=query) |

            Q(selection_process__icontains=query) |

            Q(content__icontains=query)

        ).order_by("-created_at")

    paginator = Paginator(posts, 20)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "search.html",
        {
            "posts": page_obj,
            "query": query,
        }
    )