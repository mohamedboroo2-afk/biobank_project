from django.db import models
from django.contrib.auth import get_user_model
from apps.participants.models import Participant, ParticipantVisit
from apps.studies.models import Study, CollectionProtocol
from apps.storage.models import StorageLocation

User = get_user_model()

class SpecimenType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=[
        ('BLOOD', 'Blood Products'),
        ('TISSUE', 'Tissue'),
        ('FLUID', 'Body Fluids'),
        ('MOLECULAR', 'Molecular'),
        ('OTHER', 'Other'),
    ])
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Specimen(models.Model):
    STATUS_CHOICES = [
        ('COLLECTED', 'Collected'),
        ('RECEIVED', 'Received'),
        ('PROCESSING', 'Processing'),
        ('PROCESSED', 'Processed'),
        ('STORED', 'Stored'),
        ('SHIPPED', 'Shipped'),
        ('DISTRIBUTED', 'Distributed'),
        ('DISPOSED', 'Disposed'),
        ('DESTROYED', 'Destroyed'),
        ('LOST', 'Lost'),
        ('QUARANTINED', 'Quarantined'),
    ]
    
    QUALITY_CHOICES = [
        ('EXCELLENT', 'Excellent'),
        ('GOOD', 'Good'),
        ('FAIR', 'Fair'),
        ('POOR', 'Poor'),
        ('UNKNOWN', 'Unknown'),
    ]
    
    specimen_id = models.CharField(max_length=50, unique=True, db_index=True)
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True, db_index=True)
    
    specimen_type = models.ForeignKey(SpecimenType, on_delete=models.PROTECT)
    participant = models.ForeignKey(Participant, on_delete=models.PROTECT, related_name='specimens')
    visit = models.ForeignKey(ParticipantVisit, on_delete=models.SET_NULL, null=True, blank=True, related_name='specimens')
    study = models.ForeignKey(Study, on_delete=models.PROTECT, null=True, blank=True, related_name='specimens')
    collection_protocol = models.ForeignKey(CollectionProtocol, on_delete=models.SET_NULL, null=True, blank=True)
    
    parent_specimen = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='derived_specimens')
    is_primary = models.BooleanField(default=True)
    lineage_depth = models.IntegerField(default=0)
    
    collection_date = models.DateTimeField()
    collection_notes = models.TextField(blank=True, null=True)
    collected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='collected_specimens')
    collection_container = models.CharField(max_length=100, blank=True, null=True)
    
    quantity = models.FloatField()
    quantity_unit = models.CharField(max_length=20, choices=[
        ('ml', 'mL'),
        ('µl', 'µL'),
        ('mg', 'mg'),
        ('µg', 'µg'),
        ('g', 'g'),
        ('ng', 'ng'),
    ])
    concentration = models.FloatField(blank=True, null=True)
    concentration_unit = models.CharField(max_length=20, choices=[
        ('ng_ul', 'ng/µL'),
        ('ug_ul', 'µg/µL'),
        ('mg_ml', 'mg/mL'),
        ('ng_ml', 'ng/mL'),
    ], blank=True, null=True)
    
    processing_date = models.DateTimeField(blank=True, null=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_specimens')
    processing_method = models.CharField(max_length=200, blank=True, null=True)
    
    quality = models.CharField(max_length=20, choices=QUALITY_CHOICES, default='UNKNOWN')
    quality_notes = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='COLLECTED')
    status_notes = models.TextField(blank=True, null=True)
    
    storage_location = models.ForeignKey(StorageLocation, on_delete=models.SET_NULL, null=True, blank=True, related_name='specimens')
    storage_date = models.DateTimeField(blank=True, null=True)
    
    freeze_thaw_cycles = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_specimens')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'specimens'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['specimen_id']),
            models.Index(fields=['barcode']),
            models.Index(fields=['participant', 'specimen_type']),
            models.Index(fields=['status']),
            models.Index(fields=['collection_date']),
            models.Index(fields=['parent_specimen']),
        ]
    
    def __str__(self):
        return f"{self.specimen_id} - {self.specimen_type.name}"
    
    @property
    def lineage(self):
        lineage = []
        current = self
        while current:
            lineage.append(current)
            current = current.parent_specimen
        return list(reversed(lineage))
    
    @property
    def full_location(self):
        if self.storage_location:
            return self.storage_location.get_full_path()
        return None

class SpecimenEvent(models.Model):
    EVENT_TYPES = [
        ('COLLECTION', 'Collection'),
        ('RECEIVED', 'Received'),
        ('PROCESSING_STARTED', 'Processing Started'),
        ('PROCESSING_COMPLETED', 'Processing Completed'),
        ('STORED', 'Stored'),
        ('MOVED', 'Moved'),
        ('SHIPPED', 'Shipped'),
        ('RECEIVED_SHIPMENT', 'Received Shipment'),
        ('DISTRIBUTED', 'Distributed'),
        ('QUALITY_CHECK', 'Quality Check'),
        ('DISPOSED', 'Disposed'),
        ('DESTROYED', 'Destroyed'),
        ('LOST', 'Lost'),
        ('QUARANTINED', 'Quarantined'),
        ('RELEASED', 'Released from Quarantine'),
        ('OTHER', 'Other'),
    ]
    
    specimen = models.ForeignKey(Specimen, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    event_date = models.DateTimeField()
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='specimen_events')
    notes = models.TextField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'specimen_events'
        ordering = ['-event_date']
        indexes = [
            models.Index(fields=['specimen', 'event_type']),
            models.Index(fields=['event_date']),
        ]
    
    def __str__(self):
        return f"{self.specimen.specimen_id} - {self.get_event_type_display()}"

def save(self, *args, **kwargs):
    # توليد specimen_id تلقائياً إذا لم يتم توفيره
    if not self.specimen_id:
        import uuid
        self.specimen_id = f"SP-{uuid.uuid4().hex[:8].upper()}"
    super().save(*args, **kwargs)