from django.contrib import admin
from .models import QRScan


@admin.register(QRScan)
class QRScanAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "item",
        "user",
        "ip",
        "created_at",
    )