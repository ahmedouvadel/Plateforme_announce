from django.urls import path
from .views import dashboard, annonces, users

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('annonces/', annonces, name='annonces'),
    path('users/', users, name='users'),  # Accessible uniquement par Admin
]
