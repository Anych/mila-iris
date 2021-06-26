from django.views import View


class ProductViewMixin(View):
    """Mixin for products create view classes."""
    def dispatch(self, request, *args, **kwargs):
        self.url = request.META.get('HTTP_REFERER')
        self.product_id = kwargs['product_id']
        self.request_user = request.user
        return super().dispatch(request, *args, **kwargs)
