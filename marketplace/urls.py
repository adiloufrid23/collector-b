# marketplace/urls.py
from django.urls import path
from .views import catalog, item_partial, item_create

urlpatterns = [
    path("", catalog, name="catalog"),
    path("items/partial/", item_partial, name="item_partial"),
    path("items/create/", item_create, name="item_create"),
]
