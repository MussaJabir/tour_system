from django import forms
from .models import Destination, DestinationImage


class DestinationForm(forms.ModelForm):
    """
    Form for creating/editing destinations in custom dashboard
    """
    class Meta:
        model = Destination
        fields = [
            'name',
            'short_description',
            'description',
            'country',
            'region',
            'latitude',
            'longitude',
            'featured_image',
            'video_url',
            'best_time_to_visit',
            'climate',
            'wildlife',
            'is_featured',
            'is_active',
            'order',
            'meta_title',
            'meta_description',
            'meta_keywords',
        ]
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter destination name'
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description for previews'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Full destination description'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Country name'
            }),
            'region': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Region or state'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., -3.3869',
                'step': '0.000001'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 36.2820',
                'step': '0.000001'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'YouTube or Vimeo URL'
            }),
            'best_time_to_visit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., June - October'
            }),
            'climate': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'wildlife': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO title (optional)'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'SEO description'
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Comma-separated keywords'
            }),
        }


class DestinationImageForm(forms.ModelForm):
    """
    Form for uploading gallery images
    """
    class Meta:
        model = DestinationImage
        fields = ['image', 'caption', 'order']
        
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Image caption (optional)'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'value': 0
            }),
        }

