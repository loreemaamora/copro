# copropriete/utils.py
import pandas as pd
from django.core.exceptions import ValidationError
from .models import Immeuble, Lot

def importer_lot_excel(fichier_excel):
    try:
        # Lire le fichier Excel
        df = pd.read_excel(fichier_excel, engine="openpyxl")

        # Vérifier que les colonnes nécessaires existent
        if not {'numero', 'immeuble'}.issubset(df.columns):
            raise ValidationError("Le fichier Excel doit contenir les colonnes 'numero' et 'immeuble'.")

        lots_crees = []
        for index, row in df.iterrows():
            # Récupérer l'instance d'Immeuble à partir de l'identifiant
            immeuble_id = row['immeuble']
            try:
                immeuble_instance = Immeuble.objects.get(id=immeuble_id)
            except Immeuble.DoesNotExist:
                raise ValidationError(f"L'immeuble avec l'ID {immeuble_id} n'existe pas.")

            # Créer ou mettre à jour le lot
            lot, created = Lot.objects.update_or_create(
                numero=row['numero'],
                defaults={'immeuble': immeuble_instance}
            )
            if created:
                lots_crees.append(lot)

        return f"{len(lots_crees)} lots importés avec succès."

    except Exception as e:
        return f"Erreur lors de l'importation : {str(e)}"
