from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model

from .models import QRScan
from items.models import Item
from .utils import make_qr_png

User = get_user_model()  # ✅ Use custom email-based User


def item_qr(request, item_pk: int):
    item = get_object_or_404(Item, pk=item_pk)
    url = request.build_absolute_uri(f"/items/{item.pk}/")
    png = make_qr_png(url)
    return HttpResponse(png, content_type="image/png")


def user_qr(request, user_pk: int):
    # ✅ Lookup by pk — custom User has no username field
    user = get_object_or_404(User, pk=user_pk)

    ip = request.META.get("REMOTE_ADDR")

    QRScan.objects.create(
        user=user,
        ip=ip,
    )

    return render(
        request,
        "qr/user.html",
        {"profile_user": user}
    )