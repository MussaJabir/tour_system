from django import forms
from .models import Accommodation, AccommodationImage, Room


class AccommodationForm(forms.ModelForm):
    """Form for creating/editing accommodations"""
    
    # Common amenities choices for easier selection
    AMENITIES_CHOICES = [
        'WiFi', 'Pool', 'Restaurant', 'Bar', 'Gym', 'Spa', 'Parking',
        'Airport Shuttle', 'Room Service', 'Laundry', 'Conference Room',
        'Business Center', 'Pet Friendly', 'Air Conditioning', 'Heating',
        'Garden', 'Terrace', 'Beach Access', 'Kids Club', 'Babysitting'
    ]
    
    class Meta:
        model = Accommodation
        fields = [
            'name', 'short_description', 'description',
            'destination', 'accommodation_type', 'star_rating',
            'address', 'latitude', 'longitude',
            'phone', 'email', 'website',
            'amenities', 'total_rooms',
            'price_per_night_min', 'price_per_night_max', 'currency',
            'check_in_time', 'check_out_time', 'policies',
            'featured_image', 'video_url',
            'is_featured', 'is_active', 'order',
            'meta_title', 'meta_description', 'meta_keywords',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'short_description': forms.Textarea(attrs={'rows': 2}),
            'address': forms.Textarea(attrs={'rows': 2}),
            'policies': forms.Textarea(attrs={'rows': 3}),
            'amenities': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Enter amenities separated by commas (e.g., WiFi, Pool, Restaurant)'}),
            'meta_description': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea, forms.Select, forms.URLInput, forms.NumberInput, forms.EmailInput)):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': 'form-control-file'})
        
        # Add helpful placeholders
        self.fields['name'].widget.attrs['placeholder'] = 'e.g., Serena Safari Lodge'
        self.fields['phone'].widget.attrs['placeholder'] = '+1 234 567 890'
        self.fields['email'].widget.attrs['placeholder'] = 'info@accommodation.com'
        self.fields['check_in_time'].widget.attrs['placeholder'] = '2:00 PM'
        self.fields['check_out_time'].widget.attrs['placeholder'] = '11:00 AM'
        self.fields['price_per_night_min'].widget.attrs['placeholder'] = 'Min price'
        self.fields['price_per_night_max'].widget.attrs['placeholder'] = 'Max price'


class AccommodationImageForm(forms.ModelForm):
    """Form for adding images to accommodation gallery"""
    
    class Meta:
        model = AccommodationImage
        fields = ['image', 'caption', 'order']
        widgets = {
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Image caption (optional)'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'value': 0}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }


class RoomForm(forms.ModelForm):
    """Form for adding/editing room types"""
    
    class Meta:
        model = Room
        fields = [
            'name', 'room_type', 'description',
            'max_occupancy', 'bed_type', 'number_of_beds',
            'size_sqm', 'price_per_night',
            'amenities', 'is_available', 'image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'amenities': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Room amenities (comma-separated)'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea, forms.Select, forms.NumberInput)):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': 'form-control-file'})
        
        # Add placeholders
        self.fields['name'].widget.attrs['placeholder'] = 'e.g., Deluxe Ocean View'
        self.fields['size_sqm'].widget.attrs['placeholder'] = 'Room size in sqm'
        self.fields['price_per_night'].widget.attrs['placeholder'] = 'Price per night'

