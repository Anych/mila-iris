from django.views.generic import DetailView, CreateView

from category.models import Category
from orders.models import OrderProduct
from products.forms import ReviewForm
from products.models import Product, ReviewRating, Size, ProductGallery, ProductFeatures


class ProductView(DetailView):
    """View for products which retrieve context for it and check if user was order product."""
    model = Product
    template_name = 'store/product_detail.html'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        product = self.get_object()
        product.increment_views()
        request_user = self.request.user

        # check if user bought product
        if request_user.is_authenticated:
            try:
                order_product = OrderProduct.objects.filter(user=request_user, product_id=product.id).exists()
            except OrderProduct.DoesNotExist:
                order_product = None
        else:
            order_product = None

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
            'order_product': order_product,
            'subcategory': subcategory,
            'reviews': reviews,
            'sizes': sizes,
            'product_gallery': product_gallery,
            'average_review': average_review,
            'count_review': count_review,
            'product_features': product_features,
        }
        return context


class SubmitReview(CreateView):

    form_class = ReviewForm


def submit_review(request, product_id):
    pass
    # url = request.META.get('HTTP_REFERER')
    # if request.method == 'POST':
    #     try:
    #         reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
    #         form = ReviewForm(request.POST, instance=reviews)
    #         form.save()
    #         messages.success(request, 'Спасибо! Ваш отзыв обновлён')
    #         return redirect(url)
    #     except ReviewRating.DoesNotExist:
    #         form = ReviewForm(request.POST)
    #         if form.is_valid():
    #             data = ReviewRating()
    #             data.rating = form.cleaned_data['rating']
    #             data.review = form.cleaned_data['review']
    #             data.ip = request.META.get('REMOTE_ADDR')
    #             data.product_id = product_id
    #             data.user_id = request.user.id
    #             data.save()
    #             messages.success(request, 'Спасибо! Ваш отзыв опубликован.')
    #             return redirect(url)

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
