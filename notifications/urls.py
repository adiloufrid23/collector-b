from django.urls import path
from . import views

urlpatterns = [
    path("", views.notifications_list, name="notifications_list"),
    path("preferences/", views.notification_preferences, name="notification_preferences"),
    path("read/<int:notif_id>/", views.notification_mark_read, name="notification_mark_read"),
]
