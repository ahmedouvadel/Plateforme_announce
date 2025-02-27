from django.db import models
from django.conf import settings  # ✅ Utilisation de settings.AUTH_USER_MODEL

class Categories(models.Model):
    titre = models.CharField(max_length=50)

    def __str__(self):
        return self.titre

class AnnonceStatus(models.TextChoices):
    EN_ATTENTE = 'EN_ATTENTE', 'En attente'
    VALIDEE = 'VALIDEE', 'Validée'
    REJETEE = 'REJETEE', 'Rejetée'

class Annonce(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ✅ Remplace l'import direct de User
        on_delete=models.CASCADE,
        related_name="annonces"
    )
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
    views = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.titre} - {self.user.username}"

class Favori(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favoris"
    )
    annonce = models.ForeignKey(
        Annonce,
        on_delete=models.CASCADE,
        related_name="favoris"
    )
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'annonce')

    def __str__(self):
        return f"{self.user.username} - {self.annonce.titre}"
