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
from django.utils.timezone import now

def is_admin(user):
    return user.is_authenticated and user.role == "admin"

@user_passes_test(is_admin)
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


@user_passes_test(is_admin)
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




@user_passes_test(is_admin)
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def annonces(request):
    return render(request, 'annonces.html')

 # Seuls les admins peuvent voir cette page


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from announces.models import Categories, Annonce, AnnonceStatus

def est_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(est_admin)
def valider_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    annonce.statut = AnnonceStatus.VALIDEE
    annonce.save()
    messages.success(request, "Annonce validée avec succès !")
    return redirect('dashboard')

@user_passes_test(est_admin)
def rejeter_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    annonce.statut = AnnonceStatus.REJETEE
    annonce.save()
    messages.error(request, "Annonce rejetée avec succès !")
    return redirect('dashboard')

@login_required
def marquer_annonce_payee(request, annonce_id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Méthode non autorisée."}, status=405)

    annonce = get_object_or_404(Annonce, id=annonce_id)

    if annonce.paiement_statut == "NON_PAYEE":
        annonce.paiement_statut = "PAYEE"
        annonce.save()
        return JsonResponse({"success": True, "message": "Annonce marquée comme payée."})
    else:
        return JsonResponse({"success": False, "message": "Cette annonce est déjà payée."}, status=400)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from announces.models import GroupCategorie, Categories


@login_required
def add_category(request):
    if request.method == 'POST':
        nom = request.POST.get('titre')
        group_id = request.POST.get('group_id')

        if nom and group_id:
            try:
                group = GroupCategorie.objects.get(id=group_id)
                Categories.objects.create(titre=nom, group=group)
                messages.success(request, "✅ Catégorie ajoutée avec succès !")
                return redirect('add_annonce')  # Redirection après ajout
            except GroupCategorie.DoesNotExist:
                messages.error(request, "❌ Le groupe de catégorie sélectionné n'existe pas.")
        else:
            messages.error(request, "❌ Veuillez remplir tous les champs.")

    groupes = GroupCategorie.objects.all()  # Récupérer les groupes
    return render(request, 'add_category.html', {'groupes': groupes})


from django.shortcuts import render, redirect
from announces.models import Categories, Annonce
from django.contrib import messages

@login_required
def add_annonce(request):
    categories = Categories.objects.all()

    if request.method == "POST":
        print(request.POST)  # ➜ Debug pour voir les valeurs envoyées
        print(request.FILES)  # ➜ Debug pour voir les fichiers envoyés

        titre = request.POST.get("titre")
        description = request.POST.get("description")
        prix = request.POST.get("prix")
        image = request.FILES.get("image")
        categorie_id = request.POST.get("categorie")

        if not titre or not description or not prix or not categorie_id:
            messages.error(request, "Tous les champs sont obligatoires.")
        else:
            try:
                categorie = Categories.objects.get(id=categorie_id)
                annonce = Annonce.objects.create(
                    user=request.user,
                    titre=titre,
                    description=description,
                    prix=prix,
                    image=image,
                    categorie=categorie,
                )
                annonce.save()
                messages.success(request, "Annonce ajoutée avec succès !")
                return redirect("annonces")
            except Categories.DoesNotExist:
                messages.error(request, "Catégorie invalide.")

    return render(request, "add_annonce.html", {"categories": categories})


@login_required
def my_annonces(request):
    annonces = Annonce.objects.filter(user=request.user)  # ✅ Filtre par utilisateur connecté
    return render(request, 'annonces.html', {'annonces': annonces})


from django.shortcuts import render

from authentication.models import User
from announces.models import Annonce

@user_passes_test(lambda u: u.is_superuser)
def statistics_view(request):
    total_users = User.objects.count()
    total_clients = User.objects.filter(role="client").count()
    total_admins = User.objects.filter(role="admin").count()
    total_annonces = Annonce.objects.count()
    annonces_validees = Annonce.objects.filter(statut="VALIDEE").count()
    annonces_en_attente = Annonce.objects.filter(statut="EN_ATTENTE").count()
    annonces_rejetees = Annonce.objects.filter(statut="REJETEE").count()

    context = {
        "total_users": total_users,
        "total_clients": total_clients,
        "total_admins": total_admins,
        "total_annonces": total_annonces,
        "annonces_validees": annonces_validees,
        "annonces_en_attente": annonces_en_attente,
        "annonces_rejetees": annonces_rejetees,
    }

    return render(request, "statistics.html", context)


@login_required
def supprimer_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id, user=request.user)
    annonce.delete()
    messages.success(request, "Annonce supprimée avec succès !")
    return redirect('mes_annonces')


@login_required
def modifier_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id, user=request.user)
    categories = Categories.objects.all()

    if request.method == "POST":
        titre = request.POST.get("titre")
        description = request.POST.get("description")
        prix = request.POST.get("prix")
        image = request.FILES.get("image")
        categorie_id = request.POST.get("categorie")

        if not titre or not description or not prix or not categorie_id:
            messages.error(request, "Tous les champs sont obligatoires.")
        else:
            categorie = Categories.objects.get(id=categorie_id)
            annonce.titre = titre
            annonce.description = description
            annonce.prix = prix
            if image:
                annonce.image = image
            annonce.categorie = categorie
            annonce.statut = AnnonceStatus.EN_ATTENTE  # Réinitialisation du statut
            annonce.save()
            messages.success(request, "Annonce modifiée avec succès et remise en attente de validation.")
            return redirect("mes_annonces")

    return render(request, "modifier_annonce.html", {"annonce": annonce, "categories": categories})

from django.shortcuts import render
from .models import Paiement

@user_passes_test(lambda u: u.is_superuser)
def liste_paiements(request):
    paiements = Paiement.objects.all()
    return render(request, 'liste_paiements.html', {'paiements': paiements})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.utils.timezone import now
from .models import Paiement
from announces.models import Annonce
import uuid
@login_required
def ajouter_paiement(request, annonce_id):
    if request.method == "POST":
        annonce = get_object_or_404(Annonce, id=annonce_id)

        banque = request.POST.get("banque")
        numero_facture = request.POST.get("numero_facture")
        justificatif = request.FILES.get("justificatif")

        if not banque or not numero_facture or not justificatif:
            return JsonResponse({"success": False, "error": "Tous les champs sont obligatoires."})

        paiement = Paiement.objects.create(
            numero_paiement=uuid.uuid4().hex[:10].upper(),
            annonce=annonce,
            utilisateur=request.user,
            banque=banque,
            numero_facture=numero_facture,
            justificatif=justificatif,
            date_paiement=now(),
            statut="EN_ATTENTE",
        )

        return JsonResponse({"success": True, "message": "Paiement ajouté avec succès !"})

    return JsonResponse({"success": False, "error": "Requête invalide."})

@login_required
def ajouter_paiement(request):
    """Vue pour soumettre un paiement."""
    if request.method == 'POST':
        annonce_id = request.POST.get('annonce_id')
        banque = request.POST.get('banque')
        numero_facture = request.POST.get('numero_facture')
        justificatif = request.FILES.get('justificatif')

        # Vérifier si l'annonce existe
        annonce = get_object_or_404(Annonce, id=annonce_id)

        # Vérifier si un paiement existe déjà pour cette annonce
        if Paiement.objects.filter(annonce=annonce).exists():
            return JsonResponse({"success": False, "message": "Paiement déjà soumis pour cette annonce."}, status=400)

        # Création du paiement
        paiement = Paiement.objects.create(
            numero_paiement=uuid.uuid4().hex[:10].upper(),
            annonce=annonce,
            utilisateur=request.user,
            banque=banque,
            numero_facture=numero_facture,
            justificatif=justificatif,
            date=now(),
            statut="EN_ATTENTE",
        )

        messages.success(request, "Paiement soumis avec succès !")
        return redirect('annonces')  # 🔥 Redirection après paiement

    messages.error(request, "Requête invalide.")
    return redirect('annonces')  # 🔥 Redirection en cas d'erreur

@user_passes_test(lambda u: u.is_superuser)
def liste_paiements(request):
    paiements = Paiement.objects.all()
    return render(request, "liste_paiements.html", {"paiements": paiements})

@user_passes_test(lambda u: u.is_superuser)
def payer_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)

    if request.method == "POST":
        banque = request.POST.get("banque")
        numero_facture = request.POST.get("numero_facture")
        justificatif = request.FILES.get("justificatif")

        paiement = Paiement.objects.create(
            annonce=annonce,
            utilisateur=request.user,
            banque=banque,
            numero_facture=numero_facture,
            justificatif=justificatif,
            statut="EN_ATTENTE"
        )

        messages.success(request, "Paiement soumis pour validation.")
        return redirect("dashboard")

    return redirect("dashboard")


@user_passes_test(lambda u: u.is_superuser)
def valider_paiement(request, paiement_id):
    """Valider un paiement"""
    paiement = get_object_or_404(Paiement, id=paiement_id)
    paiement.statut = "VALIDÉ"
    paiement.save()
    messages.success(request, "Paiement validé avec succès.")
    return redirect('liste_paiements')


@user_passes_test(lambda u: u.is_superuser)
def refuser_paiement(request, paiement_id):
    """Refuser un paiement"""
    paiement = get_object_or_404(Paiement, id=paiement_id)
    paiement.statut = "REFUSÉ"
    paiement.save()
    messages.error(request, "Paiement refusé.")
    return redirect('liste_paiements')