# Generated by Django 3.1.7 on 2024-01-27 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gde_gestionEntrega', '0006_oferta_horaentrega'),
    ]

    operations = [
        migrations.AddField(
            model_name='oferta',
            name='courier',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='oferta',
            name='lugarEnvio',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
