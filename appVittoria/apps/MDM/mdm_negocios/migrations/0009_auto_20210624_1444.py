# Generated by Django 3.1.7 on 2021-06-24 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_negocios', '0008_auto_20210624_1430'),
    ]

    operations = [
        migrations.RenameField(
            model_name='negocios',
            old_name='actividadEcomica',
            new_name='actividadEconomica',
        ),
    ]
