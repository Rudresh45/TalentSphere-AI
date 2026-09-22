from rest_framework import serializers
from payroll.models import SalaryStructure, Payslip


class SalaryStructureSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    gross_salary = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    net_salary = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = SalaryStructure
        fields = (
            'id', 'employee', 'employee_name', 'basic_salary', 'hra',
            'conveyance', 'medical_allowance', 'special_allowance',
            'pf_deduction', 'tax_deduction', 'gross_salary', 'net_salary',
            'created_at', 'updated_at'
        )


class PayslipSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_code = serializers.CharField(source='employee.employee_id', read_only=True)

    class Meta:
        model = Payslip
        fields = (
            'id', 'employee', 'employee_name', 'employee_code',
            'pay_period_month', 'pay_period_year', 'basic', 'allowances',
            'deductions', 'overtime_pay', 'tax', 'net_salary', 'status', 'generated_at'
        )
