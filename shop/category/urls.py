from django.urls import path

from category.views import (
    CategoryMainView,
    SalesMainView,
    CategoryView,
    SubCategoryView,
    SalesCategoryView,
    SalesSubCategoryView,
)

urlpatterns = [
    path('category/', CategoryMainView.as_view(), name='category_main'),
    path('sales/', SalesMainView.as_view(), name='sales_main'),

    path('category/<slug:category_slug>/', CategoryView.as_view(), name='category'),
    path('category/<slug:category_slug>/<slug:subcategory_slug>/', SubCategoryView.as_view(), name='subcategory'),

    path('sales/<slug:category_slug>/', SalesCategoryView.as_view(), name='sales_category'),
    path('sales/<slug:category_slug>/<slug:subcategory_slug>/',
         SalesSubCategoryView.as_view(), name='sales_subcategory'),
]
