# Generated by Django 3.1.7 on 2021-11-19 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gde_gestionEntrega', '0005_remove_oferta_codigooferta'),
    ]

    operations = [
        migrations.AddField(
            model_name='oferta',
            name='horaEntrega',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
