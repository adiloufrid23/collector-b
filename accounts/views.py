from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from marketplace.models import Category
from orders.models import Order
from marketplace.models import Item


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def dashboard(request):
    user = request.user

    my_sales = Item.objects.filter(seller=user).order_by("-created_at")
    my_orders = Order.objects.filter(buyer=user).order_by("-created_at")

    return render(request, "accounts/dashboard.html", {
        "my_sales": my_sales,
        "my_orders": my_orders,
    })


@login_required
def interests(request):
    categories = Category.objects.all().order_by("name")
    profile = request.user.profile

    if request.method == "POST":
        ids = request.POST.getlist("categories")
        profile.interests.set(Category.objects.filter(id__in=ids))
        return redirect("dashboard")

    return render(request, "accounts/interests.html", {
        "categories": categories,
        "selected": set(profile.interests.values_list("id", flat=True)),
    })
