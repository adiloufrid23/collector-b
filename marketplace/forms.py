# marketplace/forms.py
from django import forms
from .models import Item


class ItemCreateForm(forms.ModelForm):
    # ✅ champ "virtuel" (pas dans le modèle Item)
    # on ne met PAS ClearableFileInput(multiple=True) pour éviter ton erreur
    images = forms.ImageField(required=True)

    class Meta:
        model = Item
        fields = ["title", "description", "category", "price_cents", "shipping_cents"]

    def save(self, seller, commit=True):
        item = super().save(commit=False)
        item.seller = seller
        item.status = Item.Status.PENDING
        if commit:
            item.save()
        return item
