# Generated by Django 3.1.7 on 2024-01-26 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_prospectosClientes', '0011_auto_20240123_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='prospectosclientes',
            name='descuento',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='prospectosclientes',
            name='iva',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='prospectosclientes',
            name='subTotal',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='prospectosclientes',
            name='total',
            field=models.FloatField(null=True),
        ),
    ]
