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
