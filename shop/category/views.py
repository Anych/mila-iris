from category.mixins import CategoryMixin


class CategoryView(CategoryMixin):
    """View for categories from the next list: clothes, shoes, accessories"""

    def get_context_data(self, *, object_list=None, **kwargs):
        category = super().get_queryset(**kwargs).filter(slug=self.kwargs['category_slug']).first()
        context = self.mixin_context(category=category)
        return context


class SubCategoryView(CategoryMixin):
    """View for subcategories which are descending from main categories, instance of CategoryView"""

    def get_context_data(self, *, object_list=None, **kwargs):
        subcategory = super().get_queryset(**kwargs).filter(slug=self.kwargs['subcategory_slug']).first()
        context = self.mixin_context(subcategory=subcategory)
        return context


class SalesView(CategoryMixin):
    """View for subcategories which are descending from main categories, instance of CategoryView"""

    def get_context_data(self, *args, **kwargs):
        category = super().get_queryset(**kwargs).filter(slug=self.kwargs['category_slug']).first()
        categories = category.get_descendants(include_self=False)
        products = Product.objects.filter(category__in=categories, is_discount=True, size__stock__gt=0) \
            .order_by('-is_recommend', '-modified_date').distinct().select_related()
        popular_products = products.filter(views__gt=1)
        products_count = len(products)
        paginator = Paginator(products, self.paginate_by)
        page = self.request.GET.get('page')
        paged_products = paginator.get_page(page)
        context = {
                'products': products,
                'popular_products': popular_products,
                'category': category,
                'products_count': products_count,
            }
        return context
