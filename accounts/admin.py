from django.contrib import admin
from accounts.models import Member, UserProfile, MockPackages


# Register your models here.


@admin.register(Member)
class MemberModelAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'phone',
        'type'
    ]


@admin.register(UserProfile)
class UserProfileModelAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'phone',
        'package',
        'is_active',
        'is_expired',
        'email_verified',
        'type'
    ]


@admin.register(MockPackages)
class MockPackagesModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'amount_text',
        'currency',
        'is_monthly',
        'is_annually',
        'is_deleted',
        'created',
        'updated'
    ]
