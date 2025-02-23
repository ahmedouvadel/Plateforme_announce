from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Annonce, AnnonceStatus


# Create your views here.
class AnnoncesValideesListView(View):
    def get(self, request):
        annonces = Annonce.objects.filter(statut=AnnonceStatus.VALIDEE)
        response = "".join(
            f"<br>Titre: {annonce.titre}, Prix: {annonce.prix}, Catégorie: {annonce.categorie.titre}"
            for annonce in annonces
        )
        return HttpResponse(response)