# Generated by Django 3.1.7 on 2024-08-16 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vittoria_usuarios', '0008_usuarios_canal'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarios',
            name='tipoEnvio',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
