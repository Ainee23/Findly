from django.urls import path

from . import views

app_name = "qr"

urlpatterns = [
    path("item/<int:item_pk>/", views.item_qr, name="item"),
    path("user_image/<int:user_pk>/", views.user_qr_image, name="user_image"),
    # ✅ Added user QR route with pk instead of username
    path("user/<int:user_pk>/", views.user_qr, name="user"),
    path("scan/", views.qr_scan, name="scan"),
]
