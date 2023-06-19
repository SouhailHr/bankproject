from django.urls import path, include
from .views import create_bank_account, bank_account_details
from deposit.views import  deposit_funds , deposit_history
from transaction.views import send_funds_out, send_funds_within, transaction_history

urlpatterns = [
    path('create/', create_bank_account, name='create_bank_account'),
    path('details/', bank_account_details, name='bank_account_details'),
    path('deposit/', deposit_funds, name='deposit_funds'),
    path('sendout/', send_funds_out, name='send_funds_out'),
    path('sendwithin/', send_funds_within, name='send_funds_within'),
    path('transaction_history/', transaction_history, name='transaction_history')

]
