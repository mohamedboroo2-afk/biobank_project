from django.contrib import admin
from .models import Specimen, SpecimenType, SpecimenEvent

@admin.register(SpecimenType)
class SpecimenTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category')
    search_fields = ('code', 'name')
    list_filter = ('category',)

@admin.register(Specimen)
class SpecimenAdmin(admin.ModelAdmin):
    list_display = ('specimen_id', 'barcode', 'specimen_type', 'participant', 'status', 'quality', 'collection_date')
    list_filter = ('status', 'quality', 'specimen_type', 'is_primary')
    search_fields = ('specimen_id', 'barcode', 'participant__participant_id', 'participant__first_name', 'participant__last_name')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('participant', 'visit', 'study', 'parent_specimen', 'storage_location')
    fieldsets = (
        ('Identification', {
            'fields': ('specimen_id', 'barcode')
        }),
        ('Type & Classification', {
            'fields': ('specimen_type', 'is_primary', 'parent_specimen', 'lineage_depth')
        }),
        ('Relationships', {
            'fields': ('participant', 'visit', 'study', 'collection_protocol')
        }),
        ('Collection Details', {
            'fields': ('collection_date', 'collection_notes', 'collected_by', 'collection_container')
        }),
        ('Specimen Properties', {
            'fields': ('quantity', 'quantity_unit', 'concentration', 'concentration_unit')
        }),
        ('Processing', {
            'fields': ('processing_date', 'processed_by', 'processing_method')
        }),
        ('Quality & Status', {
            'fields': ('quality', 'quality_notes', 'status', 'status_notes')
        }),
        ('Storage', {
            'fields': ('storage_location', 'storage_date', 'freeze_thaw_cycles')
        }),
        ('Additional Data', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Audit', {
            'fields': ('created_by', 'created_at', 'updated_at', 'is_active'),
            'classes': ('collapse',)
        }),
    )

@admin.register(SpecimenEvent)
class SpecimenEventAdmin(admin.ModelAdmin):
    list_display = ('specimen', 'event_type', 'event_date', 'performed_by')
    list_filter = ('event_type',)
    search_fields = ('specimen__specimen_id', 'notes')
    readonly_fields = ('created_at',)