from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Shipment, ShipmentSpecimen
from .forms import ShipmentForm, ShipmentSpecimenForm

@login_required
def shipment_list(request):
    query = request.GET.get('q', '')
    shipments = Shipment.objects.filter(is_active=True).order_by('-created_at')
    
    if query:
        shipments = shipments.filter(
            Q(shipment_id__icontains=query) |
            Q(tracking_number__icontains=query) |
            Q(sender_institution__icontains=query) |
            Q(receiver_institution__icontains=query)
        )
    
    paginator = Paginator(shipments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'shipments/shipment_list.html', context)

@login_required
def shipment_create(request):
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            shipment = form.save(commit=False)
            shipment.created_by = request.user
            shipment.save()
            messages.success(request, f'تم إضافة الشحنة {shipment.shipment_id} بنجاح!')
            return redirect('shipment_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ShipmentForm()
    
    context = {
        'form': form,
    }
    return render(request, 'shipments/shipment_form.html', context)

@login_required
def shipment_detail(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk, is_active=True)
    specimens = shipment.specimens.all()
    
    context = {
        'shipment': shipment,
        'specimens': specimens,
    }
    return render(request, 'shipments/shipment_detail.html', context)

@login_required
def shipment_edit(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk, is_active=True)
    
    if request.method == 'POST':
        form = ShipmentForm(request.POST, instance=shipment)
        if form.is_valid():
            form.save()
            messages.success(request, f'تم تحديث الشحنة {shipment.shipment_id} بنجاح!')
            return redirect('shipment_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ShipmentForm(instance=shipment)
    
    context = {
        'form': form,
        'shipment': shipment,
    }
    return render(request, 'shipments/shipment_form.html', context)

@login_required
def shipment_delete(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk, is_active=True)
    
    if request.method == 'POST':
        shipment.is_active = False
        shipment.save()
        messages.success(request, f'تم حذف الشحنة {shipment.shipment_id} بنجاح!')
        return redirect('shipment_list')
    
    context = {'shipment': shipment}
    return render(request, 'shipments/shipment_confirm_delete.html', context)