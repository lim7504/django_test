from urllib.request import urlopen
from django.core.files.base import ContentFile
from social_django.models import UserSocialAuth
from django.contrib.auth.models import User

USER_FIELDS = ['email', 'nickname']


def create_user(strategy, details, user=None, *args, **kwargs):
    print(details)
    print(kwargs)

    if user:
        # if user.id == 1:
        #     su = UserSocialAuth.objects.get(uid=details['email'])
        #     u = User.objects.get(email=details['email'])
        #     if su is not None:
        #         su.user_id = u.pk
        #         su.save()
        return {'is_new': False}

    fields = {'email': details.get('email'), 'nickname': details.get('username')}

    # user = User(email=details.get('email')
    #             , password="999999"
    #             , username=details.get('username'))
    # user.save()

    if not fields:
        return

    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }

# def update_avatar(backend, response, uid, user, *args, **kwargs):
#     if backend.name == 'facebook':
#         url = &amp;quot;http://graph.facebook.com/%s/picture?type=large&amp;quot; % response['id']
#         avatar = urlopen(url)
#         user.avatar.save(slugify(user.email + &amp;quot; social&amp;quot;) + '.jpg', ContentFile(avatar.read()))
#         user.save()