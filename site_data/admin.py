from django.contrib import admin
from site_data.models import (
    SiteData,
    Partner,
    ContactedVisitor,
    PostCategory,
    Post,
    Upcoming,
    FAQ,
    Question,
    Gallery,
    Reference,
    Coupon, SiteLogo, BannerImage, Testimonial, Camp, CampImage, PrivacyPolicy, TermAndCondition, Agreement, Email,
    ContactNumber, Address, SocialLink, GalleryVideo, Document
)

# Register your models here.


@admin.register(SiteLogo)
class SiteLogoModelAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'name',
        'for_content',
        'created',
        'updated'
    ]


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


@admin.register(BannerImage)
class BannerImageAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'name',
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


@admin.register(GalleryVideo)
class GalleryVideoModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'youtube_video_id',
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


@admin.register(Testimonial)
class TestimonialModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'text',
        'created',
        'updated'
    ]


@admin.register(Address)
class AddressModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'address',
        'created',
        'updated'
    ]


@admin.register(ContactNumber)
class ContactNumberModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'number',
        'created',
        'updated'
    ]


@admin.register(Email)
class EmailModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'email',
        'created',
        'updated'
    ]


@admin.register(Agreement)
class AgreementModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'created',
        'updated'
    ]


@admin.register(TermAndCondition)
class TermAndConditionModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'text',
        'created',
        'updated'
    ]


@admin.register(PrivacyPolicy)
class PrivacyPolicyModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'text',
        'created',
        'updated'
    ]


@admin.register(CampImage)
class CampImageModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'text',
        'created',
        'updated'
    ]


@admin.register(Camp)
class CampModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'text',
        'created',
        'updated'
    ]


@admin.register(SocialLink)
class SocialLinkModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'link',
        'created',
        'updated'
    ]


@admin.register(Document)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'created',
        'updated'
    ]
