"""
Core App - Forms

Customer-facing forms for:
- Contact submissions (LEADS!)
- Newsletter subscriptions (EMAIL LIST!)
"""
from django import forms
from django.core.validators import validate_email
from .models import ContactMessage, NewsletterSubscriber, FAQ, SiteSettings, Testimonial
from .utils import normalize_whatsapp_number


class ContactForm(forms.ModelForm):
    """
    Contact form for potential customers.
    
    CRITICAL: This is your lead generation tool!
    Every submission is a potential booking.
    """
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1 (555) 123-4567',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What can we help you with?',
                'required': True,
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us more about your travel plans...',
                'rows': 6,
                'required': True,
            }),
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number (Optional)',
            'subject': 'Subject',
            'message': 'Your Message',
        }
        help_texts = {
            'phone': 'Optional - We\'ll call you if needed',
            'message': 'Share your travel dates, group size, interests, etc.',
        }
    
    def clean_email(self):
        """Validate email format"""
        email = self.cleaned_data.get('email', '').lower().strip()
        validate_email(email)
        return email
    
    def clean_name(self):
        """Validate name"""
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError('Please enter your full name.')
        return name
    
    def clean_message(self):
        """Validate message length"""
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 10:
            raise forms.ValidationError('Please provide more details (at least 10 characters).')
        if len(message) > 2000:
            raise forms.ValidationError('Message is too long (maximum 2000 characters).')
        return message


class NewsletterSubscriptionForm(forms.ModelForm):
    """
    Newsletter subscription form.
    
    MARKETING GOLD: Build your email list for promotions!
    """
    
    # Add honeypot field to prevent spam bots
    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label='Leave this field empty'
    )
    
    # Add consent checkbox (GDPR compliance)
    consent = forms.BooleanField(
        required=True,
        label='I agree to receive promotional emails and travel updates',
        error_messages={
            'required': 'You must agree to receive emails to subscribe.'
        }
    )
    
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
                'required': True,
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name (Optional)',
            }),
        }
        labels = {
            'email': 'Email Address',
            'name': 'Name',
        }
    
    def clean_email(self):
        """Validate email and check for duplicates"""
        email = self.cleaned_data.get('email', '').lower().strip()
        validate_email(email)
        
        # Check if already subscribed
        existing = NewsletterSubscriber.objects.filter(email=email).first()
        if existing:
            if existing.is_active:
                raise forms.ValidationError(
                    'This email is already subscribed to our newsletter.'
                )
            else:
                # Reactivate if previously unsubscribed
                existing.is_active = True
                existing.unsubscribed_at = None
                existing.save()
                raise forms.ValidationError(
                    'Welcome back! Your subscription has been reactivated.'
                )
        
        return email
    
    def clean_honeypot(self):
        """Check honeypot field to prevent spam"""
        honeypot = self.cleaned_data.get('honeypot')
        if honeypot:
            # Bot filled the honeypot field - reject silently
            raise forms.ValidationError('Spam detected.')
        return honeypot


class ContactMessageReplyForm(forms.Form):
    """
    Form for admin to reply to contact messages.
    Used in the dashboard.
    """
    reply_message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'placeholder': 'Type your reply here...',
        }),
        label='Your Reply',
        help_text='This will be sent via email to the customer.',
    )
    
    mark_as_replied = forms.BooleanField(
        required=False,
        initial=True,
        label='Mark this message as replied',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )
    
    def clean_reply_message(self):
        """Validate reply message"""
        message = self.cleaned_data.get('reply_message', '').strip()
        if len(message) < 10:
            raise forms.ValidationError('Reply message is too short.')
        return message


class ContactMessageNotesForm(forms.ModelForm):
    """
    Form for admin to add internal notes to contact messages.
    """
    
    class Meta:
        model = ContactMessage
        fields = ['admin_notes', 'status']
        widgets = {
            'admin_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Internal notes (not visible to customer)...',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'admin_notes': 'Internal Notes',
            'status': 'Status',
        }


