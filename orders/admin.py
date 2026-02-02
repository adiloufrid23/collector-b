from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", "item", "status", "total_cents", "created_at")
    list_filter = ("status",)
    search_fields = ("buyer__username", "item__title")
