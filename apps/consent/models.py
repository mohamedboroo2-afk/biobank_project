from django.db import models
from django.contrib.auth import get_user_model
from apps.participants.models import Participant
from apps.studies.models import Study

User = get_user_model()

class Consent(models.Model):
    CONSENT_STATUS = [
        ('DRAFT', 'Draft'),
        ('PENDING', 'Pending Signature'),
        ('SIGNED', 'Signed'),
        ('WITHDRAWN', 'Withdrawn'),
        ('EXPIRED', 'Expired'),
        ('REVOKED', 'Revoked'),
    ]
    
    consent_id = models.CharField(max_length=50, unique=True, db_index=True)
    participant = models.ForeignKey(Participant, on_delete=models.PROTECT, related_name='consents')
    study = models.ForeignKey(Study, on_delete=models.PROTECT, related_name='consents')
    
    # Consent details
    consent_version = models.CharField(max_length=20)
    consent_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    
    # Signature
    is_signed = models.BooleanField(default=False)
    signature_date = models.DateTimeField(blank=True, null=True)
    signature_method = models.CharField(max_length=50, choices=[
        ('WET', 'Wet Signature'),
        ('ELECTRONIC', 'Electronic Signature'),
        ('VERBAL', 'Verbal Consent'),
        ('OTHER', 'Other'),
    ], blank=True, null=True)
    signed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='signed_consents')
    
    # Witness
    witness_name = models.CharField(max_length=200, blank=True, null=True)
    witness_signature = models.CharField(max_length=200, blank=True, null=True)
    
    # Consent options
    consent_options = models.JSONField(default=dict, blank=True)
    
    # Withdrawal
    withdrawal_date = models.DateField(blank=True, null=True)
    withdrawal_reason = models.TextField(blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=CONSENT_STATUS, default='DRAFT')
    notes = models.TextField(blank=True, null=True)
    
    # Documents
    consent_form = models.FileField(upload_to='consents/forms/', blank=True, null=True)
    signed_form = models.FileField(upload_to='consents/signed/', blank=True, null=True)
    
    # Audit
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_consents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'consents'
        ordering = ['-consent_date']
        indexes = [
            models.Index(fields=['consent_id']),
            models.Index(fields=['participant', 'study']),
            models.Index(fields=['status']),
        ]
        unique_together = ['participant', 'study', 'consent_version']
    
    def __str__(self):
        return f"{self.consent_id} - {self.participant.participant_id} - {self.study.study_id}"