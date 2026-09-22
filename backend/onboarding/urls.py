from django.urls import path, include
from rest_framework.routers import DefaultRouter
from onboarding.views import OnboardingViewSet

app_name = 'onboarding'

router = DefaultRouter()
router.register(r'', OnboardingViewSet, basename='onboarding')

urlpatterns = [
    path('', include(router.urls)),
]
