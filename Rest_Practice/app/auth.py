from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication

from app.models import User


class LoginAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.query_params.get('token')
            u_id = cache.get(token)
            user = User.objects.get(pk=u_id)

            return user, token
        except Exception as e:
            return
