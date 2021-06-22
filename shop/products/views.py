from django.views.generic import DetailView

from category.models import Category
from products.models import Product, ReviewRating, Size, ProductGallery, ProductFeatures


class ProductView(DetailView):

    model = Product
    template_name = 'store/product_detail.html'
    slug_url_kwarg = 'product_slug'

    # def get(self, request, *args, **kwargs):
    #     # if request.user.is_authenticated:
    #     #         try:
    #     #             order_product = OrderProduct.objects.filter(user=request.user, product_id=product.id).exists()
    #     #         except OrderProduct.DoesNotExist:
    #     #             order_product = None
    #     #     else:
    #     #         order_product = None
    #     pass

    def get_context_data(self, **kwargs):
        product = self.get_object()
        product.increment_views()
        subcategory = Category.objects.get(slug=self.kwargs['subcategory_slug'])
        category = Category.objects.get(slug=self.kwargs['category_slug'])
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True).select_related()
        average_review = product.average_review
        count_review = product.count_review
        sizes = Size.objects.filter(product=product, stock__gt=0).select_related()
        product_gallery = ProductGallery.objects.filter(product=product).select_related()

        product_features = ProductFeatures.objects.filter(product=product).select_related()
        context = {
            'product': product,
            'category': category,
            'subcategory': subcategory,
            'reviews': reviews,
            'sizes': sizes,
            'product_gallery': product_gallery,
            'average_review': average_review,
            'count_review': count_review,
            'product_features': product_features,
        }
        return context


def submit_review(request, product_id):
    pass

def ask_question(request, product_id):
    pass
# def product_detail(request, category_slug, product_slug):
#
#     product = Product.objects.get(category__slug=category_slug, slug=product_slug)
#     product.increment_views()
#
#     # if request.user.is_authenticated:
#     #     try:
#     #         order_product = OrderProduct.objects.filter(user=request.user, product_id=product.id).exists()
#     #     except OrderProduct.DoesNotExist:
#     #         order_product = None
#     # else:
#     #     order_product = None
#
#     reviews = ReviewRating.objects.filter(product_id=product.id, status=True).select_related()
#     average_review = product.average_review
#     count_review = product.count_review
#     sizes = Size.objects.filter(product=product, stock__gt=0).select_related()
#
#     product_gallery = ProductGallery.objects.filter(product=product).select_related()
#
#     product_features = ProductFeatures.objects.filter(product=product).select_related()
#
#     context = {
#         'product': product,
#         'order_product': order_product,
#         'reviews': reviews,
#         'sizes': sizes,
#         'product_gallery': product_gallery,
#         'average_review': average_review,
#         'count_review': count_review,
#         'product_features': product_features,
#     }
#     return render(request, 'store/product_detail.html', context)
