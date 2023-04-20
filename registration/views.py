from django.shortcuts import render

from site_data.models import BannerImage


# Create your views here.


def reg_soccer_tryouts_2023(request):

    context = {
        'banner_images': BannerImage.objects.all(),
    }

    return render(request, 'registration/reg_soccer_tryouts_2023.html', context)
