from django.core.paginator import Paginator
from django.views.generic import ListView

from category.models import Category
from products.models import Product


class CategoryMixin(ListView):
    """
    Mixin for all category views, which do all context for them.
    The main idea that, it takes category slug, subcategory slug,
    boolean field sales or doesn't not take any arguments, and
    after make queryset of products to the particular category in django-mptt.
    """
    model = Category
    template_name = 'store/category_detail.html'
    paginate_by = 9

    def mixin_context(self, category=None, subcategory=None, sales=False, **kwargs):
        if category is not None:
            categories = category.get_descendants(include_self=False)
            if sales:
                products = Product.objects.filter(category__in=categories, is_discount=True, size__stock__gt=0). \
                    order_by('-is_recommend', '-modified_date').distinct().select_related()
            else:
                products = Product.objects.filter(category__in=categories, size__stock__gt=0). \
                    order_by('-is_recommend', '-modified_date').distinct().select_related()
        elif subcategory is not None:
            category = subcategory.get_ancestors(ascending=False, include_self=False).first()
            if sales:
                products = Product.objects.filter(category=subcategory, is_discount=True, size__stock__gt=0) \
                    .order_by('-is_recommend', '-modified_date').distinct().select_related()
            else:
                products = Product.objects.filter(category=subcategory, size__stock__gt=0). \
                    order_by('-is_recommend', '-modified_date').distinct().select_related()
        else:
            categories = Category.objects.all()
            if sales:
                products = Product.objects.filter(category__in=categories, is_discount=True, size__stock__gt=0) \
                    .order_by('-is_recommend', '-modified_date').distinct().select_related()
            else:
                products = Product.objects.filter(category__in=categories, size__stock__gt=0). \
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
