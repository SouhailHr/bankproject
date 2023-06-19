from django.shortcuts import render, redirect
from django.utils import timezone

from BankAccount.models import BankAccount
from .forms import DepositForm

# Create your views here.
from os import path
from pathlib import Path

from .models import Deposit

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent

USER_TEMPLATES_DIR = path.join(ROOT_DIR, 'templates/deposit/')


def deposit_funds(request):
    user = request.user

    if request.method == 'POST':
        form = DepositForm(request.POST, user=user)
        if form.is_valid():
            bank_account = form.cleaned_data['bank_account']
            amount = form.cleaned_data['amount']
            bank_account.balance += amount
            bank_account.save()
            deposit = Deposit(account=bank_account, amount=amount, date=timezone.now())
            deposit.save()

            return redirect('bank_account_details')
    else:
        form = DepositForm(user=user)

    context = {
        'form': form
    }

    return render(request, path.join(USER_TEMPLATES_DIR, 'deposit_funds.html'), context)


def deposit_history(request):
    user = request.user
    bank_accounts = BankAccount.objects.filter(user=user)
    deposits = Deposit.objects.filter(account__in=bank_accounts)

    context = {
        'deposits': deposits
    }

    return deposits
