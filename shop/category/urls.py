from django.urls import path

from category.views import CategoryView, SubCategoryView

urlpatterns = [
    path('<slug:category_slug>/', CategoryView.as_view(), name='category'),
    path('<slug:category_slug>/<slug:subcategory_slug>/', SubCategoryView.as_view(), name='subcategory'),
]
