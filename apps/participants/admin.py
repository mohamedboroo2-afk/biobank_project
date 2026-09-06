from django.contrib import admin
from .models import Participant, ParticipantVisit

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('participant_id', 'full_name', 'gender', 'age', 'vital_status', 'created_at')
    list_filter = ('gender', 'vital_status', 'is_active')
    search_fields = ('participant_id', 'first_name', 'last_name', 'national_id')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Identification', {
            'fields': ('participant_id', 'national_id', 'medical_record_number')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'gender', 'marital_status')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address', 'city', 'country')
        }),
        ('Clinical Information', {
            'fields': ('diagnosis', 'clinical_notes', 'vital_status', 'date_of_death')
        }),
        ('Additional Data', {
            'fields': ('demographic_data', 'medical_history'),
            'classes': ('collapse',)
        }),
        ('Audit', {
            'fields': ('created_by', 'created_at', 'updated_at', 'is_active'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ParticipantVisit)
class ParticipantVisitAdmin(admin.ModelAdmin):
    list_display = ('visit_id', 'participant', 'visit_date', 'visit_type', 'visit_number')
    list_filter = ('visit_type',)
    search_fields = ('visit_id', 'participant__participant_id')