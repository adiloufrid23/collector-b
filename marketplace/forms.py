from django import forms
from .models import Item

class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["title", "description", "category", "price_cents", "shipping_cents", "photo"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full rounded-md bg-slate-900/40 text-white border border-white/10 px-3 py-2 outline-none",
                "placeholder": "Titre",
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full rounded-md bg-slate-900/40 text-white border border-white/10 px-3 py-2 outline-none",
                "rows": 6,
                "placeholder": "Description",
            }),
            "category": forms.Select(attrs={
                "class": "w-full rounded-md bg-slate-900/40 text-white border border-white/10 px-3 py-2 outline-none",
            }),
            "price_cents": forms.NumberInput(attrs={
                "class": "w-full rounded-md bg-slate-900/40 text-white border border-white/10 px-3 py-2 outline-none",
                "placeholder": "Ex: 1299 (= 12,99€)",
                "min": 0,
            }),
            "shipping_cents": forms.NumberInput(attrs={
                "class": "w-full rounded-md bg-slate-900/40 text-white border border-white/10 px-3 py-2 outline-none",
                "placeholder": "0 si gratuit",
                "min": 0,
            }),
            "photo": forms.ClearableFileInput(attrs={
                "class": (
                    "block w-full text-sm text-white "
                    "file:mr-4 file:py-2 file:px-4 "
                    "file:rounded-lg file:border-0 "
                    "file:text-sm file:font-semibold "
                    "file:bg-white/10 file:text-white "
                    "hover:file:bg-white/20"
                ),
            }),
        }

    def save(self, seller=None, commit=True):
        obj = super().save(commit=False)
        if seller is not None:
            obj.seller = seller
        if commit:
            obj.save()
            self.save_m2m()
        return obj
