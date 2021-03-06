from django.views import View

from carts.models import Cart, CartItem
from carts.utils import _cart_id


class CartMixin(View):
    """Mixin for cart and cart actions."""
    DELIVERY = 2000
    TOTAL = 0

    def dispatch(self, request, *args, **kwargs):
        """Method which return request user and cart items."""
        self.request_user = request.user
        if self.request_user.is_anonymous:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(cart_id=_cart_id(request))
                cart_items = None
            cart.save()
            self.cart = cart
        else:
            cart_items = CartItem.objects.filter(user=self.request_user)
        self.cart_items = cart_items
        return super().dispatch(request, *args, **kwargs)

    def calculate_total(self):
        """Method which calculate total sum for order."""
        for item in self.cart_items:
            if item.product.is_discount:
                if item.product.discount_price:
                    self.TOTAL += (item.product.discount_price * item.quantity)
                else:
                    self.TOTAL += (item.product.calc_discount_price() * item.quantity)
            else:
                self.TOTAL += (item.product.price * item.quantity)
        if self.TOTAL > 50000:
            self.DELIVERY = 0
        self.TOTAL = self.TOTAL + self.DELIVERY
        return self.TOTAL

    def get_cart_item(self, product, cart_item_id=None, size=None, quantity=0):
        """Get or create cart item and check if user is authenticated."""
        if self.request_user.is_authenticated:
            if quantity == 1:
                cart_item = CartItem.objects.create(product=product,
                                                    quantity=quantity, user=self.request_user, size=size)
            elif size is not None:
                cart_item = CartItem.objects.get(product=product, user=self.request_user, size=size)
            else:
                cart_item = CartItem.objects.get(product=product, user=self.request_user, id=cart_item_id)

        else:
            if quantity == 1:
                cart_item = CartItem.objects.create(product=product, quantity=quantity, cart=self.cart, size=size)
            elif size is not None:
                cart_item = CartItem.objects.get(product=product, cart=self.cart, size=size)
            else:
                cart_item = CartItem.objects.get(product=product, cart=self.cart, id=cart_item_id)
        return cart_item
