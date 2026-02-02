from django.urls import path
from .views import buy_item, checkout_order, payment_success, payment_cancel

urlpatterns = [
    path("buy/<int:item_id>/", buy_item, name="buy_item"),
    path("checkout/<int:order_id>/", checkout_order, name="checkout_order"),
    path("success/", payment_success, name="payment_success"),
    path("cancel/", payment_cancel, name="payment_cancel"),
]
