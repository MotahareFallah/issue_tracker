import datetime
import random

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, Token

from .models import OneTimeLink, OtpCode, Section, User
from .paginations import DefaultPagination
from .permissions import IsStaff
from .serializers import OneTimeLinkSerializer, OtpRequestSerializer, SectionSerializer


class SectionViewSet(ModelViewSet):
    pagination_class = DefaultPagination
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsStaff]


class OtpRequestViewSet(ModelViewSet):
    queryset = OtpCode.objects.all()
    serializer_class = OtpRequestSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        phone = request.data.get("phone")

        if not phone:
            return Response(
                {"error": "Phone number is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user, created = User.objects.get_or_create(phone=phone)

        OtpCode.objects.filter(user=user, expires_at__lt=timezone.now()).delete()

        existing_otp = OtpCode.objects.filter(user=user, expires_at__gt=timezone.now())
        if existing_otp:
            return Response(
                "An OTP code has already been generated.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp_code, otp_created = OtpCode.objects.get_or_create(user=user)

        if created or otp_created:
            otp_code.max_otp_try = 4
        else:
            otp_code.max_otp_try = max(otp_code.max_otp_try - 1, 0)

            if (
                otp_code.max_otp_try == 0
                and otp_code.otp_max_out
                and timezone.now() < otp_code.otp_max_out
            ):
                return Response(
                    "Max OTP try reached, try after an hour",
                    status=status.HTTP_400_BAD_REQUEST,
                )

        otp = random.randint(100000, 999999)
        otp_expiry = timezone.now() + datetime.timedelta(minutes=5)
        otp_code.code = otp
        otp_code.expires_at = otp_expiry

        if otp_code.max_otp_try == 0:
            otp_code.otp_max_out = timezone.now() + datetime.timedelta(hours=1)
        elif otp_code.max_otp_try == -1:
            otp_code.otp_max_out = timezone.now() + datetime.timedelta(minutes=3)
        else:
            otp_code.otp_max_out = timezone.now()

        otp_code.save()

        # send_sms.delay(user.phone, otp)
        return Response("Successfully generated OTP", status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch"], url_path="otp-verify")
    def verify_otp(self, request):
        otp_entered = request.data.get("otp")
        phone = request.data.get("phone")

        if not otp_entered or not phone:
            return Response(
                {"error": "Phone number and OTP are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(phone=phone)
            otp_code = OtpCode.objects.get(user=user)

            if otp_code.max_otp_try >= 5:
                return Response(
                    {"error": "Maximum OTP attempts exceeded. Please try again later."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            if otp_code.is_valid() and otp_code.code == otp_entered:
                with transaction.atomic():
                    otp_code.max_otp_try = 0
                    otp_code.otp_max_out = timezone.now()
                    otp_code.save()

                    refresh = RefreshToken.for_user(user)
                    tokens = {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }

                    otp_code.delete()

                return Response({"tokens": tokens}, status=status.HTTP_200_OK)
            else:
                otp_code.max_otp_try += 1
                otp_code.save()

                return Response(
                    {"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
                )

        except User.DoesNotExist:
            return Response(
                {"error": "User not found with the provided phone number"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except OtpCode.DoesNotExist:
            return Response(
                {"error": "OTP code not found for the user"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        detail=False,
        methods=["patch"],
        url_path="setup-account",
        permission_classes=[IsAuthenticated],
    )
    def setup_account(self, request):
        password = request.data.get("password")
        if not password:
            return Response(
                "Missing required fields", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = request.user

            user.set_password(password)
            user.active_member = True
            user.save()
            return Response("Account setup successfully", status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
