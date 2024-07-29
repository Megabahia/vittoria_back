# Generated by Django 3.1.7 on 2024-07-29 22:28

import apps.WOOCOMMERCE.woocommerce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('woocommerce', '0025_uniquecode'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='archivoFormaPago',
            field=models.FileField(blank=True, null=True, upload_to=apps.WOOCOMMERCE.woocommerce.models.upload_path),
        ),
        migrations.AddField(
            model_name='pedidos',
            name='archivoFormaPagoCredito',
            field=models.FileField(blank=True, null=True, upload_to=apps.WOOCOMMERCE.woocommerce.models.upload_path),
        ),
        migrations.AddField(
            model_name='pedidos',
            name='formaPago',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='pedidos',
            name='montoCredito',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='pedidos',
            name='montoTransferencia',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='pedidos',
            name='numTransaccionCredito',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='pedidos',
            name='numTransaccionTransferencia',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='pedidos',
            name='totalCobroEfectivo',
            field=models.FloatField(null=True),
        ),
    ]
