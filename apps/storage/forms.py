from django import forms
from .models import Facility, Room, Freezer, Rack, Box, StorageLocation

class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['code', 'name', 'address', 'contact_person', 'contact_phone', 'is_active']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }