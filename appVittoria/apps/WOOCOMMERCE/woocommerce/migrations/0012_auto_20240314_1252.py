# Generated by Django 3.1.7 on 2024-03-14 17:52

import apps.WOOCOMMERCE.woocommerce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('woocommerce', '0011_pedidos_motivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='evidenciaFotoEmpaque',
            field=models.FileField(blank=True, null=True, upload_to=apps.WOOCOMMERCE.woocommerce.models.upload_path),
        ),
        migrations.AddField(
            model_name='pedidos',
            name='evidenciaVideoEmpaque',
            field=models.FileField(blank=True, null=True, upload_to=apps.WOOCOMMERCE.woocommerce.models.upload_path),
        ),
    ]
