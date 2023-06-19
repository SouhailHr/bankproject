from django import forms
from BankAccount.models import BankAccount


class DepositForm(forms.Form):
    bank_account = forms.ModelChoiceField(queryset=BankAccount.objects.none())
    amount = forms.FloatField()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['bank_account'].queryset = BankAccount.objects.filter(user=user)



