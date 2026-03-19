from django.conf import settings
from django.db import models


class Thread(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="threads")
    item = models.ForeignKey(
        "items.Item", on_delete=models.SET_NULL, null=True, blank=True, related_name="threads"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Thread {self.pk}"


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    body = models.TextField()
    is_edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Msg {self.pk} in Thread {self.thread_id}"

