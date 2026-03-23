from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReviewForm
from .models import Review
from dashboard.models import ActivityLog

User = get_user_model()  # ✅ Use custom email-based User


def user_reviews(request, user_pk: int):
    # ✅ Lookup by pk — custom User has no username field
    user = get_object_or_404(User, pk=user_pk)
    reviews = Review.objects.filter(reviewee=user).select_related("reviewer").order_by("-created_at")
    stats = reviews.aggregate(avg=Avg("rating"), count=Count("id"))
    return render(
        request,
        "reviews/user.html",
        {"profile_user": user, "reviews": reviews, "stats": stats}
    )


@login_required
def leave_review(request, user_pk: int):
    # ✅ Lookup by pk — custom User has no username field
    user = get_object_or_404(User, pk=user_pk)
    if user.pk == request.user.pk:
        messages.error(request, "You can't review yourself.")
        return redirect("reviews:user", user_pk=user.pk)

    existing = Review.objects.filter(reviewer=request.user, reviewee=user).first()
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=existing)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewee = user
            review.save()
            ActivityLog.objects.create(user=request.user, action='review_added', description=f"Left a review for {user.first_name}")
            messages.success(request, "Review saved.")
            return redirect("reviews:user", user_pk=user.pk)
    else:
        form = ReviewForm(instance=existing)
    return render(request, "reviews/leave.html", {"profile_user": user, "form": form})
