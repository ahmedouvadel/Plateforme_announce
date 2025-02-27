from django.contrib.auth.decorators import user_passes_test
from announces.forms import AnnonceForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from announces.models import Annonce, Categories
from .forms import AnnonceForm
from .forms import CategoryForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count


@login_required
def annonces_admin(request):
    """ Affiche toutes les annonces et permet le filtrage dynamique. """

    # Filtrage basé sur le statut (si sélectionné)
    statut_filtre = request.GET.get('statut', '')

    if statut_filtre:
        annonces = Annonce.objects.filter(statut=statut_filtre)
    else:
        annonces = Annonce.objects.all()

    context = {
        "annonces": annonces,
        "total_annonces": annonces.count(),
        "annonces_validees": annonces.filter(statut='VALIDEE').count(),
        "annonces_en_attente": annonces.filter(statut='EN_ATTENTE').count(),
        "annonces_rejetees": annonces.filter(statut='REJETEE').count(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            "annonces": list(annonces.values("id", "titre", "user__username", "statut", "prix"))
        })

    return render(request, "dashboard.html", context)


@login_required
def update_annonce_status(request, annonce_id):
    """Mise à jour du statut d'une annonce via AJAX."""
    if request.method == "POST":
        new_status = request.POST.get("statut")

        annonce = get_object_or_404(Annonce, id=annonce_id)

        # Vérifier si l'utilisateur est admin pour changer le statut
        if request.user.is_superuser:
            annonce.statut = new_status
            annonce.save()
            return JsonResponse({"success": True, "message": "Statut mis à jour avec succès !"})

        return JsonResponse({"success": False, "message": "Permission refusée."}, status=403)

    return JsonResponse({"success": False, "message": "Requête invalide."}, status=400)


@login_required
def dashboard_annonces(request):
    """Affiche la liste des annonces de l'utilisateur connecté et les statistiques associées."""

    # ✅ Filtrer uniquement les annonces de l'utilisateur connecté
    user_annonces = Annonce.objects.filter(user=request.user)

    # ✅ Calculer les statistiques
    total_annonces = user_annonces.count()
    annonces_validees = user_annonces.filter(statut='validee').count()
    annonces_en_attente = user_annonces.filter(statut='en_attente').count()
    annonces_rejetees = user_annonces.filter(statut='rejete').count()

    context = {
        "annonces": user_annonces,
        "total_annonces": total_annonces,
        "annonces_validees": annonces_validees,
        "annonces_en_attente": annonces_en_attente,
        "annonces_rejetees": annonces_rejetees,
    }

    return render(request, 'annonces.html', context)


def is_admin(user):
    return user.is_authenticated and user.role == "admin"

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def annonces(request):
    return render(request, 'annonces.html')

@login_required
@user_passes_test(is_admin)  # Seuls les admins peuvent voir cette page
def users(request):
    return render(request, 'users.html')

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect

def est_admin(user):
    return user.is_authenticated and user.role == "admin"

@user_passes_test(est_admin)
def valider_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    annonce.accepter()
    return redirect('liste_annonces_admin')

@user_passes_test(est_admin)
def rejeter_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    annonce.rejeter()
    return redirect('liste_annonces_admin')

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Catégorie ajoutée avec succès !")
            return redirect('add_annonce')  # Redirection après ajout
        else:
            messages.error(request, "❌ Erreur lors de l'ajout de la catégorie. Vérifiez les champs.")
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'form': form})

@login_required  # ✅ Vérifie que l'utilisateur est connecté
def add_annonce(request):
    if request.method == 'POST':
        form = AnnonceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user)  # ✅ Associe l'annonce à l'utilisateur connecté
            messages.success(request, "✅ Annonce ajoutée avec succès ! En attente de validation.")
            return redirect('annonces_validees')  # ✅ Redirige après l'ajout
        else:
            messages.error(request, "❌ Une erreur s'est produite lors de l'ajout de l'annonce.")
    else:
        form = AnnonceForm()

    return render(request, 'add_annonce.html', {'form': form})

@login_required
def my_annonces(request):
    annonces = Annonce.objects.filter(user=request.user)  # ✅ Filtre par utilisateur connecté
    return render(request, 'mes_annonces.html', {'annonces': annonces})
