from django.urls import path
from dashboard import views


urlpatterns = [
    path("", views.index),
    path("count", views.count),
    path("load/<str:data_section>", views.load),
    path("json/<str:data_section>", views.get_data)
]
