from django.utils.deprecation import MiddlewareMixin
from .models import RequestLog

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = request.META.get("REMOTE_ADDR", "")
        user = request.user if hasattr(request, "user") and request.user.is_authenticated else None

        RequestLog.objects.create(
            method=request.method,
            path=request.get_full_path(),
            query_string=request.META.get("QUERY_STRING", ""),
            remote_ip=ip,
            user=user
        )
        return None
