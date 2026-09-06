from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from apps.participants.models import Participant
from apps.specimens.models import Specimen
from apps.studies.models import Study
from apps.shipments.models import Shipment

@login_required
def reports_dashboard(request):
    context = {
        'total_participants': Participant.objects.filter(is_active=True).count(),
        'total_specimens': Specimen.objects.filter(is_active=True).count(),
        'total_studies': Study.objects.filter(is_active=True).count(),
        'total_shipments': Shipment.objects.filter(is_active=True).count(),
        'specimens_by_type': Specimen.objects.values('specimen_type__name').annotate(count=Count('id')),
        'specimens_by_status': Specimen.objects.values('status').annotate(count=Count('id')),
        'participants_by_gender': Participant.objects.values('gender').annotate(count=Count('id')),
    }
    return render(request, 'reports/reports_dashboard.html', context)