# Generated by Django 3.1.7 on 2021-10-25 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdp_parametrizaciones', '0004_auto_20210721_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametrizaciones',
            name='maximo',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='parametrizaciones',
            name='minimo',
            field=models.IntegerField(null=True),
        ),
    ]
