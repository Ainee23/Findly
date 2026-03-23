from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'items', views.ItemViewSet)
router.register(r'messages', views.MessageViewSet)

if getattr(views, 'NotificationViewSet', None):
    router.register(r'notifications', views.NotificationViewSet)

if getattr(views, 'ReviewViewSet', None):
    router.register(r'reviews', views.ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
