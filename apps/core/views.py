from django.shortcuts import render
from apps.posts.models import Post
from apps.core.models import HomeSection
from .models import HomeSection, DiscoverItem, FAQ, TopPage
home_sections = HomeSection.objects.filter(
    is_active=True
).order_by("order")

discover_items = DiscoverItem.objects.filter(
    is_active=True
).order_by("order")

faqs = FAQ.objects.filter(
    is_active=True
).order_by("order")

top_pages = TopPage.objects.filter(
    is_active=True
).order_by("row", "column")

def home(request):
    home_sections = HomeSection.objects.filter(
    is_active=True
).order_by("order")

    results = Post.objects.filter(
        category__iexact="Result"
    ).order_by("-created_at")[:15]

    admit_cards = Post.objects.filter(
        category__iexact="Admit Card"
    ).order_by("-created_at")[:15]

    latest_jobs = Post.objects.filter(
        category__iexact="Latest Jobs"
    ).order_by("-created_at")[:15]

    answer_keys = Post.objects.filter(
        category__iexact="Answer Key"
    ).order_by("-created_at")[:15]

    documents = Post.objects.filter(
        category__iexact="Documents"
    ).order_by("-created_at")[:15]

    admissions = Post.objects.filter(
        category__iexact="Admission"
    ).order_by("-created_at")[:15]

    iti_jobs = Post.objects.filter(
        category__iexact="10th/ITI Jobs"
    ).order_by("-created_at")[:15]

    outsourcing_jobs = Post.objects.filter(
        category__iexact="Outsourcing Jobs"
    ).order_by("-created_at")[:15]

    syllabus = Post.objects.filter(
        category__iexact="Syllabus"
    ).order_by("-created_at")[:15]
    latest_jobs = Post.objects.filter(
    category__iexact="Latest Jobs"
).order_by("-created_at")[:8]

    return render(request, "home.html", {
        "results": results,
        "admit_cards": admit_cards,
        "latest_jobs": latest_jobs,
        "answer_keys": answer_keys,
        "documents": documents,
        "admissions": admissions,
        "iti_jobs": iti_jobs,
        "outsourcing_jobs": outsourcing_jobs,
        "syllabus": syllabus,
        "home_sections": home_sections,
"discover_items": discover_items,
"faqs": faqs,
"top_pages": top_pages,
"latest_jobs": latest_jobs,
    })
def contact(request):
    return render(request, "contact.html")

from django.contrib import messages
from django.core import signing
from django.shortcuts import get_object_or_404, redirect, render

from .models import Feedback, FeedbackReply


# ==========================================
# SUBMIT FEEDBACK
# ==========================================

def submit_feedback(request):

    if request.method != "POST":
        return redirect("/")

    page_url = request.POST.get("page_url", "").strip()
    rating = request.POST.get("rating", "").strip()
    message = request.POST.get("message", "").strip()

    # Feedback create
    feedback = Feedback.objects.create(
        page_url=page_url,
        rating=rating,
        message=message,
    )

    # First user message as conversation reply
    if message:
        FeedbackReply.objects.create(
            feedback=feedback,
            sender="user",
            message=message,
        )

    # Secure signed conversation token
    token = signing.dumps({
        "feedback_id": feedback.id
    })

    return redirect(
        "feedback_conversation",
        token=token
    )


# ==========================================
# FEEDBACK CONVERSATION
# ==========================================

def feedback_conversation(request, token):

    try:
        data = signing.loads(token)
        feedback_id = data["feedback_id"]

    except (signing.BadSignature, signing.SignatureExpired, KeyError):
        return render(
            request,
            "feedback_invalid.html",
            status=400
        )

    feedback = get_object_or_404(
        Feedback,
        id=feedback_id
    )

    replies = feedback.replies.all()

    return render(
        request,
        "feedback_conversation.html",
        {
            "feedback": feedback,
            "replies": replies,
            "token": token,
        }
    )


# ==========================================
# USER REPLY
# ==========================================

def feedback_user_reply(request, token):

    if request.method != "POST":
        return redirect("/")

    try:
        data = signing.loads(token)
        feedback_id = data["feedback_id"]

    except (signing.BadSignature, signing.SignatureExpired, KeyError):
        return render(
            request,
            "feedback_invalid.html",
            status=400
        )

    feedback = get_object_or_404(
        Feedback,
        id=feedback_id
    )

    message = request.POST.get(
        "message",
        ""
    ).strip()

    if message:

        FeedbackReply.objects.create(
            feedback=feedback,
            sender="user",
            message=message,
        )

    return redirect(
        "feedback_conversation",
        token=token
    )