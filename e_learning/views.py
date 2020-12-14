from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
from accounts.models import CoursePackage
from core.views import get_default_contexts
from e_learning.api.serializers import CourseVideoListingSerializer, CourseVideoSingleSerializer
from e_learning.models import CourseCategory, CourseVideo


@login_required
def home_e_learning(request):
    return render(request, 'e_learning/home.html')


def profile(request):
    categories = CourseCategory.objects.all()
    context = {
        **get_default_contexts(request.user),
        'categories': categories
    }
    return render(request, 'e_learning/profile.html', context=context)


def category_videos(request, slug, selected_video_slug=None):
    package_id = request.user.user_profile.package_id
    queryset = CourseVideo.objects.prefetch_related('instructors__user', 'views').filter(is_deleted=False)
    category: CourseCategory = get_object_or_404(CourseCategory.objects.all(), slug=slug)
    queryset = CourseVideo.objects.get_course_videos_by_package_points_by_category_id(queryset, package_id, category.id)
    serializer = CourseVideoListingSerializer(instance=queryset, many=True)

    if selected_video_slug is None:
        selected_video = queryset.first()
    else:
        selected_video = get_object_or_404(queryset, slug=selected_video_slug)

    context = {
        'video_obj': CourseVideoSingleSerializer(instance=selected_video, context={'user_id': request.user.pk}).data,
        'videos': serializer.data,
        'category_slug': slug,
        **get_default_contexts(request.user)
    }
    print(context)
    return render(request, 'e_learning/video.html', context=context)
