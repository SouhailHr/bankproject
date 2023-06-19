from datetime import datetime

from django import forms
from BankAccount.models import BankAccount
from .models import Transaction
from django.utils import timezone


class SendFundsOutForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(SendFundsOutForm, self).__init__(*args, **kwargs)
        self.fields['sender'].queryset = BankAccount.objects.filter(user=self.user)
        self.fields['receiver'].queryset = BankAccount.objects.exclude(user=self.user)

    sender = forms.ModelChoiceField(queryset=BankAccount.objects.none())
    receiver = forms.ModelChoiceField(queryset=BankAccount.objects.none())
    amount = forms.FloatField()
    date = forms.DateTimeField(required=True, initial=timezone.now())

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        sender_account = cleaned_data.get('sender')
        date = cleaned_data.get('date')

        if sender_account.balance < amount:
            raise forms.ValidationError("Insufficient balance.")

        return cleaned_data

    def save_transaction(self):
        sender_account = self.cleaned_data['sender']
        receiver_account = self.cleaned_data['receiver']
        amount = self.cleaned_data['amount']
        date = self.cleaned_data['date']
        transaction = Transaction(sender=sender_account, receiver=receiver_account, amount=amount, status='pending',
                                  date=date)
        transaction.save()
        return transaction


# Send money within your bank accounts

class SendFundsWithinForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(SendFundsWithinForm, self).__init__(*args, **kwargs)
        self.fields['sender'].queryset = BankAccount.objects.filter(user=self.user)
        self.fields['receiver'].queryset = BankAccount.objects.filter(user=self.user)

    sender = forms.ModelChoiceField(queryset=BankAccount.objects.none())
    receiver = forms.ModelChoiceField(queryset=BankAccount.objects.none())
    amount = forms.FloatField()
    date = forms.DateTimeField(required=True, initial=timezone.now())

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        sender_account = cleaned_data.get('sender')
        receiver_account = cleaned_data.get('receiver')
        date = cleaned_data.get('date')

        if sender_account.balance < amount:
            raise forms.ValidationError("Insufficient balance.")

        if sender_account == receiver_account:
            raise forms.ValidationError("Sender and receiver accounts cannot be the same.")

        return cleaned_data

    def save_transaction(self):
        sender_account = self.cleaned_data['sender']
        receiver_account = self.cleaned_data['receiver']
        amount = self.cleaned_data['amount']
        date = self.cleaned_data['date']
        if date <= timezone.now():
            transaction = Transaction(sender=sender_account, receiver=receiver_account, amount=amount,
                                      status='completed',
                                      date=date)
        else:
            transaction = Transaction(sender=sender_account, receiver=receiver_account, amount=amount, status='pending',
                                      date=date)
        transaction.save()
        return transaction
