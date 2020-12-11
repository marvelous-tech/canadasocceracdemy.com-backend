from django import forms
from e_learning.models import CourseVideo


class CourseVideoModelForm(forms.ModelForm):
    upload_id = forms.CharField(max_length=255, widget=forms.HiddenInput())

    class Meta:
        model = CourseVideo
        exclude = [
            'video',
            'is_deleted',
            'slug',
            'uuid',
            'comments',
            'cc',
            'marks'
        ]





