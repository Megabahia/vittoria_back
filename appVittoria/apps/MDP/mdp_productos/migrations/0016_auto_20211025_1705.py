# Generated by Django 3.1.7 on 2021-10-25 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdp_productos', '0015_auto_20210728_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialavisos',
            name='productosVendidos',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ingresoproductos',
            name='cantidad',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='productos',
            name='caducidad',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='productos',
            name='refil',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='productos',
            name='stock',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='reportecaducidad',
            name='diasParaCaducar',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='reportecaducidad',
            name='productosCaducados',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='reporterotacion',
            name='diasPeriodo',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='reporterotacion',
            name='productosVendidos',
            field=models.IntegerField(null=True),
        ),
    ]
