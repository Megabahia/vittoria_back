# Generated by Django 3.1.7 on 2021-10-26 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vittoria_usuarios', '0004_usuarios_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='email',
            field=models.EmailField(max_length=255, unique=True),
        ),
    ]
