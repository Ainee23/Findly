from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import QRScan
from items.models import Item
from .utils import make_qr_png

User = get_user_model()


def qr_scan(request):
    """Renders the HTML5 QR Code scanner page."""
    return render(request, "qr/scan.html")


def item_qr(request, item_pk: int):
    item = get_object_or_404(Item, pk=item_pk)
    url = request.build_absolute_uri(reverse("items:detail", args=[item.pk]))
    img_bytes = make_qr_png(url)

    QRScan.objects.create(
        user=item.owner,
        item=item,
        scan_type="item",
        ip=request.META.get("REMOTE_ADDR")
    )

    return HttpResponse(img_bytes, content_type="image/png")


def user_qr_image(request, user_pk: int):
    """Generates the PNG for a user's QR code."""
    # This encodes the URL to the user_qr (scan) page
    user = get_object_or_404(User, pk=user_pk)
    url = request.build_absolute_uri(reverse("qr:user", args=[user.pk]))
    img_bytes = make_qr_png(url)
    return HttpResponse(img_bytes, content_type="image/png")


def user_qr(request, user_pk: int):
    # ✅ Lookup by pk — custom User has no username field
    user = get_object_or_404(User, pk=user_pk)

    ip = request.META.get("REMOTE_ADDR")

    QRScan.objects.create(
        user=user,
        scan_type="user",
        ip=ip,
    )

    # Pass both user and profile_user to prevent template breaking if it used profile_user
    # Also pass all items reported by this user so the finder can see them
    user_items = user.items.all().order_by("-created_at")
    return render(
        request,
        "qr/user.html",
        {"user": user, "profile_user": user, "user_items": user_items}
    )