from django.contrib import admin
from .models import Item, Category, ItemVerification, ClaimRequest, ItemMatch
from notifications.models import Notification
from django.conf import settings
import imagehash
from PIL import Image


# ================= CATEGORY =================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


# ================= ITEM =================

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    list_display = (
        "id", "title", "status", "category", "city", "owner", "created_at",
    )

    list_filter = ("status", "category", "city", "created_at")

    search_fields = (
        "title",
        "description",
        "location",
        "city",
        "owner__email",  # ✅ custom User has email not username
    )

    def save_model(self, request, obj, form, change):
        old = None
        if obj.pk:
            old = Item.objects.get(pk=obj.pk)

        super().save_model(request, obj, form, change)

        if old and old.status == "pending" and obj.status != "pending":
            Notification.objects.create(
                user=obj.owner,
                verb=f"Your item '{obj.title}' was approved",  # ✅ verb= not text=
            )


# ================= VERIFICATION =================

class ItemVerificationAdmin(admin.ModelAdmin):

    list_display = (
        "item", "owner", "approved", "finder_confirmed", "ai_match_score", "created_at",
    )

    def save_model(self, request, obj, form, change):
        score = 0
        try:
            if obj.image1 and obj.item.image:
                img1 = Image.open(obj.image1.path)
                img2 = Image.open(obj.item.image.path)
                h1 = imagehash.average_hash(img1)
                h2 = imagehash.average_hash(img2)
                diff = h1 - h2
                score = max(0, 100 - diff * 5)
        except Exception:
            score = 50

        obj.ai_match_score = score
        super().save_model(request, obj, form, change)


admin.site.register(ItemVerification, ItemVerificationAdmin)


# ================= CLAIM =================

@admin.register(ClaimRequest)
class ClaimRequestAdmin(admin.ModelAdmin):
    list_display = ("item", "sender", "approved", "rejected", "created_at")


# ================= MATCH =================

@admin.register(ItemMatch)
class ItemMatchAdmin(admin.ModelAdmin):
    list_display = ("item1", "item2", "score", "created_at")