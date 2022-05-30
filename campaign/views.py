from django.shortcuts import render

# Create your views here.


def spain_id_camp(request):
    return render(request, 'campaign/spain.html')
