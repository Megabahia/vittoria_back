# Generated by Django 3.1.7 on 2021-05-25 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_negocios', '0005_auto_20210525_1200'),
    ]

    operations = [
        migrations.RenameField(
            model_name='direccionesestablecimientosnegocios',
            old_name='idNegocio',
            new_name='negocio',
        ),
        migrations.RenameField(
            model_name='personalnegocios',
            old_name='idNegocio',
            new_name='negocio',
        ),
    ]
