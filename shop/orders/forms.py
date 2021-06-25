from django import forms
from orders.models import Order


class OrderForm(forms.ModelForm):
    """Form for order product."""
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'country', 'state', 'city', 'order_note']
