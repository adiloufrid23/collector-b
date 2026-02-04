# orders/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("buy/<int:item_id>/", views.buy_item, name="buy_item"),
    path("checkout/<int:order_id>/", views.checkout_order, name="checkout_order"),

    # ✅ ces 2 noms doivent exister car tu fais redirect("payment_success") / redirect("payment_cancel")
    path("success/", views.payment_success, name="payment_success"),
    path("cancel/", views.payment_cancel, name="payment_cancel"),

    # optionnel (si tu veux garder une autre page)
    # path("success-page/", views.success, name="success"),
]
