from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from accounts.models import MockPackages, CoursePackage
from e_learning.api.serializers import CourseVideoSingleSerializer, PostCommentSerializer, \
    CourseVideoSingleCommentSerializer, CourseVideoListingSerializer, CategoriesSerializer, PlaylistSerializer, \
    MockPackagesSerializer, PackagesSerializer
from e_learning.models import CourseVideo, CoursePlaylist, CourseCategory, WatchLetterPlaylist


@api_view(['GET'])
def get_video(request, slug):
    package_points = request.user.user_profile.package.points
    user_id = request.user.id
    queryset = CourseVideo.objects.queryset().prefetch_related('views')
    queryset = CourseVideo.objects.get_course_videos_by_package_points(queryset, package_points)
    instance = get_object_or_404(queryset, slug=slug)
    serializer = CourseVideoSingleSerializer(instance=instance, context={'user_id': user_id})
    return Response(serializer.data)


@api_view(['POST'])
def post_comment(request):
    serializer = PostCommentSerializer(data=request.data)
    if serializer.is_valid():
        comment = serializer.save()
        return Response(CourseVideoSingleCommentSerializer(instance=comment).data)
    return Response(serializer.errors)


@api_view(['GET'])
def get_videos_by_playlist_slug(request, playlist_slug):
    package_points = request.user.user_profile.package.points
    queryset = CoursePlaylist.objects.prefetch_related('videos__instructors__user', 'videos__views')
    instance = CoursePlaylist.objects.get_playlist_by_package_points_by_slug(queryset, package_points, playlist_slug)
    serializer = CourseVideoListingSerializer(instance=instance.videos.all(), many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_videos_by_category_slug(request, category_slug):
    package_points = request.user.user_profile.package.points
    queryset = CourseVideo.objects.prefetch_related('instructors__user', 'views')
    category: CourseCategory = get_object_or_404(CourseCategory.objects.all(), slug=category_slug)
    queryset = CourseVideo.objects.get_course_videos_by_package_points_by_category_id(queryset, package_points,
                                                                                      category.id)
    serializer = CourseVideoListingSerializer(instance=queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_categories_api_view(request):
    serializer = CategoriesSerializer(instance=CourseCategory.objects.filter(is_deleted=False).order_by('id'), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_to_watch_letter_api_view(request):
    video_slug = request.data.get('video_slug')
    try:
        video = CourseVideo.objects.get(slug__exact=video_slug)
    except CourseVideo.DoesNotExist as e:
        return Response({"error_msg": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    instance = WatchLetterPlaylist.objects.create(user_id=request.user.user_profile.id)
    instance.videos.add(video)
    return Response()


@api_view(['GET'])
def get_all_playlist_api_view(request):
    queryset = CoursePlaylist.objects.prefetch_related('videos__package')\
        .filter(videos__package__points__lte=request.user.user_profile.package.points).order_by('-id')
    serializer = PlaylistSerializer(instance=queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_all_packages_api_view(request):
    currency = request.query_params.get('currency', 'USD')
    serializer = MockPackagesSerializer(instance=MockPackages.objects.filter(is_deleted=False, currency__icontains=currency).order_by('id'), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_package_api_view(request, package_uuid):
    try:
        mock_package = CoursePackage.objects.get(uuid=package_uuid)
    except Exception as e:
        return Response({"error_msg": "Package not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = PackagesSerializer(instance=mock_package, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_mock_package_api_view(request, mock_package_uuid):
    try:
        mock_package = MockPackages.objects.get(uuid=mock_package_uuid)
    except Exception as e:
        return Response({"error_msg": "Package not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = MockPackagesSerializer(instance=mock_package, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
