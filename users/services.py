from dataclasses import dataclass

from asgiref.sync import sync_to_async
from django.db import transaction, IntegrityError
from .models import User, Referral

@dataclass
class StatusDTO:
    telegram_id: int
    referrer_telegram_id: int | None
    created_at: str

@transaction.atomic
def upsert_user(telegram_id: int) -> User:
    user, _ = User.objects.get_or_create(telegram_id=telegram_id)
    return user

upsert_user_async = sync_to_async(upsert_user, thread_sensitive=True)

@transaction.atomic
def create_referral(referrer_telegram_id: int, referred_telegram_id: int) -> Referral:
    if referrer_telegram_id == referred_telegram_id:
        raise ValueError("referrer و referred نمی‌توانند یکی باشند.")

    referrer = upsert_user(referrer_telegram_id)
    referred = upsert_user(referred_telegram_id)

    try:
        referral, created = Referral.objects.get_or_create(
            referred=referred,
            defaults={"referrer": referrer},
        )
    except IntegrityError:
        referral = Referral.objects.select_related("referrer", "referred").get(referred=referred)

    return referral

create_referral_async = sync_to_async(create_referral, thread_sensitive=True)

def get_status(telegram_id: int) -> StatusDTO:
    user = User.objects.get(telegram_id=telegram_id)
    ref = getattr(user, "referral_received", None)
    referrer_id = ref.referrer.telegram_id if ref else None
    return StatusDTO(
        telegram_id=user.telegram_id,
        referrer_telegram_id=referrer_id,
        created_at=user.created_at.isoformat(),
    )

get_status_async = sync_to_async(get_status, thread_sensitive=True)

def get_ref_summary(referrer_telegram_id: int) -> dict:
    referrer = User.objects.get(telegram_id=referrer_telegram_id)
    qs = referrer.referrals_made.select_related("referred").order_by("-created_at")

    last_5 = [
        {"telegram_id": r.referred.telegram_id, "created_at": r.created_at.isoformat()}
        for r in qs[:5]
    ]
    return {"count": qs.count(), "last_5_referrals": last_5}

get_ref_summary_async = sync_to_async(get_ref_summary, thread_sensitive=True)
