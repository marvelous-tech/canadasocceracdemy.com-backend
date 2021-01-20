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
    TeacherList as SiteTeacherList, BlogList as SiteBlogList, Camps as SiteCampsList, \
    post_detail as site_blog_details, camp_details as site_camp_details, \
    teacher_details as site_teacher_details, contact as site_submit_contact_data, GalleryView as SiteGallery, \
    BlankPage as SiteBlankPage, AgreementView as SiteAgreementView, agreement_details as site_agreement_details_view, \
    BlogProgramList as SiteBlogProgramList, post_program_detail as site_post_program_detail, \
    GalleryVideoView as SiteGalleryVideo
from upload_chunk_video.views import ChunkedUploadDemo, MyChunkedUploadCompleteView, MyChunkedUploadView


@login_required
def to_e_learning_platform(request):
    if settings.ON_UPLOADED is True:
        return HttpResponseRedirect(reverse('Courses E-Learning'))
    return redirect(settings.E_LEARNING_PLATFORM)


def to_registration_platform(request):
    if settings.ON_UPLOADED is True:
        return HttpResponseRedirect(reverse('Home Registration'))
    if request.user.is_authenticated:
        logout(request)
    return redirect(settings.REGISTRATION_PLATFORM)


urlpatterns = [
    path('sldfkjsdfgjsdflkgj/', admin.site.urls),
    # path("stripe/", include("djstripe.urls", namespace="djstripe")),
    path('studio/', include('studio.urls', namespace='studio')),
    re_path(r'^progressbarupload/', include('progressbarupload.urls')),
    path('to-registration-platform/', to_registration_platform, name="to_registration_platform"),
    path('to-elearning-platform/', to_e_learning_platform, name="to_e_learning_platform"),
    path('e-learning/', include([
        path('', home_e_learning, name="Home E-Learning"),
        path('courses/', home_e_learning, name="Courses E-Learning"),
        path('billing/', home_e_learning, name="Billing E-Learning"),
        path('packages/', home_e_learning, name="Packages E-Learning"),
        path('package/<uuid:mock_package_uuid>/<uuid:package_uuid>/', home_e_learning, name="Package E-Learning"),
        path('category/<str:category_name>/<slug:category_slug>/<slug:video_number>/', home_e_learning, name="Video E-Learning"),
    ])),
    path('registration/', home_registration, name="Home Registration"),
    path('registration/terms-and-condition/', home_registration, name="Home Registration Terms"),
    path('registration/refund-policy/', home_registration, name="Home Registration Refund"),
    path('registration/privacy-policy/', home_registration, name="Home Registration Policy"),
    path('registration/pre-launch/', home_registration, name="Home Pre-Launch Registration"),
    path('registration/see-packages/', home_registration, name="Home Registration See Packages"),
    path('registration/select-packages/<uuid:mock_pakcage_uuid>/<uuid:package_uuid>/', home_registration, name="Home Registration Package"),
    path('registration/fill-up/<str:file>/', home_registration, name="Home Registration File"),
    path('secure/', include('accounts.urls', namespace='secure_accounts')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('tinymce/', include('tinymce.urls')),
    path('api/', include([
        path('v1/', include([
            re_path(r'^rest-auth/', include('rest_auth.urls')),
            path('site-data/', include('site_data.api.urls_v1', namespace='SITE DATA')),
            path('courses/', include('e_learning.api.urls_v1', namespace='e_learning')),
            path('user/', include('accounts.api.urls_v1', namespace='accounts')),
            path('payment/', include('payments.api.urls_v1', namespace='payments_api')),
        ])),
        path('v2/', include([
            path('payment/', include('stripe_gateway.api.urls', namespace='STRIPE_INTEGRATIONS_CORE_API'))
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
    path('contact-now/', site_submit_contact_data, name="contact now"),
    path('team/', SiteTeacherList.as_view(), name="team"),
    path('team/<uuid:uuid>/', site_teacher_details, name="team details"),
    path('blog/', SiteBlogList.as_view(), name="blog"),
    path('programs/', SiteBlogProgramList.as_view(), name="program"),
    path('blog/<slug:slug>/', site_blog_details, name="Blog Details"),
    path('programs/<slug:slug>/', site_post_program_detail, name="Program Details"),
    path('camps/', SiteCampsList.as_view(), name="camps"),
    path('camps/<slug:slug>/', site_camp_details, name="Camp Details"),
    path('photos/', SiteGallery.as_view(), name="photos"),
    path('videos/', SiteGalleryVideo.as_view(), name="videos"),
    path('agreements/', SiteAgreementView.as_view(), name="agreements"),
    path('agreements/<slug:slug>/', site_agreement_details_view, name="Agreement Details"),
    re_path('^private-media/', include('private_storage.urls')),
    path('', ChunkedUploadDemo.as_view(), name='chunked_upload'),
    path('api/chunked_upload_complete/', MyChunkedUploadCompleteView.as_view(), name='api_chunked_upload_complete'),
    path('api/chunked_upload/', MyChunkedUploadView.as_view(), name='api_chunked_upload'),
    path('<str:page>/', SiteBlankPage.as_view(), name='documents')
]
