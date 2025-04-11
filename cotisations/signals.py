# cotisations/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Paiement
from .services import lettrer_paiement  # Assurez-vous que la fonction lettrer_paiement est importée

@receiver(post_save, sender=Paiement)
def handle_paiement_created(sender, instance, created, **kwargs):
    if created:
        lettrer_paiement(instance)