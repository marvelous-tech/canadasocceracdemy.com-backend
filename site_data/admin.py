from django.contrib import admin
from site_data.models import (
    SiteData,
    Partner,
    ContactedVisitor,
    ThreadReply,
    Thread,
    PostCategory,
    Post,
    Upcoming,
    FAQ,
    Question,
    Gallery,
    Reference,
    Coupon
)

# Register your models here.


@admin.register(SiteData)
class SiteDataModelAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'page_name',
        'name',
        'ticket',
        'created',
        'updated'
    ]


@admin.register(Partner)
class PartnerModelAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'name',
        'created',
        'updated'
    ]


@admin.register(ContactedVisitor)
class ContactedVisitorModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'email',
        'phone',
        'subject',
        'created',
        'updated'
    ]


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


@admin.register(PostCategory)
class PostCategoryModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'created',
        'updated'
    ]


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = [
        'category',
        'by',
        'name',
        'sub_title',
        'published_at',
        'created',
        'updated'
    ]


@admin.register(Upcoming)
class UpcomingModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category',
        'schedule',
        'created',
        'updated'
    ]


@admin.register(FAQ)
class FAQModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'created',
        'updated'
    ]


@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    list_display = [
        'by',
        'name',
        'created',
        'updated'
    ]


@admin.register(Gallery)
class GalleryModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'image',
        'created',
        'updated'
    ]



@admin.register(Reference)
class ReferenceModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'ticket',
        'created',
        'updated'
    ]


@admin.register(Coupon)
class CouponModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'ticket',
        'created',
        'updated'
    ]
