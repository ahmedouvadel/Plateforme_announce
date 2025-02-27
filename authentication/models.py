from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    photo_user = models.ImageField(
        upload_to='photos_users/',
        null=True,
        blank=True,
        help_text="Photo de profil de l'utilisateur"
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

class Client(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # ✅ Utilisation de settings.AUTH_USER_MODEL
        on_delete=models.CASCADE,
        related_name="client_info"
    )
    adresse = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username
