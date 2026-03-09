from rest_framework.throttling import SimpleRateThrottle

class AuthThrottle(SimpleRateThrottle):

    scope = "auth"

    def get_cache_key(self, request, view):

        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return f"throttle_auth_{ident}"