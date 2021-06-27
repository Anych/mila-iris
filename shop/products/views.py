from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import DetailView, CreateView

from category.models import Category
from orders.models import OrderProduct
from products.forms import ReviewForm, QuestionForm
from products.mixins import ProductViewMixin
from products.models import Product, ReviewRating, Size, ProductGallery, ProductFeatures, CustomerQuestion
from shop.emails import Emails


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


class SubmitReviewView(ProductViewMixin, CreateView):
    """Submit rating and review for product view. User can do it only if he already bought a product."""
    form_class = ReviewForm
    model = ReviewRating

    def post(self, request, *args, **kwargs):
        try:
            # Check if user bought the product
            reviews = ReviewRating.objects.get(user=request.user, product__id=self.product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Спасибо! Ваш отзыв обновлён')
            return redirect(self.url)

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = self.product_id
                data.user_id = self.request_user.id
                data.save()
                messages.success(request, 'Спасибо! Ваш отзыв опубликован.')
                return redirect(self.url)


class AskQuestionView(ProductViewMixin, CreateView):
    """Ask question about product view. All users can do it."""
    form_class = QuestionForm
    model = CustomerQuestion

    def post(self, request, *args, **kwargs):
        form = QuestionForm(request.POST)
        if form.is_valid():
            data = CustomerQuestion()
            data.email = form.cleaned_data['email']
            data.question = form.cleaned_data['question']
            data.name = form.cleaned_data['name']
            data.product_id = self.product_id
            if self.request_user.is_authenticated:
                data.user_id = self.request_user.id
            else:
                data.user_id = None
            data.save()
            messages.success(request, 'Спасибо! Ваш вопрос был отправлен.')
            Emails(user=data.name, email=data.email, question=data.question, product_url=self.url)
            return redirect(self.url)
