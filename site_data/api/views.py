from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions

from site_data.models import SiteData, Document
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


@api_view(['GET'])
def docs_list_api_view(request, name):
    try:
        document = Document.objects.get(name=name)
    except (Document.DoesNotExist, Document.MultipleObjectsReturned) as e:
        document = None

    if document is not None:
        response = {
            "updated": document.updated,
            "name": document.name,
            "body": document.body
        }
        return Response(data=response, status=status.HTTP_200_OK)
    return Response(data={"message": "document not found"}, status=status.HTTP_404_NOT_FOUND)
