from django.contrib import admin
from .models import Study, CollectionProtocol, StudyParticipant

@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ('study_id', 'title', 'status', 'study_type', 'start_date', 'principal_investigator')
    list_filter = ('status', 'study_type')
    search_fields = ('study_id', 'title')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Study Information', {
            'fields': ('study_id', 'title', 'short_title', 'description', 'study_type', 'status')
        }),
        ('Investigators', {
            'fields': ('principal_investigator',)
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Ethical Approval', {
            'fields': ('ethical_approval_number', 'ethical_approval_date', 'ethical_approval_body')
        }),
        ('Funding', {
            'fields': ('funding_source', 'funding_grant_number')
        }),
        ('Audit', {
            'fields': ('created_by', 'created_at', 'updated_at', 'is_active'),
            'classes': ('collapse',)
        }),
    )

@admin.register(CollectionProtocol)
class CollectionProtocolAdmin(admin.ModelAdmin):
    list_display = ('protocol_id', 'name', 'study', 'specimen_type', 'required_quantity', 'is_active')
    list_filter = ('specimen_type', 'is_active')
    search_fields = ('protocol_id', 'name')

@admin.register(StudyParticipant)
class StudyParticipantAdmin(admin.ModelAdmin):
    list_display = ('study', 'participant', 'enrollment_date', 'enrollment_status')
    list_filter = ('enrollment_status',)
    search_fields = ('study__study_id', 'participant__participant_id')