from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from marketplace.models import Item
from .models import Conversation, Message
from .utils import contains_personal_info


@login_required
def open_chat(request, item_id):
    item = get_object_or_404(Item, id=item_id, status="APPROVED")
    buyer = request.user
    seller = item.seller

    if buyer.id == seller.id:
        return redirect("item_list")

    conv, _ = Conversation.objects.get_or_create(item=item, buyer=buyer, seller=seller)
    return redirect("chat_room", conv_id=conv.id)


@login_required
def chat_room(request, conv_id):
    conv = get_object_or_404(Conversation, id=conv_id)

    if request.user not in [conv.buyer, conv.seller]:
        return redirect("item_list")

    if request.method == "POST":
        body = request.POST.get("body", "").strip()
        if body:
            flagged = contains_personal_info(body)
            Message.objects.create(
                conversation=conv,
                sender=request.user,
                body=body,
                is_flagged=flagged
            )
        return redirect("chat_room", conv_id=conv.id)

    msgs = conv.messages.order_by("created_at")
    return render(request, "chat/room.html", {"conv": conv, "messages": msgs})
