from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models import F, Q
from django.utils import timezone


class User(AbstractBaseUser):
    telegram_id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "telegram_id"


    def get_full_name(self) -> str:
        return f"{self.first_name}' '{self.last_name}"

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