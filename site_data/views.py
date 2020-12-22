from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from accounts.models import MockPackages, Member
from site_data.models import Post, SiteLogo, Email, ContactNumber, Address, BannerImage, Upcoming, SocialLink, SiteData, \
    Gallery, Partner, FAQ, Testimonial, Camp


# Create your views here.

def get_recent_posts():
    return {
        'recent_posts': Post.objects.filter(is_active=True)[:2]
    }


def get_recent_upcoming():
    return {
        'recent_upcoming': Upcoming.objects.filter(is_active=True)[:3]
    }


def get_feature_course_logo():
    return {
        'feature_course_logo': SiteLogo.objects.filter(for_content='feature_course_logo').first()
    }


def get_footer_text():
    return {
        'footer_text': SiteData.objects.filter(name__icontains='footer_text').first()
    }


def get_feature_gallery_images():
    return {
        'feature_gallery_images': Gallery.objects.filter(is_feature=True)
    }


def get_sidebar_pages_default_context():
    return {
        **get_recent_posts(),
        **get_feature_course_logo(),
        **get_footer_text(),
        **get_feature_gallery_images(),
        **get_default_contexts()
    }


def get_features():
    return {
        **get_recent_posts(),
        **get_feature_course_logo(),
        **get_feature_gallery_images()
    }


def get_testimonials():
    return {
        'testimonials': Testimonial.objects.filter(is_deleted=False)[:5]
    }


def get_teachers():
    return {'teachers': Member.objects.all()}


def get_default_contexts():
    logos = SiteLogo.objects.filter(for_content='navbar_logo')
    app_feature_image = SiteLogo.objects.filter(for_content='app_feature_image')
    emails = Email.objects.all()
    numbers = ContactNumber.objects.all()
    addresses = Address.objects.all()
    socials = SocialLink.objects.all()

    return {
        'app_feature_image': app_feature_image.first(),
        'navbar_logo': logos.first(),
        'emails': emails,
        'numbers': numbers,
        'addresses': addresses,
        'socials': socials,
        **get_footer_text()
    }


def get_faqs():
    return {'faqs': FAQ.objects.filter(is_deleted=False)}


class Home(TemplateView):
    template_name = 'site_data/home/home.html'

    def get_context_data(self, **kwargs):
        banner_logos = SiteLogo.objects.filter(for_content='banner_image')
        context = {
            'banner_logos': banner_logos,
            'banner_images': BannerImage.objects.all(),
            'mock_courses': MockPackages.objects.filter(is_deleted=False),
            'partners': Partner.objects.filter(is_deleted=False),
            'home_about_us_header': SiteData.objects.filter(name='home_about_us_header').first(),
            'home_about_us_sub_header': SiteData.objects.filter(name='home_about_us_sub_header').first(),
            'home_about_us_content_body': SiteData.objects.filter(name='home_about_us_content_body').first(),
            **get_default_contexts(),
            **get_recent_posts(),
            **get_recent_upcoming(),
            **get_faqs(),
            **get_teachers()
        }
        return context


class About(TemplateView):
    template_name = 'site_data/about/about.html'

    def get_context_data(self, **kwargs):
        images = SiteLogo.objects.filter(for_content='about_image')
        about_heading = SiteData.objects.filter(name__icontains='about_heading')
        about_text = SiteData.objects.filter(name__icontains='about_text')
        context = {
            'images': images,
            'about_heading': about_heading.first(),
            'about_text': about_text.first(),
            **get_sidebar_pages_default_context()
        }
        return context


class Contact(TemplateView):
    template_name = 'site_data/contact/contact.html'

    def get_context_data(self, **kwargs):
        images = SiteLogo.objects.filter(for_content='about_image')
        context = {
            'images': images,
            **get_default_contexts(),
            **get_feature_gallery_images()
        }
        return context


class TeacherList(TemplateView):
    template_name = 'site_data/teacher/teacher.html'

    def get_context_data(self, **kwargs):
        banner_logos = SiteLogo.objects.filter(for_content='banner_image')
        context = {
            'banner_logos': banner_logos,
            'banner_images': BannerImage.objects.all(),
            **get_sidebar_pages_default_context(),
            **get_teachers()
        }
        return context


def teacher_details(request, uuid):
    q = Member.objects.filter(uuid=uuid)

    if q.exists():
        q = q.first()
    else:
        return HttpResponse('<h1>Member Not Found</h1>')
    context = {
        'teacher': q,
        **get_sidebar_pages_default_context(),
    }
    return render(request, 'site_data/teacher/teacher_details.html', context)


class BlogList(TemplateView):
    template_name = 'site_data/blog/blog.html'

    def get_context_data(self, **kwargs):
        tag = None
        if self.request.GET.get('tag') is not None:
            tag = self.request.GET.get('tag')

        if tag is not None:
            posts = Post.objects.filter(is_active=True, tags__icontains=tag)
        else:
            posts = Post.objects.filter(is_active=True)

        paginator = Paginator(posts, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            **get_sidebar_pages_default_context(),
            'page_obj': page_obj
        }
        return context


class BlogDetail(TemplateView):
    template_name = 'site_data/blog/details/details.html'

    def get_context_data(self, **kwargs):
        tag = None
        if self.request.GET.get('tag') is not None:
            tag = self.request.GET.get('tag')

        if tag is not None:
            posts = Post.objects.filter(is_active=True, tags__icontains=tag)
        else:
            posts = Post.objects.filter(is_active=True)

        paginator = Paginator(posts, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            **get_default_contexts(),
            **get_sidebar_pages_default_context(),
            'page_obj': page_obj
        }
        return context


class Camps(TemplateView):
    template_name = 'site_data/camps/camps.html'

    def get_context_data(self, **kwargs):
        camps = Camp.objects.filter(is_deleted=False)
        paginator = Paginator(camps, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            **get_sidebar_pages_default_context(),
            'page_obj': page_obj
        }
        return context


def camp_details(request, slug):
    q = Camp.objects.filter(slug__iexact=slug)

    if q.exists():
        q = q.first()
    else:
        return HttpResponse('<h1>Camp Not Found</h1>')
    context = {
        'camp': q,
        **get_sidebar_pages_default_context(),
    }
    return render(request, 'site_data/camps/camp_details.html', context)


def post_detail(request, slug):
    q = Post.objects.filter(slug__iexact=slug)


    if q.exists():
        q = q.first()
    else:
        return HttpResponse('<h1>Post Not Found</h1>')
    context = {
        'blog': q,
        'member': q.by,
        **get_sidebar_pages_default_context(),
    }
    return render(request, 'site_data/blog/details/details.html', context)
