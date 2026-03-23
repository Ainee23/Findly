from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.shortcuts import render

from items.models import Item
from messaging.models import Message, Thread
from notifications.models import Notification
from reviews.models import Review
from dashboard.models import ActivityLog
from django.contrib.auth import get_user_model


def _is_staff(u):
    return u.is_authenticated and u.is_staff


@login_required
def home(request):
    data = {
        "my_items": Item.objects.filter(owner=request.user).count(),
        "my_threads": Thread.objects.filter(participants=request.user).count(),
        "unread_notifications": Notification.objects.filter(user=request.user, is_read=False).count(),
        "recent_activity": Notification.objects.filter(user=request.user).order_by("-created_at")[:6],
    }
    return render(request, "dashboard/home.html", {"data": data})


@user_passes_test(_is_staff)
def admin_overview(request):
    data = {
        "total_users": get_user_model().objects.count(),
        "total_items": Item.objects.count(),
        "claimed_items": Item.objects.filter(status="claimed").count(),
        "lost_items": Item.objects.filter(status="lost").count(),
        "total_messages": Message.objects.count(),
        "total_reviews": Review.objects.count(),
        "items_by_status": list(Item.objects.values("status").annotate(c=Count("id")).order_by("status")),
    }
    activities = ActivityLog.objects.select_related("user").order_by("-created_at")[:15]
    return render(request, "dashboard/admin_overview.html", {"data": data, "activities": activities})