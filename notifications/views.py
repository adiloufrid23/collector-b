# notifications/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Notification, NotificationPreference
from .forms import NotificationPreferenceForm


@login_required
def notifications_list(request):
    notifs = Notification.objects.filter(user=request.user)
    return render(request, "notifications/list.html", {"notifs": notifs})


@login_required
def notification_mark_read(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.is_read = True
    notif.save(update_fields=["is_read"])
    return redirect("notifications_list")


@login_required
def notification_preferences(request):
    pref, _ = NotificationPreference.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = NotificationPreferenceForm(request.POST, instance=pref)
        if form.is_valid():
            form.save()
            return redirect("notifications_list")
    else:
        form = NotificationPreferenceForm(instance=pref)

    return render(request, "notifications/preferences.html", {"form": form})
