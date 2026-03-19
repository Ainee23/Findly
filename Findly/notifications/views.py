from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Notification




@login_required
def notification_list(request):

    notes = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "notifications/list.html",
        {"notes": notes}
    )


@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect("notifications:list")

