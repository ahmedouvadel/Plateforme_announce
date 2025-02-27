from django.urls import path
from .views import dashboard, dashboard_annonces, users, add_annonce, add_category, my_annonces, annonces_admin, update_annonce_status

urlpatterns = [
    path('dashboard/', annonces_admin, name='dashboard'),
    path('annonces/', dashboard_annonces, name='annonces'),
    path('users/', users, name='users'),
    path('categories/add/', add_category, name='add_category'),
    path('dashboard/annonces/add/', add_annonce, name='add_annonce'),
    path('annonces/moi/', my_annonces, name='mes_annonces'),
    path("annonces/update/<int:annonce_id>/", update_annonce_status, name="update_annonce_status"),
]
