from django.urls import path

from . import views

app_name = "messaging"

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("thread/<int:pk>/", views.thread_detail, name="thread"),
    path("start/<int:item_pk>/", views.start_thread, name="start"),
    path("msg/<int:message_id>/edit/", views.edit_message, name="edit"),
    path("msg/<int:message_id>/delete/", views.delete_message, name="delete"),
    path("block/<int:user_id>/", views.block_user, name="block"),
    path("report/<int:user_id>/", views.report_user, name="report"),
]
