from datetime import datetime

from django.shortcuts import render, redirect
from django.utils import timezone

from transaction.models import Transaction
from .models import BankAccount
from .forms import BankAccountForm
from os import path
from pathlib import Path
from deposit.forms import DepositForm

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
USER_TEMPLATES_DIR = path.join(ROOT_DIR, 'templates/bankaccount/')


def create_bank_account(request):
    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            # Create bank account with the logged-in user as the owner
            bank_account = form.save(commit=False)
            bank_account.user = request.user
            bank_account.save()

            # Redirect to bank account details page
            return redirect('bank_account_details')
    else:
        form = BankAccountForm()

    context = {
        'form': form
    }
    return render(request, path.join(USER_TEMPLATES_DIR, 'create_bank_account.html'), context)


def bank_account_details(request):
    user = request.user
    bank_accounts = BankAccount.objects.filter(user=user)

    context = {
        'bank_accounts': bank_accounts
    }

    def execute_pending_transactions():
        pending_transactions = Transaction.objects.filter(status='pending')
        # get user bankaccounts
        user_bank_accounts = BankAccount.objects.filter(user=request.user)

        for transaction in pending_transactions:
            sender_account = transaction.sender
            receiver_account = transaction.receiver
            amount = transaction.amount
            date = transaction.date

            # Check if the sender's account is one of the user's bank accounts
            if sender_account in user_bank_accounts:
                # Check the balance and the date
                if sender_account.balance >= amount and date <= timezone.now():
                    # Perform the transfer
                    sender_account.balance -= amount
                    receiver_account.balance += amount
                    sender_account.save()
                    receiver_account.save()

                    # Update the transaction status
                    transaction.status = 'completed'
                    transaction.save()

                else:
                    # Update the transaction status to pending
                    transaction.status = 'pending'
                    transaction.save()
    execute_pending_transactions()
    return render(request, path.join(USER_TEMPLATES_DIR, 'bank_account_details.html'), context)
