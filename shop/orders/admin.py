from django.contrib import admin
from orders.models import Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    """Tabular Inline for order. Which contain ordered products."""
    model = OrderProduct
    readonly_fields = ('user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    """Order Admin View."""
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city',
                    'order_total', 'delivery', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]


admin.site.register(Order, OrderAdmin)
