from django.db import models
from employees.models import Employee


class PayslipStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    PROCESSED = 'PROCESSED', 'Processed'
    PAID = 'PAID', 'Paid'


class SalaryStructure(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='salary_structure')
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    hra = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="House Rent Allowance")
    conveyance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    medical_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    special_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    pf_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="Provident Fund Deduction")
    tax_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="TDS / Income Tax")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def gross_salary(self):
        return self.basic_salary + self.hra + self.conveyance + self.medical_allowance + self.special_allowance

    @property
    def net_salary(self):
        return self.gross_salary - (self.pf_deduction + self.tax_deduction)

    def __str__(self):
        return f"Salary Structure of {self.employee.full_name}"


class Payslip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payslips')
    pay_period_month = models.IntegerField(help_text="Month 1 to 12")
    pay_period_year = models.IntegerField(help_text="Year e.g. 2026")
    basic = models.DecimalField(max_digits=12, decimal_places=2)
    allowances = models.DecimalField(max_digits=12, decimal_places=2)
    deductions = models.DecimalField(max_digits=12, decimal_places=2)
    overtime_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=PayslipStatus.choices, default=PayslipStatus.DRAFT)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pay_period_year', '-pay_period_month']
        unique_together = ('employee', 'pay_period_month', 'pay_period_year')

    def __str__(self):
        return f"Payslip {self.pay_period_month}/{self.pay_period_year} for {self.employee.full_name}"
