from django.urls import path
from .views import UsersUpsert, ReferralsCreate, UserStatus, ReferrerSummary

urlpatterns = [
    path("users/upsert", UsersUpsert.as_view()),
    path("referrals", ReferralsCreate.as_view()),
    path("users/<int:telegram_id>/status", UserStatus.as_view()),
    path("referrals/<int:referrer_telegram_id>/summary", ReferrerSummary.as_view()),
]