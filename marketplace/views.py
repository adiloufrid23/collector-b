# marketplace/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q

from .models import Item, ItemImage
from .forms import ItemCreateForm


def catalog(request):
    items = (
        Item.objects.filter(status=Item.Status.APPROVED, is_sold=False)
        .order_by("-created_at")
    )
    return render(request, "marketplace/item_list.html", {"items": items})


def item_partial(request):
    q = request.GET.get("q", "").strip()
    items = Item.objects.filter(status=Item.Status.APPROVED, is_sold=False)

    if q:
        items = items.filter(Q(title__icontains=q) | Q(description__icontains=q))

    items = items.order_by("-created_at")
    return render(request, "marketplace/_items_list.html", {"items": items})


@login_required
def item_create(request):
    if request.method == "POST":
        form = ItemCreateForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(seller=request.user)

            # ✅ MULTI FILES: récupère tous les fichiers uploadés "images"
            files = request.FILES.getlist("images")

            if not files:
                # sécurité : on revient avec erreur
                form.add_error(None, "Veuillez ajouter au moins une image.")
                return render(request, "marketplace/item_create.html", {"form": form})

            for f in files:
                ItemImage.objects.create(item=item, image=f)

            return redirect("catalog")
    else:
        form = ItemCreateForm()

    return render(request, "marketplace/item_create.html", {"form": form})
