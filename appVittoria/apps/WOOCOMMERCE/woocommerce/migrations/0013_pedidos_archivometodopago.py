# Generated by Django 3.1.7 on 2024-03-22 17:10

import apps.WOOCOMMERCE.woocommerce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('woocommerce', '0012_auto_20240314_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='archivoMetodoPago',
            field=models.FileField(blank=True, null=True, upload_to=apps.WOOCOMMERCE.woocommerce.models.upload_path),
        ),
    ]
