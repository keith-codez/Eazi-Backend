from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from .serializers import AgentRegistrationSerializer, LoginSerializer, CustomerSerializer, AgencyRegistrationSerializer, CustomerRegistrationSerializer 
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Customer
from staff.models import Booking 
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.views import APIView
from django.db.models import Sum, F
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from regulator.authentication import CookieJWTAuthentication


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
            }
        }, status=status.HTTP_200_OK)

        # ✅ Set secure HttpOnly cookies with the actual tokens
        response.set_cookie(
            key='access_token',
            value=access,
            httponly=True,
            secure=True,  # Set to False in local dev if not using HTTPS, but must be True in production
            samesite='None',  # Needed for cross-site usage like React frontend
            path='/'
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite='None',
            path='/'
        )

        return response


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, "agent"):
            print("user agent seen")
            agent = user.agent
            serializer.save(related_agent=agent, related_agency=agent.agency)
        else:
            serializer.save()



    def update(self, request, *args, **kwargs):
        """Handles updating customer, including driver's license file handling"""
        customer = self.get_object()

        # Check if frontend sent a DELETE request for the driver's license
        if request.data.get("drivers_license") == "DELETE":
            customer.delete_drivers_license()

        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['DELETE'])
    def delete_drivers_license(self, request, pk=None):
        """Deletes only the driver's license image"""
        customer = self.get_object()
        customer.delete_drivers_license()
        return Response({"message": "Driver's license deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        """Returns analytics for a specific customer."""
        customer = self.get_object()

        bookings = Booking.objects.filter(customer=customer)

        total_bookings = bookings.count()

        # Correct calculation for total spent
        total_spent = bookings.aggregate(
            total=Sum(F('booking_amount') + F('booking_deposit') - F('discount_amount'))
        )['total'] or 0

        mileage_result = bookings.aggregate(Sum('estimated_mileage'))
        total_mileage = mileage_result.get('estimated_mileage__sum', 0)
        
        return Response({
            "totalBookings": total_bookings,
            "totalSpent": round(total_spent, 2),
            "totalMileage": total_mileage
        })

    def get_queryset(self):
        user = self.request.user

        if user.role == 'agent':
            return Customer.objects.filter(agents__user=user)
        elif user.role == 'agency':
            return Customer.objects.filter(related_agency__created_by=user)
        elif user.role == 'admin':
            return Customer.objects.all()
        return Customer.objects.none()


class CustomerRegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = CustomerRegistrationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Customer registered successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AgentRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = AgentRegistrationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Agent registered successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgencyRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = AgencyRegistrationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Agency registered successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.get_role(),
    })


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token', None)

        if not refresh_token:
            return Response({"detail": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={"refresh": refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        access_token = serializer.validated_data["access"]

        response = Response({"access": access_token}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='None',
            path='/',
        )
        return response
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return response