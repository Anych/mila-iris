from django.urls import path

from orders.views import OrderCompleteView

urlpatterns = [
    path('order-complete/', OrderCompleteView.as_view(), name='order_complete'),
]
