from django.urls import path
from .views import register, dashboard, interests

urlpatterns = [
    path("register/", register, name="register"),
    path("", dashboard, name="dashboard"),
    path("interests/", interests, name="interests"),
]
