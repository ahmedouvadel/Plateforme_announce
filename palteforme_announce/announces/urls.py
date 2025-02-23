from django.urls import path

from .views import AnnoncesValideesListView

urlpatterns = [
    path('annonces/validees/', AnnoncesValideesListView.as_view(), name='annonces_validees'),
]