# Generated by Django 3.1.7 on 2024-01-25 21:50

import apps.MDP.mdp_parametrizaciones.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdp_parametrizaciones', '0006_auto_20211027_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametrizaciones',
            name='archivo',
            field=models.ImageField(blank=True, null=True, upload_to=apps.MDP.mdp_parametrizaciones.models.upload_path),
        ),
    ]