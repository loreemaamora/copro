# cotisations/services.py

from .models import FactureClt, Lettrage

def lettrer_paiement(paiement):
    montant_a_affecter = paiement.montant
    if paiement.type_paiement=='lot':
        factures = FactureClt.objects.filter(lot=paiement.lot, est_lettree=False).order_by('date_facture')
    else:
        lots_proprietaire = paiement.proprietaire.lots.all()
        factures = FactureClt.objects.filter(lot__in=lots_proprietaire, est_lettree=False).order_by('date_facture')

    for facture in factures:
        if montant_a_affecter <= 0:
            break

        if montant_a_affecter >= facture.reste_a_lettrer:
            # Affecter le montant total restant de la facture
            Lettrage.objects.create(paiement=paiement, facture=facture, montant_affecte=facture.reste_a_lettrer)
            montant_a_affecter -= facture.reste_a_lettrer
            facture.reste_a_lettrer = 0
            facture.est_lettree = True  # Marquer la facture comme lettrée
            facture.save()
        else:
            # Affecter le montant restant au paiement
            Lettrage.objects.create(paiement=paiement, facture=facture, montant_affecte=montant_a_affecter)
            facture.reste_a_lettrer -= montant_a_affecter
            facture.save()
            montant_a_affecter = 0

    # Mettre à jour le montant restant à affecter dans le paiement
    paiement.montant_restant = montant_a_affecter
    paiement.save()