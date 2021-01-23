from django.http import HttpResponsePermanentRedirect
import pytz
from django.utils import timezone


class WwwRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().partition(':')[0]
        if host == "www.canadasocceracademy.com":
            return HttpResponsePermanentRedirect(
                "https://canadasocceracademy.com" + request.path
            )
        else:
            return self.get_response(request)


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = 'Canada/Central'
        if tzname:
            if request.user.is_staff():
                timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
