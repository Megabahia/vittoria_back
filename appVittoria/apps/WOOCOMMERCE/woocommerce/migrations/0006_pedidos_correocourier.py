# Generated by Django 3.1.7 on 2024-03-06 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('woocommerce', '0005_auto_20240306_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='correoCourier',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
