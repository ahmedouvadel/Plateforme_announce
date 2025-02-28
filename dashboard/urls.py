from django.urls import path
from .views import dashboard, ajouter_paiement, liste_paiements, dashboard_annonces, modifier_annonce, supprimer_annonce, rejeter_annonce, add_annonce, valider_annonce, add_category, my_annonces, annonces_admin, update_annonce_status, statistics_view, marquer_annonce_payee, refuser_paiement, valider_paiement, payer_annonce

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
    path('annonce_payee/<int:annonce_id>/', marquer_annonce_payee, name='marquer_annonce_payee'),
    path('modifier_annonce/<int:annonce_id>/', modifier_annonce, name='modifier_annonce'),
    path('supprimer_annonce/<int:annonce_id>/', supprimer_annonce, name='supprimer_annonce'),
    path("paiements/", liste_paiements, name="liste_paiements"),
    path("paiement/ajouter/", ajouter_paiement, name="ajouter_paiement"),
    path("paiement/valider/<int:paiement_id>/", valider_paiement, name="valider_paiement"),
    path("paiement/refuser/<int:paiement_id>/", refuser_paiement, name="refuser_paiement"),
    path("paiement/payer/<int:annonce_id>/", payer_annonce, name="payer_annonce"),

]
