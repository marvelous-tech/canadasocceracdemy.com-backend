from django.urls import path, include

from e_learning.api.views import get_video, \
    get_videos_by_category_slug, \
    get_videos_by_playlist_slug, get_all_categories_api_view, get_all_playlist_api_view, \
    get_all_packages_api_view, add_to_watch_letter_api_view, post_comment, \
    get_package_api_view, get_mock_package_api_view

app_name = 'e_learning'

urlpatterns = [
    path('video/', include([
        path('<slug:slug>/', get_video, name='get_video'),
        path('save/', add_to_watch_letter_api_view, name="add_to_watch_letter_api_view"),
        path('comment/', post_comment, name="post_comment"),
    ])),
    path('category/', include([
        path('', get_all_categories_api_view, name="get_all_categories_api_view"),
        path('<slug:category_slug>/', get_videos_by_category_slug, name='get_videos_by_category_slug'),
    ])),
    path('playlist/', include([
        path('', get_all_playlist_api_view, name='get_all_playlist_api_view'),
        path('<slug:playlist_slug>/', get_videos_by_playlist_slug, name='get_videos_by_playlist_slug'),
    ])),
    path('package/', include([
        path('', get_all_packages_api_view, name="get_all_packages_api_view"),
        path('<uuid:package_uuid>/', get_package_api_view, name="get_package_api_view"),
        path('mock/<uuid:mock_package_uuid>/', get_mock_package_api_view, name="get_mock_package_api_view"),
    ])),
]
