from django import forms
from django.contrib.auth import get_user_model
from .models import Shipment, ShipmentSpecimen

User = get_user_model()

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = [
            'shipment_id', 'tracking_number',
            'sender', 'sender_institution', 'sender_address',
            'receiver', 'receiver_institution', 'receiver_address',
            'receiver_contact', 'receiver_phone', 'receiver_email',
            'shipment_date', 'expected_delivery_date', 'actual_delivery_date',
            'shipping_method', 'temperature_requirements',
            'status', 'notes', 'waybill_number', 'tracking_url'
        ]
        widgets = {
            'shipment_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'expected_delivery_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'actual_delivery_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'shipment_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثال: SH-2024-001'}),
            'tracking_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم تتبع الشحنة'}),
            'sender': forms.Select(attrs={'class': 'form-select'}),
            'sender_institution': forms.TextInput(attrs={'class': 'form-control'}),
            'sender_address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'receiver': forms.TextInput(attrs={'class': 'form-control'}),
            'receiver_institution': forms.TextInput(attrs={'class': 'form-control'}),
            'receiver_address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'receiver_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'receiver_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'receiver_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'shipping_method': forms.Select(attrs={'class': 'form-select'}),
            'temperature_requirements': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'waybill_number': forms.TextInput(attrs={'class': 'form-control'}),
            'tracking_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # جعل الحقول الأساسية إجبارية
        self.fields['shipment_id'].required = True
        self.fields['sender'].required = True
        self.fields['sender_institution'].required = True
        self.fields['sender_address'].required = True
        self.fields['receiver'].required = True
        self.fields['receiver_institution'].required = True
        self.fields['receiver_address'].required = True
        self.fields['receiver_contact'].required = True
        self.fields['receiver_phone'].required = True
        self.fields['shipment_date'].required = True
        self.fields['shipping_method'].required = True
        self.fields['temperature_requirements'].required = True
        
        # ترشيح المستخدمين النشطين فقط للمرسل
        self.fields['sender'].queryset = User.objects.filter(is_active=True)
        self.fields['sender'].empty_label = "اختر المرسل"


class ShipmentSpecimenForm(forms.ModelForm):
    class Meta:
        model = ShipmentSpecimen
        fields = ['specimen', 'quantity', 'notes']
        widgets = {
            'specimen': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }