def keys(request):
    from django.conf import settings
    return {'GAK': settings.GOOGLE_API_KEY, }

