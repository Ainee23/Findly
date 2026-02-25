from django.urls import path
from .views import usersignupView, userloginView, userlogoutView, dashboardView, homeView

urlpatterns = [
    path('signup/', usersignupView, name='signup'),
    path('login/', userloginView, name='login'),
    path('logout/', userlogoutView, name='logout'),
    path('dashboard/', dashboardView, name='dashboard'),  # only one dashboard path
    path('', homeView, name='home'),  # home page
]