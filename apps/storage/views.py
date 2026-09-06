from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Facility
from .forms import FacilityForm

@login_required
def storage_list(request):
    facilities = Facility.objects.filter(is_active=True)
    context = {'facilities': facilities}
    return render(request, 'storage/storage_list.html', context)

@login_required
def facility_create(request):
    if request.method == 'POST':
        form = FacilityForm(request.POST)
        if form.is_valid():
            facility = form.save()
            messages.success(request, f'تم إضافة المرفق {facility.name} بنجاح!')
            return redirect('storage_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = FacilityForm()
    
    context = {'form': form}
    return render(request, 'storage/facility_form.html', context)

@login_required
def facility_edit(request, pk):
    facility = get_object_or_404(Facility, pk=pk, is_active=True)
    
    if request.method == 'POST':
        form = FacilityForm(request.POST, instance=facility)
        if form.is_valid():
            form.save()
            messages.success(request, f'تم تحديث المرفق {facility.name} بنجاح!')
            return redirect('storage_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = FacilityForm(instance=facility)
    
    context = {
        'form': form,
        'facility': facility,
    }
    return render(request, 'storage/facility_form.html', context)

@login_required
def facility_delete(request, pk):
    facility = get_object_or_404(Facility, pk=pk, is_active=True)
    
    if request.method == 'POST':
        facility.is_active = False
        facility.save()
        messages.success(request, f'تم حذف المرفق {facility.name} بنجاح!')
        return redirect('storage_list')
    
    context = {'facility': facility}
    return render(request, 'storage/facility_confirm_delete.html', context)