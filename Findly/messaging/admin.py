from django.contrib import admin

from .models import Message, Thread


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("id", "item", "created_at", "updated_at")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "thread", "sender", "created_at")
    search_fields = ("body", "sender__email")

