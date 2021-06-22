from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from cart.mixins import CartMixin
from cart.models import CartItem, Cart
from cart.utils import _cart_id
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
        current_user = request.user
        product = Product.objects.get(id=self.kwargs['product_id'])
        value = request.POST['size']
        size = Size.objects.get(product=product, size=value)

        is_cart_item_exists = CartItem.objects.filter(product=product, user__email=current_user.email, size=size) \
            .exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.get(product=product, user__email=current_user.email, size=size)
            cart_item.quantity += 1
            if size.stock < cart_item.quantity:
                messages.success(request, f'К сожалению, на складе осталось {size.stock}')
                return redirect('cart')
            else:
                cart_item.save()

        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
                size=size
            )
            if size.stock < cart_item.quantity:
                messages.success(request, f'К сожалению, на складе осталось {size.stock}')
                return redirect('cart')
            else:
                cart_item.save()
        return redirect('cart')

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, size=size, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.get(product=product, size=size, cart=cart)
            cart_item.quantity += 1
            if size.stock < cart_item.quantity:
                messages.success(request, f'К сожалению, на складе осталось {size.stock}')
                return redirect('cart')
            else:
                cart_item.save()

        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                size=size,
                cart=cart
            )
            if size.stock < cart_item.quantity:
                messages.success(request, f'К сожалению, на складе осталось {size.stock}')
                return redirect('cart')
            else:
                cart_item.save()
        return redirect('cart')


class RemoveFromCartItemView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user__email=request.user.email,
                                             id=self.kwargs['cart_item_id'])
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=self.kwargs['cart_item_id'])
        cart_item.delete()
        return redirect('cart')


class CheckOutView(CartMixin, View):
    pass


class ReduceCartItemView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        current_user = request.user

        try:
            if current_user.is_authenticated:
                cart_item = CartItem.objects.get(product=product, user__email=current_user.email,
                                                 id=self.kwargs['cart_item_id'])
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_item = CartItem.objects.get(product=product, cart=cart, id=self.kwargs['cart_item_id'])
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        except:
            pass
        return redirect('cart')
