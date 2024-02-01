from django.urls import path
from .api import CartView

app_name = 'checkout'

urlpatterns = [
    path('api/cart/', CartView.as_view(), name='cart'),
]
