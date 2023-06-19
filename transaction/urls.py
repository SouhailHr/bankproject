from django.urls import path
from . import views

urlpatterns = [
    # ... other URLs ...
    path('sendout/', views.send_funds_out(), name='send_funds_out'),
    path('sendwithin/', views.send_funds_within(), name='send_funds_within'),
    path('transaction_history/', views.transaction_history, name='transaction_history')

]
