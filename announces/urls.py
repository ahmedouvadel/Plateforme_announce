from django.urls import path

from .views import AnnoncesValideesListView, add_category, add_annonce, HomeView, AnnoncesParCategorieView, FilterAnnoncesView, annonce_detail

urlpatterns = [
    path('annonces/validees/', AnnoncesValideesListView.as_view(), name='annonces_validees'),
    path('categories/add/', add_category, name='add_category'),
    path('annonces/add/', add_annonce, name='add_annonce'),
    path('', HomeView.as_view(), name='home'),  # Charge base.html avec les catégories
    path('categories/<int:category_id>/', AnnoncesParCategorieView.as_view(), name='annonces_par_categorie'),
    path('filter/', FilterAnnoncesView.as_view(), name='filter_annonces'),
    path('annonce/<int:annonce_id>/', annonce_detail, name='annonce_detail'),

]