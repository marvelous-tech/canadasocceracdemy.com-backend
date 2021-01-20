from django.urls import path, include

from site_data.api.views import (
    SiteDataListCreateAPIView, SiteDataRetrieveUpdateDestroyAPIView, docs_list_api_view
)

app_name = 'SITE DATA'

urlpatterns = [
    path('list-create/', SiteDataListCreateAPIView.as_view(), name='LIST / ADD SITE DATA [GET, POST]'),
    path('retrieve-update-destroy/<uuid:uuid>/', SiteDataRetrieveUpdateDestroyAPIView.as_view(),
         name='RETRIEVE / UPDATE / DESTROY SITE DATA [GET, PUT, PATCH, DELETE]'),
    path('document/<str:name>/', docs_list_api_view)
]
