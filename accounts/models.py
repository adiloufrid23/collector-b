from django.db import models
from django.contrib.auth.models import User
from marketplace.models import Category


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    interests = models.ManyToManyField(Category, blank=True, related_name="interested_users")

    def __str__(self):
        return f"Profile({self.user.username})"


class Rating(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_ratings")
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_ratings")
    order_id = models.PositiveIntegerField()  # simple pour V1
    score = models.PositiveSmallIntegerField()  # 1..5
    comment = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("rater", "rated_user", "order_id")

    def __str__(self):
        return f"{self.rater}->{self.rated_user}: {self.score}"
