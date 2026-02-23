from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('signup/',views.usersignupView,name='signup')
]