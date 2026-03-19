from django.conf import settings
from django.db import models
from django.utils import timezone
from PIL import Image

# ✅ CATEGORY MODEL

class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        LOST = "lost", "Lost"
        FOUND = "found", "Found"
        CLOSED = "closed", "Closed"


    title = models.CharField(max_length=140)

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    location = models.CharField(
        max_length=200,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    date_happened = models.DateField(
        null=True,
        blank=True
    )

    image = models.ImageField(
        upload_to="items/",
        blank=True,
        null=True
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="items"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    latitude = models.FloatField(
        blank=True,
        null=True
    )

    longitude = models.FloatField(
        blank=True,
        null=True
    )

    location_updated_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            max_size = (800, 800)
            img.thumbnail(max_size)
            img.save(self.image.path)

        # ✅ AUTO MATCH
        try:
            from .models import ItemMatch
            import imagehash

            if not self.image:
                return

            img1 = Image.open(self.image.path)
            h1 = imagehash.average_hash(img1)

            others = Item.objects.exclude(id=self.id)

            for o in others:
                if not o.image:
                    continue

                img2 = Image.open(o.image.path)
                h2 = imagehash.average_hash(img2)

                diff = h1 - h2
                score = max(0, 100 - diff * 5)

                if score > 60:
                    ItemMatch.objects.get_or_create(
                        item1=self,
                        item2=o,
                        defaults={"score": score}
                    )

        except Exception:
            pass


class ItemVerification(models.Model):

    item = models.ForeignKey(
        "Item",
        on_delete=models.CASCADE,
        related_name="verifications"
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    description = models.TextField()

    receipt = models.ImageField(
        upload_to="verification/receipts/",
        blank=True,
        null=True
    )

    image1 = models.ImageField(
        upload_to="verification/images/",
        blank=True,
        null=True
    )

    image2 = models.ImageField(
        upload_to="verification/images/",
        blank=True,
        null=True
    )

    image3 = models.ImageField(
        upload_to="verification/images/",
        blank=True,
        null=True
    )

    ai_match_score = models.FloatField(
        default=0
    )

    approved = models.BooleanField(
        default=False
    )

    # ✅ NEW FIELD
    finder_confirmed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Verification for {self.item.title}"
    
class ClaimRequest(models.Model):

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="claims"
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_claims"
    )

    message = models.TextField(
        blank=True
    )

    proof_image = models.ImageField(
        upload_to="claims/proofs/",
        blank=True,
        null=True
    )

    proof_document = models.FileField(
        upload_to="claims/proofs/",
        blank=True,
        null=True
    )

    # Owner may ask for additional proof before approving
    proof_requested = models.BooleanField(
        default=False
    )

    owner_response = models.TextField(
        blank=True,
        help_text="Owner can leave a note for the finder (e.g., request additional proof)."
    )

    finder_lat = models.FloatField(
        blank=True,
        null=True,
        help_text="Last known latitude for the finder (shared after approval)."
    )

    finder_lng = models.FloatField(
        blank=True,
        null=True,
        help_text="Last known longitude for the finder (shared after approval)."
    )

    finder_location_updated_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    pickup_confirmed = models.BooleanField(
        default=False,
        help_text="True when finder confirms they have picked up the item."
    )

    pickup_confirmed_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    approved = models.BooleanField(
        default=False
    )

    rejected = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Claim request for {self.item.title}"
    
class ItemMatch(models.Model):

    item1 = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="matches1"
    )

    item2 = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="matches2"
    )

    score = models.FloatField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.item1} <-> {self.item2}"