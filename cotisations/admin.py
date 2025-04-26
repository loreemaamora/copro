# cotisations/admin.py

from django.contrib import admin
from .models import Paiement, Lettrage, FactureClt
from copropriete.models import Copropriete
from .forms import PaiementForm

@admin.register(FactureClt)
class FactureCltAdmin(admin.ModelAdmin):
    list_display = ('reference', 'montant_initial', 'reste_a_lettrer', 'date_facture', 'lot', 'est_validee', 'est_lettree')
    search_fields = ('reference', 'lot__numero')  # Recherche par référence et numéro de lot
    list_filter = ('est_validee', 'est_lettree', 'date_facture')  # Filtres par statut de lettrage et date
    ordering = ('date_facture',)  # Tri par date de facture

    def has_add_permission(self, request, obj=None):
        """Empêche l'ajout de nouvelles factures si l'utilisateur n'est pas comptable."""
        return Copropriete.objects.filter(
            comptable=request.user
        ).exists()

    def has_delete_permission(self, request, obj=None):
        """Empêche la suppression des factures validées. Si non validées, le comptable peut les supprimer"""
        if obj is None:
            return False

        if obj.est_validee:
            return False

        return obj.lot.immeuble.copropriete.comptable == request.user

    def has_change_permission(self, request, obj=None):
        # Seul le syndic a le droit de modifier les factures non validées
        if obj is None:
            return True

        if obj.est_validee:
            return False

        return obj.lot.immeuble.copropriete.syndic == request.user

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    form = PaiementForm
    list_display = ('lot', 'montant', 'date_paiement', 'montant_restant')
    search_fields = ('lot__nom',)  # Remplacez 'nom' par le champ approprié de votre modèle Lot
    list_filter = ('date_paiement',)

    def has_delete_permission(self, request, obj=None):
        """Empêche la suppression d'écritures si l'utilisateur n'est pas superutilisateur."""
        return False

    def has_change_permission(self, request, obj=None):
        """Empêche la modification des écritures si l'utilisateur n'est pas superutilisateur."""
        return False

@admin.register(Lettrage)
class LettrageAdmin(admin.ModelAdmin):
    list_display = ('paiement', 'facture', 'montant_affecte')
    search_fields = ('paiement__id', 'facture__reference')  # Assurez-vous que ces champs existent
    list_filter = ('paiement__date_paiement',)

    def has_add_permission(self, request, obj=None):
        """Empêche l'ajout de nouvelles écritures si l'utilisateur n'est pas superutilisateur."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Empêche la suppression d'écritures si l'utilisateur n'est pas superutilisateur."""
        return False

    def has_change_permission(self, request, obj=None):
        """Empêche la modification des écritures si l'utilisateur n'est pas superutilisateur."""
        return False

