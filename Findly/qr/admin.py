from django.contrib import admin
from django.db.models import Count
from .models import QRScan


@admin.register(QRScan)
class QRScanAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "scan_type",
        "item",
        "user",
        "ip",
        "created_at",
    )
    list_filter = ("scan_type", "created_at",)
    readonly_fields = ("created_at",)

    # 5. Admin Dashboard Analytics code snippets provided for reference
    #
    # Item vs User Scans
    # scan_summary = QRScan.objects.values("scan_type").annotate(total=Count("id"))
    #
    # Top Scanned Items
    # top_items = QRScan.objects.filter(scan_type="item").values("item__title").annotate(total=Count("id")).order_by("-total")[:10]
    #
    # Active Users
    # active_users = QRScan.objects.values("user__email").annotate(total=Count("id")).order_by("-total")[:10]