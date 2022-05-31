from django.contrib import admin

# Register your models here.
from campaign.models import Campaign, CampaignPackage, CampaignSubscriber


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    pass


@admin.register(CampaignPackage)
class CampaignPackageAdmin(admin.ModelAdmin):
    list_display = [
        'campaign',
        'name',
        'price',
        'starts',
        'ends',
        'discount_percentage_off',
        'discount_amount_off',
        'discount_starts',
        'discount_expires',
    ]


@admin.register(CampaignSubscriber)
class CampaignSubscriberAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'guid'
    ]
