from django.views import View

from cart.models import Cart, CartItem
from cart.utils import _cart_id


class CartMixin(View):

    DELIVIRY = 2000
    TOTAL = 0

    def dispatch(self, request, *args, **kwargs):
        request_user = request.user
        if request_user.is_anonymous:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(cart_id=_cart_id(request))
                cart_items = None
            cart.save()
        else:
            cart_items = CartItem.objects.filter(user=request_user)
        self.cart_items = cart_items
        return super().dispatch(request, *args, **kwargs)

    def calculate_total(self, cart_items):
        for item in self.cart_items:
            if item.product.is_discount:
                if item.product.discount_price:
                    self.TOTAL += (item.product.discount_price * item.quantity)
                else:
                    self.TOTAL += (item.product.calc_discount_price() * item.quantity)
            else:
                self.TOTAL += (item.product.price * item.quantity)
        if self.TOTAL > 50000:
            self.DELIVIRY = 0
        self.TOTAL = self.TOTAL + self.DELIVIRY
        return self.TOTAL
