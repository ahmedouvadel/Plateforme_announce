from django.urls import path

from .views import AnnoncesValideesListView, add_category, add_annonce

urlpatterns = [
    path('annonces/validees/', AnnoncesValideesListView.as_view(), name='annonces_validees'),
    path('categories/add/', add_category, name='add_category'),
    path('annonces/add/', add_annonce, name='add_annonce'),
]