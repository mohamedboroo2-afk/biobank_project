from django.utils.deprecation import MiddlewareMixin
from .models import AuditLog
import json

class AuditMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # تخزين معلومات الطلب
        request.audit_data = {
            'ip_address': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'request_path': request.path,
            'request_method': request.method,
        }
        return None
    
    def process_response(self, request, response):
        # تسجيل العمليات للمستخدمين المسجلين
        if hasattr(request, 'user') and request.user.is_authenticated:
            path = request.path
            
            # تجاهل المسارات الثابتة
            if path.startswith('/static/') or path.startswith('/media/'):
                return response
            
            # تحديد نوع الإجراء
            action_type = 'READ'
            if request.method == 'POST':
                action_type = 'CREATE'
                # إذا كان الطلب لتعديل
                if '/edit/' in path:
                    action_type = 'UPDATE'
                # إذا كان الطلب لحذف
                if '/delete/' in path:
                    action_type = 'DELETE'
            elif request.method in ['PUT', 'PATCH']:
                action_type = 'UPDATE'
            elif request.method == 'DELETE':
                action_type = 'DELETE'
            
            # تسجيل العمليات المهمة فقط
            if action_type in ['CREATE', 'UPDATE', 'DELETE', 'LOGIN', 'LOGOUT'] or '/export/' in path:
                AuditLog.objects.create(
                    user=request.user,
                    action=action_type,
                    model_name=self.get_model_name(path),
                    object_id=path,
                    object_repr=f"{request.method} {path}",
                    ip_address=request.audit_data.get('ip_address', ''),
                    user_agent=request.audit_data.get('user_agent', ''),
                    request_path=path,
                    request_method=request.method,
                    additional_data={
                        'data': dict(request.POST) if request.method == 'POST' else {},
                        'get_params': dict(request.GET) if request.GET else {},
                    }
                )
        
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def get_model_name(self, path):
        # استخراج اسم النموذج من المسار
        parts = path.strip('/').split('/')
        if len(parts) >= 1:
            return parts[0].capitalize()
        return 'Unknown'