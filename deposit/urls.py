from django.urls import path
from .views import deposit_funds , deposit_history


urlpatterns = [
    # Other URL patterns
    path('deposit/', deposit_funds, name='deposit_funds'),
    path('list/', deposit_history, name='deposit_history')
]
