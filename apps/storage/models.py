from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Facility(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True, null=True)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Room(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.facility.code} - {self.code}"

class Freezer(models.Model):
    FREEZER_TYPE = [
        ('ULTRA_LOW', 'Ultra Low (-80°C)'),
        ('LOW', 'Low (-20°C)'),
        ('REFRIGERATOR', 'Refrigerator (4°C)'),
        ('AMBIENT', 'Ambient'),
        ('LIQUID_NITROGEN', 'Liquid Nitrogen'),
    ]
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='freezers')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    freezer_type = models.CharField(max_length=20, choices=FREEZER_TYPE, default='ULTRA_LOW')
    temperature = models.FloatField(help_text="Temperature in °C")
    capacity = models.IntegerField(help_text="Maximum number of racks/boxes")
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    installation_date = models.DateField(blank=True, null=True)
    last_maintenance = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code} - {self.temperature}°C"

class Rack(models.Model):
    freezer = models.ForeignKey(Freezer, on_delete=models.CASCADE, related_name='racks')
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20, unique=True)
    rows = models.IntegerField(default=5)
    columns = models.IntegerField(default=5)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.freezer.code} - Rack {self.code}"

class Box(models.Model):
    BOX_TYPE = [
        ('STANDARD', 'Standard'),
        ('CRYO', 'Cryo Box'),
        ('PAPER', 'Paper Box'),
        ('PLASTIC', 'Plastic Box'),
        ('CUSTOM', 'Custom'),
    ]
    
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE, related_name='boxes')
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20, unique=True)
    box_type = models.CharField(max_length=20, choices=BOX_TYPE, default='STANDARD')
    rows = models.IntegerField(default=8)
    columns = models.IntegerField(default=12)
    is_full = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.rack.code} - Box {self.code}"

class StorageLocation(models.Model):
    box = models.ForeignKey(Box, on_delete=models.CASCADE, related_name='positions')
    row = models.IntegerField()
    column = models.IntegerField()
    is_occupied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['box', 'row', 'column']
        indexes = [
            models.Index(fields=['box', 'is_occupied']),
        ]
    
    def __str__(self):
        return f"{self.box.code} - Row {self.row}, Col {self.column}"
    
    def get_full_path(self):
        return f"{self.box.rack.freezer.room.facility.code} > {self.box.rack.freezer.room.code} > {self.box.rack.freezer.code} > {self.box.rack.code} > {self.box.code} > {self.row}-{self.column}"