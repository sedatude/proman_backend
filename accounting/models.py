from django.db import models

from common.models import Money
from project.models import Project


from django.db import models

class Transaction(models.Model):
    # True if the transaction is an income, False if it's an expense
    is_income = models.BooleanField(verbose_name="Is Income?", default=False)#income or expense
    # Associated project
    project = models.ForeignKey(
        Project, related_name='transactions', on_delete=models.CASCADE
    )
    # Amount of the transaction
    amount = models.BigIntegerField(verbose_name="Amount")
    # Currency used in the transaction
    currency = models.ForeignKey(
        Money, related_name='transactions', on_delete=models.PROTECT, verbose_name="Currency"
    )
    # Date of the transaction
    date = models.DateField(verbose_name="Date")
    # USD equivalent value
    usd_equivalent = models.BigIntegerField(
        verbose_name="USD Equivalent", default=0
    )
    # Additional notes
    note = models.TextField(verbose_name="Note", blank=True)

    def __str__(self):
        transaction_type = "Income" if self.is_income else "Expense"
        return f"{self.project.name} - {transaction_type} - {self.amount} {self.currency.short}"


    class Meta:
        db_table = 'transaction'  

    def __str__(self):
        return f"{self.project.name} - {self.get_type_display()} - {self.amount} {self.currency.short}"



class TransactionHistory(models.Model):
    # Reference to the original transaction
    transaction = models.ForeignKey(
        Transaction, related_name='transaction_histories', on_delete=models.CASCADE
    )
    # Partial amount of the transaction (e.g., partial payment or income)
    partial_amount = models.BigIntegerField(verbose_name="Partial Amount")
    # Remaining balance after this transaction
    remaining_balance = models.BigIntegerField(verbose_name="Remaining Balance")
    # Date of the transaction history entry
    transaction_date = models.DateField(verbose_name="Transaction Date")
    # Notes for this history entry
    note = models.TextField(verbose_name="Note", blank=True)

    class Meta:
        db_table = 'transaction_history'  

    def save(self, *args, **kwargs):
        """Automatically calculate the remaining balance."""
        if not self.id:  # Only calculate on creation
            total_processed = sum(
                history.partial_amount for history in self.transaction.transaction_histories.all()
            )
            self.remaining_balance = self.transaction.amount - total_processed - self.partial_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction} - Partial: {self.partial_amount}"


