from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import (
    Package, PackageImage, PackageItinerary, PackageInclusion,
    BookingInquiry, CustomPackage, InquiryMessage, CustomPackageItinerary,
    Booking, Passenger, Payment, Departure,
)

User = get_user_model()


class PackageForm(forms.ModelForm):
    """Form for creating and editing packages"""
    
    class Meta:
        model = Package
        fields = [
            'name', 'destinations', 'category', 'difficulty_level',
            'short_description', 'description', 'highlights',
            'duration_days', 'duration_nights',
            'group_size_min', 'group_size_max',
            'price_per_person', 'currency', 'discount_percentage',
            'availability_status', 'start_date', 'end_date',
            'max_bookings',
            'included_items', 'excluded_items', 'requirements',
            'cancellation_policy', 'terms_and_conditions',
            'featured_image', 'video_url',
            'is_customizable',
            'is_active', 'is_featured', 'order',
            'meta_title', 'meta_description', 'meta_keywords',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 7-Day Serengeti Safari Adventure'
            }),
            'destinations': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '5'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'difficulty_level': forms.Select(attrs={'class': 'form-select'}),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Brief summary for listings (max 300 characters)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Detailed package description...'
            }),
            'highlights': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Key highlights (one per line)\n- Wildlife viewing in Serengeti\n- Hot air balloon ride\n- Luxury lodge accommodation'
            }),
            'duration_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 7',
                'min': '1'
            }),
            'duration_nights': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 6',
                'min': '0'
            }),
            'group_size_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2',
                'min': '1'
            }),
            'group_size_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 12',
                'min': '1'
            }),
            'price_per_person': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2500.00',
                'step': '0.01',
                'min': '0.01'
            }),
            'currency': forms.Select(attrs={'class': 'form-select'}),
            'discount_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 10 (for 10% discount)',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'availability_status': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'max_bookings': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 10',
                'min': '0'
            }),
            'included_items': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'What\'s included (one per line):\n- Accommodation\n- Meals\n- Park fees\n- Professional guide'
            }),
            'excluded_items': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'What\'s NOT included (one per line):\n- International flights\n- Travel insurance\n- Personal expenses'
            }),
            'requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Requirements (one per line):\n- Valid passport\n- Travel insurance\n- Moderate fitness level'
            }),
            'cancellation_policy': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'terms_and_conditions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Terms and conditions...'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.youtube.com/watch?v=...'
            }),
            'is_customizable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0 (lower numbers appear first)'
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO page title (auto-generated if empty)'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'SEO meta description (150-160 characters)'
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'safari, serengeti, tour, wildlife (comma-separated)'
            }),
        }
        labels = {
            'name': 'Package Name',
            'destinations': 'Destinations',
            'category': 'Category',
            'difficulty_level': 'Difficulty Level',
            'short_description': 'Short Description',
            'description': 'Full Description',
            'highlights': 'Highlights',
            'duration_days': 'Duration (Days)',
            'duration_nights': 'Duration (Nights)',
            'group_size_min': 'Minimum Group Size',
            'group_size_max': 'Maximum Group Size',
            'price_per_person': 'Price per Person',
            'currency': 'Currency',
            'discount_percentage': 'Discount (%)',
            'availability_status': 'Availability',
            'start_date': 'Start Date (Seasonal)',
            'end_date': 'End Date (Seasonal)',
            'max_bookings': 'Maximum Bookings',
            'included_items': 'What\'s Included',
            'excluded_items': 'What\'s NOT Included',
            'requirements': 'Requirements',
            'cancellation_policy': 'Cancellation Policy',
            'terms_and_conditions': 'Terms & Conditions',
            'featured_image': 'Featured Image',
            'video_url': 'Video URL',
            'is_customizable': 'Customizable',
            'is_active': 'Active',
            'is_featured': 'Featured',
            'order': 'Display Order',
            'meta_title': 'SEO Title',
            'meta_description': 'SEO Description',
            'meta_keywords': 'SEO Keywords',
        }
        help_texts = {
            'name': 'Unique package name (e.g., "7-Day Serengeti Safari Adventure")',
            'destinations': 'Hold Ctrl/Cmd to select multiple destinations',
            'short_description': 'Brief summary (max 300 characters) for listings',
            'description': 'Detailed package description',
            'highlights': 'Key highlights - one per line or comma-separated',
            'duration_nights': 'Auto-calculated if empty (days - 1)',
            'discount_percentage': 'Discount percentage (0-100)',
            'start_date': 'Leave empty for year-round packages',
            'end_date': 'Leave empty for year-round packages',
            'max_bookings': '0 = unlimited bookings',
            'is_customizable': 'Can customers request custom modifications?',
            'is_active': 'Published and visible to public',
            'is_featured': 'Display as featured package on homepage',
            'order': 'Display order (lower numbers appear first)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make certain fields optional
        self.fields['destinations'].required = False
        self.fields['highlights'].required = False
        self.fields['start_date'].required = False
        self.fields['end_date'].required = False
        self.fields['included_items'].required = False
        self.fields['excluded_items'].required = False
        self.fields['requirements'].required = False
        self.fields['terms_and_conditions'].required = False
        self.fields['featured_image'].required = False
        self.fields['video_url'].required = False
        self.fields['meta_title'].required = False
        self.fields['meta_description'].required = False
        self.fields['meta_keywords'].required = False

    def clean(self):
        cleaned_data = super().clean()
        
        # Validate group sizes
        group_size_min = cleaned_data.get('group_size_min')
        group_size_max = cleaned_data.get('group_size_max')
        if group_size_min and group_size_max and group_size_min > group_size_max:
            raise ValidationError('Minimum group size cannot be greater than maximum group size.')
        
        # Validate dates
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise ValidationError('Start date cannot be after end date.')
        
        # Validate duration
        duration_days = cleaned_data.get('duration_days')
        duration_nights = cleaned_data.get('duration_nights')
        if duration_days and duration_nights and duration_nights >= duration_days:
            raise ValidationError('Number of nights should be less than number of days.')
        
        # Validate discount
        discount = cleaned_data.get('discount_percentage')
        if discount and (discount < 0 or discount > 100):
            raise ValidationError('Discount must be between 0 and 100.')
        
        return cleaned_data


class PackageImageForm(forms.ModelForm):
    """Form for adding images to package gallery"""
    
    class Meta:
        model = PackageImage
        fields = ['image', 'caption', 'order', 'is_active']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional image caption'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'image': 'Image',
            'caption': 'Caption',
            'order': 'Display Order',
            'is_active': 'Active',
        }


