from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # ✅ If user is already authenticated (via session), leave them alone
        if request.user.is_authenticated:
            return

        token = request.COOKIES.get('access_token')
        if not token:
            return  # Leave request.user as-is (AnonymousUser)

        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)
            request.user = user
        except Exception:
            # Don't set request.user = AnonymousUser() here — Django already defaults it
            pass
