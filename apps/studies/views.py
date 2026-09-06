from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Study
from .forms import StudyForm

@login_required
def study_list(request):
    query = request.GET.get('q', '')
    studies = Study.objects.filter(is_active=True).order_by('-created_at')
    
    if query:
        studies = studies.filter(
            Q(study_id__icontains=query) |
            Q(title__icontains=query) |
            Q(short_title__icontains=query)
        )
    
    paginator = Paginator(studies, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'studies': studies,
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'studies/study_list.html', context)

@login_required
def study_create(request):
    if request.method == 'POST':
        form = StudyForm(request.POST)
        if form.is_valid():
            study = form.save(commit=False)
            study.created_by = request.user
            study.save()
            messages.success(request, f'تم إضافة الدراسة {study.title} بنجاح!')
            return redirect('study_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = StudyForm()
    
    context = {'form': form}
    return render(request, 'studies/study_form.html', context)

@login_required
def study_edit(request, pk):
    study = get_object_or_404(Study, pk=pk, is_active=True)
    
    if request.method == 'POST':
        form = StudyForm(request.POST, instance=study)
        if form.is_valid():
            form.save()
            messages.success(request, f'تم تحديث الدراسة {study.title} بنجاح!')
            return redirect('study_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = StudyForm(instance=study)
    
    context = {
        'form': form,
        'study': study,
    }
    return render(request, 'studies/study_form.html', context)

@login_required
def study_delete(request, pk):
    study = get_object_or_404(Study, pk=pk, is_active=True)
    
    if request.method == 'POST':
        study.is_active = False
        study.save()
        messages.success(request, f'تم حذف الدراسة {study.title} بنجاح!')
        return redirect('study_list')
    
    context = {'study': study}
    return render(request, 'studies/study_confirm_delete.html', context)