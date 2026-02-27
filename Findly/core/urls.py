from django.urls import path
from .views import (
    usersignupView,
    userloginView,
    userlogoutView,
    user_dashboard,
    owner_dashboard,
    dashboardView,   # ✅ ADD THIS
    homeView,
)

urlpatterns = [
    path('', homeView, name='home'),

    path('signup/', usersignupView, name='signup'),
    path('login/', userloginView, name='login'),
    path('logout/', userlogoutView, name='logout'),

    # ✅ MAIN DASHBOARD (recommended)
    path('dashboard/', dashboardView, name='dashboard'),

    # Optional: separate dashboards
    path('dashboard/user/', user_dashboard, name='user_dashboard'),
    path('dashboard/owner/', owner_dashboard, name='admin_dashboard'),
]