from rest_framework import serializers

class UpsertUserIn(serializers.Serializer):
    telegram_id = serializers.IntegerField()

class ReferralCreateIn(serializers.Serializer):
    referrer_telegram_id = serializers.IntegerField()
    referred_telegram_id = serializers.IntegerField()

class StatusOut(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    referrer_telegram_id = serializers.IntegerField(allow_null=True)
    created_at = serializers.CharField()

class RefSummaryOut(serializers.Serializer):
    count = serializers.IntegerField()
    last_5_referrals = serializers.ListField(child=serializers.DictField())