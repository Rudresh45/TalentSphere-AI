"""
TalentSphere Quotation Business Logic Services
"""
from decimal import Decimal
from django.db import transaction
from quotations.models import Quotation, QuotationItem, Customer, QuotationStatus
from products.models import Product
from employees.models import Employee


def calculate_quotation_totals(quotation: Quotation) -> Quotation:
    """
    Recalculates subtotal, discount, tax, and grand total for a quotation.
    """
    items = quotation.items.all()
    subtotal = Decimal('0.00')
    tax_total = Decimal('0.00')

    for item in items:
        # Calculate line price with item discount
        base_price = item.unit_price * item.quantity
        item_discount = base_price * (item.discount_percentage / Decimal('100.00'))
        line_total = base_price - item_discount
        item.line_total = line_total
        item.save()

        subtotal += line_total
        # Product tax
        if item.product.tax_rate > Decimal('0.00'):
            tax_total += line_total * (item.product.tax_rate / Decimal('100.00'))

    # Overall Quotation Discount
    quotation_discount = subtotal * (quotation.discount_percentage / Decimal('100.00'))
    taxable_subtotal = subtotal - quotation_discount

    grand_total = taxable_subtotal + tax_total

    quotation.subtotal = round(subtotal, 2)
    quotation.discount_amount = round(quotation_discount, 2)
    quotation.tax_amount = round(tax_total, 2)
    quotation.grand_total = round(grand_total, 2)
    quotation.save()

    return quotation
