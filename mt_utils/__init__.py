import hashlib
import json
import uuid
import os

import string
from random import random

import requests
from django.utils.text import slugify


def create_hash(payload: str):
    return hashlib.sha256(bytes(payload, 'ascii')).hexdigest()


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


def get_package_feature_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/packages/images', filename)


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
    return os.path.join(f'uploads/courses/videos/{instance.category.name}/{uuid_}', filename)


def get_course_video_thumbnail_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (str(instance.uuid) + '-thumbnail', ext)
    return os.path.join(f'uploads/courses/videos/{instance.category.name}/{instance.uuid}', filename)


def get_course_video_cc_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (str(instance.uuid) + '-cc', ext)
    return os.path.join(f'uploads/courses/videos/{instance.category.name}/{instance.uuid}', filename)


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        print(instance)
        slug = slugify(instance.name) + '_' + uuid.uuid4().hex
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = slug

        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def email_raw(from_email, from_name, to, subject, text, html):
    requests.post(
        'https://api.mailjet.com/v3.1/send',
        auth=(os.environ.get('EMAIL_USER'), os.environ.get('EMAIL_PASS')),
        data=json.dumps({
            "Messages": [
                {
                    "From": {
                        "Email": from_email,
                        "Name": from_name
                    },
                    "To": to,
                    "Subject": subject,
                    "TextPart": text,
                    "HTMLPart": html
                }
            ]
        }),
        headers={'Content-Type': 'application/json'}
    )


def email(serializer, user_id):
    print(f"Serializer valid is ===> {serializer.is_valid()}")
    if serializer.is_valid():
        email_ = requests.post(
            'https://api.mailjet.com/v3.1/send',
            auth=(os.environ.get('EMAIL_USER'), os.environ.get('EMAIL_PASS')),
            data=json.dumps({
                "Messages": [
                    {
                        "From": {
                            "Email": serializer.validated_data["from_email"],
                            "Name": serializer.validated_data["from_name"]
                        },
                        "To": [
                            {
                                "Email": serializer.validated_data["to_email"],
                                "Name": serializer.validated_data["to_name"]
                            }
                        ],
                        "Subject": serializer.validated_data["subject"],
                        "TextPart": serializer.validated_data["text_body"],
                        "HTMLPart": serializer.validated_data["html_body"]
                    }
                ]
            }),
            headers={'Content-Type': 'application/json'}
        )
        data = email_.json()
        print("Saving to data base")
        if email_.status_code == 200:
            print("Email sent")
            to = data["Messages"][0]["To"][0]
            serializer.save(user_id=user_id, message_uuid=to["MessageUUID"], message_id=to["MessageID"],
                            status=True)
        else:
            print("Email failed to sent")
            serializer.save(user_id=user_id, status=False, status_code=email_.status_code,
                            error_message=data["ErrorMessage"])


CARD_IMAGES = {
    'VISA': 'https://usa.visa.com/dam/VCOM/regional/lac/ENG/Default/Partner%20With%20Us/Payment%20Technology/visapos/full-color-800x450.jpg',
    'AMEX': 'https://about.americanexpress.com/files/images/brand_imagery/AXP_BlueBoxLogo_EXTRALARGEscale_RGB_DIGITAL_1600x1600.png',
    'DINERS': 'https://www.dinersclub.com/assets/images/media-kit/acceptance-marks-logos-acceptance-marks.jpg',
    'DISCOVER': 'https://www.discoverglobalnetwork.com/assets/img/free-signage-logos/discover_logo.jpg',
    'JCB': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/JCB_logo.svg/993px-JCB_logo.svg.png',
    'MASTERCARD': 'https://brand.mastercard.com/content/dam/mccom/brandcenter/thumbnails/mastercard_vrt_pos_92px_2x.png',
    'UNKNOWN': 'https://occ-0-448-2705.1.nflxso.net/dnm/api/v6/LmEnxtiAuzezXBjYXPuDgfZ4zZQ/AAAABZ920_DLQ-Re8Pl8IkAwVpkXNTdWMzvkv7ZVYrcF900fDnoWAEKxLknECbhuYN1d5nXRydU83GEaZUMmVxZIV5UD2Z59-ynYBCat.png?r=9d3',
    'UNIONPAY': 'https://seeklogo.com/images/U/unionpay-logo-3E20E52659-seeklogo.com.png',
}
