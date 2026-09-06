from django.db import models
from django.contrib.auth import get_user_model
from apps.specimens.models import Specimen

User = get_user_model()

class Shipment(models.Model):
    STATUS_CHOICES = [
        ('PREPARING', 'Preparing'),
        ('READY', 'Ready for Shipment'),
        ('SHIPPED', 'Shipped'),
        ('IN_TRANSIT', 'In Transit'),
        ('DELIVERED', 'Delivered'),
        ('RECEIVED', 'Received'),
        ('CANCELLED', 'Cancelled'),
        ('LOST', 'Lost'),
        ('DAMAGED', 'Damaged'),
    ]
    
    shipment_id = models.CharField(max_length=50, unique=True, db_index=True)
    tracking_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    # Sender and receiver
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sent_shipments')
    sender_institution = models.CharField(max_length=200)
    sender_address = models.TextField()
    
    receiver = models.CharField(max_length=200)
    receiver_institution = models.CharField(max_length=200)
    receiver_address = models.TextField()
    receiver_contact = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=20)
    receiver_email = models.EmailField()
    
    # Shipment details
    shipment_date = models.DateTimeField()
    expected_delivery_date = models.DateTimeField()
    actual_delivery_date = models.DateTimeField(blank=True, null=True)
    
    shipping_method = models.CharField(max_length=100, choices=[
        ('COURIER', 'Courier'),
        ('AIR', 'Air Freight'),
        ('GROUND', 'Ground'),
        ('INTERNATIONAL', 'International'),
        ('OTHER', 'Other'),
    ])
    
    temperature_requirements = models.CharField(max_length=50, choices=[
        ('AMBIENT', 'Ambient'),
        ('REFRIGERATED', 'Refrigerated (4°C)'),
        ('FROZEN', 'Frozen (-20°C)'),
        ('ULTRA_FROZEN', 'Ultra Frozen (-80°C)'),
        ('DRY_ICE', 'Dry Ice'),
        ('LIQUID_NITROGEN', 'Liquid Nitrogen'),
    ])
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PREPARING')
    notes = models.TextField(blank=True, null=True)
    
    # Documents
    waybill_number = models.CharField(max_length=100, blank=True, null=True)
    customs_declaration = models.FileField(upload_to='shipments/customs/', blank=True, null=True)
    
    # Tracking
    tracking_url = models.URLField(blank=True, null=True)
    tracking_updates = models.JSONField(default=list, blank=True)
    
    # Audit
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_shipments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'shipments'
        ordering = ['-shipment_date']
        indexes = [
            models.Index(fields=['shipment_id']),
            models.Index(fields=['tracking_number']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.shipment_id} - {self.sender_institution} to {self.receiver_institution}"

class ShipmentSpecimen(models.Model):
    """Link specimens to shipments"""
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='specimens')
    specimen = models.ForeignKey(Specimen, on_delete=models.PROTECT, related_name='shipments')
    quantity = models.FloatField()
    notes = models.TextField(blank=True, null=True)
    received_status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('RECEIVED', 'Received'),
        ('DAMAGED', 'Damaged'),
        ('LOST', 'Lost'),
        ('REJECTED', 'Rejected'),
    ], default='PENDING')
    received_notes = models.TextField(blank=True, null=True)
    received_date = models.DateTimeField(blank=True, null=True)
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_specimens')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'shipment_specimens'
        unique_together = ['shipment', 'specimen']
    
    def __str__(self):
        return f"{self.shipment.shipment_id} - {self.specimen.specimen_id}"