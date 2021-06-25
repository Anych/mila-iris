from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """Configuration for products application."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    verbose_name = 'Товары'
