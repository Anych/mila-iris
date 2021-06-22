from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from cart.mixins import CartMixin
from products.models import Product, Size


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            self.calculate_total(self.cart_items)
        except ObjectDoesNotExist:
            pass

        context = {
            'total': self.TOTAL,
            'cart_items': self.cart_items,
        }
        return render(request, 'store/cart.html', context)


class AddToCartView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs['product_id'])
        value = request.POST['size']
        size = Size.objects.get(product=product, size=value)

        try:
            cart_item = self.get_cart_item(product=product, size=size)
            cart_item.quantity += 1
        except ObjectDoesNotExist:
            cart_item = self.get_cart_item(product=product, quantity=1, size=size)

        if size.stock < cart_item.quantity:
            messages.success(request, f'К сожалению, на складе осталось {size.stock}')
        else:
            cart_item.save()
        return redirect('cart')


class RemoveFromCartItemView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        cart_item = self.get_cart_item(product=product, cart_item_id=self.kwargs['cart_item_id'])
        cart_item.delete()
        return redirect('cart')


class ReduceCartItemView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['product_id'])

        try:
            cart_item = self.get_cart_item(product=product, cart_item_id=self.kwargs['cart_item_id'])
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        except:
            pass

        return redirect('cart')


class CheckOutView(CartMixin, View):
    pass