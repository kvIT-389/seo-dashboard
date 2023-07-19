from django.urls import path

from dashboard_api import views


urlpatterns = [
    path("count", views.count),
    path("load/<str:data_section>", views.load_data),
    path("get/<str:data_section>", views.get_data)
]
