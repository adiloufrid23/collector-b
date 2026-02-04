# notifications/models.py
from django.conf import settings
from django.db import models
from marketplace.models import Item


class NotificationPreference(models.Model):
    """
    Préférences par utilisateur :
    - recevoir des notifications en app
    - recevoir des emails (optionnel)
    - only_interests : si True, on notifie NEW_ITEM seulement si l’item est dans ses centres d’intérêt
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_pref"
    )

    in_app_enabled = models.BooleanField(default=True)
    email_enabled = models.BooleanField(default=False)
    only_interests = models.BooleanField(default=False)  # mets False par défaut si tu veux pas filtrer

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"NotificationPreference({self.user.username})"


class Notification(models.Model):
    class Type(models.TextChoices):
        NEW_ITEM = "NEW_ITEM", "Nouvel article"
        ORDER = "ORDER", "Commande"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    notif_type = models.CharField(
        max_length=30,
        choices=Type.choices,
        default=Type.NEW_ITEM
    )

    title = models.CharField(max_length=200)
    message = models.TextField(blank=True)

    # Lier une annonce (important pour "Voir l'annonce")
    item = models.ForeignKey(Item, null=True, blank=True, on_delete=models.SET_NULL)

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notif({self.user.username} - {self.title})"
