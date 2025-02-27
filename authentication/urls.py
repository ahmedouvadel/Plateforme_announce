# from django.urls import path
# from .views import login, logout_view, register
#
# urlpatterns = [
#     path('', login, name='login'),
#     path('logout/', logout_view, name='logout'),
#     path('register/', register, name='register'),
#
# ]

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import custom_redirect, register, custom_logout, profile_view, delete_account, users
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', custom_logout, name='logout'),
    path('redirect/', custom_redirect, name='custom_redirect'),
    path('profile/', profile_view, name='profile'),
    path('profile/delete/', delete_account, name='delete_account'),
    path('users/', users, name='users'),
    # Redirection après login
]
