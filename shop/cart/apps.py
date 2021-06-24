from django.apps import AppConfig


class CartConfig(AppConfig):
    """Configuration for cart application"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'
    verbose_name = 'Корзина'
