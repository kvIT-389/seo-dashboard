from django.urls import path, include


urlpatterns = [
    path("api/", include("dashboard_api.urls"))
]
