from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import (
    UserLoginView,
    UserLogoutView,
    UserPasswordChangeDoneView,
    UserPasswordChangeView,
    profile,
    register,
)

app_name = "accounts"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='accounts:login'), name="logout"),
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings_view, name="settings"),
    path("password/change/", UserPasswordChangeView.as_view(), name="password_change"),
    path("password/change/done/", UserPasswordChangeDoneView.as_view(), name="password_change_done"),
    path("verify/",views.verify_otp,name="verify_otp"),
]

urlpatterns += [

    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/password_change.html"
        ),
        name="password_change",
    ),

    path(
        "password-change-done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html"
        ),
        name="password_change_done",
    ),
]