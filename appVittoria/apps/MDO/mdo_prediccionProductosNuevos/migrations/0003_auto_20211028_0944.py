# Generated by Django 3.1.7 on 2021-10-28 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdo_prediccionProductosNuevos', '0002_prediccionproductosnuevos_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalles',
            name='informacionAdicional',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='prediccionproductosnuevos',
            name='apellidos',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='prediccionproductosnuevos',
            name='correo',
            field=models.EmailField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='prediccionproductosnuevos',
            name='identificacion',
            field=models.CharField(max_length=13),
        ),
        migrations.AlterField(
            model_name='prediccionproductosnuevos',
            name='nombres',
            field=models.CharField(max_length=255),
        ),
    ]
