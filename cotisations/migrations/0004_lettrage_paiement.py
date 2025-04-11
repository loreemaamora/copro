# Generated by Django 3.2.25 on 2025-03-18 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('copropriete', '0002_alter_lot_proprietaire'),
        ('cotisations', '0003_alter_factureclt_reste_a_lettrer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paiement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_paiement', models.DateField(auto_now_add=True)),
                ('montant_restant', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paiements', to='copropriete.lot')),
            ],
        ),
        migrations.CreateModel(
            name='Lettrage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant_affecte', models.DecimalField(decimal_places=2, max_digits=10)),
                ('facture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lettrages', to='cotisations.factureclt')),
                ('paiement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lettrages', to='cotisations.paiement')),
            ],
        ),
    ]
