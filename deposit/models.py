from django.db import models

from BankAccount.models import BankAccount


class Deposit(models.Model):
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='deposits')
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deposit {self.pk}"
