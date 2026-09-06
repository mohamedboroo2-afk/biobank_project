from django import forms
from .models import Participant, ParticipantVisit

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = [
            'participant_id', 'national_id', 'medical_record_number',
            'first_name', 'last_name', 'date_of_birth', 'gender', 'marital_status',
            'phone', 'email', 'address', 'city', 'country',
            'diagnosis', 'clinical_notes', 'vital_status'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'clinical_notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'diagnosis': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'participant_id': forms.TextInput(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control'}),
            'medical_record_number': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'vital_status': forms.Select(attrs={'class': 'form-select'}),
        }

class ParticipantVisitForm(forms.ModelForm):
    class Meta:
        model = ParticipantVisit
        fields = [
            'participant', 'visit_id', 'visit_date', 'visit_type', 'visit_number',
            'clinical_notes', 'height', 'weight',
            'blood_pressure_systolic', 'blood_pressure_diastolic',
            'heart_rate', 'temperature'
        ]
        widgets = {
            'visit_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'clinical_notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'participant': forms.Select(attrs={'class': 'form-select'}),
            'visit_type': forms.Select(attrs={'class': 'form-select'}),
            'visit_id': forms.TextInput(attrs={'class': 'form-control'}),
            'visit_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'blood_pressure_systolic': forms.NumberInput(attrs={'class': 'form-control'}),
            'blood_pressure_diastolic': forms.NumberInput(attrs={'class': 'form-control'}),
            'heart_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }