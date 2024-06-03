from django.urls import path

from .views import robots

urlpatterns = [
    path("", robots, name="robots_txt"),
]