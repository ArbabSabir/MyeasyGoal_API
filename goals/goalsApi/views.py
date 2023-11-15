from django.shortcuts import render
from rest_framework import viewsets,status
from .models import Goal_model
from .serializers import Gole_Seri,UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth import authenticate,login
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# Create your views here.
User = get_user_model()

class Goal_view(viewsets.ModelViewSet):
    queryset=Goal_model.objects.all()
    serializer_class=Gole_Seri

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Assign the current user to the goal
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    

@api_view(['POST'])
@permission_classes([AllowAny])
def Register_user(request):
    username=request.data.get('username')
    email=request.data.get('email')
    password=request.data.get('password')

    if not username or not email or not password:
        return Response({'message': 'Please provide username, email, and password'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        validate_email(email)
    except ValidationError:
           
        return Response({
               'message': 'Invalid email format',
                'sucess': False
           }, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'message': 'Email already exists'}, status=400)
    
    user=User.objects.create_user(username=username,email=email,password=password)
    if user:
        auth_user= authenticate(username=username,password=password)
        if auth_user:
            login(request,auth_user)
            token, created = Token.objects.get_or_create(user=auth_user)
            return Response({'message':"User Created"},headers={'token': token.key}, status=200)
        
    return Response({'message': 'Unable to register user'}, status=400)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer