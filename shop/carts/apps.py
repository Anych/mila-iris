from django.apps import AppConfig


class CartsConfig(AppConfig):
    """Configuration for cart application."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carts'
    verbose_name = 'Корзина'
