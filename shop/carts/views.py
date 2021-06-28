import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, CreateView

from carts.mixins import CartMixin
from carts.models import CartItem
from orders.forms import OrderForm
from orders.models import Order, OrderProduct
from products.models import Product, Size
from shop.emails import Emails


class CartView(CartMixin, View):
    """View for cart template which calculate total sum."""
    def get(self, request, *args, **kwargs):
        try:
            self.calculate_total()
        except ObjectDoesNotExist:
            pass

        context = {
            'delivery': self.DELIVERY,
            'total': self.TOTAL,
            'cart_items': self.cart_items,
        }
        return render(request, 'store/cart.html', context)


class CheckOutView(LoginRequiredMixin, CartMixin, CreateView):
    """View for checkout template which calculate total sum."""
    form_class = OrderForm

    def get(self, request, *args, **kwargs):
        """Render checkout page."""
        try:
            if self.request_user.confirm_email:
                self.calculate_total()
            else:
                return redirect('/accounts/confirm-email/')
        except ObjectDoesNotExist:
            pass
        context = {
            'delivery': self.DELIVERY,
            'total': self.TOTAL,
            'cart_items': self.cart_items,
        }
        return render(request, 'store/checkout.html', context)

    def post(self, request, *args, **kwargs):
        """Create new order method."""
        cart_count = self.cart_items.count()
        if cart_count <= 0:
            return redirect('category_main')

        # Get valid form and fill order table
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = self.request_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = self.TOTAL
            data.delivery = self.DELIVERY
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Create order number part
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=self.request_user, is_ordered=False, order_number=order_number)
            order.is_ordered = True
            order.order_total = self.calculate_total()
            order.save()

            # Get ordered product to OrderProduct model
            for item in self.cart_items:
                order_product = OrderProduct()
                order_product.order_id = order.id
                order_product.user_id = request.user.id
                order_product.size = item.size
                order_product.product_id = item.product_id
                order_product.quantity = item.quantity
                if item.product.is_discount:
                    if item.product.discount_price:
                        order_product.product_price = item.product.discount_price
                    else:
                        order_product.product_price = item.product.calc_discount_price()
                else:
                    order_product.product_price = item.product.price
                order_product.ordered = True
                order_product.save()

                # Reduce product count from warehouse
                size = Size.objects.get(product=item.product_id, size=item.size)
                size.stock -= item.quantity
                size.save()

            # Clean cart
            CartItem.objects.filter(user=self.request_user).delete()

            # Send message to user
            Emails(order=order, user=self.request_user, email=self.request_user.email)

            # Send message to admin
            Emails(order=order.id)
            return redirect('order_complete')
        else:
            return redirect('checkout')


class AddToCartView(CartMixin, View):
    """View for adding product to cart."""
    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs['product_id'])
        value = request.POST['size']
        size = Size.objects.get(product=product, size=value)

        # Checking if product has already added to cart
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
    """View for removing product from cart."""
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        cart_item = self.get_cart_item(product=product, cart_item_id=self.kwargs['cart_item_id'])
        cart_item.delete()
        return redirect('cart')


class ReduceCartItemView(CartMixin, View):
    """View for reducing product from cart."""
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
