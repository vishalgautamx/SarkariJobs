from django.urls import path

from . import views


urlpatterns = [

    path(
        "feedback/submit/",
        views.submit_feedback,
        name="feedback_submit"
    ),

    path(
        "feedback/conversation/<str:token>/",
        views.feedback_conversation,
        name="feedback_conversation"
    ),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("disclaimer/", views.disclaimer, name="disclaimer"),
    path(
    "terms-and-conditions/",
    views.terms_conditions,
    name="terms_conditions"
),
path("about/", views.about, name="about"),
    

    path(
        "feedback/conversation/<str:token>/reply/",
        views.feedback_user_reply,
        name="feedback_user_reply"
    ),

]