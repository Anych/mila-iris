from django.urls import path

from category.views import CategoryView, SubCategoryView

urlpatterns = [
    path('<slug:category_slug>/', CategoryView.as_view(), name='category'),
    path('<slug:category_slug>/<slug:sub_category_slug>/', SubCategoryView.as_view(), name='sub_category'),
]
