from django.db import models
from django.conf import settings


class QRScan(models.Model):

    item = models.ForeignKey(
        "items.Item",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    ip = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Scan {self.id}"