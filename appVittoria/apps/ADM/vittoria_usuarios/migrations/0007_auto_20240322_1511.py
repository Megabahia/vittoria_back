# Generated by Django 3.1.7 on 2024-03-22 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vittoria_usuarios', '0006_auto_20211122_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarios',
            name='ciudad',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='usuarios',
            name='provincia',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
