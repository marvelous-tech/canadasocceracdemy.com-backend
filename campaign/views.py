from django.shortcuts import render

# Create your views here.
from campaign.models import CampaignPackage, CampaignSubscriber


def spain_id_camp(request):
    fees = CampaignPackage.objects.filter(campaign_id=1).order_by('id')
    context = {
        'fees': fees
    }
    return render(request, 'campaign/spain_id_camp/spain.html', context=context)


def get_pdf(request, guid: str):
    context = {
        'subscriber': CampaignSubscriber.objects.get(guid=guid)
    }
    return render(request, 'campaign/spain_id_camp/gen_pdf.html', context=context)
