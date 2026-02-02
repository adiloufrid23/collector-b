from django.db import models
from django.contrib.auth.models import User
from marketplace.models import Category, Item


class NotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="notif_pref")
    email_enabled = models.BooleanField(default=True)
    inapp_enabled = models.BooleanField(default=True)

    # types
    notify_new_matching_interest = models.BooleanField(default=True)
    notify_price_change = models.BooleanField(default=True)

    def __str__(self):
        return f"NotifPref({self.user.username})"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = self.category or self.item
        return f"Sub({self.user.username} -> {target})"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=120)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notif({self.user.username}): {self.title}"
