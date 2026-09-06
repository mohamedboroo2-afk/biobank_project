from rest_framework import serializers
from apps.specimens.models import Specimen, SpecimenType, SpecimenEvent

class SpecimenTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecimenType
        fields = '__all__'

class SpecimenSerializer(serializers.ModelSerializer):
    specimen_type_name = serializers.CharField(source='specimen_type.name', read_only=True)
    participant_name = serializers.CharField(source='participant.full_name', read_only=True)
    full_location = serializers.ReadOnlyField()
    
    class Meta:
        model = Specimen
        fields = [
            'id', 'specimen_id', 'barcode',
            'specimen_type', 'specimen_type_name',
            'participant', 'participant_name',
            'visit', 'study', 'collection_protocol',
            'parent_specimen', 'is_primary', 'lineage_depth',
            'collection_date', 'collection_notes', 'collected_by',
            'quantity', 'quantity_unit', 'concentration',
            'processing_date', 'processing_method',
            'quality', 'quality_notes',
            'status', 'status_notes',
            'storage_location', 'full_location', 'storage_date',
            'freeze_thaw_cycles', 'metadata',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['created_at', 'updated_at']

class SpecimenEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecimenEvent
        fields = '__all__'
        read_only_fields = ['created_at']