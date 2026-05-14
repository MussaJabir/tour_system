from django import forms
from .models import Review


class ReviewSubmitForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'body', 'reviewer_name', 'reviewer_country']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Summarise your experience'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5,
                                          'placeholder': 'Tell future travelers what to expect…'}),
            'reviewer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'reviewer_country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        }
