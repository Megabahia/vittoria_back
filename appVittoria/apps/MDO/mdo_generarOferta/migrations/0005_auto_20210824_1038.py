# Generated by Django 3.1.7 on 2021-08-24 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdo_generarOferta', '0004_ofertadetalles_cantidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='oferta',
            name='descuento',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='oferta',
            name='iva',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='oferta',
            name='subTotal',
            field=models.FloatField(null=True),
        ),
    ]