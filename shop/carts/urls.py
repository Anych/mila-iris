from django.urls import path

from carts.views import CartView, CheckOutView, AddToCartView, ReduceCartItemView, RemoveFromCartItemView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),

    path('add_to_cart/<int:product_id>/<int:quantity>', AddToCartView.as_view(), name='add_to_cart'),
    path('remove_from_cart_item/<int:product_id>/<int:cart_item_id>/',
         RemoveFromCartItemView.as_view(), name='remove_from_cart_item'),
    path('reduce_cart_item/<int:product_id>/<int:cart_item_id>/',
         ReduceCartItemView.as_view(), name='reduce_cart_item'),
]
