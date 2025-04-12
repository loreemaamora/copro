# copropriete/admin.py
from django.contrib import admin
from .models import Copropriete, Immeuble, Lot

@admin.register(Copropriete)
class CoproprieteAdmin(admin.ModelAdmin):
    fields = ('nom', 'adresse', 'ville', 'syndic', 'syndic_adj', 'comptable', 'tresorier','bloquer_ajout')
    list_display = ('nom', 'adresse', 'ville', 'syndic', 'syndic_adj', 'comptable', 'tresorier')
    search_fields = ('nom', 'adresse', 'ville')
    list_filter = ('ville',)

    actions = ['generer_factures_mois_en_cours']

    def get_readonly_fields(self, request, obj=None):
        """
        Rend les champs 'nom', 'adresse', et 'ville' en lecture seule une fois l'enregistrement sauvegardé.
        """
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:  # Si l'objet existe déjà (enregistrement existant)
            readonly_fields += ('nom', 'adresse', 'ville')
        return readonly_fields

    def has_delete_permission(self, request, obj=None):
        """
        Interdit la suppression de l'objet Copropriete.
        """
        return False

    def has_change_permission(self, request, obj=None):
        """Autorise uniquement le syndic à modifier les champs restreints."""
        if obj:  # Si on modifie une copropriété existante
            if obj.syndic != request.user:  # Seul le syndic peut modifier
                return False
        return super().has_change_permission(request, obj)

    def generer_factures_mois_en_cours(self, request, queryset):
        for copropriete in queryset:
            copropriete.generer_factures()
        self.message_user(request, "Factures générées avec succès.")
    generer_factures_mois_en_cours.short_description = "Générer des factures pour les lots"

@admin.register(Immeuble)
class ImmeubleAdmin(admin.ModelAdmin):
    fields = ('numero', 'copropriete', 'cotisation_mensuelle_lot')
    list_display = ('numero', 'copropriete', 'cotisation_mensuelle_lot')
    search_fields = ('numero',)
    list_filter = ('copropriete',)

    def get_readonly_fields(self, request, obj=None):
        """
        Rend les champs 'nom', 'adresse', et 'ville' en lecture seule une fois l'enregistrement sauvegardé.
        """
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:  # Si l'objet existe déjà (enregistrement existant)
            readonly_fields += ('numero', 'copropriete')
        return readonly_fields

    def has_delete_permission(self, request, obj=None):
        """
        Interdit la suppression de l'objet Copropriete.
        """
        return False

    def has_change_permission(self, request, obj=None):
        """Autorise uniquement le syndic à modifier les champs restreints."""
        if obj:  # Si on modifie une copropriété existante
            if obj.copropriete.syndic != request.user:  # Seul le syndic peut modifier
                return False
        return super().has_change_permission(request, obj)

@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    fields = ('numero', 'immeuble', 'proprietaire','titre_foncier')
    list_display = ('numero', 'immeuble', 'proprietaire')
    search_fields = ('numero',)
    list_filter = ('immeuble', 'proprietaire')
    list_per_page = 25

    def get_readonly_fields(self, request, obj=None):
        """
        Rend les champs 'nom', 'adresse', et 'ville' en lecture seule une fois l'enregistrement sauvegardé.
        """
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:  # Si l'objet existe déjà (enregistrement existant)
            readonly_fields += ('numero', 'immeuble')
        return readonly_fields

    def has_delete_permission(self, request, obj=None):
        """
        Interdit la suppression de l'objet Copropriete.
        """
        return False