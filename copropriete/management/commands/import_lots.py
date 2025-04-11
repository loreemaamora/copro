# copropriete/management/commands/import_lots.py
# dans shell : python manage.py import_lots chemin/vers/votre/fichier.xlsx

from django.core.management.base import BaseCommand
from copropriete.utils import importer_lot_excel

class Command(BaseCommand):
    help = 'Importer des lots depuis un fichier Excel'

    def add_arguments(self, parser):
        parser.add_argument('fichier_excel', type=str, help='Le chemin vers le fichier Excel à importer')

    def handle(self, *args, **kwargs):
        fichier_excel = kwargs['fichier_excel']
        with open(fichier_excel, 'rb') as f:
            message = importer_lot_excel(f)
            self.stdout.write(self.style.SUCCESS(message))