from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models import F, Q


class User(AbstractBaseUser):
    telegram_id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "telegram_id"

    def __str__(self):
        return str(self.telegram_id)


class Referral(models.Model):
    referrer = models.ForeignKey(
        User,
        related_name="referrals_made",
        on_delete=models.CASCADE,
    )
    referred = models.OneToOneField(
        User,
        related_name="referral_received",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~Q(referrer=F("referred")),
                name="referrer_not_equal_referred",
            )
        ]