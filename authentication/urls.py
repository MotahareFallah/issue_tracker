from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OtpRequestViewSet, SectionViewSet

router = DefaultRouter()
router.register(r"sections", SectionViewSet, basename="section")
router.register(r"otp-request", OtpRequestViewSet, basename="otp_request")

urlpatterns = router.urls
