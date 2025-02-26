from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

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
