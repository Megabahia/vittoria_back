# Generated by Django 3.1.7 on 2024-03-11 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('woocommerce', '0008_auto_20240308_0922'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='codigoVendedor',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
