from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render, redirect
from os import path
from pathlib import Path

from django.utils import timezone

from BankAccount.models import BankAccount
from deposit.models import Deposit
from transaction.forms import SendFundsOutForm, SendFundsWithinForm
from transaction.models import Transaction

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
USER_TEMPLATES_DIR = path.join(ROOT_DIR, 'templates/transaction/')



def send_funds_out(request):
    user = request.user

    if request.method == 'POST':
        form = SendFundsOutForm(request.POST, user=user)
        if form.is_valid():
            sender_account = form.cleaned_data['sender']
            receiver_account = form.cleaned_data['receiver']
            amount = form.cleaned_data['amount']
            date = form.cleaned_data['date']

            if date <= timezone.now():
                # Perform instant transfer
                sender_account.balance -= amount
                receiver_account.balance += amount
                sender_account.save()
                receiver_account.save()
                status = 'completed'
            else:
                # Schedule automatic transfer
                status = 'pending'

            # Save the transaction
            transaction = form.save_transaction()
            transaction.status = status
            transaction.save()

            return redirect('bank_account_details')  # Redirect to bank account details page or display success message
    else:
        form = SendFundsOutForm(user=user)

    context = {
        'form': form
    }
    return render(request, path.join(USER_TEMPLATES_DIR, 'send_funds_out.html'), context)

def send_funds_within(request):
    user = request.user

    if request.method == 'POST':
        form = SendFundsWithinForm(request.POST, user=user)
        if form.is_valid():
            sender_account = form.cleaned_data['sender']
            receiver_account = form.cleaned_data['receiver']
            amount = form.cleaned_data['amount']
            date = form.cleaned_data['date']

            # check date
            if date <= timezone.now():
                # Update sender and receiver account balances
                sender_account.balance -= amount
                receiver_account.balance += amount
                sender_account.save()
                receiver_account.save()
                form.save_transaction()  # Save the transaction
            else:
                # save the auto trans
                form.save_transaction()


            return redirect('bank_account_details')  # Redirect to bank account details page or display success message
    else:
        form = SendFundsWithinForm(user=user)

    context = {
        'form': form
    }
    return render(request, path.join(USER_TEMPLATES_DIR, 'send_funds_within.html'), context)


def transaction_history(request):
    user = request.user
    bank_accounts = BankAccount.objects.filter(user=user)
    transactions = Transaction.objects.filter(Q(sender__in=bank_accounts) | Q(receiver__in=bank_accounts)).order_by('-date')
    deposits = Deposit.objects.filter(account__in=bank_accounts).order_by('-date')

    context = {
        'transactions': transactions,
        'deposits': deposits
    }

    # Render the HTML template
    template = path.join(USER_TEMPLATES_DIR, "transaction_history.html")
    return render(request, template, context)