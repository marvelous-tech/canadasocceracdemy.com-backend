from django.conf import settings


def tags(request):
    return {'frontend_version': settings.FRONTEND_VERSION}
