from django.contrib import admin

# Register your models here.
from e_learning.models import \
    CourseCategory, \
    CoursePackage, \
    CoursePlaylist, \
    CourseVideoMark, \
    CourseVideo, CourseVideoHistory


@admin.register(CourseCategory)
class CourseCategoryModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'created',
        'updated'
    ]


@admin.register(CoursePackage)
class CoursePackageModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'amount',
        'points',
        'stripe_price_id',
        'created',
        'updated',
        'Cycle'
    ]
    ordering = ('-points', )
    search_fields = ['stripe_price_id', 'uuid', 'slug', 'name']



@admin.register(CoursePlaylist)
class CoursePlaylistModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'created',
        'updated'
    ]


@admin.register(CourseVideoMark)
class CourseVideoMarkModelAdmin(admin.ModelAdmin):
    list_display = [
        'time',
        'note',
        'created',
        'updated'
    ]


@admin.register(CourseVideoHistory)
class CourseVideoHistoryModelAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseVideo)
class CourseVideoModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'sub_title',
        'uploaded_at',
        'slug',
        'created',
        'updated'
    ]
