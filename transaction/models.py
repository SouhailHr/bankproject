from django.db import models
from BankAccount.models import BankAccount


# Create your models here.


class Transaction(models.Model):
    TRANSACTION_STATUS = (
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
    )

    sender = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='sender_transactions')
    receiver = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='receiver_transactions')
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=TRANSACTION_STATUS)
    date = models.DateTimeField(null=False)

    def __str__(self):
        return f"Transaction {self.pk}"
