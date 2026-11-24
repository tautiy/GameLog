from django import forms

from .models import UserGameRating


class UserGameRatingForm(forms.ModelForm):
    class Meta:
        model = UserGameRating
        fields = ('rating', 'review')
        widgets = {
            'rating': forms.Select(attrs={'class': 'rating-select'}),
            'review': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Напишите свою рецензию...',
                    'class': 'review-textarea',
                }
            ),
        }
        labels = {
            'rating': 'Ваша оценка',
            'review': 'Рецензия',
        }