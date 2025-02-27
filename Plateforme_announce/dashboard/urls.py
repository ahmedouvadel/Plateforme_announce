from django.urls import path
from .views import dashboard, dashboard_annonces, rejeter_annonce, add_annonce, valider_annonce, add_category, my_annonces, annonces_admin, update_annonce_status, statistics_view

urlpatterns = [
    path('dashboard/', annonces_admin, name='dashboard'),
    path('annonces/', dashboard_annonces, name='annonces'),

    path('categories/add/', add_category, name='add_category'),
    path('dashboard/annonces/add/', add_annonce, name='add_annonce'),
    path('annonces/moi/', my_annonces, name='mes_annonces'),
    path("annonces/update/<int:annonce_id>/", update_annonce_status, name="update_annonce_status"),
    path('statistics/', statistics_view, name='statistics'),
    path('dashboard/valider_annonce/<int:annonce_id>/', valider_annonce, name='valider_annonce'),
    path('dashboard/rejeter_annonce/<int:annonce_id>/', rejeter_annonce, name='rejeter_annonce'),
]
