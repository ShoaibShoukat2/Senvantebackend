from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health, name="health"),
    path("inquiries/", views.create_inquiry, name="create-inquiry"),
]
