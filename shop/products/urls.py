from django.urls import path

from products.views import ProductView, submit_review, ask_question

urlpatterns = [
    path('<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/', ProductView.as_view(), name='product'),

    path('submit-review/<int:product_id>/', submit_review, name='submit_review'),
    path('ask_question/<int:product_id>/', ask_question, name='ask_question'),
]
