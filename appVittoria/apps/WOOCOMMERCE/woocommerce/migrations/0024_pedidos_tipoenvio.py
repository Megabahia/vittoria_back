# Generated by Django 3.1.7 on 2024-07-15 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('woocommerce', '0023_auto_20240712_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='tipoEnvio',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
