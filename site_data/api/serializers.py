from rest_framework import serializers
from site_data.models import SiteData


class SiteDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = SiteData
        fields = '__all__'
