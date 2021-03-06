# Generated by Django 3.1.7 on 2021-10-28 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdo_generarOferta', '0008_auto_20211025_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oferta',
            name='apellidos',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='oferta',
            name='canal',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='oferta',
            name='correo',
            field=models.EmailField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='oferta',
            name='descripcion',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='oferta',
            name='direccion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='oferta',
            name='identificacion',
            field=models.CharField(max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='oferta',
            name='nombreVendedor',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='oferta',
            name='nombres',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='oferta',
            name='razonSocial',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='ofertadetalles',
            name='articulo',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='ofertadetalles',
            name='cantidad',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ofertadetalles',
            name='codigo',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='ofertadetalles',
            name='informacionAdicional',
            field=models.TextField(null=True),
        ),
    ]
