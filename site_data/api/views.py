from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions

from site_data.models import SiteData
from site_data.api.serializers import SiteDataSerializer


class SiteDataListCreateAPIView(ListCreateAPIView):
    permissions = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = SiteData.objects.all()
    serializer_class = SiteDataSerializer


class SiteDataRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = SiteData.objects.all()
    lookup_field = 'uuid'
    serializer_class = SiteDataSerializer
