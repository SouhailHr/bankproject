import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BankAccount(models.Model):
    ACCOUNT_TYPES = (
        ('savings', 'Savings'),
        ('checking', 'Checking'),
        # Add more account types as needed
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.FloatField(default=0)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)

    def __str__(self):
        return f"Bank Account {self.uid} ({self.user.username})"

