from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Specimen, SpecimenType, SpecimenEvent
from .forms import SpecimenForm

@login_required
def specimen_list(request):
    query = request.GET.get('q', '')
    specimens = Specimen.objects.filter(is_active=True, is_deleted=False)
    
    if query:
        specimens = specimens.filter(
            Q(specimen_id__icontains=query) |
            Q(barcode__icontains=query) |
            Q(participant__first_name__icontains=query) |
            Q(participant__last_name__icontains=query)
        )
    
    paginator = Paginator(specimens, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'specimens/specimen_list.html', context)

@login_required
def specimen_create(request):
    if request.method == 'POST':
        form = SpecimenForm(request.POST)
        if form.is_valid():
            specimen = form.save(commit=False)
            specimen.created_by = request.user
            
            if not specimen.specimen_id:
                import uuid
                specimen.specimen_id = f"SP-{uuid.uuid4().hex[:8].upper()}"
            
            if not specimen.collected_by:
                specimen.collected_by = request.user
            
            if specimen.freeze_thaw_cycles is None:
                specimen.freeze_thaw_cycles = 0
            
            if not specimen.status:
                specimen.status = 'COLLECTED'
            
            if not specimen.quality:
                specimen.quality = 'UNKNOWN'
            
            if specimen.is_primary:
                specimen.lineage_depth = 0
            else:
                if specimen.parent_specimen:
                    specimen.lineage_depth = specimen.parent_specimen.lineage_depth + 1
            
            specimen.save()
            messages.success(request, f'تم إضافة العينة {specimen.specimen_id} بنجاح!')
            return redirect('specimen_detail', pk=specimen.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SpecimenForm()
    
    context = {
        'form': form,
    }
    return render(request, 'specimens/specimen_form.html', context)

@login_required
def specimen_detail(request, pk):
    specimen = get_object_or_404(Specimen, pk=pk, is_active=True)
    context = {
        'specimen': specimen,
        'lineage': specimen.lineage,
    }
    return render(request, 'specimens/specimen_detail.html', context)

@login_required
def specimen_edit(request, pk):
    specimen = get_object_or_404(Specimen, pk=pk, is_active=True)
    
    if request.method == 'POST':
        form = SpecimenForm(request.POST, instance=specimen)
        if form.is_valid():
            form.save()
            messages.success(request, f'تم تحديث العينة {specimen.specimen_id} بنجاح!')
            return redirect('specimen_detail', pk=specimen.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SpecimenForm(instance=specimen)
    
    context = {
        'form': form,
        'specimen': specimen,
    }
    return render(request, 'specimens/specimen_form.html', context)

@login_required
def specimen_delete(request, pk):
    specimen = get_object_or_404(Specimen, pk=pk, is_active=True)
    
    if request.method == 'POST':
        specimen.is_active = False
        specimen.is_deleted = True
        specimen.save()
        messages.success(request, f'تم حذف العينة {specimen.specimen_id} بنجاح!')
        return redirect('specimen_list')
    
    context = {'specimen': specimen}
    return render(request, 'specimens/specimen_confirm_delete.html', context)