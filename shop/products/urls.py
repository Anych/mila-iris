from django.urls import path

from products.views import ProductView, SubmitReviewView, AskQuestionView

urlpatterns = [
    path('<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/', ProductView.as_view(), name='product'),

    path('submit-review/<int:product_id>/', SubmitReviewView.as_view(), name='submit_review'),
    path('ask_question/<int:product_id>/', AskQuestionView.as_view(), name='ask_question'),
]