class PackageItineraryForm(forms.ModelForm):
    """Form for creating day-by-day itinerary"""
    
    class Meta:
        model = PackageItinerary
        fields = [
            'day_number', 'end_day_number', 'title', 'description',
            'activities', 'accommodation',
            'breakfast_included', 'lunch_included', 'dinner_included',
            'highlights', 'notes',
            'order', 'is_active'
        ]
        widgets = {
            'day_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 1',
                'min': '1'
            }),
            'end_day_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Leave blank for single day',
                'min': '1'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Days 3-7: Safari in Serengeti'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Detailed activities for this day...'
            }),
            'activities': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '5'
            }),
            'accommodation': forms.Select(attrs={'class': 'form-select'}),
            'breakfast_included': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lunch_included': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dinner_included': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'highlights': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Game drive, Sunset viewing'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Optional notes (e.g., Early morning departure)'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'day_number': 'Start Day',
            'end_day_number': 'End Day (Optional)',
            'title': 'Title',
            'description': 'Description',
            'activities': 'Activities',
            'accommodation': 'Accommodation',
            'breakfast_included': 'Breakfast',
            'lunch_included': 'Lunch',
            'dinner_included': 'Dinner',
            'highlights': 'Highlights',
            'notes': 'Notes',
            'order': 'Display Order',
            'is_active': 'Active',
        }
        help_texts = {
            'day_number': 'Starting day number (1, 2, 3, etc.)',
            'end_day_number': 'For day ranges (e.g., Days 3-7), enter end day. Leave blank for single day.',
            'activities': 'Hold Ctrl/Cmd to select multiple activities',
            'accommodation': 'Where guests stay during this period',
            'highlights': 'Key highlights for this day/period',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make certain fields optional
        self.fields['end_day_number'].required = False
        self.fields['activities'].required = False
        self.fields['accommodation'].required = False
        self.fields['highlights'].required = False
        self.fields['notes'].required = False
        self.fields['order'].required = False
        self.fields['is_active'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        day_number = cleaned_data.get('day_number')
        end_day_number = cleaned_data.get('end_day_number')
        
        # Validate end_day_number if provided
        if end_day_number:
            if day_number and end_day_number < day_number:
                raise ValidationError({
                    'end_day_number': 'End day must be greater than or equal to start day.'
                })
            if end_day_number == day_number:
                # If they're the same, just clear end_day_number (single day)
                cleaned_data['end_day_number'] = None
        
        return cleaned_data


class PackageInclusionForm(forms.ModelForm):
    """Form for managing package inclusions/exclusions"""
    
    class Meta:
        model = PackageInclusion
        fields = [
            'inclusion_type', 'item_name', 'description', 'quantity',
            'is_included', 'order', 'is_active'
        ]
        widgets = {
            'inclusion_type': forms.Select(attrs={'class': 'form-select'}),
            'item_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 4-star hotel accommodation'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Optional detailed description'
            }),
            'quantity': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 3 nights, 2 meals per day'
            }),
            'is_included': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'inclusion_type': 'Type',
            'item_name': 'Item Name',
            'description': 'Description',
            'quantity': 'Quantity',
            'is_included': 'Included (uncheck for exclusions)',
            'order': 'Display Order',
            'is_active': 'Active',
        }
        help_texts = {
            'item_name': 'Name of the included/excluded item',
            'quantity': 'Optional quantity (e.g., "3 nights", "2 meals per day")',
            'is_included': 'Check if included, uncheck if excluded',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make certain fields optional
        self.fields['description'].required = False
        self.fields['quantity'].required = False


# ============================================================================
# BOOKING INQUIRY & CUSTOM PACKAGE FORMS (Phase 2A)
# ============================================================================

class BookingInquiryForm(forms.ModelForm):
    """
    Public form for customers to submit package inquiries.
    This is the initial step before receiving a custom quote.
    """
    
    class Meta:
        model = BookingInquiry
        fields = [
            'base_package', 'customer_name', 'customer_email', 'customer_phone',
            'country', 'source',
            'preferred_travel_date', 'flexible_dates', 'alternative_date_1', 'alternative_date_2',
            'number_of_adults', 'number_of_children', 'number_of_infants',
            'budget_range', 'specific_budget',
            'accommodation_preference',
            'dietary_requirements', 'special_requests',
            'prefer_email', 'prefer_phone', 'prefer_whatsapp',
        ]
        widgets = {
            'base_package': forms.Select(attrs={
                'class': 'form-select',
                'readonly': 'readonly'
            }),
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com'
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1 (555) 123-4567'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your country of residence'
            }),
            'source': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'How did you hear about us?'),
                ('google', 'Google Search'),
                ('social', 'Social Media'),
                ('friend', 'Friend/Family Referral'),
                ('agent', 'Travel Agent'),
                ('repeat', 'Previous Customer'),
                ('other', 'Other'),
            ]),
            'preferred_travel_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': 'today'
            }),
            'flexible_dates': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'alternative_date_1': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'alternative_date_2': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'number_of_adults': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '2'
            }),
            'number_of_children': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0'
            }),
            'number_of_infants': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0'
            }),
            'budget_range': forms.Select(attrs={'class': 'form-select'}),
            'specific_budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount per person',
                'step': '0.01'
            }),
            'accommodation_preference': forms.Select(attrs={'class': 'form-select'}),
            'dietary_requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Any dietary restrictions? (Vegetarian, Vegan, Halal, Allergies, etc.)'
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about any special interests, preferences, or requirements...'
            }),
            'prefer_email': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'prefer_phone': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'prefer_whatsapp': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'base_package': 'Package Interested In',
            'customer_name': 'Full Name *',
            'customer_email': 'Email Address *',
            'customer_phone': 'Phone Number *',
            'country': 'Country',
            'source': 'How did you find us?',
            'preferred_travel_date': 'Preferred Travel Date',
            'flexible_dates': 'My dates are flexible (±3 days)',
            'alternative_date_1': 'Alternative Date 1',
            'alternative_date_2': 'Alternative Date 2',
            'number_of_adults': 'Number of Adults (18+)',
            'number_of_children': 'Number of Children (3-17)',
            'number_of_infants': 'Number of Infants (0-2)',
            'budget_range': 'Budget per Person (USD)',
            'specific_budget': 'Specific Budget Amount',
            'accommodation_preference': 'Accommodation Preference',
            'dietary_requirements': 'Dietary Requirements',
            'special_requests': 'Special Interests & Requests',
            'prefer_email': 'Email',
            'prefer_phone': 'Phone Call',
            'prefer_whatsapp': 'WhatsApp',
        }
    
    def __init__(self, *args, **kwargs):
        # Extract package if provided
        package = kwargs.pop('package', None)
        super().__init__(*args, **kwargs)
        
        # Set package if provided (from detail page)
        if package:
            self.fields['base_package'].initial = package
            self.fields['base_package'].widget.attrs['readonly'] = True
        
        # Make some fields optional
        self.fields['country'].required = False
        self.fields['source'].required = False
        self.fields['alternative_date_1'].required = False
        self.fields['alternative_date_2'].required = False
        self.fields['specific_budget'].required = False
        self.fields['dietary_requirements'].required = False
        self.fields['special_requests'].required = False
        
        # Set default checked for email preference
        self.fields['prefer_email'].initial = True
    
    def clean(self):
        cleaned_data = super().clean()
        budget_range = cleaned_data.get('budget_range')
        specific_budget = cleaned_data.get('specific_budget')
        
        # Validate specific budget if range is 'specific'
        if budget_range == 'specific' and not specific_budget:
            self.add_error('specific_budget', 'Please enter your specific budget amount.')
        
        # Ensure at least one contact preference is selected
        prefer_email = cleaned_data.get('prefer_email')
        prefer_phone = cleaned_data.get('prefer_phone')
        prefer_whatsapp = cleaned_data.get('prefer_whatsapp')
        
        if not (prefer_email or prefer_phone or prefer_whatsapp):
            raise ValidationError('Please select at least one preferred contact method.')
        
        return cleaned_data


