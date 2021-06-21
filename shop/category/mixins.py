from django.core.paginator import Paginator
from django.views.generic import ListView

from category.models import Category
from products.models import Product


class CategoryMixin(ListView):

    model = Category
    template_name = 'store/category_detail.html'
    paginate_by = 9

    def mixin_context(self, category=None, subcategory=None, **kwargs):
        if category is not None:
            categories = category.get_descendants(include_self=False)
            products = Product.objects.filter(category__in=categories, size__stock__gt=0). \
                order_by('-is_recommend', '-modified_date').distinct().select_related()
        elif subcategory is not None:
            category = subcategory.get_ancestors(ascending=False, include_self=False).first()
            products = Product.objects.filter(category=subcategory, size__stock__gt=0). \
                order_by('-is_recommend', '-modified_date').distinct().select_related()
        popular_products = products.filter(views__gt=1)
        products_count = len(products)
        paginator = Paginator(products, self.paginate_by)
        page = self.request.GET.get('page')
        paged_products = paginator.get_page(page)
        category = category
        context = {
                'category': category,
                'subcategory': subcategory,
                'products': paged_products,
                'popular_products': popular_products,
                'products_count': products_count,
            }
        return context
