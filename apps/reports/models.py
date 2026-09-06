from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Report(models.Model):
    REPORT_TYPES = [
        ('SPECIMEN', 'Specimen Report'),
        ('PARTICIPANT', 'Participant Report'),
        ('STUDY', 'Study Report'),
        ('SHIPMENT', 'Shipment Report'),
        ('CONSENT', 'Consent Report'),
        ('STORAGE', 'Storage Report'),
        ('CUSTOM', 'Custom Report'),
    ]
    
    FORMAT_CHOICES = [
        ('PDF', 'PDF'),
        ('CSV', 'CSV'),
        ('EXCEL', 'Excel'),
        ('HTML', 'HTML'),
        ('JSON', 'JSON'),
    ]
    
    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    description = models.TextField(blank=True, null=True)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='PDF')
    
    # Query parameters
    parameters = models.JSONField(default=dict, blank=True)
    filters = models.JSONField(default=dict, blank=True)
    
    # Schedule
    is_scheduled = models.BooleanField(default=False)
    schedule_frequency = models.CharField(max_length=50, choices=[
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
    ], blank=True, null=True)
    schedule_time = models.TimeField(blank=True, null=True)
    last_run = models.DateTimeField(blank=True, null=True)
    next_run = models.DateTimeField(blank=True, null=True)
    
    # Recipients
    recipients = models.JSONField(default=list, blank=True)
    
    # Output
    output_file = models.FileField(upload_to='reports/', blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('DRAFT', 'Draft'),
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ], default='DRAFT')
    error_message = models.TextField(blank=True, null=True)
    
    # Audit
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_reports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'reports'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['report_type']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.get_report_type_display()}"