from django.urls import path, include
from rest_framework.routers import DefaultRouter
from performance.views import PerformanceViewSet

app_name = 'performance'

router = DefaultRouter()
router.register(r'', PerformanceViewSet, basename='performance')

urlpatterns = [
    path('', include(router.urls)),
]
