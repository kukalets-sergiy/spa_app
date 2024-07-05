from django.urls import path
from .views import HomePageView, UserRegisterView, UserLogin, UserLogoutView, UserLoginView, UserListView, \
    UserDetailView

app_name = 'user_management_app'

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('api/login/', UserLogin.as_view(), name='api-login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
