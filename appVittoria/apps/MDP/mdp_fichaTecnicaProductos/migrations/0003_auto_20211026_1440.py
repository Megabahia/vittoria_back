# Generated by Django 3.1.7 on 2021-10-26 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdp_fichaTecnicaProductos', '0002_auto_20211025_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichatecnicaproductos',
            name='nombreAtributo',
            field=models.CharField(max_length=255),
        ),
    ]
