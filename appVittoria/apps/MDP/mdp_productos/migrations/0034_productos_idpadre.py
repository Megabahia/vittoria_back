# Generated by Django 3.1.7 on 2024-04-23 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdp_productos', '0033_productos_proveedor'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='idPadre',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
