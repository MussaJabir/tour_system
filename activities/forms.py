from django import forms
from .models import Activity, ActivityImage


class ActivityForm(forms.ModelForm):
    """Form for creating/editing activities"""
    
    class Meta:
        model = Activity
        fields = [
            'name', 'short_description', 'description',
            'destination', 'category', 'difficulty',
            'duration', 'duration_unit', 'min_age', 'max_group_size',
            'price_per_person', 'currency',
            'featured_image', 'video_url',
            'requirements', 'included_items', 'excluded_items', 'best_season',
            'is_featured', 'is_active', 'order',
            'meta_title', 'meta_description', 'meta_keywords',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'short_description': forms.Textarea(attrs={'rows': 2}),
            'requirements': forms.Textarea(attrs={'rows': 3}),
            'included_items': forms.Textarea(attrs={'rows': 3}),
            'excluded_items': forms.Textarea(attrs={'rows': 3}),
            'best_season': forms.TextInput(attrs={'placeholder': 'e.g., June - October'}),
            'meta_description': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea, forms.Select, forms.URLInput, forms.NumberInput)):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': 'form-control-file'})
        
        # Add helpful placeholders
        self.fields['name'].widget.attrs['placeholder'] = 'e.g., Morning Game Drive'
        self.fields['price_per_person'].widget.attrs['placeholder'] = '0.00'
        self.fields['duration'].widget.attrs['placeholder'] = 'e.g., 2.5'
        self.fields['min_age'].widget.attrs['placeholder'] = 'Minimum age (optional)'
        self.fields['max_group_size'].widget.attrs['placeholder'] = 'Max group size (optional)'


class ActivityImageForm(forms.ModelForm):
    """Form for adding images to activity gallery"""
    
    class Meta:
        model = ActivityImage
        fields = ['image', 'caption', 'order']
        widgets = {
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Image caption (optional)'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'value': 0}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

