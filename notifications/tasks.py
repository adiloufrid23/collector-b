# notifications/tasks.py
from celery import shared_task
from django.contrib.auth import get_user_model
from django.db.models import Q

from marketplace.models import Item
from orders.models import Order
from .models import Notification, NotificationPreference

User = get_user_model()


def _user_interests_categories(user):
    """
    On essaye de récupérer une relation d'intérêts si tu en as une.
    - Si tu as un Profile avec interests = ManyToMany(Category)
    - ou directement user.interests
    Sinon => None
    """
    if hasattr(user, "profile") and hasattr(user.profile, "interests"):
        return user.profile.interests.all()
    if hasattr(user, "interests"):
        return user.interests.all()
    return None


@shared_task
def notify_new_item(item_id: int):
    """
    Notifie les utilisateurs qu'un nouvel item est en vente.
    """
    try:
        item = Item.objects.select_related("seller", "category").get(id=item_id)
    except Item.DoesNotExist:
        return

    # On notifie seulement si l'item est réellement "en vente"
    if item.is_sold:
        return

    # Option: tu peux limiter à APPROVED si tu veux
    # if item.status != Item.Status.APPROVED:
    #     return

    users = User.objects.exclude(id=item.seller_id)

    for u in users:
        pref, _ = NotificationPreference.objects.get_or_create(user=u)
        if not pref.in_app_enabled:
            continue

        if pref.only_interests:
            interests = _user_interests_categories(u)
            # Si pas d'intérêts configurés => on skip (ou tu peux décider de notifier quand même)
            if interests is not None and item.category not in list(interests):
                continue
            if interests is None:
                # pas de système d'intérêts => on notifie quand même (sinon tu ne verras jamais rien)
                pass

        Notification.objects.create(
            user=u,
            notif_type=Notification.Type.NEW_ITEM,
            title=f"Nouveau : {item.title}",
            message=f"{item.seller.username} a mis en vente « {item.title} ».",
            item=item,
        )


@shared_task
def notify_order_created(order_id: int):
    """
    Notifie le vendeur (et optionnellement l'acheteur) lors d'un achat.
    """
    try:
        order = (
            Order.objects
            .select_related("buyer", "item", "item__seller")
            .get(id=order_id)
        )
    except Order.DoesNotExist:
        return

    item = order.item
    seller = item.seller
    buyer = order.buyer

    # Notif vendeur
    pref_seller, _ = NotificationPreference.objects.get_or_create(user=seller)
    if pref_seller.in_app_enabled:
        Notification.objects.create(
            user=seller,
            notif_type=Notification.Type.ORDER,
            title="Ton article a été vendu ✅",
            message=f"{buyer.username} a acheté « {item.title} ».",
            item=item,
        )

    # (Optionnel) Notif acheteur
    pref_buyer, _ = NotificationPreference.objects.get_or_create(user=buyer)
    if pref_buyer.in_app_enabled:
        Notification.objects.create(
            user=buyer,
            notif_type=Notification.Type.ORDER,
            title="Achat confirmé ✅",
            message=f"Tu as acheté « {item.title} » à {seller.username}.",
            item=item,
        )