class InquiryManagementForm(forms.ModelForm):
    """
    Staff form for managing booking inquiries.
    Used in the dashboard to update status, assign staff, and add notes.
    """
    
    class Meta:
        model = BookingInquiry
        fields = [
            'status', 'priority', 'staff_assigned', 'staff_notes'
        ]
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'staff_assigned': forms.Select(attrs={'class': 'form-select'}),
            'staff_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Internal notes (not visible to client)...'
            }),
        }
        labels = {
            'status': 'Inquiry Status',
            'priority': 'Priority Level',
            'staff_assigned': 'Assign to Staff',
            'staff_notes': 'Internal Notes',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter staff users (only active staff members)
        self.fields['staff_assigned'].queryset = User.objects.filter(
            is_staff=True,
            is_active=True
        )
        self.fields['staff_assigned'].required = False
        self.fields['staff_notes'].required = False


class CustomPackageForm(forms.ModelForm):
    """
    Staff form for creating and editing custom packages.
    Used in the custom package builder.
    """
    
    # Explicitly define currency as ChoiceField to ensure choices work
    currency = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        initial='USD'
    )
    
    class Meta:
        model = CustomPackage
        fields = [
            'inquiry', 'base_package', 'name', 'short_description', 'description',
            'duration_days', 'duration_nights',
            'original_price', 'adjusted_price', 'currency',
            'modifications_made', 'staff_notes_to_client', 'staff_internal_notes',
            'status', 'expires_at', 'featured_image'
        ]
        widgets = {
            'inquiry': forms.Select(attrs={
                'class': 'form-select',
                'readonly': 'readonly'
            }),
            'base_package': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '7-Day Serengeti Safari - Custom for John Doe'
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Brief summary of customizations...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Full package description...'
            }),
            'duration_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'duration_nights': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'original_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'readonly': 'readonly'
            }),
            'adjusted_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'modifications_made': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'List of modifications:\n- Changed Day 3 accommodation\n- Added photography guide\n- Adjusted pricing for budget'
            }),
            'staff_notes_to_client': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Personal message to client (they will see this)...'
            }),
            'staff_internal_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Internal notes (client will NOT see this)...'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'expires_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'inquiry': 'For Inquiry',
            'base_package': 'Base Package Template',
            'name': 'Custom Package Name',
            'short_description': 'Short Description',
            'description': 'Full Description',
            'duration_days': 'Duration (Days)',
            'duration_nights': 'Duration (Nights)',
            'original_price': 'Original Price (per person)',
            'adjusted_price': 'Custom Price (per person)',
            'currency': 'Currency',
            'modifications_made': 'Modifications Summary',
            'staff_notes_to_client': 'Message to Client (Visible)',
            'staff_internal_notes': 'Internal Notes (Hidden)',
            'status': 'Status',
            'expires_at': 'Quote Expires At',
            'featured_image': 'Custom Package Image',
        }
    
    def __init__(self, *args, **kwargs):
        inquiry = kwargs.pop('inquiry', None)
        super().__init__(*args, **kwargs)
        
        # Set currency choices (same as Package model) - MUST be done first
        from .models import Package
        self.fields['currency'].choices = Package.CURRENCY_CHOICES
        
        # Set inquiry if provided
        if inquiry:
            self.fields['inquiry'].initial = inquiry
            self.fields['inquiry'].widget.attrs['readonly'] = True
            
            # Pre-populate currency from base package if available
            if inquiry.base_package:
                self.fields['currency'].initial = inquiry.base_package.currency
            else:
                # Set default currency if no base package
                self.fields['currency'].initial = 'USD'
        else:
            # Set default currency if no inquiry
            self.fields['currency'].initial = 'USD'
        
        # Make some fields optional
        self.fields['modifications_made'].required = False
        self.fields['staff_notes_to_client'].required = False
        self.fields['staff_internal_notes'].required = False
        self.fields['expires_at'].required = False
        self.fields['featured_image'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        duration_days = cleaned_data.get('duration_days')
        duration_nights = cleaned_data.get('duration_nights')
        
        # Validate duration
        if duration_days and duration_nights and duration_nights > duration_days:
            self.add_error('duration_nights', 'Nights cannot exceed days.')
        
        return cleaned_data


class InquiryMessageForm(forms.ModelForm):
    """
    Form for sending messages related to inquiries.
    Used for communication between staff and clients.
    """
    
    class Meta:
        model = InquiryMessage
        fields = ['subject', 'message', 'attachment', 'is_internal']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Message subject (optional)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Type your message here...'
            }),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
            'is_internal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'subject': 'Subject',
            'message': 'Message',
            'attachment': 'Attach File',
            'is_internal': 'Internal Note (Staff Only)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make optional fields
        self.fields['subject'].required = False
        self.fields['attachment'].required = False
        self.fields['is_internal'].initial = False