class FAQForm(forms.ModelForm):
    """
    Form for creating and editing FAQs in the dashboard.
    """
    
    class Meta:
        model = FAQ
        fields = ['category', 'question', 'answer', 'is_active', 'is_featured', 'order']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'question': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the question...',
            }),
            'answer': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Enter the detailed answer...',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
        }
        labels = {
            'category': 'Category',
            'question': 'Question',
            'answer': 'Answer',
            'is_active': 'Published (visible to public)',
            'is_featured': 'Featured (show at top)',
            'order': 'Display Order',
        }
        help_texts = {
            'order': 'Lower numbers appear first (0 = first)',
            'is_featured': 'Featured FAQs appear at the top of the list',
        }
    
    def clean_question(self):
        """Validate question"""
        question = self.cleaned_data.get('question', '').strip()
        if len(question) < 10:
            raise forms.ValidationError('Question must be at least 10 characters long.')
        return question
    
    def clean_answer(self):
        """Validate answer"""
        answer = self.cleaned_data.get('answer', '').strip()
        if len(answer) < 20:
            raise forms.ValidationError('Answer must be at least 20 characters long.')
        return answer


class TestimonialForm(forms.ModelForm):
    """
    Form for creating and editing testimonials in the dashboard.
    """
    
    class Meta:
        model = Testimonial
        fields = [
            'customer_name', 'customer_location', 'customer_image',
            'quote', 'rating', 'is_active', 'is_featured', 'order'
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Customer full name',
            }),
            'customer_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., New York, USA',
            }),
            'customer_image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'quote': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Customer testimonial...',
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
        }
        labels = {
            'customer_name': 'Customer Name',
            'customer_location': 'Location',
            'customer_image': 'Customer Photo (Optional)',
            'quote': 'Testimonial',
            'rating': 'Rating',
            'is_active': 'Published (visible to public)',
            'is_featured': 'Featured (show on homepage)',
            'order': 'Display Order',
        }
        help_texts = {
            'order': 'Lower numbers appear first (0 = first)',
            'is_featured': 'Featured testimonials appear on the homepage',
            'customer_image': 'Upload a photo of the customer (optional)',
        }
    
    def clean_customer_name(self):
        """Validate customer name"""
        name = self.cleaned_data.get('customer_name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError('Customer name must be at least 2 characters.')
        return name
    
    def clean_quote(self):
        """Validate testimonial quote"""
        quote = self.cleaned_data.get('quote', '').strip()
        if len(quote) < 20:
            raise forms.ValidationError('Testimonial must be at least 20 characters long.')
        if len(quote) > 500:
            raise forms.ValidationError('Testimonial is too long (maximum 500 characters).')
        return quote



class SiteSettingsForm(forms.ModelForm):
    """
    Form for the dashboard Site Settings page (singleton).
    """

    class Meta:
        model = SiteSettings
        fields = [
            'whatsapp_number',
            'bank_name', 'bank_account_name', 'bank_account_number', 'bank_swift',
            'mpesa_name', 'mpesa_number', 'invoice_footer_note',
        ]
        widgets = {
            'whatsapp_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+255 744 000 000',
            }),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CRDB Bank'}),
            'bank_account_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account holder name'}),
            'bank_account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account number'}),
            'bank_swift': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CORUTZTZ'}),
            'mpesa_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Registered name'}),
            'mpesa_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 0744 000 000 or Lipa number'}),
            'invoice_footer_note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Terms, thank-you note, etc.'}),
        }
        labels = {
            'whatsapp_number': 'WhatsApp Number',
            'bank_name': 'Bank Name',
            'bank_account_name': 'Account Name',
            'bank_account_number': 'Account Number',
            'bank_swift': 'SWIFT / BIC',
            'mpesa_name': 'M-Pesa Name',
            'mpesa_number': 'M-Pesa Number',
            'invoice_footer_note': 'Invoice Footer Note',
        }
        help_texts = {
            'whatsapp_number': (
                'International format preferred (e.g. +255744000000). '
                'Powers all "Chat on WhatsApp" buttons on the public site and dashboard. '
                'Leave empty to hide them.'
            ),
            'invoice_footer_note': 'Printed at the bottom of every invoice PDF.',
        }

    def clean_whatsapp_number(self):
        """Accept any format a human types, but reject undialable numbers."""
        raw = self.cleaned_data.get('whatsapp_number', '').strip()
        if raw and not normalize_whatsapp_number(raw):
            raise forms.ValidationError(
                'Enter a valid phone number, e.g. +255744123456 or 0744123456.'
            )
        return raw
