from django.urls import path

from category.views import ClothesView

urlpatterns = [
    path('clothes/', ClothesView, name='clothes'),
]
