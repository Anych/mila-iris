from django.views.generic import ListView

from category.models import Category
from products.models import Product


class CategoryView(ListView):

    model = Category
    template_name = 'shop/category_detail.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        category = super().get_queryset(**kwargs).filter(slug=self.kwargs['category_slug']).first()
        products = Product.objects.filter(category=category, size__stock__gt=0). \
            order_by('-is_recommend', '-modified_date').distinct().select_related()
        popular_products = products.filter(views__gt=1)
        products_count = len(products)
        context = {
                'products': products,
                'popular_products': popular_products,
                'category': category,
                'products_count': products_count,
            }
        return context


class SubCategoryView(CategoryView):

    def get_context_data(self, **kwargs):
        sub_category = super().get_queryset(**kwargs).filter(slug=self.kwargs['sub_category_slug']).first()
        category = sub_category.get_ancestors(ascending=False, include_self=False).first()
        products = Product.objects.filter(category=sub_category, size__stock__gt=0). \
            order_by('-is_recommend', '-modified_date').distinct().select_related()
        popular_products = products.filter(views__gt=1)
        products_count = len(products)
        context = {
                'products': products,
                'popular_products': popular_products,
                'category': category,
                'sub_category': sub_category,
                'products_count': products_count,
            }
        return context
