from django.contrib.auth.models import AbstractUser
from django.db import models


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
        help_text="Photo de profil de l'utilisateur")

    def __str__(self):
        return f"{self.username} ({self.role})"


from django.db import models


