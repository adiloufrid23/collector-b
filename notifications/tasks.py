from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Notification, NotificationPreference


@shared_task
def push_notification(user_id: int, title: str, message: str):
    Notification.objects.create(user_id=user_id, title=title, message=message)

    pref, _ = NotificationPreference.objects.get_or_create(user_id=user_id)
    if pref.email_enabled:
        # si tu as un email réel, sinon console backend
        send_mail(
            subject=title,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[f"{user_id}@example.local"],  # pour V1 dev
            fail_silently=True,
        )


@shared_task
def notify_order_created(order_id: int, buyer_username: str, item_title: str):
    # simple log / notif admin ou buyer
    # tu peux l’améliorer ensuite
    return True

@shared_task
def fraud_hook(event_type: str, payload: dict):
    # Ici tu brancheras un outil externe (API interne ou SaaS)
    # Pour V1 : log console
    print("[FRAUD_HOOK]", event_type, payload)
    return True