from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View

class PasswordResetConfirmView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Get the uid and token from the request body
            uidb64 = request.data.get('uid')
            token = request.data.get('token')
            new_password = request.data.get('new_password')

            # Decode uidb64 to get the user ID
            uid = urlsafe_base64_decode(uidb64).decode()

            # Get the user instance
            user = User.objects.get(pk=uid)

            # Verify the token
            if not default_token_generator.check_token(user, token):
                return JsonResponse({"error": "Invalid token"}, status=400)

            # Validate the new password
            try:
                password_validation.validate_password(new_password, user)
            except ValidationError as e:
                return JsonResponse({"error": str(e)}, status=400)

            # Set the new password and save the user
            user.set_password(new_password)
            user.save()

            return JsonResponse({"message": "Password successfully reset!"}, status=200)

        except Exception as e:
            return JsonResponse({"error": "Something went wrong. Please try again."}, status=500)



User = get_user_model()

@api_view(["POST"])
def register_manager(request):
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_manager(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(request, username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }, status=status.HTTP_200_OK)

    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
