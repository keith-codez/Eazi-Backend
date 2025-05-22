from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Try to get the token from the cookie
        raw_token = request.COOKIES.get('access_token')
        if raw_token is None:
            return None

        # If a token is found, use the parent method to validate it
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # Disable CSRF check