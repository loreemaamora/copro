# copropriete/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date
from cotisations.models import FactureClt

MyUser  = get_user_model()

class Copropriete(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)
    ville = models.CharField(max_length=50)
    syndic = models.ForeignKey(MyUser , on_delete=models.SET_NULL, null=True, related_name='syndic_pour')
    syndic_adj = models.ForeignKey(MyUser , on_delete=models.SET_NULL, null=True, related_name='syndic_adj_pour')
    comptable = models.ForeignKey(MyUser , on_delete=models.SET_NULL, null=True, related_name='comptable_pour')
    tresorier = models.ForeignKey(MyUser , on_delete=models.SET_NULL, null=True, related_name='tresorier_pour')
    bloquer_ajout = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nom', 'ville'], name='unique_nom_ville')
        ]

    def __str__(self):
        return f"{self.nom} - {self.adresse} - {self.ville}"

    def clean(self):
        # Validation pour s'assurer qu'un utilisateur ne peut pas être syndic et comptable ou trésorier
        if self.syndic == self.syndic_adj:
            raise ValidationError("Un utilisateur ne peut pas être à la fois syndic et syndic adjoint.")
        if self.comptable == self.tresorier:
            raise ValidationError("Un utilisateur ne peut pas être à la fois comptable et trésorier.")

    def generer_factures(self):
        # Obtenir le mois et l'année en cours
        annee = date.today().year
        mois = date.today().month

        # Format du numéro de facture
        for immeuble in self.immeubles.all():  # Assurez-vous que 'lots' est le related_name correct
            for lot in immeuble.lots.all():
                # Vérifier si une facture existe déjà pour ce lot pour le mois en cours
                reference = f"{annee % 100:02d}{mois:02d}{immeuble.numero}{lot.numero}"
                if not FactureClt.objects.filter(reference=reference).exists():
                    # Créer la facture
                    FactureClt.objects.create(
                        reference=reference,
                        montant_initial=immeuble.cotisation_mensuelle_lot,
                        reste_a_lettrer=immeuble.cotisation_mensuelle_lot,
                        date_facture=date(annee, mois, 1),
                        lot=lot,
                        est_lettree=False
                    )

class Immeuble(models.Model):
    numero = models.CharField(max_length=20)  # Numéro de l'immeuble
    copropriete = models.ForeignKey(Copropriete, on_delete=models.CASCADE, related_name='immeubles')  # Relation avec la copropriété
    cotisation_mensuelle_lot = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        unique_together = ('numero', 'copropriete')  # Unicité du numéro de lot par copropriété

    def __str__(self):
        return f"{self.pk} - {self.numero} - {self.copropriete.nom}"

    def clean(self):
        # Empêcher l'ajout d'immeubles si copropriete.bloquer_ajout==True
        if not self.pk and self.copropriete.bloquer_ajout:
            raise ValidationError("L'ajout d'immeubles est bloqué pour cette copropriété.")

class Lot(models.Model):
    numero = models.CharField(max_length=20)  # Numéro du lot
    immeuble = models.ForeignKey(Immeuble, on_delete=models.CASCADE, related_name='lots')  # Relation avec l'immeuble
    proprietaire = models.ForeignKey(MyUser , on_delete=models.SET_NULL, null=True, blank=True, related_name='lots')  # Propriétaire du lot
    titre_foncier = models.FileField(upload_to='titres_propriete/',
                                    null=True,
                                    blank=True,
                                    validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
                                    )
    class Meta:
        unique_together = ('numero', 'immeuble')  # Unicité du numéro de lot par immeuble

    def __str__(self):
        return f"Lot {self.numero} - {self.immeuble.numero} - {self.immeuble.copropriete.nom}"

    def clean(self):
        # Empêcher l'ajout d'immeubles si copropriete.bloquer_ajout==True
        if not self.pk and self.immeuble.copropriete.bloquer_ajout:
            raise ValidationError("L'ajout de lots est bloqué pour cette copropriété ! ")
        # Validation de la taille du fichier
        if self.titre_foncier and self.titre_foncier.size > 0.5 * 1024 * 1024:  # 0.5 Mo
            raise ValidationError("La taille du fichier ne doit pas dépasser 0.5 Mo.")

    def save(self, *args, **kwargs):
        # Vérifie si l'utilisateur qui modifie est syndic ou syndic adjoint
        user = kwargs.get('user', None)  # Tu devras passer l'utilisateur lors de l'appel de save
        if user and not (user == self.immeuble.copropriete.syndic or user == self.immeuble.copropriete.syndic_adj):
            raise ValidationError("Seul le syndic ou l'adjoint peut modifier le titre foncier.")

        # Appelle la méthode save d'origine
        super().save(*args, **kwargs)