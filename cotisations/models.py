# cotisations/models.py

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

MyUser  = get_user_model()

#from copropriete.models import Lot

class FactureClt(models.Model):
    reference = models.CharField(max_length=50, unique=True) # format AAMMLL
    montant_initial = models.DecimalField(max_digits=10, decimal_places=2)
    reste_a_lettrer = models.DecimalField(max_digits=10, decimal_places=2)
    date_facture = models.DateField()
    lot = models.ForeignKey('copropriete.Lot', on_delete=models.CASCADE)
    est_lettree = models.BooleanField(default=False)  # Facture verrouillée ?

    def __str__(self):
        return f"{self.reference} - montant : {self.montant_initial}"

class Paiement(models.Model):
    TYPE_PAIEMENT_CHOICES = [
        ('lot', 'Lot'),
        ('proprietaire', 'Propriétaire'),
    ]

    type_paiement = models.CharField(max_length=15, choices=TYPE_PAIEMENT_CHOICES, default='lot')
    lot = models.ForeignKey('copropriete.Lot', on_delete=models.CASCADE, related_name='paiements', null=True, blank=True)
    proprietaire = models.ForeignKey(MyUser , on_delete=models.CASCADE, related_name='paiements', null=True, blank=True)

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField(auto_now_add=True)
    montant_restant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def clean(self):
        # Validation pour s'assurer qu'un seul des deux champs est rempli
        if self.type_paiement == 'lot' and not self.lot:
            raise ValidationError("Si le type de paiement est 'Lot', un lot doit être sélectionné.")
        if self.type_paiement == 'proprietaire' and not self.proprietaire:
            raise ValidationError("Si le type de paiement est 'Propriétaire', un propriétaire doit être sélectionné.")
        if self.type_paiement == 'lot' and self.proprietaire:
            raise ValidationError("Vous ne pouvez pas sélectionner à la fois un lot et un propriétaire.")
        if self.type_paiement == 'proprietaire' and self.lot:
            raise ValidationError("Vous ne pouvez pas sélectionner à la fois un propriétaire et un lot.")

    def __str__(self):
        return f'Paiement de {self.montant} pour {self.proprietaire or self.lot}'

class Lettrage(models.Model):
    paiement = models.ForeignKey(Paiement, on_delete=models.CASCADE, related_name='lettrages')
    facture = models.ForeignKey(FactureClt, on_delete=models.CASCADE, related_name='lettrages')
    montant_affecte = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Lettrage de {self.montant_affecte} pour le paiement {self.paiement.id} et la facture {self.facture.reference}'