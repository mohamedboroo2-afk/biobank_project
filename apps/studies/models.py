from django.db import models
from django.contrib.auth import get_user_model
from apps.participants.models import Participant

User = get_user_model()

class Study(models.Model):
    STUDY_STATUS = [
        ('DRAFT', 'Draft'),
        ('ACTIVE', 'Active'),
        ('CLOSED', 'Closed'),
        ('ARCHIVED', 'Archived'),
    ]
    
    STUDY_TYPE = [
        ('CROSS_SECTIONAL', 'Cross-sectional'),
        ('LONGITUDINAL', 'Longitudinal'),
        ('CASE_CONTROL', 'Case-control'),
        ('COHORT', 'Cohort'),
        ('OTHER', 'Other'),
    ]
    
    study_id = models.CharField(max_length=50, unique=True, db_index=True)
    title = models.CharField(max_length=200)
    short_title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    study_type = models.CharField(max_length=20, choices=STUDY_TYPE, default='CROSS_SECTIONAL')
    status = models.CharField(max_length=20, choices=STUDY_STATUS, default='DRAFT')
    
    principal_investigator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='led_studies')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    
    ethical_approval_number = models.CharField(max_length=100, blank=True, null=True)
    ethical_approval_date = models.DateField(blank=True, null=True)
    ethical_approval_body = models.CharField(max_length=200, blank=True, null=True)
    
    funding_source = models.CharField(max_length=200, blank=True, null=True)
    funding_grant_number = models.CharField(max_length=100, blank=True, null=True)
    
    metadata = models.JSONField(default=dict, blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_studies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'studies'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['study_id']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.study_id} - {self.title}"

class CollectionProtocol(models.Model):
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='protocols')
    protocol_id = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    specimen_type = models.CharField(max_length=50)
    collection_tube_type = models.CharField(max_length=100, blank=True, null=True)
    required_quantity = models.FloatField()
    quantity_unit = models.CharField(max_length=20, choices=[
        ('ml', 'mL'),
        ('µl', 'µL'),
        ('mg', 'mg'),
        ('µg', 'µg'),
    ])
    required_volume = models.FloatField(blank=True, null=True)
    
    processing_instructions = models.TextField(blank=True, null=True)
    storage_conditions = models.CharField(max_length=100, blank=True, null=True)
    storage_temperature = models.FloatField(blank=True, null=True, help_text="Temperature in °C")
    
    collection_time_window = models.IntegerField(blank=True, null=True, help_text="Time window in minutes")
    processing_time_window = models.IntegerField(blank=True, null=True, help_text="Time window in minutes")
    
    quality_requirements = models.TextField(blank=True, null=True)
    acceptance_criteria = models.TextField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'collection_protocols'
        indexes = [
            models.Index(fields=['protocol_id']),
        ]
    
    def __str__(self):
        return f"{self.protocol_id} - {self.name}"

class StudyParticipant(models.Model):
    ENROLLMENT_STATUS = [
        ('ENROLLED', 'Enrolled'),
        ('WITHDRAWN', 'Withdrawn'),
        ('COMPLETED', 'Completed'),
        ('LOST_TO_FOLLOWUP', 'Lost to follow-up'),
        ('DECEASED', 'Deceased'),
    ]
    
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='participants')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='studies')
    enrollment_date = models.DateField()
    enrollment_status = models.CharField(max_length=20, choices=ENROLLMENT_STATUS, default='ENROLLED')
    withdrawal_date = models.DateField(blank=True, null=True)
    withdrawal_reason = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'study_participants'
        unique_together = ['study', 'participant']
        indexes = [
            models.Index(fields=['study', 'enrollment_status']),
        ]
    
    def __str__(self):
        return f"{self.study.study_id} - {self.participant.participant_id}"