class InquiryFilterForm(forms.Form):
    """
    Filter form for inquiry list in staff dashboard.
    """
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + list(BookingInquiry.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    priority = forms.ChoiceField(
        choices=[('', 'All Priorities')] + list(BookingInquiry.PRIORITY_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    staff_assigned = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True, is_active=True),
        required=False,
        empty_label='All Staff',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    package = forms.ModelChoiceField(
        queryset=Package.objects.filter(is_active=True).order_by('name'),
        required=False,
        empty_label='All Packages',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, email, phone, reference...'
        })
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='From Date'
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='To Date'
    )


class CustomPackageItineraryForm(forms.ModelForm):
    """
    Form for adding/editing custom package itinerary days.
    """
    
    class Meta:
        model = CustomPackageItinerary
        fields = [
            'day_number', 'end_day_number', 'title', 'description',
            'location', 'accommodation_name', 'accommodation_type',
            'activities', 'breakfast_included', 'lunch_included', 'dinner_included',
            'transport_details', 'distance', 'drive_time',
            'featured_image', 'order', 'is_active'
        ]
        widgets = {
            'day_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': '1'
            }),
            'end_day_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Leave empty for single day'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Arrival in Nairobi & Transfer to Hotel'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Detailed description of the day\'s activities...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Nairobi, Kenya'
            }),
            'accommodation_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Serena Hotel'
            }),
            'accommodation_type': forms.Select(attrs={'class': 'form-select'}),
            'activities': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Activities for this day'
            }),
            'breakfast_included': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lunch_included': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dinner_included': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'transport_details': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Private 4x4 Safari Vehicle'
            }),
            'distance': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 120km'
            }),
            'drive_time': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2-3 hours'
            }),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make order and end_day_number not required
        self.fields['order'].required = False
        self.fields['end_day_number'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        day_number = cleaned_data.get('day_number')
        end_day_number = cleaned_data.get('end_day_number')
        
        # Validate end_day_number
        if end_day_number and day_number:
            if end_day_number < day_number:
                raise ValidationError({
                    'end_day_number': 'End day must be equal to or greater than start day.'
                })

        return cleaned_data


# ============================================================================
# BOOKING SYSTEM FORMS
# ============================================================================

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'package', 'inquiry', 'custom_package',
            'departure_date', 'return_date',
            'num_adults', 'num_children',
            'quoted_price', 'deposit_amount', 'currency',
            'status', 'staff_assigned',
            'special_requirements', 'internal_notes',
        ]
        widgets = {
            'departure_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'return_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'special_requirements': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'internal_notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault('class', 'form-control')
        self.fields['inquiry'].queryset = BookingInquiry.objects.filter(
            status__in=['approved', 'converted']
        )
        self.fields['inquiry'].required = False
        self.fields['custom_package'].required = False
        self.fields['return_date'].required = False
        self.fields['staff_assigned'].required = False


class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = [
            'first_name', 'last_name', 'passport_number', 'nationality',
            'date_of_birth', 'dietary_requirements', 'medical_notes',
            'emergency_contact_name', 'emergency_contact_phone', 'is_lead_passenger',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'medical_notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, (forms.Textarea, forms.CheckboxInput)):
                field.widget.attrs.setdefault('class', 'form-control')


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'payment_type', 'amount', 'currency', 'payment_method',
            'status', 'reference_number', 'received_at', 'notes',
        ]
        widgets = {
            'received_at': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault('class', 'form-control')
        self.fields['received_at'].required = False


class DepartureForm(forms.ModelForm):
    class Meta:
        model = Departure
        fields = ['departure_date', 'max_seats', 'status', 'notes']
        widgets = {
            'departure_date': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date',
            }),
            'max_seats': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_departure_date(self):
        from django.utils import timezone
        date = self.cleaned_data['departure_date']
        if not self.instance.pk and date < timezone.now().date():
            raise ValidationError("Departure date cannot be in the past.")
        return date

