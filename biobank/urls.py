from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from apps.users.views import user_list, user_create, user_edit, user_delete, user_toggle_active

# Import Views
from apps.dashboard.views import dashboard
from apps.participants.views import (
    participant_list, participant_detail, 
    participant_create, participant_edit, participant_delete,
    export_participants_excel
)
from apps.specimens.views import (
    specimen_list, specimen_create, 
    specimen_detail, specimen_edit, specimen_delete
)
from apps.studies.views import study_list, study_create, study_edit, study_delete
from apps.storage.views import storage_list, facility_create, facility_edit, facility_delete
from apps.shipments.views import shipment_list, shipment_create, shipment_detail, shipment_edit, shipment_delete
from apps.reports.views import reports_dashboard
from apps.audit.views import audit_log_list

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Allauth
    path('accounts/', include('allauth.urls')),
    
    # Dashboard
    path('', dashboard, name='dashboard'),
    
    # Profile
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    
    # Participants
    path('participants/', participant_list, name='participant_list'),
    path('participants/add/', participant_create, name='participant_create'),
    path('participants/<int:pk>/', participant_detail, name='participant_detail'),
    path('participants/<int:pk>/edit/', participant_edit, name='participant_edit'),
    path('participants/<int:pk>/delete/', participant_delete, name='participant_delete'),
    path('participants/export/', export_participants_excel, name='export_participants'),
    
# Users Management
path('users/', user_list, name='user_list'),
path('users/add/', user_create, name='user_create'),
path('users/<int:pk>/edit/', user_edit, name='user_edit'),
path('users/<int:pk>/delete/', user_delete, name='user_delete'),
path('users/<int:pk>/toggle/', user_toggle_active, name='user_toggle_active'),

    # Specimens
    path('specimens/', specimen_list, name='specimen_list'),
    path('specimens/add/', specimen_create, name='specimen_create'),
    path('specimens/<int:pk>/', specimen_detail, name='specimen_detail'),
    path('specimens/<int:pk>/edit/', specimen_edit, name='specimen_edit'),
    path('specimens/<int:pk>/delete/', specimen_delete, name='specimen_delete'),
    
    # Studies
    path('studies/', study_list, name='study_list'),
    path('studies/add/', study_create, name='study_create'),
    path('studies/<int:pk>/edit/', study_edit, name='study_edit'),
    path('studies/<int:pk>/delete/', study_delete, name='study_delete'),
    
    # Storage
    path('storage/', storage_list, name='storage_list'),
    path('storage/facility/add/', facility_create, name='facility_create'),
    path('storage/facility/<int:pk>/edit/', facility_edit, name='facility_edit'),
    path('storage/facility/<int:pk>/delete/', facility_delete, name='facility_delete'),
    
# Shipments
path('shipments/', shipment_list, name='shipment_list'),
path('shipments/add/', shipment_create, name='shipment_create'),
path('shipments/<int:pk>/', shipment_detail, name='shipment_detail'),
path('shipments/<int:pk>/edit/', shipment_edit, name='shipment_edit'),
path('shipments/<int:pk>/delete/', shipment_delete, name='shipment_delete'),
    
    # Reports
    path('reports/', reports_dashboard, name='reports_dashboard'),
    
    # Audit
    path('audit/', audit_log_list, name='audit_log_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)