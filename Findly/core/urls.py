from django.urls import path
from . import views

urlpatterns = [
    path("", views.homeView, name="home"),
    path("dashboard/", views.dashboardView, name="dashboard"),
    path("owner/dashboard/", views.owner_dashboard, name="admin_dashboard"),
    path("user/dashboard/", views.user_dashboard, name="user_dashboard"),
    path("owner/create-place/", views.createPlace, name="create_place"),
    path("signup/", views.usersignupView, name="signup"),
    path("login/", views.userloginView, name="login"),
    path("logout/", views.userlogoutView, name="logout"),
]