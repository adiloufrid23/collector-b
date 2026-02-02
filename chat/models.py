from django.db import models
from django.contrib.auth.models import User
from marketplace.models import Item


class Conversation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="conversations")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer_conversations")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller_conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("item", "buyer", "seller")

    def __str__(self):
        return f"Conv(item={self.item_id}, buyer={self.buyer_id}, seller={self.seller_id})"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    is_flagged = models.BooleanField(default=False)  # modération
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Msg#{self.id} by {self.sender.username}"
