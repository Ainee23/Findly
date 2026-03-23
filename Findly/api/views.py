from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from items.models import Item
from messaging.models import Message

User = get_user_model()

try:
    from notifications.models import Notification
except ImportError:
    Notification = None

try:
    from reviews.models import Review
except ImportError:
    Review = None

from . import serializers

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('-created_at')
    serializer_class = serializers.ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-created_at')
    serializer_class = serializers.MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(sender=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

if Notification:
    class NotificationViewSet(viewsets.ModelViewSet):
        queryset = Notification.objects.all().order_by('-created_at')
        serializer_class = serializers.NotificationSerializer
        permission_classes = [permissions.IsAuthenticated]
        
        def get_queryset(self):
            return self.queryset.filter(user=self.request.user)

if Review:
    class ReviewViewSet(viewsets.ModelViewSet):
        queryset = Review.objects.all().order_by('-created_at')
        serializer_class = serializers.ReviewSerializer
        permission_classes = [permissions.IsAuthenticatedOrReadOnly]
