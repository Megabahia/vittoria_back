# Generated by Django 3.1.7 on 2021-05-10 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vittoria_usuarios', '0002_auto_20210426_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
