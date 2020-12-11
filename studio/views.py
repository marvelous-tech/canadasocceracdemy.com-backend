import os

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.files import File
from django.conf import settings
from django_q.tasks import async_task

# Create your views here.
from django.urls import reverse

from e_learning.models import CourseVideo
from studio.forms import CourseVideoModelForm


def save_from_disk_to_storage_server(upload_id, video_id):
    file_path = os.path.join(settings.BASE_DIR, settings.CHUNKED_UPLOAD_PATH, upload_id + '.part')
    print("File found")
    f = File(open(file_path, "rb"))
    print(f.size)
    print("File stored in memory")
    video: CourseVideo = CourseVideo.objects.get(pk=video_id)
    print("Course video found")
    print("Course video is being uploaded")
    video.video.save(f.name, f.file, save=True)
    print("File finalizing uploading")
    print("File uploaded")
    os.remove(file_path)
    f.close()
    print("File removed from disk")


@login_required
def add_course_video(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == "POST":
            form = CourseVideoModelForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                instance = form.save()
                print(form.data.get('upload_id'))
                async_task("studio.views.save_from_disk_to_storage_server", form.data.get('upload_id'), instance.id)
                messages.add_message(request, level=messages.SUCCESS,
                                     message="Video is uploaded successfully. Shortly it will be live.")
                return HttpResponseRedirect(reverse('studio:ALL VIDEOS'))
            print(form.cleaned_data)
            messages.add_message(request, level=messages.ERROR, message="Errors in form")
            form = CourseVideoModelForm(data=request.POST)
            return render(request, 'studio/add-video.html', {'form': form})
        form = CourseVideoModelForm()
        return render(request, 'studio/add-video.html', {'form': form})
    messages.add_message(request, level=messages.ERROR, message="Must be staff of canadasocceracademy.com")
    logout(request)
    return HttpResponseRedirect(reverse('secure_accounts:Login to your account'))


@login_required
def all_videos(request):
    if request.method == "GET":
        if request.user.is_staff:
            videos = CourseVideo.objects.select_related('category', 'package').order_by('-id')
            context = {
                'videos': videos
            }
            return render(request, "studio/all-videos.html", context=context)
        messages.add_message(request, level=messages.ERROR, message="Must be staff of canadasocceracademy.com")
        logout(request)
        return HttpResponseRedirect(reverse('secure_accounts:Login to your account'))
    messages.add_message(request, level=messages.ERROR, message="Not allowed")
    logout(request)
    return HttpResponseRedirect(reverse('secure_accounts:Login to your account'))
