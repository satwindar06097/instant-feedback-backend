from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from testimonial.serializers import UserSerializer, UserSerializerWithToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework import status

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def registerUser(request):
    data = request.data
    email = data.get('email')
    
    # Check if the user with this email already exists
    if User.objects.filter(email=email).exists():
        return Response({'detail': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create user
    user = User.objects.create(
        first_name=data.get('name'),
        username=email,
        email=email,
        password=make_password(data.get('password'))
    )
    
    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def allUser(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    data = request.data
    
    # Update user profile
    user.first_name = data.get('name', user.first_name)
    user.username = data.get('email', user.username)
    user.email = data.get('email', user.email)
    
    # Update password if provided
    if data.get('password'):
        user.password = make_password(data['password'])
    
    user.save()
    
    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
