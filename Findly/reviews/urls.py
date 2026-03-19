from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    # ✅ Changed from <str:username> to <int:user_pk> — custom User has no username
    path("user/<int:user_pk>/", views.user_reviews, name="user"),
    path("user/<int:user_pk>/leave/", views.leave_review, name="leave"),
]
