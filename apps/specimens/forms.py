from django import forms
from .models import Specimen, SpecimenType
from apps.participants.models import Participant
from apps.studies.models import Study, CollectionProtocol

class SpecimenForm(forms.ModelForm):
    class Meta:
        model = Specimen
        fields = [
            'specimen_id', 'barcode',
            'specimen_type', 'participant', 'visit', 'study', 'collection_protocol',
            'parent_specimen', 'is_primary',
            'collection_date', 'collection_notes', 'collected_by', 'collection_container',
            'quantity', 'quantity_unit', 'concentration', 'concentration_unit',
            'processing_date', 'processing_method',
            'quality', 'quality_notes',
            'status', 'status_notes',
            'storage_location', 'storage_date',
            'freeze_thaw_cycles', 'metadata'
        ]
        widgets = {
            'collection_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'processing_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'storage_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'collection_notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'quality_notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'status_notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'metadata': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'JSON format'}),
            'specimen_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اتركه فارغاً للتوليد التلقائي'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'specimen_type': forms.Select(attrs={'class': 'form-select'}),
            'participant': forms.Select(attrs={'class': 'form-select'}),
            'visit': forms.Select(attrs={'class': 'form-select'}),
            'study': forms.Select(attrs={'class': 'form-select'}),
            'collection_protocol': forms.Select(attrs={'class': 'form-select'}),
            'parent_specimen': forms.Select(attrs={'class': 'form-select'}),
            'collected_by': forms.Select(attrs={'class': 'form-select'}),
            'collection_container': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quantity_unit': forms.Select(attrs={'class': 'form-select'}),
            'concentration': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'concentration_unit': forms.Select(attrs={'class': 'form-select'}),
            'processing_method': forms.TextInput(attrs={'class': 'form-control'}),
            'quality': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'storage_location': forms.Select(attrs={'class': 'form-select'}),
            'freeze_thaw_cycles': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # جعل specimen_id اختيارياً (سيتولد تلقائياً)
        self.fields['specimen_id'].required = False
        self.fields['specimen_id'].widget.attrs['placeholder'] = 'اتركه فارغاً للتوليد التلقائي'
        
        # جعل الحقول الأساسية إجبارية فقط
        self.fields['specimen_type'].required = True
        self.fields['participant'].required = True
        self.fields['collection_date'].required = True
        self.fields['quantity'].required = True
        self.fields['quantity_unit'].required = True
        
        # جعل الحقول الأخرى اختيارية
        self.fields['collected_by'].required = False
        self.fields['freeze_thaw_cycles'].required = False
        self.fields['barcode'].required = False
        self.fields['visit'].required = False
        self.fields['study'].required = False
        self.fields['collection_protocol'].required = False
        self.fields['parent_specimen'].required = False
        self.fields['concentration'].required = False
        self.fields['concentration_unit'].required = False
        self.fields['processing_date'].required = False
        self.fields['processing_method'].required = False
        self.fields['quality'].required = False
        self.fields['quality_notes'].required = False
        self.fields['status'].required = False
        self.fields['status_notes'].required = False
        self.fields['storage_location'].required = False
        self.fields['storage_date'].required = False
        self.fields['metadata'].required = False
        self.fields['collection_notes'].required = False
        self.fields['collection_container'].required = False
        
        # إضافة خيار "اختر" فارغ
        self.fields['specimen_type'].empty_label = "اختر نوع العينة"
        self.fields['participant'].empty_label = "اختر المشارك"
        self.fields['study'].empty_label = "اختر الدراسة (اختياري)"
        self.fields['collection_protocol'].empty_label = "اختر البروتوكول (اختياري)"
        self.fields['parent_specimen'].empty_label = "اختر العينة الأم (اختياري)"
        self.fields['storage_location'].empty_label = "اختر موقع التخزين (اختياري)"
        self.fields['collected_by'].empty_label = "اختر جامع العينة (اختياري)"
        self.fields['visit'].empty_label = "اختر الزيارة (اختياري)"
        
        # ترشيح المشاركين النشطين فقط
        self.fields['participant'].queryset = Participant.objects.filter(is_active=True)
        
        # ترشيح الدراسات النشطة
        self.fields['study'].queryset = Study.objects.filter(is_active=True)
        
        # ترشيح المستخدمين النشطين لـ collected_by
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.fields['collected_by'].queryset = User.objects.filter(is_active=True)