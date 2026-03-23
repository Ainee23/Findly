from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ActivityLog(models.Model):
    ACTION_CHOICES = (
        ('item_added', 'Item Added'),
        ('item_claimed', 'Item Claimed'),
        ('message_sent', 'Message Sent'),
        ('review_added', 'Review Added'),
        ('status_changed', 'Status Changed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.get_action_display()}"
