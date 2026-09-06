from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

def is_admin(user):
    return user.is_superuser or user.role == 'ADMIN'

@login_required
@user_passes_test(is_admin)
def user_list(request):
    query = request.GET.get('q', '')
    users = User.objects.all().order_by('-date_joined')
    
    if query:
        users = users.filter(
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'users/user_list.html', context)

@login_required
@user_passes_test(is_admin)
def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, f'تم إضافة المستخدم {user.email} بنجاح!')
            return redirect('user_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'users/user_form.html', context)

@login_required
@user_passes_test(is_admin)
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # تحذير فقط
    if user.pk == request.user.pk:
        messages.info(request, '⚠️ أنت تقوم بتعديل حسابك الخاص. تأكد من التغييرات.')
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            # إذا كان المستخدم يعدل حسابه الخاص، لا نغير is_active
            if user.pk == request.user.pk:
                # نمنع تعطيل الحساب الخاص
                if 'is_active' in form.cleaned_data and not form.cleaned_data['is_active']:
                    messages.error(request, 'لا يمكنك تعطيل حسابك الخاص!')
                    form.fields['is_active'].initial = True
                    return render(request, 'users/user_form.html', {'form': form, 'user_obj': user})
            
            form.save()
            messages.success(request, f'تم تحديث بيانات المستخدم {user.email} بنجاح!')
            return redirect('user_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserChangeForm(instance=user)
    
    context = {
        'form': form,
        'user_obj': user,
    }
    return render(request, 'users/user_form.html', context)

@login_required
@user_passes_test(is_admin)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # منع حذف الحساب الخاص
    if user.pk == request.user.pk:
        messages.error(request, '❌ لا يمكنك حذف حسابك الخاص!')
        return redirect('user_list')
    
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'تم حذف المستخدم {user.email} بنجاح!')
        return redirect('user_list')
    
    context = {'user_obj': user}
    return render(request, 'users/user_confirm_delete.html', context)

@login_required
@user_passes_test(is_admin)
def user_toggle_active(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # منع تعطيل الحساب الخاص
    if user.pk == request.user.pk:
        messages.error(request, '❌ لا يمكنك تعطيل حسابك الخاص!')
        return redirect('user_list')
    
    user.is_active = not user.is_active
    user.save()
    status = 'نشط' if user.is_active else 'غير نشط'
    messages.success(request, f'تم تغيير حالة المستخدم {user.email} إلى {status}!')
    return redirect('user_list')