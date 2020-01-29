from rest_framework.throttling import UserRateThrottle

from app.models import User


class Throttle(UserRateThrottle):

    scope = 'user'

    def get_cache_key(self, request, view):
        if isinstance(request.user, User):
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
