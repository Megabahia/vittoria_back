# Generated by Django 3.1.7 on 2024-07-16 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdp_productos', '0040_productos_imagen_principal'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='peso',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productos',
            name='tamanio',
            field=models.FloatField(blank=True, null=True),
        ),
    ]