from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

User = get_user_model()

class Participant(models.Model):
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
        ('PREFER_NOT_SAY', 'Prefer not to say'),
    ]
    
    MARITAL_STATUS = [
        ('SINGLE', 'Single'),
        ('MARRIED', 'Married'),
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed'),
    ]
    
    participant_id = models.CharField(max_length=50, unique=True, db_index=True)
    national_id = models.CharField(max_length=20, blank=True, null=True)
    medical_record_number = models.CharField(max_length=50, blank=True, null=True)
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS, blank=True, null=True)
    
    # Contact Information
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    # Clinical Information
    diagnosis = models.TextField(blank=True, null=True)
    clinical_notes = models.TextField(blank=True, null=True)
    vital_status = models.CharField(max_length=20, choices=[
        ('ALIVE', 'Alive'),
        ('DECEASED', 'Deceased'),
        ('UNKNOWN', 'Unknown'),
    ], default='UNKNOWN')
    date_of_death = models.DateField(blank=True, null=True)
    
    # Additional Data
    demographic_data = models.JSONField(default=dict, blank=True)
    medical_history = models.JSONField(default=dict, blank=True)
    
    # Audit Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_participants')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'participants'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['participant_id']),
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.participant_id} - {self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    
    @property
    def specimen_count(self):
        return self.specimens.filter(is_active=True).count()

class ParticipantVisit(models.Model):
    VISIT_TYPES = [
        ('SCREENING', 'Screening'),
        ('BASELINE', 'Baseline'),
        ('FOLLOW_UP', 'Follow-up'),
        ('SURGERY', 'Surgery'),
        ('TREATMENT', 'Treatment'),
        ('OTHER', 'Other'),
    ]
    
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='visits')
    visit_id = models.CharField(max_length=50, unique=True, db_index=True)
    visit_date = models.DateTimeField()
    visit_type = models.CharField(max_length=20, choices=VISIT_TYPES)
    visit_number = models.IntegerField()
    clinical_notes = models.TextField(blank=True, null=True)
    
    # Vital Signs
    height = models.FloatField(blank=True, null=True, help_text="Height in cm")
    weight = models.FloatField(blank=True, null=True, help_text="Weight in kg")
    blood_pressure_systolic = models.IntegerField(blank=True, null=True)
    blood_pressure_diastolic = models.IntegerField(blank=True, null=True)
    heart_rate = models.IntegerField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    
    # Additional Data
    metadata = models.JSONField(default=dict, blank=True)
    
    # Audit Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'participant_visits'
        ordering = ['participant', 'visit_date']
        unique_together = ['participant', 'visit_number']
        indexes = [
            models.Index(fields=['participant', 'visit_date']),
        ]
    
    def __str__(self):
        return f"{self.participant.participant_id} - Visit {self.visit_number}"