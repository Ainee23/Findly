from django.urls import path

from . import views

app_name = "items"

urlpatterns = [
    path("", views.item_list, name="list"),
    path("new/", views.item_create, name="create"),
    path("mine/", views.my_items, name="mine"),
    path("<int:pk>/", views.item_detail, name="detail"),
    path("update-location/<int:pk>/",views.update_location,name="update_location",),
    path("status/<int:pk>/<str:status>/",views.change_status,name="change_status",),
    path("map/", views.map_view, name="map"),
    path("map/data/", views.map_items_json, name="map_data"),
    path("dashboard/",views.dashboard,name="dashboard",),
    path("<int:pk>/verify/", views.verify_item, name="verify_item"),
    path("<int:pk>/confirm-owner/", views.confirm_owner, name="confirm_owner"),
    path("<int:pk>/send-claim/", views.send_claim, name="send_claim"),
    path("<int:pk>/accept-claim/", views.accept_claim, name="accept_claim"),
    path("<int:pk>/reject-claim/", views.reject_claim, name="reject_claim"),
    path("<int:pk>/request-proof/", views.request_claim_proof, name="request_claim_proof"),
    path("<int:pk>/location/", views.update_claim_location, name="update_claim_location"),
    path("<int:pk>/confirm-pickup/", views.confirm_pickup, name="confirm_pickup"),
    path("claim/<int:pk>/edit/", views.edit_claim, name="edit_claim"),
]

