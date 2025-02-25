from django.db import models

# Create your models here.
class Categories(models.Model):
    titre = models.CharField(max_length=50)

    def __str__(self):
        return self.titre

class AnnonceStatus(models.TextChoices):
    EN_ATTENTE = 'EN_ATTENTE'
    VALIDEE = 'VALIDEE'
    REJETEE = 'REJETEE'


class Annonce(models.Model):
    titre = models.CharField(max_length=50)
    description = models.TextField()
    prix = models.IntegerField()
    image = models.ImageField(upload_to='annonces/')
    statut = models.CharField(
        max_length=10,
        choices=AnnonceStatus.choices,
        default=AnnonceStatus.EN_ATTENTE
    )
    categorie = models.ForeignKey(Categories, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    # ✅ Ajouter le champ views
    views = models.IntegerField(default=0)  # Initialise avec 0

    def __str__(self):
        return self.titre