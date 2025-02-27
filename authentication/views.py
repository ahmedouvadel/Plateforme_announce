from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages

User = get_user_model()

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User  # Assurez-vous que User est bien importé
from django.core.files.storage import default_storage
from authentication.models import Client  # ✅ Corrige l'import

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        role = request.POST.get('role', 'client')  # Valeur par défaut : "client"
        photo = request.FILES.get('photo')  # Récupérer la photo de profil

        # Récupération des informations supplémentaires
        telephone = request.POST.get('telephone', '').strip()
        adresse = request.POST.get('adresse', '').strip()

        # Vérification des champs vides
        if not username or not email or not password1 or not password2 or not telephone or not adresse:
            messages.error(request, "Tous les champs sont obligatoires.")
            return redirect('register')

        # Vérification du mot de passe
        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('register')

        # Vérification si l'utilisateur existe déjà
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect('register')

        # Gestion de la photo de profil
        if photo:
            photo_path = default_storage.save(f'profile_pictures/{photo.name}', photo)
        else:
            photo_path = "default/avatar.png"  # Image par défaut si l'utilisateur ne met pas de photo

        # Création de l'utilisateur
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            role=role,
            photo_user=photo_path  # Assurez-vous que ce champ existe dans votre modèle User
        )
        if role == 'client':
            Client.objects.create(user=user, adresse=adresse, telephone=telephone)  # Créer un client lié à cet utilisateur

        # Connexion automatique après l'inscription
        login(request, user)
        messages.success(request, "Inscription réussie ! Bienvenue, " + user.username)

        return redirect('login')  # Redirection après l'inscription

    return render(request, 'registre.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages



# def login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password_usr')  # Vérifie que le champ du formulaire a bien ce nom
#
#         # Vérifier si un utilisateur avec cet email existe
#         try:
#             user_instance = User.objects.get(email=email)
#         except User.DoesNotExist:
#             messages.error(request, "Utilisateur non trouvé.")
#             return redirect('login')
#
#         # Authentifier l'utilisateur avec le mot de passe
#         user = authenticate(request, username=user_instance.username, password=password)
#
#         if user is not None:
#             # Vérifier si l'utilisateur est admin mais pas encore validé
#             if user.role == 'admin' and not user.is_staff:
#                 messages.error(request, "Votre compte nécessite une validation par un administrateur.")
#                 return redirect('login')
#
#             # Connecter l'utilisateur
#             auth_login(request, user)
#             messages.success(request, f"Bienvenue, {user.username} !")
#
#             # Redirection selon le rôle de l'utilisateur
#             if user.role == 'admin':
#                 return redirect('register')  # Tableau de bord admin
#             elif user.role == 'vendeur':
#                 return redirect('register')  # Tableau de bord vendeur
#             elif user.role == 'client':
#                 return redirect('AnnoncesValideesListView')  # Fonction pour insérer une réclamation
#             else:
#                 return redirect('home')  # Redirection par défaut si aucun rôle ne correspond
#
#         else:
#             messages.error(request, "Mot de passe incorrect.")
#             return redirect('login')
#
#     return render(request, 'login.html')


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def custom_redirect(request):
    user = request.user
    if user.role == 'admin':
        return redirect('add_annonce')  # Tableau de bord admin
    elif user.role == 'client':
        return redirect('add_annonce')  # Page client
    else:
        return redirect('add_annonce')  # Redirection par défaut

def logout_view(request):
    next_page = request.GET.get('next', '')  # Récupère l'URL précédente
    logout(request)  # Déconnecte l'utilisateur
    return redirect(next_page if next_page else 'home')  # Redirige vers la même page ou vers home
