# orders/views.py
import stripe
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse

from marketplace.models import Item
from .models import Order
from notifications.tasks import notify_order_created

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def buy_item(request, item_id):
    buyer = request.user
    item = get_object_or_404(Item, id=item_id, status=Item.Status.APPROVED)

    if item.seller_id == buyer.id:
        return HttpResponseForbidden("Tu ne peux pas acheter ton propre article.")
    if item.is_sold:
        return HttpResponseForbidden("Cet article est déjà vendu.")

    order = Order.objects.create(
        buyer=buyer,
        item=item,
        total_cents=item.total_cents,
        status=Order.Status.PENDING
    )

    item.is_sold = True
    item.save(update_fields=["is_sold"])

    # ✅ notif vendeur/acheteur
    notify_order_created.delay(order.id)

    # ✅ Mode démo si Stripe non configuré
    if not settings.STRIPE_SECRET_KEY:
        order.status = Order.Status.PAID
        order.save(update_fields=["status"])
        return redirect("payment_success")

    return redirect("checkout_order", order_id=order.id)


@login_required
def checkout_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)

    if not settings.STRIPE_SECRET_KEY:
        # tu as un template checkout_demo.html => on l’utilise
        return render(request, "orders/checkout_demo.html", {"order": order})

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {"name": order.item.title},
                    "unit_amount": order.total_cents,
                },
                "quantity": 1,
            }
        ],
        success_url=settings.STRIPE_SUCCESS_URL + f"?order_id={order.id}",
        cancel_url=settings.STRIPE_CANCEL_URL + f"?order_id={order.id}",
        metadata={"order_id": str(order.id)},
    )

    return redirect(session.url, code=303)


def payment_success(request):
    # ✅ tu as déjà orders_success.html
    return render(request, "orders/orders_success.html")


def payment_cancel(request):
    # ✅ tu as déjà orders_cancel.html
    return render(request, "orders/orders_cancel.html")
