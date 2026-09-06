from django import forms
from .models import Study, CollectionProtocol, StudyParticipant

class StudyForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = [
            'study_id', 'title', 'short_title', 'description',
            'study_type', 'status', 'principal_investigator',
            'start_date', 'end_date',
            'ethical_approval_number', 'ethical_approval_date', 'ethical_approval_body',
            'funding_source', 'funding_grant_number'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'ethical_approval_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'study_id': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'short_title': forms.TextInput(attrs={'class': 'form-control'}),
            'study_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'principal_investigator': forms.Select(attrs={'class': 'form-select'}),
            'ethical_approval_number': forms.TextInput(attrs={'class': 'form-control'}),
            'ethical_approval_body': forms.TextInput(attrs={'class': 'form-control'}),
            'funding_source': forms.TextInput(attrs={'class': 'form-control'}),
            'funding_grant_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # جعل الحقول الأساسية إجبارية
        self.fields['study_id'].required = True
        self.fields['title'].required = True
        self.fields['short_title'].required = True
        self.fields['study_type'].required = True
        self.fields['status'].required = True
        self.fields['start_date'].required = True