# Generated by Django 3.1.7 on 2021-10-25 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gde_gestionEntrega', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oferta',
            name='vigenciaOferta',
            field=models.IntegerField(null=True),
        ),
    ]