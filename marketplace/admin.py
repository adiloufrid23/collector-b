# marketplace/admin.py
from django.contrib import admin
from .models import Category, Item, ItemImage, PriceHistory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "price_cents",
        "shipping_cents",
        "status",
        "is_sold",
        "seller",
        "created_at",
    )
    list_filter = ("status", "is_sold", "category", "created_at")
    search_fields = ("title", "description")
    inlines = [ItemImageInline]

    # ✅ pour pouvoir changer PENDING -> APPROVED facilement
    actions = ["make_approved", "make_rejected", "make_pending"]

    @admin.action(description="Marquer comme APPROVED")
    def make_approved(self, request, queryset):
        queryset.update(status=Item.Status.APPROVED)

    @admin.action(description="Marquer comme REJECTED")
    def make_rejected(self, request, queryset):
        queryset.update(status=Item.Status.REJECTED)

    @admin.action(description="Marquer comme PENDING")
    def make_pending(self, request, queryset):
        queryset.update(status=Item.Status.PENDING)


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "item", "old_price_cents", "new_price_cents", "changed_at")
    list_filter = ("changed_at",)
