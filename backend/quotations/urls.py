from django.urls import path, include
from rest_framework.routers import DefaultRouter
from quotations.views import CustomerViewSet, QuotationViewSet, QuotationItemViewSet

app_name = 'quotations'

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'items', QuotationItemViewSet, basename='quotation_item')
router.register(r'', QuotationViewSet, basename='quotation')

urlpatterns = [
    path('', include(router.urls)),
]
