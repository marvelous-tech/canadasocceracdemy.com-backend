from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from site_data.models import Post


# Create your views here.


class Home(TemplateView):
    template_name = 'site_data/home/home.html'


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
