from django import forms

from destinations.models import Destination
from .models import BrochureParseJob, ItineraryGenerationJob, RouteOptimizationJob


class BrochureUploadForm(forms.ModelForm):
    class Meta:
        model = BrochureParseJob
        fields = ['pdf_file', 'target_accommodation']
        widgets = {
            'target_accommodation': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pdf_file'].widget.attrs['class'] = 'form-control'
        self.fields['pdf_file'].widget.attrs['accept'] = '.pdf'
        self.fields['target_accommodation'].required = False
        self.fields['target_accommodation'].help_text = (
            'Optional — link to an existing accommodation to apply results later.'
        )


class ItineraryGenerateForm(forms.ModelForm):
    class Meta:
        model = ItineraryGenerationJob
        fields = ['destination', 'duration_days', 'budget_usd', 'group_size', 'interests']
        widgets = {
            'destination': forms.Select(attrs={'class': 'form-select'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 30}),
            'budget_usd': forms.NumberInput(attrs={'class': 'form-control', 'min': 500}),
            'group_size': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 50}),
            'interests': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. wildlife safari, photography, culture, hiking',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['destination'].queryset = Destination.objects.all().order_by('name')
        self.fields['destination'].required = False


class RouteOptimizeForm(forms.ModelForm):
    class Meta:
        model = RouteOptimizationJob
        fields = ['destination_names']
        widgets = {
            'destination_names': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': (
                    'Serengeti National Park\nNgorongoro Crater\nLake Manyara\nTarangire National Park'
                ),
            }),
        }
        labels = {
            'destination_names': 'Destinations / Parks (one per line or comma-separated)',
        }
