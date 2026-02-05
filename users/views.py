from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from users.serializer import UpsertUserIn, ReferralCreateIn, StatusOut, RefSummaryOut
from users import services

class UsersUpsert(APIView):
    def post(self, request):
        ser = UpsertUserIn(data=request.data)
        ser.is_valid(raise_exception=True)
        user = services.upsert_user(ser.validated_data["telegram_id"])
        return Response({"telegram_id": user.telegram_id, "created_at": user.created_at.isoformat()})

class ReferralsCreate(APIView):
    def post(self, request):
        ser = ReferralCreateIn(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            ref = services.create_referral(**ser.validated_data)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "referrer_telegram_id": ref.referrer.telegram_id,
            "referred_telegram_id": ref.referred.telegram_id,
            "created_at": ref.created_at.isoformat()
        }, status=status.HTTP_201_CREATED)

class UserStatus(APIView):
    def get(self, request, telegram_id: int):
        try:
            dto = services.get_status(telegram_id)
        except ObjectDoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        out = StatusOut(dto.__dict__)
        return Response(out.data)

class ReferrerSummary(APIView):
    def get(self, request, referrer_telegram_id: int):
        try:
            data = services.get_ref_summary(referrer_telegram_id)
        except ObjectDoesNotExist:
            return Response({"detail": "Referrer not found"}, status=status.HTTP_404_NOT_FOUND)

        out = RefSummaryOut(data)
        return Response(out.data)