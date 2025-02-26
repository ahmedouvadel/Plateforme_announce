from django.db import models
from authentication.models import User

# Create your models here.
class Categories(models.Model):
    titre = models.CharField(max_length=50)

    def __str__(self):
        return self.titre

class AnnonceStatus(models.TextChoices):
    EN_ATTENTE = 'EN_ATTENTE'
    VALIDEE = 'VALIDEE'
    REJETEE = 'REJETEE'

from django.conf import settings
from django.db import models
  # Importer User depuis authentification

class Annonce(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reclamations"
    )
    titre = models.CharField(max_length=50)
    description = models.TextField()
    prix = models.IntegerField()
    image = models.ImageField(upload_to='annonces/')
    statut = models.CharField(
        max_length=10,
        choices=[('en_attente', 'En attente'), ('rejete', 'Rejeté'), ('accepte', 'Accepté')],
        default='en_attente'
    )
    categorie = models.ForeignKey('Categories', on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    views = models.IntegerField(default=0)  # Nombre de vues, initialise à 0

    def __str__(self):
        return f"{self.titre} - {self.user.username}"  # Affiche le titre et l'utilisateur qui l'a créée


from django.db import models
 # Importer User depuis authentification

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_info")
    adresse = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username


