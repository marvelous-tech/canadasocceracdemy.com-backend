from django.urls import path
from studio.views import *

app_name = 'studio'

urlpatterns = [
    path('', all_videos, name="ALL VIDEOS"),
    path('upload/', add_course_video, name="UPLOAD VIDEO"),
]
