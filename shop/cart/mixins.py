from django.views import View

from cart.models import Cart
from cart.utils import _cart_id


class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
            except Cart.DoesNotExist:
                cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()
        return super().dispatch(request, *args, **kwargs)

