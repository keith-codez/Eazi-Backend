from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from staff.models import Customer 
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from staff.serializers import CustomerRegisterSerializer

User = get_user_model()




@api_view(['POST'])
@permission_classes([AllowAny])
def customer_register(request):
    serializer = CustomerRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response(serializer.errors, status=400)



@api_view(['POST'])
@permission_classes([AllowAny])
def customer_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)

    if user is not None:
        try:
            user.customer  # confirm this is a customer
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        except Customer.DoesNotExist:
            return Response({'error': 'Not a customer account'}, status=403)
    return Response({'error': 'Invalid credentials'}, status=401)



@api_view(['POST'])
@permission_classes([AllowAny])
def staff_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)

    if user is not None and user.is_staff:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'error': 'Invalid credentials or not staff'}, status=401)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me(request):
    user = request.user
    role = 'staff' if user.is_staff else 'customer'
    return Response({
        'username': user.get_full_name(),
        'email': user.email,
        'role': role
    })