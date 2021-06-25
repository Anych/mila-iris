from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView

from orders.forms import OrderForm


class OrderCompleteView(View):
    """View for render template, when orders posted successfully."""

    def get(self, request, *args, **kwargs):
        return render(request, 'orders/order_complete.html')


# @login_required(login_url='login')
# def orders(request, order_number):
#
#     order = Order.objects.get(order_number=order_number)
#     order_products = order.orderproduct_set.all()
#     context = {
#         'order': order,
#         'order_products': order_products,
#     }
#     return render(request, 'orders/order.html', context)