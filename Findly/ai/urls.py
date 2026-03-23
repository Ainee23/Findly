from django.urls import path

from . import views

app_name = "ai"

urlpatterns = [
    path("health/", views.health, name="health"),
    path("match/<int:item_id>/", views.ai_match, name="ai_match"),
    path("search/", views.ai_search, name="ai_search"),
    path("suggest/", views.ai_suggest, name="ai_suggest"),
    path("generate-description/", views.ai_generate_description, name="ai_generate_description"),
]

