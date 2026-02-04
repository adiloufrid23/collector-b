from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Item
from notifications.tasks import notify_new_item


@receiver(pre_save, sender=Item)
def remember_old_status(sender, instance: Item, **kwargs):
    if not instance.pk:
        instance._old_status = None
        return
    try:
        old = Item.objects.get(pk=instance.pk)
        instance._old_status = old.status
    except Item.DoesNotExist:
        instance._old_status = None


@receiver(post_save, sender=Item)
def notify_when_approved(sender, instance: Item, created, **kwargs):
    old_status = getattr(instance, "_old_status", None)

    # On déclenche quand un item passe à APPROVED
    if instance.status == "APPROVED" and old_status != "APPROVED":
        notify_new_item.delay(instance.id)
