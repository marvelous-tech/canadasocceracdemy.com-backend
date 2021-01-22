from django.conf import settings


def tags(request):
    return {'frontend_version': settings.FRONTEND_VERSION, 'phone': settings.SUPPORT_PHONE_NUMBER}
