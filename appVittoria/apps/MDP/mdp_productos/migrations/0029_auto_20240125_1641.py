# Generated by Django 3.1.7 on 2024-01-25 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdp_productos', '0028_auto_20240125_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='envioNivelNacional',
            field=models.BooleanField(default=1),
        ),
    ]
