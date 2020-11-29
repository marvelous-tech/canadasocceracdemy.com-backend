import uuid
import os

import string
from random import random

from django.utils.text import slugify


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/files', filename)


def get_logo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/logos', filename)


def get_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/images', filename)


def get_news_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/news/images', filename)


def get_profile_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/profiles/images', filename)


def get_agreement_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/agreements/images', filename)


def get_camp_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/camps/images', filename)


def get_gallery_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/gallery/images', filename)


def get_course_video_path(instance, filename):
    ext = filename.split('.')[-1]
    uuid_ = uuid.uuid4()
    filename = "%s.%s" % (str(uuid_) + '-video', ext)
    return os.path.join(f'uploads/courses/videos/{instance.category.slug}/{uuid_}', filename)


def get_course_video_thumbnail_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (str(instance.uuid) + '-thumbnail', ext)
    return os.path.join(f'uploads/courses/videos/{instance.category.slug}/{instance.uuid}', filename)


def get_course_video_cc_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (str(instance.uuid) + '-cc', ext)
    return os.path.join(f'uploads/courses/videos/{instance.category.slug}/{instance.uuid}', filename)


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name) + '_' + uuid.uuid4().hex
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = slug

        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
