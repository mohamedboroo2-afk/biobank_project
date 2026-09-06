from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import AuditLog

@login_required
def audit_log_list(request):
    query = request.GET.get('q', '')
    action_type = request.GET.get('action_type', '')
    
    logs = AuditLog.objects.all().order_by('-timestamp')
    
    if query:
        logs = logs.filter(
            Q(user__email__icontains=query) |
            Q(model_name__icontains=query) |
            Q(object_repr__icontains=query)
        )
    
    if action_type:
        logs = logs.filter(action=action_type)
    
    paginator = Paginator(logs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'action_type': action_type,
        'action_choices': AuditLog._meta.get_field('action').choices,
    }
    return render(request, 'audit/audit_log_list.html', context)