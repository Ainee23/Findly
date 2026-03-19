from django.urls import path
from . import views

urlpatterns = [
    path("", views.homeView, name="home"),
    path("owner/create-place/", views.createPlace, name="create_place"),
    path("signup/", views.usersignupView, name="signup"),
    path("login/", views.userloginView, name="login"),
    path("logout/", views.userlogoutView, name="logout"),
]