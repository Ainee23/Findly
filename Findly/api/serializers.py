from rest_framework import serializers
from django.contrib.auth import get_user_model
from items.models import Item
from messaging.models import Message
try:
    from notifications.models import Notification
except ImportError:
    Notification = None
    
try:
    from reviews.models import Review
except ImportError:
    Review = None

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'date_joined']

class ItemSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Item
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = '__all__'

if Notification:
    class NotificationSerializer(serializers.ModelSerializer):
        class Meta:
            model = Notification
            fields = '__all__'
            
if Review:
    class ReviewSerializer(serializers.ModelSerializer):
        class Meta:
            model = Review
            fields = '__all__'
