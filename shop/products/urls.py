from django.urls import path

from products.views import ProductView

urlpatterns = [
    path('<slug:category_slug>/<slug:sub_category_slug>/<slug:product_slug>/', ProductView.as_view(), name='product'),
]
