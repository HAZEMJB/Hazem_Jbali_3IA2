from django import forms
from .models import Conference

class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['name', 'theme', 'location', 'start_date', 'end_date', 'description']


        labels = {
            'name': 'Nom de la conférence',
            'theme': 'Thème principal',
            'lieu': 'Lieu',
            'start_date': 'Date de début',
            'end_date': 'Date de fin',
            'description': 'Description',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex : AI for Good'
            }),
            'theme': forms.Select(attrs={
                'class': 'form-select'
            }),
            'lieu': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex : Paris, France'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ajoutez une description détaillée...',
                'rows': 3
            }),
        }
