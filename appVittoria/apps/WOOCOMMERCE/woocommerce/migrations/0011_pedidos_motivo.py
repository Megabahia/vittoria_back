# Generated by Django 3.1.7 on 2024-03-11 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('woocommerce', '0010_pedidos_urlmetodopago'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='motivo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
