from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("admin/", admin.site.urls),

    # ✅ Core app — home, login, logout, signup, dashboards
    path("", include("core.urls")),

    # ✅ Accounts — register, login (CBV), logout, profile
    path("accounts/", include("accounts.urls")),

    # ✅ Items — list, create, detail, verify, map, etc.
    path("items/", include("items.urls")),

    # ✅ Messaging — inbox, thread, start
    path("messaging/", include("messaging.urls")),

    # ✅ Notifications — list, mark-read
    path("notifications/", include("notifications.urls")),

    # ✅ Reviews — user reviews, leave review
    path("reviews/", include("reviews.urls")),

    # ✅ Dashboard — home, admin overview
    path("dashboard/", include("dashboard.urls")),

    # ✅ QR — item QR, user QR
    path("qr/", include("qr.urls")),

    # ✅ AI — health endpoint
    path("ai/", include("ai.urls")),
    
    path(
    "password_reset/",
    auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html"
    ),
    name="password_reset",
),

path(
    "password_reset_done/",
    auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"
    ),
    name="password_reset_done",
),

path(
    "reset/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html"
    ),
    name="password_reset_confirm",
),

path(
    "reset_done/",
    auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"
    ),
    name="password_reset_complete",
),
]

# ✅ Serve media files (development + production without external storage)
from django.urls import re_path
from django.views.static import serve
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# -- TEMPORARY ENDPOINT TO CREATE ADMIN --
from django.http import HttpResponse
def create_admin(request):
    from core.models import User
    user, created = User.objects.get_or_create(email="owner@findly.com")
    user.set_password("findly123")
    user.is_staff = True
    user.is_superuser = True
    user.role = "owner"
    user.save()
    if created:
        return HttpResponse("✅ Admin created! Email: <b>owner@findly.com</b> | Password: <b>findly123</b>")
    return HttpResponse("✅ Admin password reset to <b>findly123</b>! Please try logging in now at /login/")

urlpatterns += [
    path("setup-admin-user/", create_admin),
]