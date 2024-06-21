# Generated by Django 3.1.7 on 2024-05-06 18:03

import apps.WOOCOMMERCE.gdc_gestor_contactos.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gdc_gestor_contactos', '0002_contactos_numerocomprobante'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactos',
            name='archivoFormaPago',
            field=models.FileField(blank=True, null=True, upload_to=apps.WOOCOMMERCE.gdc_gestor_contactos.models.upload_path),
        ),
        migrations.AddField(
            model_name='contactos',
            name='formaPago',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
