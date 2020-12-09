"""canadasocceracademy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import path, include, re_path, reverse

from e_learning.views import home_e_learning
from payments.views import list_all_payment_methods
from accounts.views import login_user, home_registration
from django.contrib.auth import logout

from site_data.views import Home as SiteHome, About as SiteAbout, Contact as SiteContact, \
    TeacherList as SiteTeacherList, BlogList as SiteBlogList


@login_required
def to_e_learning_platform(request):
    if settings.ON_UPLOADED is True:
        return HttpResponseRedirect(reverse('Home E-Learning'))
    return redirect(settings.E_LEARNING_PLATFORM)


def to_registration_platform(request):
    if settings.ON_UPLOADED is True:
        return HttpResponseRedirect(reverse('Home Registration'))
    if request.user.is_authenticated:
        logout(request)
    return redirect(settings.REGISTRATION_PLATFORM)


urlpatterns = [
    path('to-registration-platform/', to_registration_platform, name="to_registration_platform"),
    path('to-elearning-platform/', to_e_learning_platform, name="to_e_learning_platform"),
    path('e-learning/', home_e_learning, name="Home E-Learning"),
    path('registration/', home_registration, name="Home Registration"),
    path('registration/see-packages/', home_registration, name="Home Registration"),
    path('registration/select-packages/<uuid:mock_pakcage_uuid>/<uuid:package_uuid>/', home_registration, name="Home Registration"),
    path('registration/fill-up/<str:file>/', home_registration, name="Home Registration"),
    path('secure/', include('accounts.urls', namespace='secure_accounts')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls),
    path('api/', include([
        path('v1/', include([
            re_path(r'^rest-auth/', include('rest_auth.urls')),
            path('site-data/', include('site_data.api.urls_v1', namespace='SITE DATA')),
            path('courses/', include('e_learning.api.urls_v1', namespace='e_learning')),
            path('user/', include('accounts.api.urls_v1', namespace='accounts')),
            path('payment/', include('payments.api.urls_v1', namespace='payments_api')),
        ]))
    ])),
    path('dashboard/', include([
        path('', list_all_payment_methods, name="dashboard"),
        path('payments/', include('payments.urls', namespace="payments")),
        path('e-learning/', include('e_learning.urls', namespace='e_learning_view')),
    ])),
    path('accounts/login/', login_user, name="login"),
    path('', SiteHome.as_view(), name="home"),
    path('about/', SiteAbout.as_view(), name="about"),
    path('contact/', SiteContact.as_view(), name="contact"),
    path('teachers/', SiteTeacherList.as_view(), name="teachers"),
    path('blog/', SiteBlogList.as_view(), name="blog"),
    re_path('^private-media/', include('private_storage.urls')),
]
