from django.shortcuts import render

# Create your views here.
from campaign.models import CampaignPackage


def spain_id_camp(request):
    fees = CampaignPackage.objects.filter(campaign_id=1)
    context = {
        'fees': fees
    }
    return render(request, 'campaign/spain_id_camp/spain.html', context=context)
