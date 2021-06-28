from django.urls import path

from orders.views import OrderCompleteView, OrdersView

urlpatterns = [
    path('order-complete/', OrderCompleteView.as_view(), name='order_complete'),
    path('order/<int:order_number>', OrdersView.as_view(), name='order'),
]
