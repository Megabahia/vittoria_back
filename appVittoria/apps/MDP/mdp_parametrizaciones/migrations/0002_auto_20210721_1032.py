# Generated by Django 3.1.7 on 2021-07-21 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdp_parametrizaciones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametrizaciones',
            name='maximo',
            field=models.CharField(default=0, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametrizaciones',
            name='minimo',
            field=models.CharField(default=0, max_length=150),
            preserve_default=False,
        ),
    ]