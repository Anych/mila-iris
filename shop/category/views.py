from category.mixins import CategoryMixin


class CategoryMainView(CategoryMixin):
    """View for main page of categories don't take any arguments and shows all products in the site"""

    def get_context_data(self, *, object_list=None, **kwargs):
        context = self.mixin_context()
        return context


class SalesMainView(CategoryMixin):
    """View for main sales page of categories don't take any arguments and shows all sale products in the site"""

    def get_context_data(self, *, object_list=None, **kwargs):
        context = self.mixin_context(sales=True)
        return context


class CategoryView(CategoryMixin):
    """View for categories from the next list: clothes, shoes, accessories"""

    def get_context_data(self, *, object_list=None, **kwargs):
        category = super().get_queryset(**kwargs).filter(slug=self.kwargs['category_slug']).first()
        context = self.mixin_context(category=category)
        return context


class SubCategoryView(CategoryMixin):
    """View for subcategories which are descending from the main categories"""

    def get_context_data(self, *, object_list=None, **kwargs):
        subcategory = super().get_queryset(**kwargs).filter(slug=self.kwargs['subcategory_slug']).first()
        context = self.mixin_context(subcategory=subcategory)
        return context


class SalesCategoryView(CategoryMixin):
    """View for sales categories from the next list: clothes, shoes, accessories"""

    def get_context_data(self, *, object_list=None, **kwargs):
        category = super().get_queryset(**kwargs).filter(slug=self.kwargs['category_slug']).first()
        context = self.mixin_context(category=category, sales=True)
        return context


class SalesSubCategoryView(CategoryMixin):
    """View for sales subcategories which are descending from the main categories"""

    def get_context_data(self, *, object_list=None, **kwargs):
        subcategory = super().get_queryset(**kwargs).filter(slug=self.kwargs['subcategory_slug']).first()
        context = self.mixin_context(subcategory=subcategory, sales=True)
        return context
