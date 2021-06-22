from django.urls import path

from cart import views

urlpatterns = [
    path('add_cart/<int:product_id>/<int:quantity>', views.add_cart, name='add_cart'),
]