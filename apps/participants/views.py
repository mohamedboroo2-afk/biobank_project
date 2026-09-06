from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Participant, ParticipantVisit
from .forms import ParticipantForm

@login_required
def participant_list(request):
    query = request.GET.get('q', '')
    participants = Participant.objects.filter(is_active=True, is_deleted=False)
    
    if query:
        participants = participants.filter(
            Q(participant_id__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(national_id__icontains=query)
        )
    
    paginator = Paginator(participants, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'participants/participant_list.html', context)

@login_required
def participant_detail(request, pk):
    participant = get_object_or_404(Participant, pk=pk, is_active=True)
    specimens = participant.specimens.filter(is_active=True)[:10]
    visits = participant.visits.all()[:10]
    
    context = {
        'participant': participant,
        'specimens': specimens,
        'visits': visits,
    }
    return render(request, 'participants/participant_detail.html', context)

@login_required
def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.created_by = request.user
            participant.save()
            messages.success(request, f'تم إضافة المشارك {participant.full_name} بنجاح!')
            return redirect('participant_detail', pk=participant.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ParticipantForm()
    
    context = {'form': form}
    return render(request, 'participants/participant_form.html', context)

@login_required
def participant_edit(request, pk):
    participant = get_object_or_404(Participant, pk=pk, is_active=True)
    
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, f'تم تحديث بيانات المشارك {participant.full_name} بنجاح!')
            return redirect('participant_detail', pk=participant.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ParticipantForm(instance=participant)
    
    context = {'form': form, 'participant': participant}
    return render(request, 'participants/participant_form.html', context)

@login_required
def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk, is_active=True)
    
    if request.method == 'POST':
        participant.is_active = False
        participant.is_deleted = True
        participant.save()
        messages.success(request, f'تم حذف المشارك {participant.full_name} بنجاح!')
        return redirect('participant_list')
    
    context = {'participant': participant}
    return render(request, 'participants/participant_confirm_delete.html', context)

@login_required
def export_participants_excel(request):
    import openpyxl
    from django.http import HttpResponse
    from openpyxl.styles import Font, Alignment
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "المشاركون"
    
    headers = ['المعرف', 'الاسم الأول', 'الاسم الأخير', 'الجنس', 'تاريخ الميلاد', 'العمر', 'رقم الهاتف', 'البريد الإلكتروني', 'الحالة']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')
    
    participants = Participant.objects.filter(is_active=True, is_deleted=False)
    for row, participant in enumerate(participants, 2):
        ws.cell(row=row, column=1, value=participant.participant_id)
        ws.cell(row=row, column=2, value=participant.first_name)
        ws.cell(row=row, column=3, value=participant.last_name)
        ws.cell(row=row, column=4, value=participant.get_gender_display())
        ws.cell(row=row, column=5, value=participant.date_of_birth.strftime('%Y-%m-%d'))
        ws.cell(row=row, column=6, value=participant.age)
        ws.cell(row=row, column=7, value=participant.phone or '')
        ws.cell(row=row, column=8, value=participant.email or '')
        ws.cell(row=row, column=9, value=participant.get_vital_status_display())
    
    for col in range(1, 10):
        ws.column_dimensions[chr(64 + col)].width = 20
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=participants.xlsx'
    wb.save(response)
    return response