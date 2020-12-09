from django.urls import path, include

from e_learning.views import profile, category_videos

app_name = 'e_learning_view'

urlpatterns = [
    path('profile/', include([
        path('details/', profile, name="Profile"),
    ])),
    path('category/', include([
        path('<slug:slug>/', category_videos, name="Course videos"),
        path('<slug:slug>/<slug:selected_video_slug>/', category_videos, name="Course video")
    ]))
]
