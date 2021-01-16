from django.shortcuts import get_object_or_404
from rest_framework import serializers

from accounts.models import Member, UserProfile, MockPackages, CoursePackage
from e_learning.models import CourseVideo, CourseVideoMark, Comment, CourseCategory, CoursePlaylist

from django.db.models import Q


class PackagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoursePackage
        fields = [
            'uuid',
            'name',
            'amount',
            'description_box',
            'cycle'
        ]


class MockPackagesSerializer(serializers.ModelSerializer):
    packages = PackagesSerializer(many=True, read_only=True)

    class Meta:
        model = MockPackages
        fields = [
            'uuid',
            'name',
            'amount_text',
            'description_box',
            'is_monthly',
            'is_annually',
            'packages'
        ]


class PlaylistSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoursePlaylist
        fields = [
            'name',
            'description_box',
            'slug',
        ]


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseCategory
        fields = [
            'name',
            'description_box',
            'slug'
        ]


class PostCommentSerializer(serializers.Serializer):
    video_slug = serializers.SlugField(max_length=255)
    sent_by = serializers.IntegerField(allow_null=True)
    message = serializers.CharField(allow_null=True)

    def save(self, **kwargs):
        instance: CourseVideo = get_object_or_404(
            CourseVideo.objects.all(), slug=self.validated_data.get('video_slug')
        )
        comment = Comment.objects.create(
            sender_id=self.validated_data.get('send_to'),
            to_id=None,
            message=self.validated_data.get('message')
        )
        instance.comments.add(comment)
        return comment

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class CourseVideoSingleMemberSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Member
        fields = ('username', 'profile_image')

    @staticmethod
    def get_username(obj):
        return obj.user.username


class CourseVideoSingleCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('sender_id', 'to_id', 'message')


class CourseVideoMarkMarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseVideoMark
        fields = ('time', 'note')


class CourseVideoSingleSerializer(serializers.ModelSerializer):
    instructors = CourseVideoSingleMemberSerializer(many=True, read_only=True)
    marks = CourseVideoMarkMarkSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    # user = serializers.SerializerMethodField(read_only=True)
    last_watched_current_time = serializers.SerializerMethodField(read_only=True)
    thumb_ups = serializers.SerializerMethodField(read_only=True)
    views = serializers.SerializerMethodField(read_only=True)
    thumbnail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CourseVideo
        fields = [
            'instructors',
            'marks',
            'comments',
            'last_watched_current_time',
            'thumb_ups',
            'description_box',
            'sub_title',
            'uploaded_at',
            'name',
            'video',
            'slug',
            'uuid',
            'views',
            'thumbnail'
        ]

    # def get_user(self, obj):
    #     user = UserProfile.objects.get(user_id=self.user_id)
    #     return {
    #         'username': user.user.username,
    #         'profile_image': user.profile_image.url
    #     }

    @staticmethod
    def get_thumbnail(obj):
        return obj.thumbnail.url

    @property
    def user_id(self):
        return self.context.get('user_id')

    def get_last_watched_current_time(self, obj):
        user_id = self.user_id
        queryset = obj.views.filter(user_id=user_id)
        history = queryset.first()
        if history is None:
            return 0
        return history.at_time

    @staticmethod
    def get_views(obj):
        return obj.views.count()

    @staticmethod
    def get_thumb_ups(obj):
        return obj.thumb_ups.count()

    def get_comments(self, obj):
        user_id = self.user_id
        queryset = obj.comments.filter(Q(sender_id=user_id) | Q(to_id=user_id))
        serializer = CourseVideoSingleCommentSerializer(instance=queryset, many=True, read_only=True)
        return serializer.data


class CourseVideoListingSerializer(serializers.ModelSerializer):
    instructors = CourseVideoSingleMemberSerializer(many=True, read_only=True)
    # last_watched_current_time = serializers.SerializerMethodField(read_only=True)
    views = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CourseVideo
        fields = [
            'slug',
            'thumbnail',
            'name',
            'uploaded_at',
            'instructors',
            # 'last_watched_current_time',
            'views'
        ]

    # @property
    # def user_id(self):
    #     return self.context.get('user_id')

    # def get_last_watched_current_time(self, obj):
    #     user_id = self.user_id
    #     queryset = obj.views.filter(user_id=user_id)
    #     history = queryset.first()
    #     if history is None:
    #         return 0
    #     return history.at_time

    @staticmethod
    def get_views(obj):
        return obj.views.count()

