from django.apps import AppConfig


class CategoryConfig(AppConfig):
    """Application to using categories and all features about them"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'category'
    verbose_name = 'Категории'
