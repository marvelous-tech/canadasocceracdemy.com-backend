from django.contrib import admin

# Register your models here.
from comment.models import ThreadReply, Thread


@admin.register(ThreadReply)
class ThreadReplyModelAdmin(admin.ModelAdmin):
    list_display = [
        'by',
        'created',
        'updated'
    ]


@admin.register(Thread)
class ThreadModelAdmin(admin.ModelAdmin):
    list_display = [
        'by',
        'created',
        'updated'
    ]
