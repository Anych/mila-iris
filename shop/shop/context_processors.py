from cart.utils import _cart_id
from category.models import Category
from cart.models import Cart, CartItem


def menu_links(request):
    cloth_categories = Category.objects.get(slug='clothes').get_descendants(include_self=False)
    shoe_categories = Category.objects.get(slug='shoes').get_descendants(include_self=False)
    accessor_categories = Category.objects.get(slug='accessories').get_descendants(include_self=False)
    return dict(cloth_categories=cloth_categories, shoe_categories=shoe_categories,
                accessor_categories=accessor_categories)


def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user__email=request.user.email)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)