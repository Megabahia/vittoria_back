# Generated by Django 3.1.7 on 2024-02-21 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdp_gestionInventario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='fechaAdquisicion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
