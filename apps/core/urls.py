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

    path(
        "feedback/conversation/<str:token>/reply/",
        views.feedback_user_reply,
        name="feedback_user_reply"
    ),

]