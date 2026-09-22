from django.urls import path, include
from rest_framework.routers import DefaultRouter
from offboarding.views import OffboardingViewSet

app_name = 'offboarding'

router = DefaultRouter()
router.register(r'', OffboardingViewSet, basename='offboarding')

urlpatterns = [
    path('', include(router.urls)),
]
