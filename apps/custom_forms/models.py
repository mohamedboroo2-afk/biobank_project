from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()

class CustomForm(models.Model):
    FORM_TYPES = [
        ('PARTICIPANT', 'Participant Form'),
        ('SPECIMEN', 'Specimen Form'),
        ('STUDY', 'Study Form'),
        ('VISIT', 'Visit Form'),
        ('OTHER', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    form_type = models.CharField(max_length=20, choices=FORM_TYPES)
    description = models.TextField(blank=True, null=True)
    
    # Form structure
    fields = models.JSONField(default=list, blank=True)
    layout = models.JSONField(default=dict, blank=True)
    
    # Validation rules
    validation_rules = models.JSONField(default=dict, blank=True)
    
    # Versioning
    version = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)
    
    # Audit
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_custom_forms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'custom_forms'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['form_type']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class CustomFormData(models.Model):
    """Store data for custom forms"""
    form = models.ForeignKey(CustomForm, on_delete=models.CASCADE, related_name='form_data')
    object_id = models.CharField(max_length=100)  # ID of the related object
    data = models.JSONField(default=dict)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_form_data')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'custom_form_data'
        unique_together = ['form', 'object_id']
        indexes = [
            models.Index(fields=['form', 'object_id']),
        ]
    
    def __str__(self):
        return f"{self.form.code} - {self.object_id}"