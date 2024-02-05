from django.urls import path
from .api import CartView, ExtraView, TipView
from .views import checkout

app_name = 'checkout'

urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path('api/cart/', CartView.as_view(), name='cart'),
    path('api/extra-list/', ExtraView.as_view(), name='extra_list'),
    path('api/tip-list/', TipView.as_view(), name='tip_list'),
]
