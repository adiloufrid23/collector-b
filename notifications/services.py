# notifications/services.py
from django.contrib.auth import get_user_model
from .models import Notification, NotificationPreference

User = get_user_model()


def get_or_create_pref(user):
    pref, _ = NotificationPreference.objects.get_or_create(user=user)
    return pref


def create_in_app_notification(*, user, notif_type, title, message="", item=None):
    """
    Crée une notif en DB si le user a activé in_app_enabled.
    """
    pref = get_or_create_pref(user)
    if not pref.in_app_enabled:
        return None

    return Notification.objects.create(
        user=user,
        notif_type=notif_type,
        title=title,
        message=message,
        item=item,
    )
