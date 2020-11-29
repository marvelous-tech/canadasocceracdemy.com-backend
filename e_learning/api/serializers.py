from rest_framework import serializers

from e_learning.models import CourseVideo


class CourseVideoSingleSerializer(serializers.ModelSerializer):


    class Meta:
        model = CourseVideo
        fields = '__all__'
