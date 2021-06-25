from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """Configuration for orders application"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
    verbose_name = 'Заказы'
