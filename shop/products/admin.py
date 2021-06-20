from django.contrib import admin

from products.models import Product, ProductGallery, Size, ProductFeatures


class ProductGalleryInline(admin.StackedInline):
    model = ProductGallery
    extra = 2


class ProductSizeInline(admin.StackedInline):
    model = Size
    extra = 1


class ProductFeatureInline(admin.StackedInline):
    model = ProductFeatures
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    """
    In product model only ProductAdmin has interface for changing.
    Another models can fill only throw this interface
    """
    list_display = ('article', 'brand', 'category', 'price', 'is_recommend')
    list_display_links = ('article', 'brand')
    exclude = ['slug', 'views']
    inlines = [ProductFeatureInline, ProductGalleryInline, ProductSizeInline]


admin.site.register(Product, ProductAdmin)
