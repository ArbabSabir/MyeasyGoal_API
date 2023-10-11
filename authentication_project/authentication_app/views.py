from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from .models import Goal
from .serializers import UserSerializer, RegistrationSerializer, GoalSerializer
from rest_framework.permissions import IsAuthenticated

class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            list_data = {"success" : True, "message":"User registered successfully", "code":"Register_API", "data":serializer.data}
            return Response(list_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            list_data = {"success" : True, "message":"User login successfully", "code":"Login_API", "data":user.data}
            return Response(list_data,headers={'token': token.key},status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        list_data = {"success" : True, "message":"User loout successfully", "code":"Logout_API"}
        return Response(list_data,status=status.HTTP_200_OK)

class GoalListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        goals = Goal.objects.filter(user=request.user)
        serializer = GoalSerializer(goals, many=True)
        list_data = {"success" : True, "message":"Goal list get successfully", "code":"Goal_list_API","data":serializer.data}
        return Response(list_data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GoalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            list_data = {"success" : True, "message":"Goal created successfully", "code":"Goal_create_API","data":serializer.data}
            return Response(list_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoalDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Goal.objects.get(pk=pk)
        except Goal.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        goal = self.get_object(pk)
        serializer = GoalSerializer(goal)
        
        list_data = {"success" : True, "message":" Get goals Successfuly ", "code":"Goal_get_Api ", "data":serializer.data}

        return Response(list_data)

    def put(self, request, pk):
        goal = self.get_object(pk)
        serializer = GoalSerializer(goal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            list_data = {"success" : True, "message":"Update goals Successfuly ", "code":"Goal_PUT_API", "data":serializer.data}
            return Response(list_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        goal = self.get_object(pk)
        goal.delete()
        list_data = {"success" : True, "message":"Delete goals Successfuly ", "code":"Goal_get_Api "}
        return Response(list_data,status=status.HTTP_200_OK)
