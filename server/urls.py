from django.urls import path
from dashboard import views


urlpatterns = [
    path("", views.index),
    path("json/<str:data_section>", views.get_data)
]
