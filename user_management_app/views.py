from django.shortcuts import redirect, render
from django.views import generic, View
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserDataSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework import generics, status
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
    template_name = "auth/register.html"
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        form = self.serializer_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        headers = self.get_success_headers(serializer.data)
        return Response({
            "token": token.key,
            "redirect_url": reverse('user_management_app:homepage')
        }, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginView(View):
    permission_classes = [AllowAny]
    template_name = "auth/login.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return redirect('user_management_app:homepage')
        return render(request, self.template_name, {'errors': serializer.errors})


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'redirect_url': reverse('user_management_app:auth')}, status=status.HTTP_200_OK)
