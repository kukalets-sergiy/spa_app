from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views import generic
from django.views.generic import TemplateView
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserDataSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.urls import reverse
from .models import UserData

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()


class HomePageView(generic.TemplateView):
    template_name = "user_management/homepage.html"


class UserListView(generics.ListAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer
    lookup_field = 'pk'


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)  # Create or get existing token
        return Response({
            "token": token.key,
            "redirect_url": redirect(reverse('user_management_app:homepage'))  # Replace 'homepage' with your actual homepage URL name
        }, status=status.HTTP_201_CREATED)


class UserLoginView(TemplateView):
    template_name = "login/login.html"


class UserLogin(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({
                'token': token,
                'redirect_url': reverse('user_management_app:homepage')
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'redirect_url': reverse('user_management_app:login')}, status=status.HTTP_200_OK)
