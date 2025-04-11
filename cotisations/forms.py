# cotisations/forms.py

from django import forms
from django.db.models import Count
from django.contrib.auth import get_user_model
from .models import Paiement

MyUser  = get_user_model()

class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['type_paiement', 'lot', 'proprietaire', 'montant']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les copropriétaires pour n'afficher que ceux qui ont au moins un lot
        self.fields['proprietaire'].queryset = MyUser .objects.annotate(nombre_lots=Count('lots')).filter(nombre_lots__gt=0)