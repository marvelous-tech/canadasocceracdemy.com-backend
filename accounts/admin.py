from django.contrib import admin
from accounts.models import Member

# Register your models here.


@admin.register(Member)
class MemberModelAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'phone',
        'type'
    ]
