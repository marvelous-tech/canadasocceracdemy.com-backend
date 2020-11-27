from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from site_data.models import Post, SiteLogo, Email, ContactNumber, Address, BannerImage


# Create your views here.


def get_default_contexts():
    logos = SiteLogo.objects.all()
    emails = Email.objects.all()
    numbers = ContactNumber.objects.all()
    addresses = Address.objects.all()

    return {
        'nav_logo': logos.first(),
        'logos': logos,
        'emails': emails,
        'numbers': numbers,
        'addresses': addresses
    }


class Home(TemplateView):
    template_name = 'site_data/home/home.html'

    def get_context_data(self, **kwargs):
        context = {'banner_images': BannerImage.objects.all(), **get_default_contexts()}
        return context


def post_detail(request, slug):
    q = Post.objects.filter(slug__iexact=slug)


    if q.exists():
        q = q.first()
    else:
        return HttpResponse('<h1>Post Not Found</h1>')
    context = {

        'post': q
    }
    return render(request, 'posts/details.html', context)
