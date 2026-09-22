from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sprints.views import SprintViewSet

app_name = 'sprints'

router = DefaultRouter()
router.register(r'', SprintViewSet, basename='sprint')

urlpatterns = [
    path('', include(router.urls)),
]
