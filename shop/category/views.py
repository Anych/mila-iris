from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from category.models import Category
from products.models import Product


class CategoryView(ListView):

    model = Category
    template_name = 'shop/category_detail.html'
    paginate_by = 2


class ClothesView(ListView):

    # model = Category.objects.get(slug='clothes')
    pass