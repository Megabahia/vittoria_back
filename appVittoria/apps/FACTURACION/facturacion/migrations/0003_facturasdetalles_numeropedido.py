# Generated by Django 3.1.7 on 2024-02-08 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0002_auto_20240208_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturasdetalles',
            name='numeroPedido',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
