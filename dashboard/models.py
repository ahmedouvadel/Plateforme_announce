from django.db import models

from authentication.models import User
from announces.models import Annonce
import uuid

class Paiement(models.Model):
    numero_paiement = models.CharField(max_length=20, unique=True, default=uuid.uuid4().hex[:10].upper())
    annonce = models.OneToOneField(Annonce, on_delete=models.CASCADE, related_name="paiement")
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    banque = models.CharField(max_length=50, choices=[
        ("Bankily", "Bankily"),
        ("Masrivi", "Masrivi"),
        ("Sedad", "Sedad"),
    ])
    numero_facture = models.CharField(max_length=50)
    justificatif = models.ImageField(upload_to="paiements/")
    date = models.DateTimeField(
        auto_now_add=True,
        help_text="Date et heure de soumission de l'annonce."
    )
    statut = models.CharField(max_length=20, choices=[
        ("EN_ATTENTE", "En attente"),
        ("VALIDÉ", "Validé"),
        ("REFUSÉ", "Refusé"),
    ], default="EN_ATTENTE")

    def __str__(self):
        return f"Paiement {self.numero_paiement} - {self.annonce.titre}"
