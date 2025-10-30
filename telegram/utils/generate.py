from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import uuid
from telegram.models import Token
from telegram.utils.hash import hash_value
# adjust to your model

def generate_one_time_link(user, expires_in_minutes=10):
    token_obj = Token.objects.create(
        token=uuid.uuid4(),
        creator=user,
    )

    # because you used app_name = 'telegram' and name='users_list'
    url_path = reverse('telegram:users_list', args=[token_obj.token, hash_value(user.chat_id)])
    absolute_link = f"{settings.SITE_URL}{url_path}"

    return absolute_link, token_obj
def generate_one_time_admin_link(user, expires_in_minutes=10):
    token_obj = Token.objects.create(
        token=uuid.uuid4(),
        creator=user,
    )

    # because you used app_name = 'telegram' and name='users_list'
    url_path = reverse('telegram:admins_list', args=[token_obj.token, hash_value(user.chat_id)])
    absolute_link = f"{settings.SITE_URL}{url_path}"

    return absolute_link, token_obj