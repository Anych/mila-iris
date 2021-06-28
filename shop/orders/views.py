from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from orders.models import Order


class OrderCompleteView(View):
    """View for render template, when orders posted successfully."""

    def get(self, request, *args, **kwargs):
        return render(request, 'orders/order_complete.html')


class OrdersView(LoginRequiredMixin, DetailView):
    """View for see already done orders."""
    model = Order
    slug_url_kwarg = 'order_number'

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(order_number=kwargs['order_number'])
        order_products = order.orderproduct_set.all()
        context = {
            'order': order,
            'order_products': order_products,
        }
        return render(request, 'orders/order.html', context)
