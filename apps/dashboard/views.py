from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.participants.models import Participant
from apps.specimens.models import Specimen
from apps.studies.models import Study
from apps.shipments.models import Shipment

@login_required
def dashboard(request):
    context = {
        'total_participants': Participant.objects.filter(is_active=True).count(),
        'total_specimens': Specimen.objects.filter(is_active=True).count(),
        'total_studies': Study.objects.filter(is_active=True).count(),
        'total_shipments': Shipment.objects.filter(is_active=True).count(),
    }
    return render(request, 'dashboard/dashboard.html', context)