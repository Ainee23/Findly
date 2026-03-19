from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Notification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    verb = models.CharField(
        max_length=255
    )

    link = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.verb