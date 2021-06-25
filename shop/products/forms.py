from django import forms

from products.models import ReviewRating, CustomerQuestion


class ReviewForm(forms.ModelForm):
    """Form for product review."""
    class Meta:
        model = ReviewRating
        fields = ['review', 'rating']


class QuestionForm(forms.ModelForm):
    """Form for question about product."""
    class Meta:
        model = CustomerQuestion
        fields = ['question', 'name', 'email']
