from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Annonce, AnnonceStatus, Categories
from django.shortcuts import render, redirect
from .forms import CategoryForm, AnnonceForm

# Create your views here.
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


class HomeView(View):
    def get(self, request):
        categories = Categories.objects.all()
        annonces = Annonce.objects.filter(statut=AnnonceStatus.VALIDEE)
        annonces_payees = Annonce.objects.filter(is_paid=True, statut="VALIDEE")
        return render(request, 'base.html', {'categories': categories, 'annonces': annonces, 'annonces_payees': annonces_payees})



class AnnoncesParCategorieView(View):
    def get(self, request, category_id):
        categorie = get_object_or_404(Categories, id=category_id)
        annonces = Annonce.objects.filter(categorie=categorie, statut=AnnonceStatus.VALIDEE)

        # Vérifier si c'est une requête AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            annonces_data = [
                {
                    'titre': annonce.titre,
                    'prix': annonce.prix,
                    'categorie': annonce.categorie.titre,
                    'description': annonce.description,
                    'image': annonce.image.url if annonce.image else None
                }
                for annonce in annonces
            ]
            return JsonResponse({'annonces': annonces_data})

        return render(request, "liste_annonces.html", {"annonces": annonces, "categorie": categorie})

class FilterAnnoncesView(View):
    def get(self, request):
        prix_min = request.GET.get('prix_min')
        prix_max = request.GET.get('prix_max')
        categorie_id = request.GET.get('categorie')

        annonces = Annonce.objects.filter(statut="VALIDEE")

        if prix_min:
            annonces = annonces.filter(prix__gte=prix_min)
        if prix_max:
            annonces = annonces.filter(prix__lte=prix_max)
        if categorie_id and categorie_id != "all":
            annonces = annonces.filter(categorie_id=categorie_id)

        categories = Categories.objects.all()

        # Si la requête est AJAX, ne renvoyer que la partie des annonces
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return render(request, "liste_annonces.html", {"annonces": annonces})

        return render(request, 'filter.html', {"annonces": annonces, "categories": categories})


def annonce_detail(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)

    # Exemple : Récupérer le nombre de vues (implique une colonne `views` dans le modèle)
    annonce.views += 1
    annonce.save()

    return render(request, 'annonce_detail.html', {'annonce': annonce})