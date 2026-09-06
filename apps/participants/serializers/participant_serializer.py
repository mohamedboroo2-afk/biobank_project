from rest_framework import serializers
from apps.participants.models import Participant, ParticipantVisit

class ParticipantSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    specimen_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Participant
        fields = [
            'id', 'participant_id', 'national_id', 'medical_record_number',
            'first_name', 'last_name', 'full_name', 'date_of_birth', 'age',
            'gender', 'marital_status', 'phone', 'email', 'address', 'city', 'country',
            'diagnosis', 'clinical_notes', 'vital_status', 'date_of_death',
            'demographic_data', 'medical_history', 'specimen_count',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ParticipantVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantVisit
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']