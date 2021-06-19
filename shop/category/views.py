from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from category.models import Category


class Store(ListView):

    model = Category
    template_name = 'store/category_detail.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        ancestor = None
        if self.kwargs['category_slug']:
            category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
            if category.is_root_node():
                categories = category.get_descendants(include_self=False)
                products = Product.objects.filter(category__in=categories, size__stock__gt=0).\
                    order_by('-is_recommend', '-modified_date').distinct().select_related()
                popular_products = products.filter(views__gt=1)
                products_count = len(products)
            else:
                ancestor = category.get_ancestors(ascending=False, include_self=False).first()
                print(123)
                products = Product.objects.filter(category=category, size__stock__gt=0).\
                    order_by('-is_recommend', '-modified_date').distinct().select_related()
                popular_products = products.filter(views__gt=1)
                products_count = len(products)
        else:
            category = Category.objects.get(id=1)
            categories = category.get_children()
            products = Product.objects.filter(category__in=categories, size__stock__gt=0). \
                order_by('-is_recommend', '-modified_date').distinct().select_related()
            products_count = products.count()
            popular_products = products.filter(views__gt=1)

        context = {
                'products': products,
                'popular_products': popular_products,
                'category': category,
                'ancestor': ancestor,
                'products_count': products_count,
            }
        return context
