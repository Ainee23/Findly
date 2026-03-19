from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "reviewer", "reviewee", "rating", "created_at")
    search_fields = ("reviewer__email", "reviewee__email", "comment")
    list_filter = ("rating", "created_at")

