from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Annonce, AnnonceStatus, Categories
from django.shortcuts import render, redirect
from .forms import CategoryForm, AnnonceForm

# Create your views here.
def categories_dropdown(request):
    categories = Categories.objects.all()  # Récupère toutes les catégories

    # Afficher les catégories dans la console pour vérifier
    print("Catégories récupérées :", list(categories))

    return render(request, 'categories_dropdown.html', {'categories': categories})

class AnnoncesValideesListView(View):
    def get(self, request):
        annonces = Annonce.objects.filter(statut=AnnonceStatus.VALIDEE)
        return render(request, "liste_annonces.html", {"annonces": annonces})



# View to add a category
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_annonce')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

# View to add an announcement
def add_annonce(request):
    if request.method == 'POST':
        form = AnnonceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Automatically sets "En attente"
            return redirect('annonces_validees')
    else:
        form = AnnonceForm()

    return render(request, 'add_annonce.html', {'form': form})
