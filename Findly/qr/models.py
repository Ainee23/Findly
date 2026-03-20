from django.db import models
from django.conf import settings
from items.models import Item


class QRScan(models.Model):

    SCAN_TYPES = (
        ('user', 'User QR Scan'),
        ('item', 'Item QR Scan'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="qr_scans"
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="qr_scans"
    )

    scan_type = models.CharField(
        max_length=10, 
        choices=SCAN_TYPES,
        default='item'
    )

    ip = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.scan_type} scan for {self.user} at {self.created_at}"