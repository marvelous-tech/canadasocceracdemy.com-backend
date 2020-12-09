from django.shortcuts import render


# Create your views here.


def get_default_contexts(user):
    user_profile = user.user_profile
    return {
        'email': user.email,
        'phone': user_profile.phone,
        'name': f'{user.first_name} {user.last_name}',
        'type': user_profile.type,
        'profile_image': user_profile.profile_image,
        'valid': user_profile.is_active is True and user_profile.is_deleted is False and user_profile.is_expired is False and user_profile.email_verified is True
    }
