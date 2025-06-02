from django.conf import settings

def settings_context(request):
    return {
        "DJANGO_DEBUG": settings.DEBUG,
        "ALLOWED_HOSTS": settings.ALLOWED_HOSTS,
    }
