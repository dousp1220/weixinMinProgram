# coding: utf-8
import datetime

from django.contrib.auth.models import User


def user_to_payload(user):
    exp = datetime.datetime.now() + datetime.timedelta(seconds=3600 * 7)
    return {
        'user_id': str(user.id),
        'exp': exp
    }


def payload_to_user(payload):
    if not payload:
        return None
    user_id = payload.get('user_id')
    user = User.objects.get(id=user_id)
    return user
