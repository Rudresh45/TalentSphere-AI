from django.urls import path, include
from rest_framework.routers import DefaultRouter
from departments.views import DepartmentViewSet, DesignationViewSet

app_name = 'departments'

router = DefaultRouter()
router.register(r'designations', DesignationViewSet, basename='designation')
router.register(r'', DepartmentViewSet, basename='department')

urlpatterns = [
    path('', include(router.urls)),
]
