from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from quotations.models import Customer, Quotation, QuotationItem
from quotations.serializers import CustomerSerializer, QuotationSerializer, QuotationItemSerializer
from quotations.services import calculate_quotation_totals


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]


class QuotationViewSet(viewsets.ModelViewSet):
    queryset = Quotation.objects.select_related('customer', 'created_by').prefetch_related('items__product').all()
    serializer_class = QuotationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def calculate(self, request, pk=None):
        """
        POST /api/v1/quotations/{id}/calculate/
        Recalculates subtotal, discount, tax, and grand totals.
        """
        quotation = self.get_object()
        updated_quote = calculate_quotation_totals(quotation)
        return Response(
            {
                "success": True,
                "message": "Quotation totals calculated successfully.",
                "data": QuotationSerializer(updated_quote).data
            },
            status=status.HTTP_200_OK
        )


class QuotationItemViewSet(viewsets.ModelViewSet):
    queryset = QuotationItem.objects.select_related('quotation', 'product').all()
    serializer_class = QuotationItemSerializer
    permission_classes = [IsAuthenticated]
