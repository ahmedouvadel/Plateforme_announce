from django.urls import path

from .views import AnnoncesValideesListView, HomeView, AnnoncesParCategorieView, FilterAnnoncesView, annonce_detail, mes_favoris, ajouter_favori, retirer_favori

urlpatterns = [
    path('annonces/validees/', AnnoncesValideesListView.as_view(), name='annonces_validees'),
    path('', HomeView.as_view(), name='home'),
    path('categories/<int:category_id>/', AnnoncesParCategorieView.as_view(), name='annonces_par_categorie'),
    path('filter/', FilterAnnoncesView.as_view(), name='filter_annonces'),
    path('annonce/<int:annonce_id>/', annonce_detail, name='annonce_detail'),
    path('ajouter_favori/<int:annonce_id>/', ajouter_favori, name='ajouter_favori'),
    path('mes-favoris/', mes_favoris, name='mes_favoris'),
    path('retirer_favori/<int:annonce_id>/', retirer_favori, name='retirer_favori'),

]